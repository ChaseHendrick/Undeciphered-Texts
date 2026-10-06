/* A many-to-one key from cell symbols to letters, annealed, for
 * engine.dagapeyeff_homophone. Not a reading.
 *
 * Each of the 25 symbols is sent to one of 25 letters; two symbols may share
 * a letter. A move sends one symbol to another letter, or swaps the letters
 * of two symbols. The score is a quadgram log probability. A key that gives
 * any letter more than cap places is refused: the model scores a run of one
 * letter above English, so without the cap the key collapses onto one letter.
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

static double score(const int *ct, int n, const double *logp, const int *letters, const int *key, int cap,
                    int *buf) {
    int counts[25] = {0};
    for (int i = 0; i < n; i++) {
        if (++counts[key[ct[i]]] > cap) return -1e300;
        buf[i] = letters[key[ct[i]]];
    }
    double total = 0.0;
    for (int i = 3; i < n; i++)
        total += logp[((buf[i - 3] * 26 + buf[i - 2]) * 26 + buf[i - 1]) * 26 + buf[i]];
    return total;
}

double homophone_anneal(const int *ct, int n, const double *logp, const int *letters, int cap,
                        unsigned long long seed, int restarts, int steps, double t0, int *best_key, int *best_plain) {
    int buf[N_MAX], key[25], cur_key[25];
    double best = -1e300;
    unsigned long long state = seed * 2654435761ULL + 88172645463325252ULL;
    if (n > N_MAX) return 0.0;
    for (int r = 0; r < restarts; r++) {
        /* A one-to-one start always meets the cap when no symbol is too common. */
        for (int i = 0; i < 25; i++) cur_key[i] = i;
        for (int i = 24; i > 0; i--) {
            int j = next_u32(&state) % (i + 1);
            int t = cur_key[i]; cur_key[i] = cur_key[j]; cur_key[j] = t;
        }
        double cur = score(ct, n, logp, letters, cur_key, cap, buf);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(key, cur_key, sizeof key);
            if (next_unit(&state) < 0.5) {
                key[next_u32(&state) % 25] = next_u32(&state) % 25;
            } else {
                int i = next_u32(&state) % 25, j = next_u32(&state) % 25;
                int t = key[i]; key[i] = key[j]; key[j] = t;
            }
            double s = score(ct, n, logp, letters, key, cap, buf);
            if (s >= cur || next_unit(&state) < exp((s - cur) / temp)) {
                cur = s;
                memcpy(cur_key, key, sizeof key);
                if (cur > best) { best = cur; memcpy(best_key, cur_key, sizeof key); }
            }
        }
    }
    score(ct, n, logp, letters, best_key, cap, buf);
    memcpy(best_plain, buf, sizeof(int) * n);
    return best;
}
