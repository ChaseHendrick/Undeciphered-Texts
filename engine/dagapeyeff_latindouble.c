/* Double columnar transposition with a letter key, annealed together under a
 * quadgram model, for engine.dagapeyeff_latindouble. Not a reading.
 *
 * Encryption: 196 letters are put through a keyed square (one-to-one, 25
 * symbols), written in rows of w1 (short last row allowed: the first 196 % w1
 * columns are one longer), read out by columns in key order; the result is
 * written in rows of w2 and read out the same way. The cipher symbols are the
 * second read-out. slot[c] is the place column c is read in.
 * The kernel undoes both transpositions and scores the letters.
 */
#include <math.h>
#include <string.h>

#define MAXW 32
#define N 196

static unsigned int next_u32(unsigned long long *s) {
    *s ^= *s << 13; *s ^= *s >> 7; *s ^= *s << 17;
    return (unsigned int)(*s >> 32);
}
static double next_unit(unsigned long long *s) { return (next_u32(s) + 0.5) / 4294967296.0; }

/* src[i]: position in the written text of the i-th read-out symbol. */
static void read_map(int w, const int *slot, int *src) {
    int rows = (N + w - 1) / w, rem = N % w, inv[MAXW], at = 0;
    for (int c = 0; c < w; c++) inv[slot[c]] = c;
    for (int j = 0; j < w; j++) {
        int c = inv[j], len = (rem == 0 || c < rem) ? rows : rows - 1;
        for (int r = 0; r < len; r++) src[at++] = r * w + c;
    }
}

static double score(const int *ct, const double *logp, const int *letters, int w1, int w2,
                    const int *s1, const int *s2, const int *key, int *buf) {
    int m1[N], m2[N];
    read_map(w1, s1, m1);
    read_map(w2, s2, m2);
    /* cipher i came from intermediate m2[i], which came from plaintext m1[m2[i]] */
    for (int i = 0; i < N; i++) buf[m1[m2[i]]] = letters[key[ct[i]]];
    double t = 0.0;
    for (int i = 3; i < N; i++)
        t += logp[((buf[i - 3] * 26 + buf[i - 2]) * 26 + buf[i - 1]) * 26 + buf[i]];
    return t;
}

static void shuffle(int *a, int n, unsigned long long *s) {
    for (int i = n - 1; i > 0; i--) { int j = next_u32(s) % (i + 1), t = a[i]; a[i] = a[j]; a[j] = t; }
}

static void move_order(int *o, int W, unsigned long long *s) {
    unsigned int kind = next_u32(s) % 4;
    int i = next_u32(s) % W, j = next_u32(s) % W;
    if (i == j) j = (j + 1) % W;
    if (kind == 0) { int t = o[i]; o[i] = o[j]; o[j] = t; }
    else if (kind == 1) {
        int t = o[i];
        if (i < j) memmove(o + i, o + i + 1, sizeof(int) * (j - i));
        else memmove(o + j + 1, o + j, sizeof(int) * (i - j));
        o[j] = t;
    } else if (kind == 2) {
        int a = i < j ? i : j, b = i < j ? j : i;
        while (a < b) { int t = o[a]; o[a] = o[b]; o[b] = t; a++; b--; }
    } else {
        int len = 1 + next_u32(s) % 4; if (len > W - 1) len = W - 1;
        int from = next_u32(s) % (W - len + 1), tmp[MAXW], run[4], n = 0;
        for (int k = 0; k < len; k++) run[k] = o[from + k];
        for (int k = 0; k < W; k++) if (k < from || k >= from + len) tmp[n++] = o[k];
        int to = next_u32(s) % (n + 1), out = 0;
        for (int k = 0; k < to; k++) o[out++] = tmp[k];
        for (int k = 0; k < len; k++) o[out++] = run[k];
        for (int k = to; k < n; k++) o[out++] = tmp[k];
    }
}

/* Key-invariant score: repeated pairs and triples in plaintext order. A
 * one-to-one letter key cannot change it. */
static double iscore(const int *ct, int w1, int w2, const int *s1, const int *s2, int *buf, double tri) {
    int m1[N], m2[N];
    static __thread int pc[625];
    static __thread unsigned short tc[15625];
    read_map(w1, s1, m1);
    read_map(w2, s2, m2);
    for (int i = 0; i < N; i++) buf[m1[m2[i]]] = ct[i];
    memset(pc, 0, sizeof pc);
    double t = 0.0;
    for (int i = 1; i < N; i++) t += pc[buf[i - 1] * 25 + buf[i]]++;
    if (tri > 0) {
        double u = 0.0;
        for (int i = 2; i < N; i++) u += tc[(buf[i - 2] * 25 + buf[i - 1]) * 25 + buf[i]]++;
        for (int i = 2; i < N; i++) tc[(buf[i - 2] * 25 + buf[i - 1]) * 25 + buf[i]] = 0;
        t += tri * u;
    }
    return t;
}

/* slot arrays are kept as "order" lists: order[j] = column read j-th. */
static void order_to_slot(const int *o, int W, int *slot) { for (int j = 0; j < W; j++) slot[o[j]] = j; }

double dt_anneal(const int *ct, const double *logp, const int *letters, const int *start_key,
                 int w1, int w2, unsigned long long seed, int restarts, int steps, double t0,
                 double key_share, int *best_s1, int *best_s2, int *best_key, int *best_plain) {
    int buf[N], o1[MAXW], o2[MAXW], c1[MAXW], c2[MAXW], key[25], ck[25], s1[MAXW], s2[MAXW];
    double best = -1e300;
    unsigned long long st = seed * 2654435761ULL + 88172645463325252ULL;
    for (int r = 0; r < restarts; r++) {
        for (int i = 0; i < w1; i++) c1[i] = i;
        for (int i = 0; i < w2; i++) c2[i] = i;
        shuffle(c1, w1, &st); shuffle(c2, w2, &st);
        memcpy(ck, start_key, sizeof ck);
        order_to_slot(c1, w1, s1); order_to_slot(c2, w2, s2);
        double cur = score(ct, logp, letters, w1, w2, s1, s2, ck, buf);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(o1, c1, sizeof(int) * w1); memcpy(o2, c2, sizeof(int) * w2); memcpy(key, ck, sizeof key);
            double u = next_unit(&st);
            if (u < key_share) {
                int i = next_u32(&st) % 25, j = next_u32(&st) % 25, t = key[i]; key[i] = key[j]; key[j] = t;
            } else if (u < key_share + (1.0 - key_share) / 2) move_order(o1, w1, &st);
            else move_order(o2, w2, &st);
            order_to_slot(o1, w1, s1); order_to_slot(o2, w2, s2);
            double sc = score(ct, logp, letters, w1, w2, s1, s2, key, buf);
            if (sc >= cur || next_unit(&st) < exp((sc - cur) / temp)) {
                cur = sc;
                memcpy(c1, o1, sizeof(int) * w1); memcpy(c2, o2, sizeof(int) * w2); memcpy(ck, key, sizeof ck);
                if (cur > best) {
                    best = cur;
                    order_to_slot(c1, w1, best_s1); order_to_slot(c2, w2, best_s2);
                    memcpy(best_key, ck, sizeof ck);
                }
            }
        }
    }
    score(ct, logp, letters, w1, w2, best_s1, best_s2, best_key, buf);
    memcpy(best_plain, buf, sizeof(int) * N);
    return best;
}

/* Phase one: both orders under the key-invariant score. Returns the best. */
double dt_orders(const int *ct, int w1, int w2, unsigned long long seed, int restarts, int steps, double t0,
                 double tri, int *best_o1, int *best_o2) {
    int buf[N], o1[MAXW], o2[MAXW], c1[MAXW], c2[MAXW], s1[MAXW], s2[MAXW];
    double best = -1e300;
    unsigned long long st = seed * 2654435761ULL + 88172645463325252ULL;
    for (int r = 0; r < restarts; r++) {
        for (int i = 0; i < w1; i++) c1[i] = i;
        for (int i = 0; i < w2; i++) c2[i] = i;
        shuffle(c1, w1, &st); shuffle(c2, w2, &st);
        order_to_slot(c1, w1, s1); order_to_slot(c2, w2, s2);
        double cur = iscore(ct, w1, w2, s1, s2, buf, tri);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(o1, c1, sizeof(int) * w1); memcpy(o2, c2, sizeof(int) * w2);
            if (next_unit(&st) < 0.5) move_order(o1, w1, &st); else move_order(o2, w2, &st);
            order_to_slot(o1, w1, s1); order_to_slot(o2, w2, s2);
            double sc = iscore(ct, w1, w2, s1, s2, buf, tri);
            if (sc >= cur || next_unit(&st) < exp((sc - cur) / temp)) {
                cur = sc;
                memcpy(c1, o1, sizeof(int) * w1); memcpy(c2, o2, sizeof(int) * w2);
                if (cur > best) { best = cur; memcpy(best_o1, c1, sizeof(int) * w1); memcpy(best_o2, c2, sizeof(int) * w2); }
            }
        }
    }
    return best;
}

/* Phase two: the letter key alone under the quadgram model, orders fixed,
 * then a joint polish. Orders are given as read orders (order[j] = column). */
double dt_key(const int *ct, const double *logp, const int *letters, const int *start_key, int w1, int w2,
              const int *o1in, const int *o2in, unsigned long long seed, int restarts, int steps, double t0,
              double polish_share, int *best_o1, int *best_o2, int *best_key) {
    int buf[N], o1[MAXW], o2[MAXW], c1[MAXW], c2[MAXW], key[25], ck[25], s1[MAXW], s2[MAXW];
    double best = -1e300;
    unsigned long long st = seed * 2654435761ULL + 88172645463325252ULL;
    for (int r = 0; r < restarts; r++) {
        memcpy(c1, o1in, sizeof(int) * w1); memcpy(c2, o2in, sizeof(int) * w2);
        memcpy(ck, start_key, sizeof ck);
        if (r > 0) for (int k = 0; k < 25; k++) { int i = next_u32(&st) % 25, t = ck[i]; ck[i] = ck[k]; ck[k] = t; }
        order_to_slot(c1, w1, s1); order_to_slot(c2, w2, s2);
        double cur = score(ct, logp, letters, w1, w2, s1, s2, ck, buf);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(o1, c1, sizeof(int) * w1); memcpy(o2, c2, sizeof(int) * w2); memcpy(key, ck, sizeof key);
            double u = next_unit(&st);
            if (u >= polish_share) { int i = next_u32(&st) % 25, j = next_u32(&st) % 25, t = key[i]; key[i] = key[j]; key[j] = t; }
            else if (u < polish_share / 2) move_order(o1, w1, &st);
            else move_order(o2, w2, &st);
            order_to_slot(o1, w1, s1); order_to_slot(o2, w2, s2);
            double sc = score(ct, logp, letters, w1, w2, s1, s2, key, buf);
            if (sc >= cur || next_unit(&st) < exp((sc - cur) / temp)) {
                cur = sc;
                memcpy(c1, o1, sizeof(int) * w1); memcpy(c2, o2, sizeof(int) * w2); memcpy(ck, key, sizeof ck);
                if (cur > best) {
                    best = cur;
                    memcpy(best_o1, c1, sizeof(int) * w1); memcpy(best_o2, c2, sizeof(int) * w2);
                    memcpy(best_key, ck, sizeof ck);
                }
            }
        }
    }
    return best;
}
