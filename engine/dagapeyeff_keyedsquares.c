/* Four-square with all four squares keyed, annealed, for engine.dagapeyeff_keyedsquares.
 * Not a reading. Two-square, and two-square behind an unknown Polybius labelling, are
 * special cases of this model.
 *
 * State: p1[cell] and p2[cell] are the letters (0..24) in the two plain squares;
 * u[cell] and l[cell] are the cipher symbols (0..24) in the two cipher squares. A
 * cipher pair (x, y) sits at u-cell (r1, c2) and l-cell (r2, c1); the plain pair is
 * p1[r1][c1], p2[r2][c2]. Moves swap two cells of one square, or two of its rows or
 * columns, the move set of Colossus's two-square solver (S. Blake, MIT licence). The
 * score is a quadgram log probability.
 */
#include <math.h>
#include <string.h>

#define N_MAX 512

static unsigned int next_u32(unsigned long long *s) {
    *s ^= *s << 13; *s ^= *s >> 7; *s ^= *s << 17;
    return (unsigned int)(*s >> 32);
}
static double next_unit(unsigned long long *s) { return (next_u32(s) + 0.5) / 4294967296.0; }

static double score(const int *ct, int n, const double *logp, const int *letters, const int *sq, int *buf) {
    const int *p1 = sq, *p2 = sq + 25, *u = sq + 50, *l = sq + 75;
    int pu[25], pl[25];
    for (int i = 0; i < 25; i++) { pu[u[i]] = i; pl[l[i]] = i; }
    for (int k = 0; k + 1 < n; k += 2) {
        int a = pu[ct[k]], b = pl[ct[k + 1]];
        int r1 = a / 5, c2 = a % 5, r2 = b / 5, c1 = b % 5;
        buf[k] = letters[p1[r1 * 5 + c1]];
        buf[k + 1] = letters[p2[r2 * 5 + c2]];
    }
    double total = 0.0;
    for (int i = 3; i < n; i++)
        total += logp[((buf[i - 3] * 26 + buf[i - 2]) * 26 + buf[i - 1]) * 26 + buf[i]];
    return total;
}

static void move(int *sq, unsigned long long *s) {
    int *q = sq + 25 * (next_u32(s) % 4);
    unsigned int kind = next_u32(s) % 20;
    if (kind < 18) {
        int i = next_u32(s) % 25, j = next_u32(s) % 25, t = q[i]; q[i] = q[j]; q[j] = t;
    } else if (kind == 18) {
        int r = next_u32(s) % 5, t2 = next_u32(s) % 5;
        for (int c = 0; c < 5; c++) { int t = q[r * 5 + c]; q[r * 5 + c] = q[t2 * 5 + c]; q[t2 * 5 + c] = t; }
    } else {
        int c = next_u32(s) % 5, t2 = next_u32(s) % 5;
        for (int r = 0; r < 5; r++) { int t = q[r * 5 + c]; q[r * 5 + c] = q[r * 5 + t2]; q[r * 5 + t2] = t; }
    }
}

/* ct holds n symbols (n even) in 0..24. Returns the best total score; best holds the
 * four squares and plain the letters behind it. */
double keyed_anneal(const int *ct, int n, const double *logp, const int *letters, unsigned long long seed,
                    int restarts, int steps, double t0, int *best, int *plain) {
    int buf[N_MAX], cur[100], trial[100];
    double top = -1e300;
    unsigned long long s = seed * 2654435761ULL + 88172645463325252ULL;
    if (n > N_MAX) return 0.0;
    for (int r = 0; r < restarts; r++) {
        for (int q = 0; q < 4; q++) {
            int *sq = cur + 25 * q;
            for (int i = 0; i < 25; i++) sq[i] = i;
            for (int i = 24; i > 0; i--) { int j = next_u32(&s) % (i + 1), t = sq[i]; sq[i] = sq[j]; sq[j] = t; }
        }
        double now = score(ct, n, logp, letters, cur, buf);
        for (int step = 0; step < steps; step++) {
            double temp = t0 * (1.0 - (double)step / steps) + 1e-3;
            memcpy(trial, cur, sizeof trial);
            move(trial, &s);
            double sc = score(ct, n, logp, letters, trial, buf);
            if (sc >= now || next_unit(&s) < exp((sc - now) / temp)) {
                now = sc; memcpy(cur, trial, sizeof cur);
                if (now > top) { top = now; memcpy(best, cur, sizeof cur); }
            }
        }
    }
    score(ct, n, logp, letters, best, buf);
    memcpy(plain, buf, sizeof(int) * n);
    return top;
}
