/* Clue-only checks of transposition plus periodic substitution, for
 * engine.k4_transposition_sub. Not a reading.
 *
 * A hypothesis is a transposition T (T[j] is the ciphertext position of
 * plaintext position j), an order of composition and a period p.
 *   comp 0, transpose then substitute: clue j uses column T[j] mod p.
 *   comp 1, substitute then transpose: clue j uses column j mod p.
 * Either way clue j shows as ciphertext symbol ct[T[j]].
 *
 * Bijection bound: inside one column two clue letters with equal plaintext
 * need equal ciphertext and the other way round, for any alphabet.
 * Strong filter on bijection survivors, four variants v:
 *   v = 2a + b, alphabet a (0 A-Z, 1 KRYPTOS keyed), b = 0 Vigenere
 *   rank(c) = rank(p) + k, b = 1 Beaufort rank(c) = k - rank(p).
 * One shift per column. A ciphertext symbol 26 ('?') never matches a shift.
 *
 * stats layout: [comp][p][NSTAT] with p from 0 to maxp (0 unused).
 *   0 checked, 1 bijection survivors, 2..5 strong survivors per variant,
 *   6..9 strong survivors whose key is complete (every column fixed),
 *   10 hypotheses passing at least one variant, 11 with a complete key in at least one.
 * A complete-key strong survivor is written to cands as CANDW ints:
 *   comp, p, v, nident, ident[0..nident-1].
 */
#include <string.h>

#define MAXCL 32
#define MAXP 32
#define NV 4
#define NSTAT 12
#define CANDW 32

typedef struct {
    const int *ct;
    int ncl;
    const int *cpos;
    const int *cpl;
    const int *rank; /* rank[a * 26 + letter] */
    int maxp;
    long long *stats;
    int *cands;
    int cap;
    int *ncand;
} Ctx;

static int bijection_ok(const int *col, const int *cl, const int *pl, int ncl) {
    /* pm[col][plain] = cipher + 1, cm[col][cipher] = plain + 1 */
    unsigned char pm[MAXP * 26];
    unsigned char cm[MAXP * 27];
    int ok = 1, k;
    for (k = 0; k < ncl; k++) {
        pm[col[k] * 26 + pl[k]] = 0;
        cm[col[k] * 27 + cl[k]] = 0;
    }
    for (k = 0; k < ncl; k++) {
        int a = col[k] * 26 + pl[k], b = col[k] * 27 + cl[k];
        if (pm[a] == 0 && cm[b] == 0) {
            pm[a] = (unsigned char)(cl[k] + 1);
            cm[b] = (unsigned char)(pl[k] + 1);
        } else if (pm[a] != cl[k] + 1 || cm[b] != pl[k] + 1) {
            ok = 0;
            break;
        }
    }
    return ok;
}

static int strong_ok(const Ctx *x, int v, const int *col, const int *cl, int p, int *complete) {
    int key[MAXP];
    const int *r = x->rank + (v >> 1) * 26;
    int beau = v & 1, k, filled = 0;
    for (k = 0; k < p; k++) key[k] = -1;
    for (k = 0; k < x->ncl; k++) {
        int c = cl[k], s;
        if (c > 25) return 0;
        s = beau ? (r[c] + r[x->cpl[k]]) % 26 : (r[c] - r[x->cpl[k]] + 26) % 26;
        if (key[col[k]] < 0) {
            key[col[k]] = s;
            filled++;
        } else if (key[col[k]] != s) {
            return 0;
        }
    }
    *complete = (filled == p);
    return 1;
}

static void evaluate(const Ctx *x, const int *tp, const int *ident, int nident) {
    int cl[MAXCL], col[MAXCL];
    int comp, p, k, v;
    for (k = 0; k < x->ncl; k++) cl[k] = x->ct[tp[k]];
    for (comp = 0; comp < 2; comp++) {
        for (p = 1; p <= x->maxp; p++) {
            long long *s = x->stats + ((long long)comp * (x->maxp + 1) + p) * NSTAT;
            for (k = 0; k < x->ncl; k++) col[k] = (comp == 0 ? tp[k] : x->cpos[k]) % p;
            s[0]++;
            if (!bijection_ok(col, cl, x->cpl, x->ncl)) continue;
            s[1]++;
            int any = 0, anyc = 0;
            for (v = 0; v < NV; v++) {
                int complete = 0;
                if (!strong_ok(x, v, col, cl, p, &complete)) continue;
                s[2 + v]++;
                any = 1;
                if (!complete) continue;
                s[6 + v]++;
                anyc = 1;
                if (*x->ncand < x->cap) {
                    int *rec = x->cands + (long long)(*x->ncand) * CANDW, i;
                    rec[0] = comp; rec[1] = p; rec[2] = v; rec[3] = nident;
                    for (i = 0; i < nident && i < CANDW - 4; i++) rec[4 + i] = ident[i];
                }
                (*x->ncand)++;
            }
            s[10] += any;
            s[11] += anyc;
        }
    }
}

/* Every permutation in perms (count rows of n), ident = idbase + row. */
void ts_perms(int n, const int *ct, int ncl, const int *cpos, const int *cpl, const int *rank, int maxp,
              const int *perms, int count, int idbase, long long *stats, int *cands, int cap, int *ncand) {
    Ctx x = {ct, ncl, cpos, cpl, rank, maxp, stats, cands, cap, ncand};
    int tp[MAXCL];
    for (int i = 0; i < count; i++) {
        const int *t = perms + (long long)i * n;
        int ident = idbase + i;
        for (int k = 0; k < ncl; k++) tp[k] = t[cpos[k]];
        evaluate(&x, tp, &ident, 1);
    }
}

/* Columnar, width w, incomplete last row, every column order with
 * order[0] == first. order[k] is the column read k-th.
 * dir 0: write rows, read columns in order. dir 1: the inverse
 * (write columns in order, read rows). ident = w, dir, order[0..w-1]. */
static void columnar_one(const Ctx *x, int n, int w, const int *order) {
    int len[16], start[16], tp[MAXCL], ident[18];
    int rows = (n + w - 1) / w, full = n % w, cum = 0, k, c;
    for (c = 0; c < w; c++) len[c] = (full == 0 || c < full) ? rows : rows - 1;
    for (k = 0; k < w; k++) {
        start[order[k]] = cum;
        cum += len[order[k]];
    }
    ident[0] = w;
    for (k = 0; k < w; k++) ident[2 + k] = order[k];
    /* dir 0 */
    for (k = 0; k < x->ncl; k++) tp[k] = start[x->cpos[k] % w] + x->cpos[k] / w;
    ident[1] = 0;
    evaluate(x, tp, ident, w + 2);
    /* dir 1: ciphertext position q with T0[q] == j */
    for (k = 0; k < x->ncl; k++) {
        int j = x->cpos[k], i;
        for (i = 0; i < w; i++) {
            c = order[i];
            if (j < start[c] + len[c]) break;
        }
        tp[k] = (j - start[c]) * w + c;
    }
    ident[1] = 1;
    evaluate(x, tp, ident, w + 2);
}

long long ts_columnar(int n, const int *ct, int ncl, const int *cpos, const int *cpl, const int *rank, int maxp,
                      int w, int first, long long *stats, int *cands, int cap, int *ncand) {
    Ctx x = {ct, ncl, cpos, cpl, rank, maxp, stats, cands, cap, ncand};
    int order[16], rest[16], cnt[16], m = 0, i, done = 0;
    long long orders = 0;
    if (w < 1 || w > 15 || first < 0 || first >= w) return -1;
    for (i = 0; i < w; i++)
        if (i != first) rest[m++] = i;
    /* Heap's algorithm over the w - 1 columns after first */
    for (i = 0; i < m; i++) cnt[i] = 0;
    order[0] = first;
    while (!done) {
        for (i = 0; i < m; i++) order[1 + i] = rest[i];
        columnar_one(&x, n, w, order);
        orders++;
        i = 1;
        while (i < m && cnt[i] >= i) {
            cnt[i] = 0;
            i++;
        }
        if (i >= m) {
            done = 1;
        } else {
            int j = (i % 2) ? cnt[i] : 0, t = rest[j];
            rest[j] = rest[i];
            rest[i] = t;
            cnt[i]++;
        }
    }
    return orders;
}
