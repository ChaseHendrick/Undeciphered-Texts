/* Columnar transposition of any width with a letter key, annealed together,
 * for engine.dagapeyeff_columnarw. Not a reading.
 *
 * The plaintext of 196 letters is written in rows of `width`; the last row
 * may be short, so the first 196 % width columns are one letter longer.
 * Columns are copied out in key order: slot[c] is the place column c is
 * copied in. Each cipher symbol (0 to 24) is sent to one of 25 plaintext
 * letters. The score is a quadgram log probability. The best order, key and
 * score are returned; the caller decides what, if anything, to keep.
 */
#include <math.h>
#include <string.h>

#define MAXW 32
#define N 196

/* The generator state is per call, so calls may run side by side. */
static unsigned int next_u32(unsigned long long *state) {
    *state ^= *state << 13;
    *state ^= *state >> 7;
    *state ^= *state << 17;
    return (unsigned int)(*state >> 32);
}

static double next_unit(unsigned long long *state) { return (next_u32(state) + 0.5) / 4294967296.0; }

static double score(const int *ct, const double *logp, const int *letters, int w,
                    const int *slot, const int *key, int done, int *buf) {
    int rows = (N + w - 1) / w, rem = N % w, inv[MAXW], off[MAXW], run = 0;
    for (int c = 0; c < w; c++) inv[slot[c]] = c;
    for (int j = 0; j < w; j++) {
        int c = inv[j];
        off[c] = run;
        run += (rem == 0 || c < rem) ? rows : rows - 1;
    }
    for (int c = 0; c < w; c++) {
        int len = (rem == 0 || c < rem) ? rows : rows - 1;
        for (int r = 0; r < len; r++) {
            if (done) buf[off[c] + r] = letters[key[ct[r * w + c]]];
            else buf[r * w + c] = letters[key[ct[off[c] + r]]];
        }
    }
    double total = 0.0;
    for (int i = 3; i < N; i++)
        total += logp[((buf[i - 3] * 26 + buf[i - 2]) * 26 + buf[i - 1]) * 26 + buf[i]];
    return total;
}

static void shuffle(int *a, int n, unsigned long long *state) {
    for (int i = n - 1; i > 0; i--) {
        int j = next_u32(state) % (i + 1);
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
}

static void move_order(int *order, int W, unsigned long long *state) {
    unsigned int kind = next_u32(state) % 4;
    int i = next_u32(state) % W, j = next_u32(state) % W;
    if (i == j) j = (j + 1) % W;
    if (kind == 0) {
        int t = order[i]; order[i] = order[j]; order[j] = t;
    } else if (kind == 1) {
        int t = order[i];
        if (i < j) { memmove(order + i, order + i + 1, sizeof(int) * (j - i)); }
        else { memmove(order + j + 1, order + j, sizeof(int) * (i - j)); }
        order[j] = t;
    } else if (kind == 2) {
        int a = i < j ? i : j, b = i < j ? j : i;
        while (a < b) { int t = order[a]; order[a] = order[b]; order[b] = t; a++; b--; }
    } else {
        /* move a run of columns to another place */
        int len = 1 + next_u32(state) % 4;
        if (len > W - 1) len = W - 1;
        int from = next_u32(state) % (W - len + 1);
        int tmp[MAXW], run[4], n = 0;
        for (int k = 0; k < len; k++) run[k] = order[from + k];
        for (int k = 0; k < W; k++) if (k < from || k >= from + len) tmp[n++] = order[k];
        int to = next_u32(state) % (n + 1);
        int out = 0;
        for (int k = 0; k < to; k++) order[out++] = tmp[k];
        for (int k = 0; k < len; k++) order[out++] = run[k];
        for (int k = to; k < n; k++) order[out++] = tmp[k];
    }
}

/* ct holds 196 symbols in 0..24; W is the width, 2 to 32; start_key is the
 * key each restart begins from; done picks the direction. Returns the best
 * score over the restarts. */
double cw_anneal(const int *ct, const double *logp, const int *letters, const int *start_key,
                 int W, int done, unsigned long long seed, int restarts, int steps, double t0,
                 double key_share, int *best_order, int *best_key, int *best_plain) {
    int buf[N], order[MAXW], key[25], cur_order[MAXW], cur_key[25];
    double best = -1e300;
    unsigned long long state = seed * 2654435761ULL + 88172645463325252ULL;
    for (int r = 0; r < restarts; r++) {
        for (int i = 0; i < W; i++) cur_order[i] = i;
        shuffle(cur_order, W, &state);
        memcpy(cur_key, start_key, sizeof cur_key);
        double cur = score(ct, logp, letters, W, cur_order, cur_key, done, buf);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(order, cur_order, sizeof(int) * W); memcpy(key, cur_key, sizeof key);
            if (next_unit(&state) < key_share) {
                int i = next_u32(&state) % 25, j = next_u32(&state) % 25;
                int t = key[i]; key[i] = key[j]; key[j] = t;
            } else {
                move_order(order, W, &state);
            }
            double s = score(ct, logp, letters, W, order, key, done, buf);
            if (s >= cur || next_unit(&state) < exp((s - cur) / temp)) {
                cur = s;
                memcpy(cur_order, order, sizeof(int) * W); memcpy(cur_key, key, sizeof key);
                if (cur > best) {
                    best = cur;
                    memcpy(best_order, cur_order, sizeof(int) * W); memcpy(best_key, cur_key, sizeof key);
                }
            }
        }
    }
    score(ct, logp, letters, W, best_order, best_key, done, buf);
    memcpy(best_plain, buf, sizeof(int) * N);
    return best;
}
