/* Turning grille on a 14 by 14 square with a letter key, annealed together,
 * for engine.dagapeyeff_grillec. Not a reading.
 *
 * Orbit k = row * 7 + column of the top-left quarter. Its hole at turn t is
 * the cell reached by turning (row, column) a quarter (choice[k] + t) & 3
 * times, a quarter turn sending (r, c) to (c, 13 - r). The plaintext is read
 * turn by turn, holes in row order, as engine.dagapeyeff_grille does. Each
 * cipher symbol (0 to 24) is sent to one of 25 plaintext letters. The score
 * is a quadgram log probability.
 */
#include <math.h>
#include <string.h>

#define SIDE 14
#define HALF 7
#define ORBITS 49
#define N 196

/* The generator state is per call, so calls may run side by side. */
static unsigned int next_u32(unsigned long long *state) {
    *state ^= *state << 13;
    *state ^= *state >> 7;
    *state ^= *state << 17;
    return (unsigned int)(*state >> 32);
}

static double next_unit(unsigned long long *state) { return (next_u32(state) + 0.5) / 4294967296.0; }

static void tables(int *orbit_of, int *turns_of) {
    for (int row = 0; row < HALF; row++)
        for (int column = 0; column < HALF; column++) {
            int r = row, c = column;
            for (int t = 0; t < 4; t++) {
                orbit_of[r * SIDE + c] = row * HALF + column;
                turns_of[r * SIDE + c] = t;
                int nr = c, nc = SIDE - 1 - r;
                r = nr; c = nc;
            }
        }
}

static double score(const int *ct, const double *logp, const int *letters, const int *orbit_of,
                    const int *turns_of, const int *choice, const int *key, int done, int *buf) {
    int index = 0;
    for (int t = 0; t < 4; t++)
        for (int p = 0; p < N; p++)
            if (((choice[orbit_of[p]] + t) & 3) == turns_of[p]) {
                if (done) buf[p] = letters[key[ct[index]]];
                else buf[index] = letters[key[ct[p]]];
                index++;
            }
    double total = 0.0;
    for (int i = 3; i < N; i++)
        total += logp[((buf[i - 3] * 26 + buf[i - 2]) * 26 + buf[i - 1]) * 26 + buf[i]];
    return total;
}

/* ct holds 196 symbols in 0..24. start_key is the key each restart begins
 * from; with fixed_key set the key never moves. done picks the direction:
 * 0 means the plaintext went into the holes and the square was read in row
 * order. Returns the best score over the restarts. */
double grille_anneal(const int *ct, const double *logp, const int *letters, const int *start_key,
                     int fixed_key, int done, unsigned long long seed, int restarts, int steps,
                     double t0, double key_share, int *best_choice, int *best_key, int *best_plain) {
    int orbit_of[N], turns_of[N], buf[N], choice[ORBITS], key[25], cur_choice[ORBITS], cur_key[25];
    double best = -1e300;
    unsigned long long state = seed * 2654435761ULL + 88172645463325252ULL;
    tables(orbit_of, turns_of);
    for (int r = 0; r < restarts; r++) {
        for (int k = 0; k < ORBITS; k++) cur_choice[k] = next_u32(&state) & 3;
        memcpy(cur_key, start_key, sizeof cur_key);
        double cur = score(ct, logp, letters, orbit_of, turns_of, cur_choice, cur_key, done, buf);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(choice, cur_choice, sizeof choice); memcpy(key, cur_key, sizeof key);
            if (!fixed_key && next_unit(&state) < key_share) {
                int i = next_u32(&state) % 25, j = next_u32(&state) % 25;
                int t = key[i]; key[i] = key[j]; key[j] = t;
            } else {
                int k = next_u32(&state) % ORBITS;
                choice[k] = (choice[k] + 1 + next_u32(&state) % 3) & 3;
                if (next_unit(&state) < 0.3) {
                    int m = next_u32(&state) % ORBITS;
                    choice[m] = (choice[m] + 1 + next_u32(&state) % 3) & 3;
                }
            }
            double s = score(ct, logp, letters, orbit_of, turns_of, choice, key, done, buf);
            if (s >= cur || next_unit(&state) < exp((s - cur) / temp)) {
                cur = s;
                memcpy(cur_choice, choice, sizeof choice); memcpy(cur_key, key, sizeof key);
                if (cur > best) {
                    best = cur;
                    memcpy(best_choice, cur_choice, sizeof choice); memcpy(best_key, cur_key, sizeof key);
                }
            }
        }
    }
    score(ct, logp, letters, orbit_of, turns_of, best_choice, best_key, done, buf);
    memcpy(best_plain, buf, sizeof(int) * N);
    return best;
}
