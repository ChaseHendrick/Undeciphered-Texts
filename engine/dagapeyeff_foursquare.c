/* Four-square annealing kernel for engine.dagapeyeff_foursquare. Not a reading.
 *
 * The plain squares are fixed. The two cipher squares are searched. The
 * score is a quadgram log probability. The best squares and score are
 * returned; the caller decides what, if anything, to keep.
 */
#include <math.h>
#include <string.h>

static unsigned long long state;

static unsigned int next_u32(void) {
    state ^= state << 13;
    state ^= state >> 7;
    state ^= state << 17;
    return (unsigned int)(state >> 32);
}

static double next_unit(void) { return (next_u32() + 0.5) / 4294967296.0; }

static double score(const int *ct, int n, const double *logp, const int *plain,
                    const int *ur, const int *ll, int *buf) {
    int pos_ur[25], pos_ll[25];
    for (int i = 0; i < 25; i++) { pos_ur[ur[i]] = i; pos_ll[ll[i]] = i; }
    for (int k = 0; k < n; k++) {
        int a = pos_ur[ct[2 * k]], b = pos_ll[ct[2 * k + 1]];
        int r1 = a / 5, c2 = a % 5, r2 = b / 5, c1 = b % 5;
        buf[2 * k] = plain[r1 * 5 + c1];
        buf[2 * k + 1] = plain[r2 * 5 + c2];
    }
    double total = 0.0;
    int m = 2 * n;
    for (int i = 3; i < m; i++)
        total += logp[((buf[i - 3] * 26 + buf[i - 2]) * 26 + buf[i - 1]) * 26 + buf[i]];
    return total;
}

static void shuffle(int *sq) {
    for (int i = 24; i > 0; i--) {
        int j = next_u32() % (i + 1);
        int t = sq[i]; sq[i] = sq[j]; sq[j] = t;
    }
}

static void move(int *sq) {
    unsigned int kind = next_u32() % 20;
    if (kind < 18) {
        int i = next_u32() % 25, j = next_u32() % 25;
        int t = sq[i]; sq[i] = sq[j]; sq[j] = t;
    } else if (kind == 18) {
        int r = next_u32() % 5, s = next_u32() % 5;
        for (int c = 0; c < 5; c++) { int t = sq[r * 5 + c]; sq[r * 5 + c] = sq[s * 5 + c]; sq[s * 5 + c] = t; }
    } else {
        int r = next_u32() % 5, s = next_u32() % 5;
        for (int c = 0; c < 5; c++) { int t = sq[c * 5 + r]; sq[c * 5 + r] = sq[c * 5 + s]; sq[c * 5 + s] = t; }
    }
}

/* ct holds 2n symbols in 0..24. Returns the best score over the restarts. */
double fs_anneal(const int *ct, int n, const double *logp, const int *plain,
                 unsigned long long seed, int restarts, int steps, double t0,
                 int *best_ur, int *best_ll, int *best_plain) {
    int buf[4096], ur[25], ll[25], cur_ur[25], cur_ll[25];
    double best = -1e300;
    state = seed * 2654435761ULL + 88172645463325252ULL;
    if (2 * n > 4096) return 0.0;
    for (int r = 0; r < restarts; r++) {
        for (int i = 0; i < 25; i++) { cur_ur[i] = i; cur_ll[i] = i; }
        shuffle(cur_ur); shuffle(cur_ll);
        double cur = score(ct, n, logp, plain, cur_ur, cur_ll, buf);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(ur, cur_ur, sizeof ur); memcpy(ll, cur_ll, sizeof ll);
            unsigned int which = next_u32() % 3;
            if (which != 1) move(ur);
            if (which != 0) move(ll);
            double s = score(ct, n, logp, plain, ur, ll, buf);
            if (s >= cur || next_unit() < exp((s - cur) / temp)) {
                cur = s;
                memcpy(cur_ur, ur, sizeof ur); memcpy(cur_ll, ll, sizeof ll);
                if (cur > best) {
                    best = cur;
                    memcpy(best_ur, cur_ur, sizeof ur); memcpy(best_ll, cur_ll, sizeof ll);
                }
            }
        }
    }
    score(ct, n, logp, plain, best_ur, best_ll, buf);
    memcpy(best_plain, buf, sizeof(int) * 2 * n);
    return best;
}
