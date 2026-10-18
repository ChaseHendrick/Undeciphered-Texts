/* Simulated annealing for in-place periodic Quagmire I, II and IV.
 *
 * Letters are 0..25. A[r] is the letter at rank r of the plain alphabet and
 * Binv[c] is the rank of ciphertext letter c in the cipher alphabet.
 *   family 1 (Quagmire I):  c = rank_A(p) + K           decrypt p = A[c - K]
 *   family 2 (Quagmire II): rank_B(c) = p + K           decrypt p = Binv[c] - K
 *   family 4 (Quagmire IV): rank_B(c) = rank_A(p) + K   decrypt p = A[Binv[c] - K]
 * K is K[i mod period]; all arithmetic is mod 26.
 *
 * Clue handling. Every column that holds at least one clue letter takes its
 * key shift from the alphabets: each clue letter in the column votes for the
 * shift that would make it decrypt right, and the column takes the shift with
 * the most votes. Clue letters that still decrypt wrong are counted as
 * violations and cost `lambda` nats each. Columns without clue letters keep
 * their shift as free state. With `derive` = 0 every shift is free state and
 * the same penalty applies (used only for comparison runs).
 *
 * Objective: full English log probability of the decryption (first three
 * letters from the shorter contexts, then quadgrams) minus lambda * violations.
 */

#include <math.h>
#include <stdint.h>
#include <string.h>

#define MAXN 512
#define MAXP 128

static uint64_t rng_state = 88172645463325252ULL;

static inline uint64_t rnd(void) {
    uint64_t x = rng_state;
    x ^= x >> 12;
    x ^= x << 25;
    x ^= x >> 27;
    rng_state = x;
    return x * 2685821657736338717ULL;
}

static inline int rndint(int n) { return (int)((rnd() >> 33) % (uint64_t)n); }
static inline double rnd01(void) { return (double)(rnd() >> 11) * (1.0 / 9007199254740992.0); }

static inline int md(int x) {
    x %= 26;
    return x < 0 ? x + 26 : x;
}

typedef struct {
    int family, n, period, derive;
    const int *ct;
    int ncl;
    const int *cpos, *cpl;
    const double *q4, *p1, *p2, *p3;
    double lambda;
    int clue_col[MAXP];   /* 1 when column has a clue letter */
    /* Letters tied by sharing a clue column, per alphabet side (0 = A, 1 = B). */
    int comp[2][26];      /* component id, -1 when the letter is in no tie */
    int cand[2][26], ncand[2];
    int clue[2][26], nclue[2], other[2][26], nother[2];  /* clue letters and the rest, per side */
} Ctx;

static double g_pshift = 0.2;  /* share of component-shift moves */
static double g_pheat = 0.0;   /* share of heat-bath moves (all 25 swaps of one letter tried) */

static double g_pkey = 0.15;   /* share of free key-shift moves */
static double g_plns = 0.0;    /* share of large moves: move a clue letter, then re-fit the rest */
static int g_inner = 200;      /* greedy steps after a large move */

void q_set_moves(double pshift, double pheat, double pkey) { g_pshift = pshift; g_pheat = pheat; g_pkey = pkey; }
void q_set_lns(double plns, int inner) { g_plns = plns; g_inner = inner; }

typedef struct {
    int A[26], Ainv[26], B[26], Binv[26], K[MAXP];
    int plain[MAXN];
    int viol;
    double lang, obj;
} State;

static double lang_score(const Ctx *c, const int *s) {
    int n = c->n;
    if (n <= 0) return 0.0;
    double t = c->p1[s[0]];
    if (n > 1) t += c->p2[s[0] * 26 + s[1]];
    if (n > 2) t += c->p3[(s[0] * 26 + s[1]) * 26 + s[2]];
    for (int i = 3; i < n; i++)
        t += c->q4[((s[i - 3] * 26 + s[i - 2]) * 26 + s[i - 1]) * 26 + s[i]];
    return t;
}

/* Shift that makes clue letter k decrypt right under the current alphabets. */
static inline int clue_shift(const Ctx *c, const State *st, int k) {
    int cc = c->ct[c->cpos[k]], p = c->cpl[k];
    switch (c->family) {
    case 1: return md(cc - st->Ainv[p]);
    case 2: return md(st->Binv[cc] - p);
    default: return md(st->Binv[cc] - st->Ainv[p]);
    }
}

static inline int decrypt_one(const Ctx *c, const State *st, int cc, int k) {
    switch (c->family) {
    case 1: return st->A[md(cc - k)];
    case 2: return md(st->Binv[cc] - k);
    default: return st->A[md(st->Binv[cc] - k)];
    }
}

static void evaluate(const Ctx *c, State *st) {
    int P = c->period;
    if (c->derive) {
        int votes[MAXP][26];
        memset(votes, 0, sizeof(int) * 26 * P);
        for (int k = 0; k < c->ncl; k++) votes[c->cpos[k] % P][clue_shift(c, st, k)]++;
        for (int j = 0; j < P; j++) {
            if (!c->clue_col[j]) continue;
            int best = votes[j][st->K[j]], arg = st->K[j];
            for (int v = 0; v < 26; v++)
                if (votes[j][v] > best) { best = votes[j][v]; arg = v; }
            st->K[j] = arg;
        }
    }
    int viol = 0;
    for (int i = 0; i < c->n; i++) st->plain[i] = decrypt_one(c, st, c->ct[i], st->K[i % P]);
    for (int k = 0; k < c->ncl; k++)
        if (st->plain[c->cpos[k]] != c->cpl[k]) viol++;
    st->viol = viol;
    st->lang = lang_score(c, st->plain);
    st->obj = st->lang - c->lambda * viol;
}

static void set_inverse(State *st) {
    for (int r = 0; r < 26; r++) {
        st->Ainv[st->A[r]] = r;
        st->B[st->Binv[r]] = r; /* B[rank] = letter */
    }
}

static void random_perm(int *a) {
    for (int i = 0; i < 26; i++) a[i] = i;
    for (int i = 25; i > 0; i--) {
        int j = rndint(i + 1), t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
}

/* Lists of ranks so a swap is two letters of one alphabet. */
static void swap_A(State *st, int x, int y) { /* swap letters x and y in A */
    int rx = st->Ainv[x], ry = st->Ainv[y];
    st->A[rx] = y; st->A[ry] = x;
    st->Ainv[x] = ry; st->Ainv[y] = rx;
}

static void swap_B(State *st, int x, int y) {
    int rx = st->Binv[x], ry = st->Binv[y];
    st->Binv[x] = ry; st->Binv[y] = rx;
    st->B[rx] = y; st->B[ry] = x;
}

static int uf_find(int *par, int x) {
    while (par[x] != x) x = par[x] = par[par[x]];
    return x;
}

/* Clue letters in one column must keep fixed rank differences in each keyed alphabet
 * (Quagmire I: plain letters in A; II: cipher letters in B; IV: both, given the other).
 * Union them per side so a move can shift a whole tied group at once. */
static void setup_components(Ctx *c) {
    for (int side = 0; side < 2; side++) {
        int par[26], size[26];
        for (int i = 0; i < 26; i++) { par[i] = i; size[i] = 0; }
        int used = (side == 0) ? (c->family != 2) : (c->family != 1);
        c->ncand[side] = 0;
        c->nclue[side] = c->nother[side] = 0;
        for (int i = 0; i < 26; i++) c->comp[side][i] = -1;
        if (!used) continue;
        for (int j = 0; j < c->period; j++) {
            int first = -1;
            for (int k = 0; k < c->ncl; k++) {
                if (c->cpos[k] % c->period != j) continue;
                int letter = side == 0 ? c->cpl[k] : c->ct[c->cpos[k]];
                if (first < 0) first = letter;
                else par[uf_find(par, letter)] = uf_find(par, first);
            }
        }
        int isclue[26] = {0};
        for (int k = 0; k < c->ncl; k++) isclue[side == 0 ? c->cpl[k] : c->ct[c->cpos[k]]] = 1;
        c->nclue[side] = c->nother[side] = 0;
        for (int i = 0; i < 26; i++) {
            if (isclue[i]) c->clue[side][c->nclue[side]++] = i;
            else c->other[side][c->nother[side]++] = i;
        }
        for (int i = 0; i < 26; i++) size[uf_find(par, i)]++;
        for (int i = 0; i < 26; i++) {
            int r = uf_find(par, i);
            if (size[r] >= 2) {
                c->comp[side][i] = r;
                c->cand[side][c->ncand[side]++] = i;
            }
        }
    }
}

/* Move the group of letter x (one side) d ranks along, keeping its internal spacing;
 * letters pushed out take the freed ranks in rank order. L[rank] = letter, R[letter] = rank. */
static void shift_group(int *L, int *R, const int *comp, int x, int d) {
    int in[26] = {0}, target[26] = {0};
    int g = comp[x];
    for (int i = 0; i < 26; i++) if (comp[i] == g) in[i] = 1;
    for (int i = 0; i < 26; i++) if (in[i]) target[(R[i] + d) % 26] = 1;
    int vac[26], nv = 0, disp[26], nd = 0;
    for (int r = 0; r < 26; r++) {
        if (in[L[r]] && !target[r]) vac[nv++] = r;
        if (target[r] && !in[L[r]]) disp[nd++] = L[r];
    }
    int newL[26];
    for (int r = 0; r < 26; r++) newL[r] = -1;
    for (int i = 0; i < 26; i++) if (in[i]) newL[(R[i] + d) % 26] = i;
    for (int r = 0; r < 26; r++) if (newL[r] < 0 && !target[r] && !in[L[r]]) newL[r] = L[r];
    for (int k = 0; k < nd && k < nv; k++) newL[vac[k]] = disp[k];
    for (int r = 0; r < 26; r++) { L[r] = newL[r]; R[newL[r]] = r; }
}

static void propose(const Ctx *c, State *cand, const int *free_cols, int nfree) {
    double u = rnd01();
    int family = c->family;
    int side = family == 1 ? 0 : family == 2 ? 1 : (int)(rnd() & 1);
    if (nfree > 0 && u < g_pkey) {
        int j = free_cols[rndint(nfree)];
        cand->K[j] = (cand->K[j] + 1 + rndint(25)) % 26;
    } else if (u < g_pkey + g_pshift && c->ncand[side] > 0) {
        int x = c->cand[side][rndint(c->ncand[side])];
        int d = 1 + rndint(25);
        if (side == 0) shift_group(cand->A, cand->Ainv, c->comp[0], x, d);
        else shift_group(cand->B, cand->Binv, c->comp[1], x, d);
    } else {
        int x = rndint(26), y = rndint(25);
        if (y >= x) y++;
        if (side == 0) swap_A(cand, x, y); else swap_B(cand, x, y);
    }
}

/* A move that keeps every clue-derived shift: swap two non-clue letters of one side,
 * or change a free column's shift. */
static void propose_inner(const Ctx *c, State *cand, const int *free_cols, int nfree) {
    int side = c->family == 1 ? 0 : c->family == 2 ? 1 : (int)(rnd() & 1);
    int no = c->nother[side];
    if (no < 2 || (nfree > 0 && rnd01() < 0.2)) {
        if (nfree == 0) return;
        int j = free_cols[rndint(nfree)];
        cand->K[j] = (cand->K[j] + 1 + rndint(25)) % 26;
        return;
    }
    int a = rndint(no), b = rndint(no - 1);
    if (b >= a) b++;
    int x = c->other[side][a], y = c->other[side][b];
    if (side == 0) swap_A(cand, x, y); else swap_B(cand, x, y);
}

/* Large move: move one clue letter (swap with any letter, or shift its tied group),
 * which changes the shifts of its columns, then hill-climb the non-clue letters. */
static void large_move(const Ctx *c, State *cand, const int *free_cols, int nfree, long long *evals) {
    int side = c->family == 1 ? 0 : c->family == 2 ? 1 : (int)(rnd() & 1);
    if (c->nclue[side] == 0) return;
    int x = c->clue[side][rndint(c->nclue[side])];
    if (c->comp[side][x] >= 0 && rnd01() < 0.5) {
        int d = 1 + rndint(25);
        if (side == 0) shift_group(cand->A, cand->Ainv, c->comp[0], x, d);
        else shift_group(cand->B, cand->Binv, c->comp[1], x, d);
    } else {
        int y = rndint(25);
        if (y >= x) y++;
        if (side == 0) swap_A(cand, x, y); else swap_B(cand, x, y);
    }
    evaluate(c, cand);
    (*evals)++;
    static State trial;
    for (int k = 0; k < g_inner; k++) {
        trial = *cand;
        propose_inner(c, &trial, free_cols, nfree);
        evaluate(c, &trial);
        (*evals)++;
        if (trial.obj >= cand->obj) *cand = trial;
    }
}

/* Decrypt and score one supplied key (no derivation of shifts).
 * A_in: plain alphabet as A[rank] = letter; Binv_in: cipher ranks Binv[letter]. */
void q_eval(int family, int n, const int *ct, int period, int ncl, const int *cpos, const int *cpl,
            const double *q4, const double *p1, const double *p2, const double *p3, double lambda,
            const int *A_in, const int *Binv_in, const int *K_in, int *out_plain, double *out) {
    Ctx c;
    memset(&c, 0, sizeof c);
    c.family = family; c.n = n; c.period = period; c.derive = 0; c.ct = ct;
    c.ncl = ncl; c.cpos = cpos; c.cpl = cpl; c.q4 = q4; c.p1 = p1; c.p2 = p2; c.p3 = p3;
    c.lambda = lambda;
    State st;
    memcpy(st.A, A_in, sizeof st.A);
    memcpy(st.Binv, Binv_in, sizeof st.Binv);
    set_inverse(&st);
    for (int j = 0; j < period; j++) st.K[j] = K_in[j];
    evaluate(&c, &st);
    memcpy(out_plain, st.plain, sizeof(int) * n);
    out[0] = st.obj; out[1] = st.lang; out[2] = st.viol;
}

/* Annealing with restarts.
 * seed_mode 0: random start; 1: start every restart from the supplied A/Binv/K.
 * out_best: A[26], Binv[26], K[period], plain[n] of the best objective state.
 * out_feas: same layout, best state with zero violations (if any).
 * out[0..5]: best obj, its lang, its viol, best feasible lang (or -1e300), evals, restarts reaching
 *            within 0.5 nats of the final best objective.
 * restart_best: per restart best objective (length restarts). */
void q_anneal(int family, int n, const int *ct, int period, int ncl, const int *cpos, const int *cpl,
              const double *q4, const double *p1, const double *p2, const double *p3, double lambda,
              int derive, int restarts, long long iters, double t0, double t1, unsigned long long seed,
              int seed_mode, const int *A_seed, const int *Binv_seed, const int *K_seed,
              int *out_best, int *out_feas, double *out, double *restart_best) {
    Ctx c;
    memset(&c, 0, sizeof c);
    c.family = family; c.n = n; c.period = period; c.derive = derive; c.ct = ct;
    c.ncl = ncl; c.cpos = cpos; c.cpl = cpl; c.q4 = q4; c.p1 = p1; c.p2 = p2; c.p3 = p3;
    c.lambda = lambda;
    for (int k = 0; k < ncl; k++) c.clue_col[cpos[k] % period] = 1;
    setup_components(&c);
    rng_state = seed * 0x9E3779B97F4A7C15ULL + 0x1234567ULL;
    if (rng_state == 0) rng_state = 1;
    for (int w = 0; w < 10; w++) rnd();

    int free_cols[MAXP], nfree = 0;
    for (int j = 0; j < period; j++)
        if (!derive || !c.clue_col[j]) free_cols[nfree++] = j;

    State best, feas, cur, cand;
    best.obj = -1e300;
    double feas_lang = -1e300;
    long long evals = 0;
    double ratio = (iters > 1) ? pow(t1 / t0, 1.0 / (double)(iters - 1)) : 1.0;

    for (int r = 0; r < restarts; r++) {
        if (seed_mode == 1) {
            memcpy(cur.A, A_seed, sizeof cur.A);
            memcpy(cur.Binv, Binv_seed, sizeof cur.Binv);
            for (int j = 0; j < period; j++) cur.K[j] = K_seed[j];
        } else {
            if (family == 2) for (int i = 0; i < 26; i++) cur.A[i] = i; else random_perm(cur.A);
            if (family == 1) for (int i = 0; i < 26; i++) cur.Binv[i] = i; else random_perm(cur.Binv);
            for (int j = 0; j < period; j++) cur.K[j] = seed_mode == 2 ? K_seed[j] : rndint(26);
        }
        set_inverse(&cur);
        evaluate(&c, &cur);
        evals++;
        State rbest = cur;
        double T = t0;
        for (long long it = 0; it < iters; it++, T = t0 * pow(ratio, (double)it)) {
            if (g_pheat > 0 && rnd01() < g_pheat) {
                /* Heat bath: every swap of one letter, chosen by its Boltzmann weight. */
                static State opt[26];
                double w[26], top = cur.obj;
                int side = family == 1 ? 0 : family == 2 ? 1 : (int)(rnd() & 1);
                int x = rndint(26);
                for (int y = 0; y < 26; y++) {
                    opt[y] = cur;
                    if (y != x) {
                        if (side == 0) swap_A(&opt[y], x, y); else swap_B(&opt[y], x, y);
                        evaluate(&c, &opt[y]);
                        evals++;
                    }
                    if (opt[y].obj > top) top = opt[y].obj;
                }
                double sum = 0;
                for (int y = 0; y < 26; y++) { w[y] = exp((opt[y].obj - top) / T); sum += w[y]; }
                double u = rnd01() * sum;
                int pick = 25;
                for (int y = 0; y < 26; y++) { u -= w[y]; if (u <= 0) { pick = y; break; } }
                cur = opt[pick];
                if (cur.obj > rbest.obj) rbest = cur;
                if (cur.viol == 0 && cur.lang > feas_lang) { feas_lang = cur.lang; feas = cur; }
                it += 24;
                continue;
            }
            cand = cur;
            if (g_plns > 0 && rnd01() < g_plns) {
                long long before = evals;
                large_move(&c, &cand, free_cols, nfree, &evals);
                it += evals - before - 1;
            } else {
                propose(&c, &cand, free_cols, nfree);
                evaluate(&c, &cand);
                evals++;
            }
            double d = cand.obj - cur.obj;
            if (d >= 0 || rnd01() < exp(d / T)) {
                cur = cand;
                if (cur.obj > rbest.obj) rbest = cur;
                if (cur.viol == 0 && cur.lang > feas_lang) { feas_lang = cur.lang; feas = cur; }
            }
        }
        restart_best[r] = rbest.obj;
        if (rbest.obj > best.obj) best = rbest;
    }
    int hits = 0;
    for (int r = 0; r < restarts; r++)
        if (restart_best[r] > best.obj - 0.5) hits++;

    memcpy(out_best, best.A, sizeof(int) * 26);
    memcpy(out_best + 26, best.Binv, sizeof(int) * 26);
    memcpy(out_best + 52, best.K, sizeof(int) * period);
    memcpy(out_best + 52 + period, best.plain, sizeof(int) * n);
    if (feas_lang > -1e299) {
        memcpy(out_feas, feas.A, sizeof(int) * 26);
        memcpy(out_feas + 26, feas.Binv, sizeof(int) * 26);
        memcpy(out_feas + 52, feas.K, sizeof(int) * period);
        memcpy(out_feas + 52 + period, feas.plain, sizeof(int) * n);
    }
    out[0] = best.obj; out[1] = best.lang; out[2] = best.viol; out[3] = feas_lang;
    out[4] = (double)evals; out[5] = hits;
}

/* Parallel tempering. `replicas` chains at temperatures geometric from t_hi down to t_lo,
 * `iters` moves per chain, neighbour exchange tried every `exch` moves. Restarts repeat the
 * whole ladder from fresh random states. Outputs as in q_anneal. */
void q_tempering(int family, int n, const int *ct, int period, int ncl, const int *cpos, const int *cpl,
                 const double *q4, const double *p1, const double *p2, const double *p3, double lambda,
                 int restarts, int replicas, long long iters, double t_hi, double t_lo, int exch,
                 unsigned long long seed, int *out_best, int *out_feas, double *out, double *restart_best) {
    Ctx c;
    memset(&c, 0, sizeof c);
    c.family = family; c.n = n; c.period = period; c.derive = 1; c.ct = ct;
    c.ncl = ncl; c.cpos = cpos; c.cpl = cpl; c.q4 = q4; c.p1 = p1; c.p2 = p2; c.p3 = p3;
    c.lambda = lambda;
    for (int k = 0; k < ncl; k++) c.clue_col[cpos[k] % period] = 1;
    setup_components(&c);
    rng_state = seed * 0x9E3779B97F4A7C15ULL + 0x7654321ULL;
    if (rng_state == 0) rng_state = 1;
    for (int w = 0; w < 10; w++) rnd();
    int free_cols[MAXP], nfree = 0;
    for (int j = 0; j < period; j++)
        if (!c.clue_col[j]) free_cols[nfree++] = j;
    if (replicas > 32) replicas = 32;
    static State ch[32];
    double T[32];
    for (int m = 0; m < replicas; m++)
        T[m] = replicas > 1 ? t_hi * pow(t_lo / t_hi, (double)m / (replicas - 1)) : t_lo;
    State best, feas, cand;
    best.obj = -1e300;
    double feas_lang = -1e300;
    long long evals = 0;
    for (int r = 0; r < restarts; r++) {
        for (int m = 0; m < replicas; m++) {
            State *cur = &ch[m];
            if (family == 2) for (int i = 0; i < 26; i++) cur->A[i] = i; else random_perm(cur->A);
            if (family == 1) for (int i = 0; i < 26; i++) cur->Binv[i] = i; else random_perm(cur->Binv);
            for (int j = 0; j < period; j++) cur->K[j] = rndint(26);
            set_inverse(cur);
            evaluate(&c, cur);
            evals++;
        }
        double rb = -1e300;
        for (long long it = 0; it < iters; it++) {
            for (int m = 0; m < replicas; m++) {
                State *cur = &ch[m];
                cand = *cur;
                propose(&c, &cand, free_cols, nfree);
                evaluate(&c, &cand);
                evals++;
                double d = cand.obj - cur->obj;
                if (d >= 0 || rnd01() < exp(d / T[m])) {
                    *cur = cand;
                    if (cur->obj > rb) rb = cur->obj;
                    if (cur->obj > best.obj) best = *cur;
                    if (cur->viol == 0 && cur->lang > feas_lang) { feas_lang = cur->lang; feas = *cur; }
                }
            }
            if (exch > 0 && it % exch == exch - 1) {
                for (int m = 0; m + 1 < replicas; m++) {
                    double a = (ch[m + 1].obj - ch[m].obj) * (1.0 / T[m] - 1.0 / T[m + 1]);
                    if (a >= 0 || rnd01() < exp(a)) {
                        State t = ch[m]; ch[m] = ch[m + 1]; ch[m + 1] = t;
                    }
                }
            }
        }
        restart_best[r] = rb;
    }
    int hits = 0;
    for (int r = 0; r < restarts; r++)
        if (restart_best[r] > best.obj - 0.5) hits++;
    memcpy(out_best, best.A, sizeof(int) * 26);
    memcpy(out_best + 26, best.Binv, sizeof(int) * 26);
    memcpy(out_best + 52, best.K, sizeof(int) * period);
    memcpy(out_best + 52 + period, best.plain, sizeof(int) * n);
    if (feas_lang > -1e299) {
        memcpy(out_feas, feas.A, sizeof(int) * 26);
        memcpy(out_feas + 26, feas.Binv, sizeof(int) * 26);
        memcpy(out_feas + 52, feas.K, sizeof(int) * period);
        memcpy(out_feas + 52 + period, feas.plain, sizeof(int) * n);
    }
    out[0] = best.obj; out[1] = best.lang; out[2] = best.viol; out[3] = feas_lang;
    out[4] = (double)evals; out[5] = hits;
}
