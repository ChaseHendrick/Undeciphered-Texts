/* Turning grille on the 14 by 14 square with the letter key re-solved at
 * every grille move, for engine.dagapeyeff_latingrille. Not a reading.
 *
 * Grille convention as engine/dagapeyeff_grillec.c:
 * orbit k = row * 7 + column of the top-left quarter; its hole at turn t is
 * (row, column) turned (choice[k] + t) & 3 quarters, a quarter sending
 * (r, c) to (c, 13 - r); plaintext goes into the holes turn by turn, holes in
 * row order, and the square is read in row order.
 *
 * Phase one scores a grille by the best letter key for its symbol-pair
 * counts under a letter-pair model (greedy swaps from the current key).
 * Phase two polishes grille and key together under a quadgram model.
 */
#include <math.h>
#include <string.h>

#define SIDE 14
#define HALF 7
#define ORBITS 49
#define N 196

static unsigned int next_u32(unsigned long long *s) {
    *s ^= *s << 13; *s ^= *s >> 7; *s ^= *s << 17;
    return (unsigned int)(*s >> 32);
}
static double next_unit(unsigned long long *s) { return (next_u32(s) + 0.5) / 4294967296.0; }

static void tables(int *orbit_of, int *turns_of) {
    for (int row = 0; row < HALF; row++)
        for (int column = 0; column < HALF; column++) {
            int r = row, c = column;
            for (int t = 0; t < 4; t++) {
                orbit_of[r * SIDE + c] = row * HALF + column;
                turns_of[r * SIDE + c] = t;
                int nr = c, nc = SIDE - 1 - r; r = nr; c = nc;
            }
        }
}

/* symbols in plaintext order */
static void order(const int *ct, const int *orbit_of, const int *turns_of, const int *choice, int *seq) {
    int i = 0;
    for (int t = 0; t < 4; t++)
        for (int p = 0; p < N; p++)
            if (((choice[orbit_of[p]] + t) & 3) == turns_of[p]) seq[i++] = ct[p];
}

static void pair_counts(const int *seq, int *cnt) {
    memset(cnt, 0, sizeof(int) * 625);
    for (int i = 1; i < N; i++) cnt[seq[i - 1] * 25 + seq[i]]++;
}

/* L: 25 x 25 letter-pair log probabilities on letter indices 0..24 */
static double key_score(const int *cnt, const double *L, const int *key) {
    double t = 0.0;
    for (int a = 0; a < 25; a++) for (int b = 0; b < 25; b++)
        if (cnt[a * 25 + b]) t += cnt[a * 25 + b] * L[key[a] * 25 + key[b]];
    return t;
}

/* change in score when symbols i and j swap letters */
static double swap_delta(const int *cnt, const double *L, const int *key, int i, int j) {
    int ki = key[i], kj = key[j];
    double d = 0.0;
    for (int b = 0; b < 25; b++) {
        if (b == i || b == j) continue;
        int kb = key[b];
        d += cnt[i * 25 + b] * (L[kj * 25 + kb] - L[ki * 25 + kb]);
        d += cnt[j * 25 + b] * (L[ki * 25 + kb] - L[kj * 25 + kb]);
        d += cnt[b * 25 + i] * (L[kb * 25 + kj] - L[kb * 25 + ki]);
        d += cnt[b * 25 + j] * (L[kb * 25 + ki] - L[kb * 25 + kj]);
    }
    d += cnt[i * 25 + i] * (L[kj * 25 + kj] - L[ki * 25 + ki]);
    d += cnt[j * 25 + j] * (L[ki * 25 + ki] - L[kj * 25 + kj]);
    d += cnt[i * 25 + j] * (L[kj * 25 + ki] - L[ki * 25 + kj]);
    d += cnt[j * 25 + i] * (L[ki * 25 + kj] - L[kj * 25 + ki]);
    return d;
}

/* greedy best-swap climb; returns the score */
static double climb_key(const int *cnt, const double *L, int *key) {
    double s = key_score(cnt, L, key);
    for (int pass = 0; pass < 200; pass++) {
        double bd = 1e-9; int bi = -1, bj = -1;
        for (int i = 0; i < 25; i++) for (int j = i + 1; j < 25; j++) {
            double d = swap_delta(cnt, L, key, i, j);
            if (d > bd) { bd = d; bi = i; bj = j; }
        }
        if (bi < 0) break;
        int t = key[bi]; key[bi] = key[bj]; key[bj] = t; s += bd;
    }
    return s;
}

double grille_nested(const int *ct, const double *L, const int *start_key, unsigned long long seed,
                     int restarts, int steps, double t0, int *best_choice, int *best_key) {
    int orbit_of[N], turns_of[N], seq[N], cnt[625], choice[ORBITS], cur[ORBITS], key[25], ck[25];
    double best = -1e300;
    unsigned long long st = seed * 2654435761ULL + 88172645463325252ULL;
    tables(orbit_of, turns_of);
    for (int r = 0; r < restarts; r++) {
        for (int k = 0; k < ORBITS; k++) cur[k] = next_u32(&st) & 3;
        memcpy(ck, start_key, sizeof ck);
        order(ct, orbit_of, turns_of, cur, seq); pair_counts(seq, cnt);
        double cs = climb_key(cnt, L, ck);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(choice, cur, sizeof choice); memcpy(key, ck, sizeof key);
            int k = next_u32(&st) % ORBITS;
            choice[k] = (choice[k] + 1 + next_u32(&st) % 3) & 3;
            if (next_unit(&st) < 0.3) { int m = next_u32(&st) % ORBITS; choice[m] = (choice[m] + 1 + next_u32(&st) % 3) & 3; }
            order(ct, orbit_of, turns_of, choice, seq); pair_counts(seq, cnt);
            double s = climb_key(cnt, L, key);
            if (s >= cs || next_unit(&st) < exp((s - cs) / temp)) {
                cs = s; memcpy(cur, choice, sizeof cur); memcpy(ck, key, sizeof ck);
                if (cs > best) { best = cs; memcpy(best_choice, cur, sizeof cur); memcpy(best_key, ck, sizeof ck); }
            }
        }
    }
    return best;
}

static double quad(const int *seq, const double *logp, const int *letters, const int *key) {
    int b[N];
    for (int i = 0; i < N; i++) b[i] = letters[key[seq[i]]];
    double t = 0.0;
    for (int i = 3; i < N; i++) t += logp[((b[i - 3] * 26 + b[i - 2]) * 26 + b[i - 1]) * 26 + b[i]];
    return t;
}

/* Phase two: grille and key together under quadgrams from a given start. */
double grille_polish(const int *ct, const double *logp, const int *letters, const int *start_choice,
                     const int *start_key, unsigned long long seed, int steps, double t0, double key_share,
                     int *best_choice, int *best_key) {
    int orbit_of[N], turns_of[N], seq[N], choice[ORBITS], cur[ORBITS], key[25], ck[25];
    unsigned long long st = seed * 2654435761ULL + 88172645463325252ULL;
    tables(orbit_of, turns_of);
    memcpy(cur, start_choice, sizeof cur); memcpy(ck, start_key, sizeof ck);
    order(ct, orbit_of, turns_of, cur, seq);
    double cs = quad(seq, logp, letters, ck), best = cs;
    memcpy(best_choice, cur, sizeof cur); memcpy(best_key, ck, sizeof ck);
    for (int step = 0; step < steps; step++) {
        double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
        memcpy(choice, cur, sizeof choice); memcpy(key, ck, sizeof key);
        if (next_unit(&st) < key_share) {
            int i = next_u32(&st) % 25, j = next_u32(&st) % 25, t = key[i]; key[i] = key[j]; key[j] = t;
        } else {
            int k = next_u32(&st) % ORBITS;
            choice[k] = (choice[k] + 1 + next_u32(&st) % 3) & 3;
        }
        order(ct, orbit_of, turns_of, choice, seq);
        double s = quad(seq, logp, letters, key);
        if (s >= cs || next_unit(&st) < exp((s - cs) / temp)) {
            cs = s; memcpy(cur, choice, sizeof cur); memcpy(ck, key, sizeof ck);
            if (cs > best) { best = cs; memcpy(best_choice, cur, sizeof cur); memcpy(best_key, ck, sizeof ck); }
        }
    }
    return best;
}

/* Phase one, quadgram form: each grille move is scored by a greedy key climb
 * (first improving swap, random order) under the quadgram model. */
static double qscore(const int *seq, const double *logp, const int *letters, const int *key) { return quad(seq, logp, letters, key); }

static double qclimb(const int *seq, const double *logp, const int *letters, int *key, unsigned long long *st,
                     int max_pass) {
    double s = qscore(seq, logp, letters, key);
    for (int pass = 0; pass < max_pass; pass++) {
        int improved = 0, off = next_u32(st) % 300;
        for (int q = 0; q < 300; q++) {
            int idx = (q + off) % 300, i = 0, j;
            /* map idx to pair i < j */
            int rem = idx;
            for (i = 0; i < 25; i++) { int row = 24 - i; if (rem < row) break; rem -= row; }
            j = i + 1 + rem;
            int t = key[i]; key[i] = key[j]; key[j] = t;
            double v = qscore(seq, logp, letters, key);
            if (v > s + 1e-9) { s = v; improved = 1; }
            else { t = key[i]; key[i] = key[j]; key[j] = t; }
        }
        if (!improved) break;
    }
    return s;
}

double grille_nestq(const int *ct, const double *logp, const int *letters, const int *start_key,
                    unsigned long long seed, int restarts, int steps, double t0, int max_pass,
                    int *best_choice, int *best_key) {
    int orbit_of[N], turns_of[N], seq[N], choice[ORBITS], cur[ORBITS], key[25], ck[25];
    double best = -1e300;
    unsigned long long st = seed * 2654435761ULL + 88172645463325252ULL;
    tables(orbit_of, turns_of);
    for (int r = 0; r < restarts; r++) {
        for (int k = 0; k < ORBITS; k++) cur[k] = next_u32(&st) & 3;
        memcpy(ck, start_key, sizeof ck);
        order(ct, orbit_of, turns_of, cur, seq);
        double cs = qclimb(seq, logp, letters, ck, &st, 50);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(choice, cur, sizeof choice); memcpy(key, ck, sizeof key);
            int k = next_u32(&st) % ORBITS;
            choice[k] = (choice[k] + 1 + next_u32(&st) % 3) & 3;
            if (next_unit(&st) < 0.3) { int m = next_u32(&st) % ORBITS; choice[m] = (choice[m] + 1 + next_u32(&st) % 3) & 3; }
            order(ct, orbit_of, turns_of, choice, seq);
            double s = qclimb(seq, logp, letters, key, &st, max_pass);
            if (s >= cs || next_unit(&st) < exp((s - cs) / temp)) {
                cs = s; memcpy(cur, choice, sizeof cur); memcpy(ck, key, sizeof ck);
                if (cs > best) { best = cs; memcpy(best_choice, cur, sizeof cur); memcpy(best_key, ck, sizeof ck); }
            }
        }
    }
    return best;
}
