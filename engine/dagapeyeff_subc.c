/* Periodic substitution with null symbols, annealed. Not a reading.
 *
 * Kernel for engine.dagapeyeff_subc. The cipher has n symbols in 0..24.
 * There are `period` alphabets; symbol s at position i reads as
 * key[(i % period) * 25 + s]. Each alphabet is a permutation of the 25
 * plain letters. Up to `max_nulls` symbols of the first alphabet may be
 * marked null and are then dropped from every position. The score is the
 * quadgram log probability per scored letter of what remains. The best key,
 * null mask and score are returned; the caller decides what to keep.
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

static double score(const int *ct, int n, int period, const double *logp, const int *plain,
                    const int *key, const int *null, int min_letters, int *buf, int *len) {
    int m = 0;
    for (int i = 0; i < n; i++) {
        if (null[ct[i]]) continue;
        buf[m++] = plain[key[(i % period) * 25 + ct[i]]];
    }
    *len = m;
    if (m < min_letters || m < 4) return -1e300;
    double total = 0.0;
    for (int i = 3; i < m; i++)
        total += logp[((buf[i - 3] * 26 + buf[i - 2]) * 26 + buf[i - 1]) * 26 + buf[i]];
    return total / (m - 3);
}

static void shuffle(int *a) {
    for (int i = 24; i > 0; i--) {
        int j = next_u32() % (i + 1);
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
}

/* Returns the best per-letter score. best_key holds period * 25 entries,
 * best_null 25 flags, best_plain the scored letters and *best_len their count. */
double sub_anneal(const int *ct, int n, int period, int max_nulls, int min_letters,
                  const double *logp, const int *plain, unsigned long long seed,
                  int restarts, int steps, double t0,
                  int *best_key, int *best_null, int *best_plain, int *best_len) {
    int buf[4096], key[25 * 8], cur_key[25 * 8], null[25], cur_null[25], used[25];
    double best = -1e300;
    int len = 0;
    if (n > 4096 || period < 1 || period > 8) return -1e300;
    memset(used, 0, sizeof used);
    for (int i = 0; i < n; i++) used[ct[i]] = 1;
    state = seed * 2654435761ULL + 88172645463325252ULL;
    for (int r = 0; r < restarts; r++) {
        for (int p = 0; p < period; p++) {
            for (int i = 0; i < 25; i++) cur_key[p * 25 + i] = i;
            shuffle(cur_key + p * 25);
        }
        memset(cur_null, 0, sizeof cur_null);
        int nulls = 0;
        double cur = score(ct, n, period, logp, plain, cur_key, cur_null, min_letters, buf, &len);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-4;
            memcpy(key, cur_key, sizeof(int) * 25 * period);
            memcpy(null, cur_null, sizeof null);
            int toggled = 0;
            if (max_nulls > 0 && next_u32() % 10 == 0) {
                int s = next_u32() % 25;
                if (!used[s]) continue;
                if (!null[s] && nulls >= max_nulls) continue;
                null[s] = !null[s];
                toggled = null[s] ? 1 : -1;
            } else {
                int p = next_u32() % period;
                int i = next_u32() % 25, j = next_u32() % 25;
                int t = key[p * 25 + i]; key[p * 25 + i] = key[p * 25 + j]; key[p * 25 + j] = t;
            }
            double s = score(ct, n, period, logp, plain, key, null, min_letters, buf, &len);
            if (s >= cur || next_unit() < exp((s - cur) / temp)) {
                cur = s;
                nulls += toggled;
                memcpy(cur_key, key, sizeof(int) * 25 * period);
                memcpy(cur_null, null, sizeof null);
                if (cur > best) {
                    best = cur;
                    memcpy(best_key, cur_key, sizeof(int) * 25 * period);
                    memcpy(best_null, cur_null, sizeof cur_null);
                    memcpy(best_plain, buf, sizeof(int) * len);
                    *best_len = len;
                }
            }
        }
    }
    return best;
}
