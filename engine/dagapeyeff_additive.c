/* Keyed Polybius square with a repeating coordinate shift, annealed, for
 * engine.dagapeyeff_additive. Not a reading.
 *
 * Cipher cell x at place i is (row, column) = (x / 5, x % 5). Phase j = i mod
 * period carries a shift (dr, dc). The plaintext cell is ((row - dr) mod 5,
 * (column - dc) mod 5) and the square sends that cell to one of 25 letters.
 * mode 0 shifts both coordinates, 1 the column only, 2 the row only. The
 * square and the shifts are annealed together under a quadgram score.
 */
#include <math.h>
#include <string.h>

#define N_MAX 512

static unsigned int next_u32(unsigned long long *state) {
    *state ^= *state << 13;
    *state ^= *state >> 7;
    *state ^= *state << 17;
    return (unsigned int)(*state >> 32);
}

static double next_unit(unsigned long long *state) { return (next_u32(state) + 0.5) / 4294967296.0; }

static double score(const int *ct, int n, int period, const double *logp, const int *letters,
                    const int *square, const int *dr, const int *dc, int *buf) {
    for (int i = 0; i < n; i++) {
        int j = i % period, x = ct[i];
        int r = (x / 5 - dr[j] + 5) % 5, c = (x % 5 - dc[j] + 5) % 5;
        buf[i] = letters[square[r * 5 + c]];
    }
    double total = 0.0;
    for (int i = 3; i < n; i++)
        total += logp[((buf[i - 3] * 26 + buf[i - 2]) * 26 + buf[i - 1]) * 26 + buf[i]];
    return total;
}

double additive_anneal(const int *ct, int n, int period, int mode, const double *logp, const int *letters,
                       unsigned long long seed, int restarts, int steps, double t0, double key_share,
                       int *best_square, int *best_dr, int *best_dc, int *best_plain) {
    int buf[N_MAX], square[25], dr[N_MAX], dc[N_MAX], cur_square[25], cur_dr[N_MAX], cur_dc[N_MAX];
    double best = -1e300;
    unsigned long long state = seed * 2654435761ULL + 88172645463325252ULL;
    if (n > N_MAX || period < 1 || period > n) return 0.0;
    for (int r = 0; r < restarts; r++) {
        for (int i = 0; i < 25; i++) cur_square[i] = i;
        for (int i = 24; i > 0; i--) {
            int j = next_u32(&state) % (i + 1);
            int t = cur_square[i]; cur_square[i] = cur_square[j]; cur_square[j] = t;
        }
        for (int j = 0; j < period; j++) {
            cur_dr[j] = (mode == 1 || j == 0) ? 0 : next_u32(&state) % 5;
            cur_dc[j] = (mode == 2 || j == 0) ? 0 : next_u32(&state) % 5;
        }
        double cur = score(ct, n, period, logp, letters, cur_square, cur_dr, cur_dc, buf);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(square, cur_square, sizeof square);
            memcpy(dr, cur_dr, sizeof(int) * period); memcpy(dc, cur_dc, sizeof(int) * period);
            if (period > 1 && next_unit(&state) < key_share) {
                /* Phase 0 stays at zero: a shift of every phase is a turn of the square. */
                int j = 1 + next_u32(&state) % (period - 1);
                if (mode != 1) dr[j] = next_u32(&state) % 5;
                if (mode != 2) dc[j] = next_u32(&state) % 5;
            } else {
                int i = next_u32(&state) % 25, k = next_u32(&state) % 25;
                int t = square[i]; square[i] = square[k]; square[k] = t;
            }
            double s = score(ct, n, period, logp, letters, square, dr, dc, buf);
            if (s >= cur || next_unit(&state) < exp((s - cur) / temp)) {
                cur = s;
                memcpy(cur_square, square, sizeof square);
                memcpy(cur_dr, dr, sizeof(int) * period); memcpy(cur_dc, dc, sizeof(int) * period);
                if (cur > best) {
                    best = cur;
                    memcpy(best_square, cur_square, sizeof square);
                    memcpy(best_dr, cur_dr, sizeof(int) * period); memcpy(best_dc, cur_dc, sizeof(int) * period);
                }
            }
        }
    }
    score(ct, n, period, logp, letters, best_square, best_dr, best_dc, buf);
    memcpy(best_plain, buf, sizeof(int) * n);
    return best;
}
