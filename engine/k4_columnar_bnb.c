/* Branch and bound over columnar orders for engine.k4_columnar_bnb.
 * Not a reading.
 *
 * Same model and conventions as engine/k4_transposition_sub.c: width w,
 * incomplete last row (the first n mod w columns are one letter longer),
 * dir 0 writes rows and reads columns in order, dir 1 is the inverse.
 * comp 0 transposes then substitutes (clue k keys on column T[j] mod p),
 * comp 1 substitutes then transposes (clue k keys on column j mod p).
 *
 * Variants v = 2a + b as there (a 0 A-Z, 1 KRYPTOS; b 0 Vigenere,
 * 1 Beaufort), and v = 4 for any alphabet per column (the bijection bound).
 *
 * The order is built one read column at a time. Choosing the k-th column
 * fixes where every clue letter in it lands, so its key letters can be
 * checked at once and a contradiction drops every order with that prefix.
 * Counts are of complete orders that survive, the same unit as the full
 * enumeration, so the two can be compared width by width.
 */
#include <string.h>

#define MAXW 24
#define MAXCL 32
#define MAXP 32

typedef struct {
    int n, w, dir, comp, p, v, ncl;
    const int *ct, *cpos, *cpl, *rank;
    int len[MAXW];
    int key[MAXP];
    unsigned char pm[MAXP * 26], cm[MAXP * 27];
    int filled;
    long long leaves, complete, nodes;
    int order[MAXW];
    int *found;     /* complete-key orders, w ints each */
    int cap, nfound;
    long long node_limit;
    int stopped;
} Search;

/* Place clue k at ciphertext position t. Returns 0 on contradiction.
 * Undo information is pushed on the caller's stack. */
static int place(Search *s, int k, int t, int *undo, int *nundo) {
    int c = s->ct[t], pl = s->cpl[k];
    int col = (s->comp == 0 ? t : s->cpos[k]) % s->p;
    if (s->v == 4) {
        int a = col * 26 + pl, b = col * 27 + c;
        if (s->pm[a] == 0 && s->cm[b] == 0) {
            s->pm[a] = (unsigned char)(c + 1);
            s->cm[b] = (unsigned char)(pl + 1);
            undo[(*nundo)++] = a;
            undo[(*nundo)++] = b;
            return 1;
        }
        return s->pm[a] == c + 1 && s->cm[b] == pl + 1;
    }
    if (c > 25) return 0;
    const int *r = s->rank + (s->v >> 1) * 26;
    int shift = (s->v & 1) ? (r[c] + r[pl]) % 26 : (r[c] - r[pl] + 26) % 26;
    if (s->key[col] < 0) {
        s->key[col] = shift;
        s->filled++;
        undo[(*nundo)++] = col;
        return 1;
    }
    return s->key[col] == shift;
}

static void unplace(Search *s, const int *undo, int nundo) {
    if (s->v == 4) {
        for (int i = 0; i < nundo; i += 2) {
            s->pm[undo[i]] = 0;
            s->cm[undo[i + 1]] = 0;
        }
        return;
    }
    for (int i = 0; i < nundo; i++) {
        s->key[undo[i]] = -1;
        s->filled--;
    }
}

static void dfs(Search *s, int depth, int cum, unsigned used) {
    if (s->stopped) return;
    if (++s->nodes > s->node_limit && s->node_limit > 0) {
        s->stopped = 1;
        return;
    }
    if (depth == s->w) {
        s->leaves++;
        if (s->v != 4 && s->filled == s->p) {
            if (s->nfound < s->cap) memcpy(s->found + (long long)s->nfound * s->w, s->order, sizeof(int) * s->w);
            s->nfound++;
            s->complete++;
        }
        return;
    }
    for (int c = 0; c < s->w; c++) {
        if (used & (1u << c)) continue;
        int undo[2 * MAXCL], nundo = 0, ok = 1;
        for (int k = 0; k < s->ncl && ok; k++) {
            int j = s->cpos[k], t;
            if (s->dir == 0) {
                if (j % s->w != c) continue;
                t = cum + j / s->w;
            } else {
                if (j < cum || j >= cum + s->len[c]) continue;
                t = (j - cum) * s->w + c;
            }
            ok = place(s, k, t, undo, &nundo);
        }
        if (ok) {
            s->order[depth] = c;
            dfs(s, depth + 1, cum + s->len[c], used | (1u << c));
        }
        unplace(s, undo, nundo);
    }
}

/* One (w, dir, comp, p, v) search. out[0] leaves, out[1] complete keys,
 * out[2] nodes, out[3] 1 if the node limit stopped it. */
void bnb(int n, const int *ct, int ncl, const int *cpos, const int *cpl, const int *rank,
         int w, int dir, int comp, int p, int v, long long node_limit,
         int *found, int cap, long long *out) {
    Search s;
    memset(&s, 0, sizeof s);
    s.n = n; s.w = w; s.dir = dir; s.comp = comp; s.p = p; s.v = v; s.ncl = ncl;
    s.ct = ct; s.cpos = cpos; s.cpl = cpl; s.rank = rank;
    s.found = found; s.cap = cap; s.node_limit = node_limit;
    int rows = (n + w - 1) / w, full = n % w;
    for (int c = 0; c < w; c++) s.len[c] = (full == 0 || c < full) ? rows : rows - 1;
    for (int i = 0; i < p; i++) s.key[i] = -1;
    dfs(&s, 0, 0, 0u);
    out[0] = s.leaves;
    out[1] = s.complete;
    out[2] = s.nodes;
    out[3] = s.stopped;
}

/* Direction 1 (write columns in order, read rows) by slot patterns.
 *
 * Only the long or short type of earlier read slots fixes where a slot's
 * plaintext range starts, so the search walks the slots in order, picks a
 * type for each, and picks an actual column only for slots whose range
 * holds clue letters. Past the last clue position nothing else can be
 * checked, and the remaining choices are counted, not listed:
 * C(open slots, open long slots) * (unused long columns)! * (unused short columns)!.
 * Columns c < n mod w are the long ones, as in the enumeration.
 */
typedef struct {
    Search *s;
    int last;          /* largest clue plaintext position */
    int nlong, nshort; /* column counts by type */
    double fact[MAXW + 1];
    double total, complete;
} Slots;

static double choose(int n, int k) {
    double r = 1;
    if (k < 0 || k > n) return 0;
    for (int i = 1; i <= k; i++) r = r * (n - k + i) / i;
    return r;
}

static void slot_dfs(Slots *z, int depth, int cum, int long_used, int short_used, int long_cols_used,
                     int short_cols_used, unsigned used) {
    Search *s = z->s;
    if (++s->nodes > s->node_limit && s->node_limit > 0) {
        s->stopped = 1;
        return;
    }
    if (s->stopped) return;
    if (cum > z->last || depth == s->w) {
        int open = s->w - depth;
        int open_long = z->nlong - long_used;
        double ways = choose(open, open_long) * z->fact[z->nlong - long_cols_used] * z->fact[z->nshort - short_cols_used];
        z->total += ways;
        if (s->v != 4 && s->filled == s->p) z->complete += ways;
        return;
    }
    for (int type = 0; type < 2; type++) { /* 0 long, 1 short */
        if (type == 0 && long_used == z->nlong) continue;
        if (type == 1 && short_used == z->nshort) continue;
        int len = type == 0 ? s->len[0] : s->len[s->w - 1];
        int holds = 0;
        for (int k = 0; k < s->ncl; k++)
            if (s->cpos[k] >= cum && s->cpos[k] < cum + len) { holds = 1; break; }
        if (!holds) {
            slot_dfs(z, depth + 1, cum + len, long_used + (type == 0), short_used + (type == 1),
                     long_cols_used, short_cols_used, used);
            continue;
        }
        int lo = type == 0 ? 0 : z->nlong, hi = type == 0 ? z->nlong : s->w;
        for (int c = lo; c < hi; c++) {
            if (used & (1u << c)) continue;
            int undo[2 * MAXCL], nundo = 0, ok = 1;
            for (int k = 0; k < s->ncl && ok; k++) {
                int j = s->cpos[k];
                if (j < cum || j >= cum + len) continue;
                ok = place(s, k, (j - cum) * s->w + c, undo, &nundo);
            }
            if (ok)
                slot_dfs(z, depth + 1, cum + len, long_used + (type == 0), short_used + (type == 1),
                         long_cols_used + (type == 0), short_cols_used + (type == 1), used | (1u << c));
            unplace(s, undo, nundo);
        }
    }
}

/* Direction 1 counts. out_d[0] surviving orders, out_d[1] complete keys;
 * out[0] nodes, out[1] 1 if the node limit stopped it. */
void bnb_dir1(int n, const int *ct, int ncl, const int *cpos, const int *cpl, const int *rank,
              int w, int comp, int p, int v, long long node_limit, double *out_d, long long *out) {
    Search s;
    Slots z;
    memset(&s, 0, sizeof s);
    memset(&z, 0, sizeof z);
    s.n = n; s.w = w; s.dir = 1; s.comp = comp; s.p = p; s.v = v; s.ncl = ncl;
    s.ct = ct; s.cpos = cpos; s.cpl = cpl; s.rank = rank; s.node_limit = node_limit;
    int rows = (n + w - 1) / w, full = n % w;
    for (int c = 0; c < w; c++) s.len[c] = (full == 0 || c < full) ? rows : rows - 1;
    for (int i = 0; i < p; i++) s.key[i] = -1;
    z.s = &s;
    z.nlong = full == 0 ? w : full;
    z.nshort = w - z.nlong;
    for (int k = 0; k < ncl; k++) if (cpos[k] > z.last) z.last = cpos[k];
    z.fact[0] = 1;
    for (int i = 1; i <= MAXW; i++) z.fact[i] = z.fact[i - 1] * i;
    slot_dfs(&z, 0, 0, 0, 0, 0, 0, 0u);
    out_d[0] = z.total;
    out_d[1] = z.complete;
    out[0] = s.nodes;
    out[1] = s.stopped;
}
