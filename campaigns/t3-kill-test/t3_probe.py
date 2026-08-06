#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t3_probe.py — pre-registered T3 kill-test probe for the CCM operator family D_log^{(lambda,N)}
==============================================================================================

PURPOSE
  Instantiates the repo kill-switch statement T3 (riemann-resolvent-programme,
  HYPOTHESIS_FRONTIER.md: "sup_{lambda,N} Tr (D_{lambda,N}^2 + x0 I)^-1 < inf",
  operational layer S_{lambda,N}(x) = (1/2) Tr((D^2+xI)^-1)) for the concrete
  Connes–Consani–Moscovici operators D_log^{(lambda,N)} of arXiv:2511.22755,
  on the registered (lambda, N) grid, at x0 = 1.

  The COMPLETE pre-registration (operator variant, every formula with equation
  numbers, judges J1/J2/J3, kill rule, scope clause) is design.md in this same
  directory. The REG block below is a frozen copy of the registered constants;
  editing it after full-grid data exists voids any verdict.

CONVENTIONS (every printed number travels with these)
  [conv:CCM]    arXiv:2511.22755: F(s) = Int f(u) u^{-is} d*u on R*_+;
                interval [lambda^-1, lambda]; L = 2 log lambda; von Mangoldt sum
                over ALL prime powers 1 < k <= lambda^2 (cutoff slaved to lambda).
  [conv:S-half] S = half-trace = sum over POSITIVE IR spectrum z_k of D'' of
                1/(z_k^2 + x0)  (repo convention, FiniteStieltjes.lean).
                The UV lattice tail S_tail = sum_{j>N} 1/((2 pi j/L)^2 + x0) is
                closed-form and reported SEPARATELY (design.md section 2.1).
  [conv:zeros]  zeta ordinates gamma_j with zeta(1/2 + i gamma_j) = 0, from
                mpmath.zetazero (dps 30, cached) + 10 hardcoded anchors.

JUDGES (design.md sections 6-8)
  J1: S_IR vs zero-side benchmark B_zero(T) = sum_{gamma <= T} 1/(gamma^2+x0),
      T = pi N / log lambda; plus Riemann–von Mangoldt smooth integral and the
      target anchor S_Xi(x0) = (xi'/xi)(1/2+sqrt(x0))/(2 sqrt(x0)).
  J2: dual-resolution replicas (dps/maxdegree/scan density), count gate = N
      positive zeros, even-simplicity gate (VOID handling), stability tolerances.
  J3: mechanical kill/survive rule; the verdict line is printed ONLY by the
      aggregator and ONLY if the registered grid is complete and all J2 pass;
      otherwise INCONCLUSIVE.

ENVIRONMENT
  Single process. BLAS pinned to 1 thread (set before numpy import). No RNG:
  fully deterministic. numpy used only for a float64 eigen pre-scan; all
  load-bearing arithmetic is mpmath. Checkpoints: JSON, atomic temp+rename.

USAGE
  python t3_probe.py --pilot                          # self-tests + tiny points
  python t3_probe.py --build-zeros 560                # build zeta zero cache
  python t3_probe.py --lambdas 2,sqrt8 --sizes 20,40,80,120
  python t3_probe.py --verdict-only                   # aggregate + verdict line

Honesty label: everything this script outputs is VERIFIED NUMERICS (repo
tricotomy); nothing is exact or certified.
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"

import argparse
import hashlib
import json
import math
import sys
import time

import mpmath as mp

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

# ----------------------------------------------------------------------------
# REG: frozen registered constants (design.md).  DO NOT EDIT AFTER DATA EXISTS.
# ----------------------------------------------------------------------------

REG = {
    "design": "design.md v1.0 2026-08-05",
    "x0": "1",
    "x0_secondary": ["1/2", "2"],
    "grid_lambdas": ["2", "sqrt8", "3", "sqrt13"],
    "grid_sizes": [20, 40, 80, 120],
    "t_spur": "10",                       # low-energy band cutoff (gamma_1=14.13)
    "dps_formula": "50 + ceil(2.2*(4*pi*lam2 - 4.5*log(lam2))/log(10))",
    "dps_hi_extra": 60,
    "quad_extra_dps": 40,
    "maxdeg_base": 12,
    "maxdeg_hi": 14,
    "msamp_base": 9,
    "msamp_hi": 17,
    "scan_refine_factors": [4, 16],
    "j2_zero_tol_rel": "1e-8",
    "j2_S_tol": "1e-8",
    "even_defect_tol": "1e-10",
    "simplicity_min_ratio": "1e-6",
    "deltaN_exp_div": 2,                  # |sum xi| >= 10^-(dps/2) * ||xi||
    "kill_count_min": 4,
    "kill_count_growth": 2,
    "kill_persist_dz": "0.5",
    "kill_Slow_abs": "0.25",
    "kill_Slow_factor": "2.0",
    "kill_Slow_floor": "0.02",
    "mono_slack": "1e-6",
    "survive_nspur_max": 1,
    "survive_Slow_max": "0.02",
    "survive_SIR_max": "0.030",
    "j1_pass_rel": "0.1",
    "j1_pass_edge_factor": "5",
    "pilot": {"lambdas": ["2"], "sizes": [6, 8], "dps_base": 60, "dps_hi": 90},
    "st1_tol_rel": "1e-8",
    "st2_tol": "2e-3",
    "zeros_dps": 30,
    "output_dps": 30,
}

REG_HASH = hashlib.sha256(
    json.dumps(REG, sort_keys=True).encode("utf-8")).hexdigest()

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(HERE, "results")
ZCACHE_PATH = os.path.join(RESULTS_DIR, "zeta_zeros_cache.json")

# First 10 zeta ordinates, standard tables, ~18 digits [conv:zeros].
HARDCODED_ZEROS = [
    "14.134725141734693790", "21.022039638771554993",
    "25.010857580145688763", "30.424876125859513210",
    "32.935061587739189690", "37.586178158825671257",
    "40.918719012147495187", "43.327073280914999519",
    "48.005150881167159727", "49.773832477672302181",
]


def script_sha256():
    with open(os.path.abspath(__file__), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def provenance(args_ns):
    return {
        "script_sha256": script_sha256(),
        "reg_sha256": REG_HASH,
        "mpmath": mp.__version__,
        "numpy": (np.__version__ if np is not None else None),
        "python": sys.version.split()[0],
        "platform": sys.platform,
        "argv": vars(args_ns),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def atomic_write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


# ----------------------------------------------------------------------------
# lambda parsing (exact lambda^2 required: the prime cutoff is slaved to it)
# ----------------------------------------------------------------------------

def parse_lambda(tok):
    tok = tok.strip().lower()
    if tok.startswith("sqrt"):
        k = int(tok[4:])
        if k < 2:
            raise ValueError("need lambda > 1")
        return tok, ("sqrt", k)
    k = int(tok)  # raises on floats: exact lambda^2 is mandatory
    if k < 2:
        raise ValueError("need lambda > 1")
    return tok, ("int", k)


def lam_value(spec):
    kind, k = spec
    return mp.sqrt(k) if kind == "sqrt" else mp.mpf(k)


def lam_sq(spec):
    kind, k = spec
    return k if kind == "sqrt" else k * k


def dps_schedule(spec):
    m = lam_sq(spec)
    nats = 4.0 * math.pi * m - 4.5 * math.log(m)
    digits = max(nats / math.log(10.0), 5.0)
    return 50 + int(math.ceil(2.2 * digits))


# ----------------------------------------------------------------------------
# prime powers with von Mangoldt weights, 1 < k <= x  (x exact integer)
# ----------------------------------------------------------------------------

def prime_powers_upto(x):
    sieve = [True] * (x + 1)
    out = []
    for p in range(2, x + 1):
        if sieve[p]:
            for q in range(2 * p, x + 1, p):
                sieve[q] = False
            pk = p
            while pk <= x:
                out.append((pk, p))  # (prime power, base prime)
                pk *= p
    out.sort()
    return out


# ----------------------------------------------------------------------------
# matrix assembly  [conv:CCM]  (design.md section 3.1)
# tau = W02 - WR - Wp,  indices n,m in {-N..N},  stored as list-of-lists,
# entry [i][j] with i = n+N.
# ----------------------------------------------------------------------------

def rho(x):
    # e^{x/2}/(e^x - e^{-x}) = 1/(e^{x/2} - e^{-3x/2}); integrable ~1/(2x) at 0
    return 1 / (mp.exp(x / 2) - mp.exp(-3 * x / 2))


def archimedean_tables(L, N, maxdeg):
    """alpha[n], beta[n], gamma_[n] for n = 0..N (Prop 4.3 defining integrals).
    Runs at current mp.dps; integrands evaluated at that precision."""
    twopiL = 2 * mp.pi / L
    alpha, beta, gamma_ = [], [], []
    cw = (mp.mpf(1) / 2 * mp.log((mp.exp(L / 2) - 1) / (mp.exp(L / 2) + 1))
          + mp.atan(mp.exp(L / 2)) - mp.pi / 4 + mp.euler / 2
          + mp.mpf(1) / 2 * mp.log(8 * mp.pi))
    errmax = mp.mpf(0)
    for n in range(N + 1):
        a = twopiL * n
        if n == 0:
            va, ea = mp.mpf(0), mp.mpf(0)
        else:
            va, ea = mp.quad(lambda x: mp.sin(a * x) * rho(x), [0, L],
                             maxdegree=maxdeg, error=True)
            va /= mp.pi
        vb, eb = mp.quad(lambda x: x * mp.cos(a * x) * rho(x), [0, L],
                         maxdegree=maxdeg, error=True)
        vb /= L
        # gamma_L(n): eq (4.14) PRINTS the (cos - exp(-x/2)) integrand together
        # with the constant c(L)+w(L), which double-counts c(L): by (4.11),
        # int (cos - e^{-x/2}) rho = int (cos - 1) rho + c(L).  Deriving the
        # diagonal straight from (3.15)/(4.4) — with omega(x) = q(U_n,U_n)(x),
        # omega(0) = 2 (Lemma 2.3) and e^{-x/2} rho(x) = 1/(e^x - e^{-x}) —
        # gives  WR(n,n) = 2[int_0^L (cos - e^{-x/2}) rho + w(L)] - 2 beta(n)
        #                = 2[int_0^L (cos - 1)      rho + c(L) + w(L)] - 2 beta(n),
        # i.e. gamma_L(n) = int (cos - 1) rho + c(L) + w(L).  We quadrature the
        # (cos - 1) form, which is exactly the integral the paper evaluates in
        # closed form in Prop. 4.2 eq (4.7), and keep the p.15 closed-form
        # constant c(L)+w(L) verbatim (so c(L) enters exactly, not by
        # quadrature).  Repaired 2026-08-06, design.md amendment A2; before the
        # repair every diagonal entry of WR was too large by exactly 2 c(L)
        # (0.7489 at lambda = 2), caught by gate ST2.
        vg, eg = mp.quad(lambda x: (mp.cos(a * x) - 1) * rho(x),
                         [0, L], maxdegree=maxdeg, error=True)
        vg += cw
        alpha.append(va)
        beta.append(vb)
        gamma_.append(vg)
        errmax = max(errmax, abs(ea), abs(eb), abs(eg))
    return alpha, beta, gamma_, errmax


def assemble(spec, N, dps, maxdeg):
    """Return (tau list-of-lists mpf, meta dict). Assembly at dps+quad_extra."""
    t0 = time.time()
    lam2 = lam_sq(spec)
    dim = 2 * N + 1
    with mp.workdps(dps + REG["quad_extra_dps"]):
        lam = lam_value(spec)
        L = 2 * mp.log(lam)
        twopiL = 2 * mp.pi / L
        # --- archimedean tables (quadrature) ---
        alpha, beta, gamma_, quad_err = archimedean_tables(L, N, maxdeg)

        def al(n):
            return alpha[n] if n >= 0 else -alpha[-n]

        # --- prime block precomputations ---
        pps = prime_powers_upto(lam2)
        prime_data = []
        for (k, p) in pps:
            y = mp.log(k)
            lam_vm = mp.log(p)
            w = lam_vm / mp.sqrt(k)
            sins = [mp.sin(twopiL * n * y) for n in range(N + 1)]
            coss = [mp.cos(twopiL * n * y) for n in range(N + 1)]
            prime_data.append((y, w, sins, coss))

        def psin(n, sins):
            return sins[n] if n >= 0 else -sins[-n]

        def pcos(n, coss):
            return coss[abs(n)]

        # --- fill upper triangle ---
        tau = [[mp.mpf(0)] * dim for _ in range(dim)]
        sh2 = mp.sinh(L / 4) ** 2
        pi2_16 = 16 * mp.pi ** 2
        for i in range(dim):
            n = i - N
            for j in range(i, dim):
                m = j - N
                w02 = (32 * L * sh2 * (L * L - pi2_16 * m * n)
                       / ((L * L + pi2_16 * m * m) * (L * L + pi2_16 * n * n)))
                if n == m:
                    wr = 2 * gamma_[abs(n)] - 2 * beta[abs(n)]
                else:
                    # Prop 4.3 verbatim: (alpha_L(m)-alpha_L(n))/(n-m).
                    # A previous draft had /(m-n) — a global sign flip of the
                    # whole WR off-diagonal block, caught by adversarial
                    # verification against the paper's raw LaTeX (2026-08-05)
                    # and now also gated by ST2b below.
                    wr = (al(m) - al(n)) / (n - m)
                wp = mp.mpf(0)
                for (y, w, sins, coss) in prime_data:
                    if n == m:
                        q = 2 * (1 - y / L) * pcos(n, coss)
                    else:
                        q = (psin(m, sins) - psin(n, sins)) / (mp.pi * (n - m))
                    wp += w * q
                val = w02 - wr - wp
                tau[i][j] = val
                tau[j][i] = val
    meta = {
        "quad_err_max": mp.nstr(quad_err, 5),
        "prime_powers": [k for (k, _p) in prime_powers_upto(lam2)],
        "assembly_seconds": round(time.time() - t0, 2),
    }
    return tau, meta


# ----------------------------------------------------------------------------
# dense linear algebra on list-of-lists mpf (deterministic, single process)
# ----------------------------------------------------------------------------

def lu_factor(A):
    n = len(A)
    M = [row[:] for row in A]
    piv = list(range(n))
    for k in range(n):
        pmax, prow = abs(M[k][k]), k
        for r in range(k + 1, n):
            a = abs(M[r][k])
            if a > pmax:
                pmax, prow = a, r
        if prow != k:
            M[k], M[prow] = M[prow], M[k]
            piv[k], piv[prow] = piv[prow], piv[k]
        d = M[k][k]
        if d == 0:
            raise ZeroDivisionError("singular pivot in LU")
        for r in range(k + 1, n):
            f = M[r][k] / d
            M[r][k] = f
            Mr, Mk = M[r], M[k]
            for c in range(k + 1, n):
                Mr[c] -= f * Mk[c]
    return M, piv


def lu_solve(fac, b):
    M, piv = fac
    n = len(M)
    x = [b[piv[i]] for i in range(n)]
    for i in range(1, n):
        Mi = M[i]
        s = x[i]
        for k in range(i):
            s -= Mi[k] * x[k]
        x[i] = s
    for i in range(n - 1, -1, -1):
        Mi = M[i]
        s = x[i]
        for k in range(i + 1, n):
            s -= Mi[k] * x[k]
        x[i] = s / Mi[i]
    return x


def matvec(A, v):
    n = len(A)
    return [mp.fsum(A[i][j] * v[j] for j in range(n)) for i in range(n)]


def dot(u, v):
    return mp.fsum(u[i] * v[i] for i in range(len(u)))


def norm(v):
    return mp.sqrt(dot(v, v))


def mgs(vectors):
    out = []
    for v in vectors:
        w = v[:]
        for u in out:
            c = dot(u, w)
            w = [w[i] - c * u[i] for i in range(len(w))]
        nw = norm(w)
        if nw > 0:
            out.append([x / nw for x in w])
    return out


def small_symmetric_eig(M):
    """Eigen decomposition of a small dense symmetric mp.matrix via mp.eigsy."""
    A = mp.matrix(M)
    E, Q = mp.eigsy(A)
    pairs = sorted(range(A.rows), key=lambda i: E[i])
    evals = [E[i] for i in pairs]
    evecs = [[Q[r, i] for r in range(A.rows)] for i in pairs]
    return evals, evecs


def bottom_cluster(tau, dps):
    """Smallest algebraic eigenvalues of tau (design.md 4.1).
    Returns dict with eps1, eps2, xi (eigenvector of eps1), diagnostics."""
    t0 = time.time()
    n = len(tau)
    if np is None:
        raise RuntimeError("numpy required for the float64 pre-scan")
    A64 = np.array([[float(tau[i][j]) for j in range(n)] for i in range(n)])
    w64 = np.linalg.eigvalsh(A64)
    cluster = int(np.sum(np.abs(w64) < 1e-4))
    block = min(max(cluster + 2, 4), 40)
    neg_big = [float(w) for w in w64 if w < -1e-4]

    with mp.workdps(dps):
        fac = lu_factor(tau)
        # deterministic start block
        V = []
        for k in range(block):
            V.append([mp.cos(mp.mpf((k + 1) * (i + 1))) for i in range(n)])
        V = mgs(V)
        for _ in range(12):
            V = [lu_solve(fac, v) for v in V]
            V = mgs(V)
        # Rayleigh-Ritz
        TV = [matvec(tau, v) for v in V]
        Msmall = [[dot(V[a], TV[b]) for b in range(len(V))]
                  for a in range(len(V))]
        evals, evecs = small_symmetric_eig(Msmall)
        ritz = []
        for ev, c in zip(evals, evecs):
            vec = [mp.fsum(c[a] * V[a][i] for a in range(len(V)))
                   for i in range(n)]
            nv = norm(vec)
            vec = [x / nv for x in vec]
            ritz.append((ev, vec))
        def refine_at(sigma):
            """Shifted inverse iteration at sigma; returns (eigenvalue, vector)
            or None on singular shift."""
            shifted = [[tau[i][j] - (sigma if i == j else 0) for j in range(n)]
                       for i in range(n)]
            try:
                fac2 = lu_factor(shifted)
            except ZeroDivisionError:
                return None
            v = [mp.cos(mp.mpf(3 * (i + 1))) for i in range(n)]
            for _ in range(5):
                v = lu_solve(fac2, v)
                nv = norm(v)
                v = [x / nv for x in v]
            return (dot(v, matvec(tau, v)), v)

        # refine any float64-visible large negative eigenvalue (design U2)
        for wneg in neg_big:
            r2 = refine_at(mp.mpf(wneg))
            if r2 is not None:
                ritz.append(r2)

        # dedup refined candidates: same value AND same eigenvector = duplicate;
        # same value but orthogonal vectors = genuine (near-)degeneracy, kept.
        ritz.sort(key=lambda t: t[0])
        dedup = []
        for (ev, v) in ritz:
            dup = False
            for (ev2, v2) in dedup:
                if (abs(ev - ev2) <= mp.mpf("1e-9") * max(1, abs(ev2))
                        and abs(dot(v, v2)) > mp.mpf("0.9")):
                    dup = True
                    break
            if not dup:
                dedup.append((ev, v))
        ritz = dedup

        # float64 outer values not already represented by a refined candidate
        extras = []
        for w in w64:
            wv = float(w)
            if not any(abs(mp.mpf(wv) - ev) <= mp.mpf("1e-6") * max(1, abs(ev))
                       for (ev, _v) in ritz):
                extras.append(mp.mpf(wv))
        extras.sort()

        # eps1 must come from a refined candidate; refine an extra if it
        # undercuts the current refined minimum
        if extras and (not ritz or extras[0] < ritz[0][0] - mp.mpf("1e-9")):
            r2 = refine_at(extras[0])
            if r2 is not None:
                ritz.append(r2)
                ritz.sort(key=lambda t: t[0])
                extras = extras[1:]
        eps1, xi = ritz[0]
        # eps2 = next distinct algebraic value; refine an unrefined extra when
        # it is close enough to eps1 to matter for the simplicity gate
        cands2 = [ev for (ev, _v) in ritz[1:]] + extras
        if not cands2:
            eps2 = mp.mpf("inf")
        else:
            eps2 = min(cands2)
            if (eps2 in extras
                    and abs(eps2 - eps1) < mp.mpf("1e-3") * max(1, abs(eps1))):
                r2 = refine_at(eps2)
                if r2 is not None and abs(dot(r2[1], xi)) < mp.mpf("0.9"):
                    eps2 = r2[0]
        # residual check
        r = matvec(tau, xi)
        resid = norm([r[i] - eps1 * xi[i] for i in range(n)])
        # even defect and delta_N degeneracy
        mx = max(abs(x) for x in xi)
        Nhalf = (n - 1) // 2
        even_defect = max(abs(xi[Nhalf + j] - xi[Nhalf - j])
                          for j in range(Nhalf + 1)) / mx
        odd_defect = max(abs(xi[Nhalf + j] + xi[Nhalf - j])
                         for j in range(Nhalf + 1)) / mx
        sum_xi = mp.fsum(xi)
        simp = (eps2 - eps1) / (abs(eps1) + abs(eps2) + mp.mpf(10) ** (-2 * dps))
        return {
            "eps1": eps1, "eps2": eps2, "xi": xi,
            "resid": resid, "even_defect": even_defect,
            "odd_defect": odd_defect, "sum_xi": sum_xi,
            "simplicity_ratio": simp, "cluster64": cluster,
            "neg_big64": neg_big, "seconds": round(time.time() - t0, 2),
        }


# ----------------------------------------------------------------------------
# IR spectrum: positive real zeros of xi_hat (Prop 5.9), pole-stable form
# ----------------------------------------------------------------------------

def make_phi(xi, L, N):
    halfL = L / 2
    idx = list(range(-N, N + 1))
    coeffs = []
    for j in idx:
        c = xi[j + N]
        if j & 1:
            c = -c
        coeffs.append((j, c))
    twopiL = 2 * mp.pi / L

    def phi(z):
        tot = mp.mpf(0)
        for (j, c) in coeffs:
            d = z - twopiL * j
            if d == 0:
                tot += c * halfL
            else:
                tot += c * mp.sin(d * halfL) / d
        return tot
    return phi


def make_g(xi, L, N):
    """g(z) = sum_{|j|<=N} xi_j/(z - p_j), the pole part of xi_hat:
    xi_hat(z) = 2 L^{-1/2} sin(zL/2) g(z)   (source eq. 5.25).
    Above p_N, g is holomorphic and its zeros are exactly the zeros of xi_hat
    that belong to D'' -- the sin factor's zeros there are the UV lattice
    {p_k : |k| > N}, which live on E_N^perp (Thm 5.10 iii), not on E'_N."""
    twopiL = 2 * mp.pi / L
    poles = [(twopiL * j, xi[j + N]) for j in range(-N, N + 1)]

    def g(z):
        return mp.fsum([c / (z - p) for (p, c) in poles])
    return g


def newton_root_sum_sq(xi, N):
    """sum_k s_k^2 over the 2N roots s_k of Det(D''-s) (source Lemma 5.4 iii).

    P(s) = sum_j xi_j prod_{i!=j}(s-i) over i,j in [-N,N].  Since
    sum_{i!=j} i = -j and e_2({i!=j}) = -S/2 + j^2 with S = sum_i i^2 =
    2 sum_{j=1..N} j^2, the top three coefficients are
        c_{2N} = sum_j xi_j,  c_{2N-1} = sum_j j xi_j = 0 (xi even),
        c_{2N-2} = -c_{2N} S/2 + sum_j j^2 xi_j,
    so by Newton's relation  sum_k s_k^2 = -2 c_{2N-2}/c_{2N} =
        2 sum_{j=1..N} j^2 - 2 (sum_j j^2 xi_j)/(sum_j xi_j).
    All 2N roots are real (Thm 5.10 iii), hence max_k |s_k| <= sqrt of this.
    The denominator is sum_j xi_j = sqrt(L) delta_N(xi), whose vanishing is
    already the registered VOID condition, so the bound is finite exactly
    where the point is admissible at all."""
    A = mp.fsum(xi)
    m2 = mp.fsum([xi[j + N] * (j * j) for j in range(-N, N + 1)])
    S = 2 * mp.fsum([mp.mpf(j) ** 2 for j in range(1, N + 1)])
    return S - 2 * m2 / A


def positive_zeros(xi, L, N, dps, msamp):
    """The N positive zeros of xi_hat that belong to the compressed D''.

    Amendment A3 (design.md sec.13).  The registered count gate (exactly N) is
    unchanged and is correct: dim E'_N = (2N+1)-1 = 2N (Thm 5.10 i), D'' is
    selfadjoint (Lemma 5.4 ii) so all 2N roots of Det(D''-s) are real, and that
    polynomial is even with Det(D''-0) = xi_0 prod_{i!=0} i != 0 -- hence N
    positive and N negative.  What was wrong is the SEARCH DOMAIN: nothing in
    the source confines those roots to the pole hull, and at lambda=2 two of
    them provably sit above p_{N+1}.  Two regimes:

    * 0 < z <= p_N : pole gaps (p_j, p_{j+1}), j = 0..N-1, scanning phi
      (= xi_hat up to a positive constant).  Lattice ENDPOINTS are now sampled:
      phi(p_j) = (-1)^j xi_j L/2 exactly, and Det(D''-j) = xi_j prod_{k!=j}(k-j),
      so p_j is itself a D'' eigenvalue precisely when xi_j = 0 -- a root the
      old interior-only sampling could never see.
    * z > p_N : scan g, NOT phi (see make_g: phi would also vanish at every UV
      lattice point p_k, |k| > N, which are not D'' eigenvalues).  Cells walk
      upward and stop as soon as the source's N zeros are all accounted for;
      the hard ceiling is Z_max = (2pi/L) sqrt(sum_k s_k^2) from
      newton_root_sum_sq, which no root can exceed.

    Every change here strictly widens the search or merges coincident hits, so
    the count can only rise toward N or stay put -- the gate cannot be passed by
    anything this function invents.  Registered refinement rounds x4, x16 kept.
    Returns (zeros, meta)."""
    t0 = time.time()
    with mp.workdps(dps):
        twopiL = 2 * mp.pi / L
        phi = make_phi(xi, L, N)
        g = make_g(xi, L, N)
        ref = max(abs(x) for x in xi) * (L / 2)
        zero_thresh = ref * mp.mpf(10) ** (-(dps - 15))
        ssq = newton_root_sum_sq(xi, N)
        zmax = twopiL * mp.sqrt(ssq) if ssq > 0 else twopiL * (N + 1)
        if zmax < twopiL * (N + 1):
            zmax = twopiL * (N + 1)
        kmax = int(mp.floor(zmax / twopiL)) + 1

        def bisect(f, lo, hi_, flo):
            for _ in range(120):
                mid = (lo + hi_) / 2
                fm = f(mid)
                if fm == 0:
                    return mid
                if flo * fm < 0:
                    hi_ = mid
                else:
                    lo, flo = mid, fm
            return (lo + hi_) / 2

        def cell(f, a, b, mcount, inc_lo, inc_hi):
            h = (b - a) / (mcount + 1)
            pts = [a + h * (i + 1) for i in range(mcount)]
            if inc_lo:
                pts.insert(0, a)
            if inc_hi:
                pts.append(b)
            vals = [f(t) for t in pts]
            out = []
            for i in range(len(pts) - 1):
                va, vb = vals[i], vals[i + 1]
                if abs(va) <= zero_thresh:
                    out.append(pts[i])
                    continue
                if i == len(pts) - 2 and abs(vb) <= zero_thresh:
                    out.append(pts[i + 1])
                    continue
                if va * vb < 0:
                    out.append(bisect(f, pts[i], pts[i + 1], va))
            return out

        def dedup(zs, tol):
            zs = sorted(zs)
            out = []
            for z in zs:
                if not out or abs(z - out[-1]) > tol:
                    out.append(z)
            return out

        def scan(mcount):
            tol = twopiL / (4 * (mcount + 1))
            zeros = []
            # --- regime 1: the pole hull (0, p_N], phi, endpoints included ---
            for j in range(N):
                zeros += cell(phi, twopiL * j, twopiL * (j + 1), mcount,
                              j > 0, j == N - 1)
            # --- regime 2: z > p_N, g, walk up to Z_max, stop at N ---
            k = N
            while k < kmax and len(dedup(zeros, tol)) < N:
                a, b = twopiL * k, twopiL * (k + 1)
                if a >= zmax:
                    break
                zeros += cell(g, a, b if b < zmax else zmax, mcount,
                              False, True)
                k += 1
            return dedup(zeros, tol), k

        zeros, kstop = scan(msamp)
        rounds = 0
        for fac in REG["scan_refine_factors"]:
            if len(zeros) == N:
                break
            rounds += 1
            zeros, kstop = scan(msamp * fac)

        # free consistency invariants: DIAGNOSTIC ONLY, never a gate.
        seq = [((-1) ** j) * xi[N + j] for j in range(N + 1)]
        sg = [(1 if v > 0 else -1) for v in seq]
        V = sum(1 for i in range(len(sg) - 1) if sg[i] != sg[i + 1])
        pN = twopiL * N
        n_lo = sum(1 for z in zeros if z <= pN)
        newton_found = 2 * mp.fsum([(z / twopiL) ** 2 for z in zeros])
        meta = {"count": len(zeros), "expected": N,
                "refine_rounds": rounds,
                "sign_changes_V": V,
                "n_below_pN": n_lo, "n_above_pN": len(zeros) - n_lo,
                "V_consistent": bool(n_lo == V),
                "zmax_newton": mp.nstr(zmax, 12),
                "cells_walked_above_pN": kstop - N,
                "newton_sum_sq": mp.nstr(ssq, 15),
                "newton_sum_sq_from_found": mp.nstr(newton_found, 15),
                "seconds": round(time.time() - t0, 2)}
        return sorted(zeros), meta


# ----------------------------------------------------------------------------
# benchmarks [conv:zeros] (design.md section 6)
# ----------------------------------------------------------------------------

def load_zero_cache():
    if os.path.exists(ZCACHE_PATH):
        with open(ZCACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [mp.mpf(s) for s in data["gammas"]]
    return None


def build_zero_cache(tmax):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    gammas = []
    with mp.workdps(REG["zeros_dps"]):
        k = 1
        while True:
            g = mp.im(mp.zetazero(k))
            gammas.append(g)
            if g > tmax:
                break
            k += 1
            if k % 25 == 0:
                print(f"  zetazero progress: k={k} gamma={mp.nstr(g, 12)}",
                      flush=True)
    atomic_write_json(ZCACHE_PATH, {
        "dps": REG["zeros_dps"], "tmax_requested": tmax,
        "gammas": [mp.nstr(g, 25) for g in gammas],
        "source": "mpmath.zetazero", "mpmath": mp.__version__,
    })
    print(f"zeros cache written: {len(gammas)} ordinates up to "
          f"{mp.nstr(gammas[-1], 12)} -> {ZCACHE_PATH}")


def zeros_upto(T):
    """All gamma_j <= T. Hardcoded anchors for T <= 49.77, else cache."""
    cache = load_zero_cache()
    if cache is not None and cache[-1] > T:
        gam = [g for g in cache if g <= T]
        # anchor consistency check on the first 10
        with mp.workdps(30):
            for i in range(min(10, len(gam))):
                if abs(gam[i] - mp.mpf(HARDCODED_ZEROS[i])) > mp.mpf("1e-12"):
                    raise RuntimeError(
                        f"zero cache disagrees with hardcoded anchor #{i+1}")
        return gam
    hard = [mp.mpf(s) for s in HARDCODED_ZEROS]
    if T < float(HARDCODED_ZEROS[-1]):
        return [g for g in hard if g <= T]
    raise RuntimeError(
        f"need zeta zeros up to T={float(T):.1f}; run --build-zeros "
        f"{int(float(T)) + 20} first")


def rvm_count(T):
    Tf = mp.mpf(T)
    if Tf <= 2 * mp.pi * mp.e:
        return mp.mpf(0)
    return (Tf / (2 * mp.pi)) * mp.log(Tf / (2 * mp.pi * mp.e)) + mp.mpf(7) / 8


def rvm_smooth_benchmark(T, x0):
    def dens(t):
        v = mp.log(t / (2 * mp.pi)) / (2 * mp.pi)
        return (v if v > 0 else mp.mpf(0)) / (t * t + x0)
    return mp.quad(dens, [2 * mp.pi, T])


def xi_completed(s):
    return s * (s - 1) / 2 * mp.pi ** (-s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def S_Xi_target(x0):
    s0 = mp.mpf(1) / 2 + mp.sqrt(x0)
    d = mp.diff(xi_completed, s0)
    return d / xi_completed(s0) / (2 * mp.sqrt(x0))


def S_tail_closed(L, N, x0):
    a = L * mp.sqrt(x0) / (2 * mp.pi)
    full = (mp.pi / (2 * a)) * mp.coth(mp.pi * a) - 1 / (2 * a * a)
    partial = mp.fsum(1 / (mp.mpf(j) ** 2 + a * a) for j in range(1, N + 1))
    return (L / (2 * mp.pi)) ** 2 * (full - partial)


# ----------------------------------------------------------------------------
# per-point runner
# ----------------------------------------------------------------------------

def run_mode(spec, N, x0, dps, maxdeg, msamp, mode_name):
    tag = spec_tag(spec)
    print(f"[{tag} N={N} {mode_name}] dps={dps} maxdeg={maxdeg} "
          f"msamp={msamp}", flush=True)
    tau, ameta = assemble(spec, N, dps, maxdeg)
    print(f"  assembled in {ameta['assembly_seconds']}s "
          f"(quad_err<={ameta['quad_err_max']})", flush=True)
    eig = bottom_cluster(tau, dps)
    void = []
    if eig["even_defect"] > mp.mpf(REG["even_defect_tol"]):
        void.append("even_defect")
    if eig["simplicity_ratio"] < mp.mpf(REG["simplicity_min_ratio"]):
        void.append("not_simple")
    with mp.workdps(dps):
        xinorm = norm(eig["xi"])
        if abs(eig["sum_xi"]) < mp.mpf(10) ** (-(dps // REG["deltaN_exp_div"])) * xinorm:
            void.append("deltaN_degenerate")
    lam = lam_value(spec)
    with mp.workdps(dps):
        L = 2 * mp.log(lam)
    zeros, smeta = positive_zeros(eig["xi"], L, N, dps, msamp)
    invalid = []
    if smeta["count"] != N:
        invalid.append(f"count_mismatch:{smeta['count']}!={N}")
    with mp.workdps(REG["output_dps"]):
        x0m = mp.mpf(x0)
        T = mp.pi * N / mp.log(lam)
        S_IR = mp.fsum(1 / (z * z + x0m) for z in zeros)
        S_IR_sec = {}
        for xs in REG["x0_secondary"]:
            xv = mp.mpf(mp.mpf(xs.split("/")[0]) / mp.mpf(xs.split("/")[1])) \
                if "/" in xs else mp.mpf(xs)
            S_IR_sec[xs] = mp.nstr(
                mp.fsum(1 / (z * z + xv) for z in zeros), 12)
        tc = mp.mpf(REG["t_spur"])
        low = [z for z in zeros if z <= tc]
        n_spur = len(low)
        S_low = mp.fsum(1 / (z * z + x0m) for z in low)
        S_tail = S_tail_closed(L, N, x0m)
        gam = zeros_upto(T)
        B_zero = mp.fsum(1 / (g * g + x0m) for g in gam)
        B_smooth = rvm_smooth_benchmark(T, x0m)
        Nbar = rvm_count(T)
        tol_edge = (abs(N - Nbar) + 2) / ((T / 2) ** 2 + x0m)
        S_Xi = S_Xi_target(x0m)
        E = S_IR - B_zero
        j1_tol = max(mp.mpf(REG["j1_pass_rel"]) * B_zero,
                     mp.mpf(REG["j1_pass_edge_factor"]) * tol_edge)
        rec = {
            "mode": mode_name, "dps": dps, "maxdeg": maxdeg, "msamp": msamp,
            "lambda_tag": tag, "lambda_sq": lam_sq(spec), "N": N,
            "x0": x0, "conv": "S-half",
            "eps1": mp.nstr(eig["eps1"], 20), "eps2": mp.nstr(eig["eps2"], 20),
            "eps1_sign": (1 if eig["eps1"] > 0 else -1),
            "resid": mp.nstr(eig["resid"], 5),
            "even_defect": mp.nstr(eig["even_defect"], 5),
            "odd_defect": mp.nstr(eig["odd_defect"], 5),
            "simplicity_ratio": mp.nstr(eig["simplicity_ratio"], 5),
            "cluster64": eig["cluster64"], "neg_big64": eig["neg_big64"],
            "void": void, "invalid": invalid,
            "zeros_pos": [mp.nstr(z, 25) for z in zeros],
            "count_found": smeta["count"], "refine_rounds": smeta["refine_rounds"],
            "scan_diag": {k: smeta[k] for k in (
                "sign_changes_V", "n_below_pN", "n_above_pN", "V_consistent",
                "zmax_newton", "cells_walked_above_pN",
                "newton_sum_sq", "newton_sum_sq_from_found") if k in smeta},
            "T_window": mp.nstr(T, 12), "Nbar_rvm": mp.nstr(Nbar, 12),
            "n_zeros_benchmark": len(gam),
            "S_IR": mp.nstr(S_IR, 15), "S_IR_secondary_x0": S_IR_sec,
            "S_low": mp.nstr(S_low, 15), "n_spur": n_spur,
            "S_tail_UV_closed_form": mp.nstr(S_tail, 15),
            "B_zero": mp.nstr(B_zero, 15), "B_smooth": mp.nstr(B_smooth, 15),
            "S_Xi_anchor": mp.nstr(S_Xi, 15),
            "E_excess": mp.nstr(E, 15), "tol_edge": mp.nstr(tol_edge, 8),
            "J1": ("PASS" if abs(E) <= j1_tol else "NOTE"),
            "J1_tol": mp.nstr(j1_tol, 8),
            "assembly": ameta, "scan_seconds": smeta["seconds"],
            "eig_seconds": eig["seconds"],
        }
    print(f"  S_IR={rec['S_IR']}  B_zero={rec['B_zero']}  "
          f"n_spur={n_spur}  J1={rec['J1']}  void={void} invalid={invalid}",
          flush=True)
    return rec


def spec_tag(spec):
    kind, k = spec
    return f"sqrt{k}" if kind == "sqrt" else str(k)


def point_path(tag, N):
    return os.path.join(RESULTS_DIR, f"point_L{tag}_N{N}.json")


def run_point(spec, N, x0, args_ns, dps_base=None, dps_hi=None):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    tag = spec_tag(spec)
    path = point_path(tag, N)
    if os.path.exists(path) and not args_ns.force:
        with open(path, "r", encoding="utf-8") as f:
            old = json.load(f)
        if (old.get("reg_sha256") == REG_HASH and "base" in old
                and "hi" in old):
            print(f"[{tag} N={N}] checkpoint exists, skipping "
                  f"(--force to redo)", flush=True)
            return old
    if dps_base is None:
        dps_base = dps_schedule(spec)
    if dps_hi is None:
        dps_hi = dps_base + REG["dps_hi_extra"]
    rec = {"reg_sha256": REG_HASH, "provenance": provenance(args_ns),
           "lambda_tag": tag, "N": N, "x0": x0}
    rec["base"] = run_mode(spec, N, x0, dps_base, REG["maxdeg_base"],
                           REG["msamp_base"], "base")
    atomic_write_json(path, rec)
    rec["hi"] = run_mode(spec, N, x0, dps_hi, REG["maxdeg_hi"],
                         REG["msamp_hi"], "hi")
    atomic_write_json(path, rec)
    return rec


# ----------------------------------------------------------------------------
# judges: J2 per point, J3 aggregate (design.md sections 7-8)
# ----------------------------------------------------------------------------

def judge_point(rec):
    """Returns status in {OK, VOID, INVALID, MISSING} + reasons."""
    if rec is None or "base" not in rec or "hi" not in rec:
        return "MISSING", ["incomplete checkpoint"]
    # registration gate (adversarial verification 2026-08-06, pre-run): a
    # checkpoint computed at any x0 other than the registered one must never
    # feed the x0=1-labeled verdict (S_low scales like 1/x0 — an off-
    # registration x0 could manufacture or mask a kill).
    if str(rec.get("x0")) != REG["x0"]:
        return "INVALID", [
            f"x0={rec.get('x0')!r} != registered x0={REG['x0']}"]
    b, h = rec["base"], rec["hi"]
    reasons = []
    if b["void"] or h["void"]:
        return "VOID", sorted(set(b["void"]) | set(h["void"]))
    if b["invalid"] or h["invalid"]:
        return "INVALID", b["invalid"] + h["invalid"]
    N = rec["N"]
    if b["count_found"] != N or h["count_found"] != N:
        return "INVALID", ["count gate"]
    with mp.workdps(40):
        zb = [mp.mpf(s) for s in b["zeros_pos"]]
        zh = [mp.mpf(s) for s in h["zeros_pos"]]
        ztol = mp.mpf(REG["j2_zero_tol_rel"])
        for k in range(N):
            if abs(zb[k] - zh[k]) > ztol * max(mp.mpf(1), abs(zb[k])):
                reasons.append(f"J2.b zero {k+1} unstable")
                break
        if abs(mp.mpf(b["S_IR"]) - mp.mpf(h["S_IR"])) > mp.mpf(REG["j2_S_tol"]):
            reasons.append("J2.c S_IR unstable")
        if abs(mp.mpf(b["S_low"]) - mp.mpf(h["S_low"])) > mp.mpf(REG["j2_S_tol"]):
            reasons.append("J2.c S_low unstable")
    if reasons:
        return "INVALID", reasons
    return "OK", []


def _monotone(vals, slack):
    return all(vals[i + 1] >= vals[i] - slack for i in range(len(vals) - 1))


def aggregate_verdict(print_table=True):
    lam_specs = [parse_lambda(t)[1] for t in REG["grid_lambdas"]]
    tags = [spec_tag(s) for s in lam_specs]
    sizes = REG["grid_sizes"]
    recs, status = {}, {}
    for tg in tags:
        for N in sizes:
            p = point_path(tg, N)
            rec = None
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    rec = json.load(f)
                if rec.get("reg_sha256") != REG_HASH:
                    rec = None
            recs[(tg, N)] = rec
            status[(tg, N)] = judge_point(rec)

    if print_table:
        print("\n== T3 probe grid table [conv:S-half, x0=1] ==")
        hdr = (f"{'lambda':>7} {'N':>4} {'status':>8} {'n_spur':>6} "
               f"{'S_low':>12} {'S_IR':>12} {'B_zero':>12} {'E':>12} "
               f"{'J1':>5} {'S_tail(UV)':>12}")
        print(hdr)
        for tg in tags:
            for N in sizes:
                st, why = status[(tg, N)]
                rec = recs[(tg, N)]
                if rec is None or "base" not in rec:
                    print(f"{tg:>7} {N:>4} {'MISSING':>8}")
                    continue
                bb = rec["base"]
                print(f"{tg:>7} {N:>4} {st:>8} {bb['n_spur']:>6} "
                      f"{bb['S_low']:>12} {bb['S_IR']:>12} "
                      f"{bb['B_zero']:>12} {bb['E_excess']:>12} "
                      f"{bb['J1']:>5} {bb['S_tail_UV_closed_form']:>12}"
                      + (f"   [{','.join(why)}]" if why else ""))
        anchor = recs.get((tags[0], sizes[0]))
        if anchor and "base" in anchor:
            print(f"anchor S_Xi(x0=1) = {anchor['base']['S_Xi_anchor']} "
                  f"[verified numerics]")

    missing = [k for k, s in status.items() if s[0] == "MISSING"]
    invalid = [k for k, s in status.items() if s[0] == "INVALID"]
    void = [k for k, s in status.items() if s[0] == "VOID"]
    detail = {"missing": [f"{t}:{n}" for (t, n) in missing],
              "invalid": [f"{t}:{n}" for (t, n) in invalid],
              "void": [f"{t}:{n}" for (t, n) in void]}
    gridstr = ("L{" + ",".join(REG["grid_lambdas"]) + "}xN{"
               + ",".join(str(s) for s in sizes) + "}")

    def emit(verdict, extra=None):
        d = dict(detail)
        if extra:
            d.update(extra)
        line = (f"T3-VERDICT: {verdict} conv=S-half;x0=1;grid={gridstr} "
                f"detail={json.dumps(d, sort_keys=True)}")
        print("\n" + line)
        print("SCOPE: a KILL kills the repo's concrete T3 arm as instantiated "
              "(CCM D_log^{(lambda,N)}, IR trace, probed box); it does NOT "
              "refute the CCM papers' own claims, RH, or the abstract Lean "
              "core. A SURVIVE licenses only 'no low-energy accumulation at "
              "probed scales'. See design.md section 8.1.")
        return line

    if missing or invalid:
        return emit("INCONCLUSIVE", {"reason": "grid incomplete or J2 failed"})
    if void:
        return emit("INCONCLUSIVE", {
            "reason": "even-simplicity/deltaN hypothesis VOID at listed points "
                      "(news about the source hypothesis, not about T3)"})

    # all OK: evaluate J3 (base replicas)
    nsp = {k: recs[k]["base"]["n_spur"] for k in recs}
    slow = {k: float(mp.mpf(recs[k]["base"]["S_low"])) for k in recs}
    sir = {k: float(mp.mpf(recs[k]["base"]["S_IR"])) for k in recs}
    lam_max, lam_min = tags[-1], tags[0]
    N_max, N_min, N_mid = sizes[-1], sizes[0], sizes[-2]
    slack = float(mp.mpf(REG["mono_slack"]))

    # count-form
    with mp.workdps(40):
        ztop = [mp.mpf(s) for s in recs[(lam_max, N_max)]["base"]["zeros_pos"]
                if mp.mpf(s) <= mp.mpf(REG["t_spur"])]
        zmid = [mp.mpf(s) for s in recs[(lam_max, N_mid)]["base"]["zeros_pos"]
                if mp.mpf(s) <= mp.mpf(REG["t_spur"])]
        dz = mp.mpf(REG["kill_persist_dz"])
        persist = (abs(len(ztop) - len(zmid)) <= 1 and
                   all(any(abs(z - w) <= dz for w in zmid) for z in ztop))
    k2 = nsp[(lam_max, N_max)] >= REG["kill_count_min"]
    k3 = all(_monotone([nsp[(tg, N)] for tg in tags], 0)
             for N in sizes[1:]) and \
         all(_monotone([nsp[(tg, N)] for N in sizes], 0)
             for tg in tags[1:])
    k4 = (nsp[(lam_max, N_max)] >= nsp[(lam_min, N_max)] + REG["kill_count_growth"]
          and nsp[(lam_max, N_max)] >= nsp[(lam_max, N_min)] + REG["kill_count_growth"])
    count_kill = persist and k2 and k3 and k4

    # trace-form
    sl_abs = float(mp.mpf(REG["kill_Slow_abs"]))
    sl_fac = float(mp.mpf(REG["kill_Slow_factor"]))
    sl_floor = float(mp.mpf(REG["kill_Slow_floor"]))
    t1 = slow[(lam_max, N_max)] >= sl_abs
    t2 = (slow[(lam_max, N_max)] >= sl_fac * max(slow[(lam_min, N_max)], sl_floor)
          and slow[(lam_max, N_max)] >= sl_fac * max(slow[(lam_max, N_min)], sl_floor))
    t3g = (_monotone([slow[(tg, N_max)] for tg in tags], slack)
           and _monotone([slow[(lam_max, N)] for N in sizes], slack))
    trace_kill = t1 and t2 and t3g

    if count_kill or trace_kill:
        return emit("KILL", {
            "count_form": count_kill, "trace_form": trace_kill,
            "n_spur_top": nsp[(lam_max, N_max)],
            "S_low_top": slow[(lam_max, N_max)]})

    surv = (max(nsp.values()) <= REG["survive_nspur_max"]
            and max(slow.values()) <= float(mp.mpf(REG["survive_Slow_max"]))
            and max(sir.values()) <= float(mp.mpf(REG["survive_SIR_max"])))
    if surv:
        return emit("SURVIVE-AT-PROBED-SCALES", {
            "max_n_spur": max(nsp.values()),
            "max_S_low": max(slow.values()), "max_S_IR": max(sir.values())})
    # diagnostic trend label (detail only, never a verdict): low-band mass
    # shrinking as lambda grows, clean at lambda_max = the CCM mechanism
    # engaging late; see design.md section 8.
    trend = None
    if (all(_monotone([nsp[(tg, N)] for tg in reversed(tags)], 0)
            for N in sizes)
            and all(nsp[(lam_max, N)] <= 1 for N in sizes)):
        trend = "low-band-decreasing-in-lambda(clean-at-lambda-max)"
    return emit("AMBIGUOUS", {
        "max_n_spur": max(nsp.values()), "max_S_low": max(slow.values()),
        "max_S_IR": max(sir.values()), "trend": trend,
        "note": "patterns match neither registered kill nor survive; "
                "see J1 table for diagnosis"})


# ----------------------------------------------------------------------------
# self-tests ST1/ST2/ST3 (design.md section 7.4) — pilot-stage gates
# ----------------------------------------------------------------------------

def st1_pole_block(spec, dps=40):
    """W02 diagonal (eq 4.2) vs (3.19) pole term 2Re(fhat(i/2)fhat(-i/2))."""
    ok_all = True
    with mp.workdps(dps):
        lam = lam_value(spec)
        L = 2 * mp.log(lam)
        sh2 = mp.sinh(L / 4) ** 2
        pi2_16 = 16 * mp.pi ** 2
        for n in (0, 1):
            w02 = (32 * L * sh2 * (L * L - pi2_16 * n * n)
                   / ((L * L + pi2_16 * n * n) ** 2))
            om = 2 * mp.pi * n / L

            def fh(sig):  # fhat(±i/2) = int_0^L L^-1/2 e^{i om x} e^{sig(x-L/2)/2} dx
                return mp.quad(
                    lambda x: mp.exp(1j * om * x) * mp.exp(sig * (x - L / 2) / 2),
                    [0, L], maxdegree=8) / mp.sqrt(L)

            fp, fm_ = fh(mp.mpf(1)), fh(mp.mpf(-1))
            v_plain = 2 * mp.re(fp * fm_)
            v_conj = 2 * mp.re(fp * mp.conj(fm_))
            tol = mp.mpf(REG["st1_tol_rel"]) * max(1, abs(w02))
            match = ("plain" if abs(v_plain - w02) <= tol else
                     ("conj" if abs(v_conj - w02) <= tol else "NONE"))
            ok = match != "NONE"
            ok_all = ok_all and ok
            print(f"ST1 n={n}: W02={mp.nstr(w02, 12)} plain="
                  f"{mp.nstr(v_plain, 12)} conj={mp.nstr(v_conj, 12)} "
                  f"-> {'PASS(' + match + ')' if ok else 'FAIL'}")
    return ok_all


def st2_archimedean(spec, dps=40):
    """Assembled WR diag (2 gamma - 2 beta, rho-integrals) vs the independent
    spectral form -int |fhat_n(t)|^2 theta'(t)/pi dt.  Sign is part of the test."""
    ok_all = True
    with mp.workdps(dps):
        lam = lam_value(spec)
        L = 2 * mp.log(lam)
        alpha, beta, gamma_, _err = archimedean_tables(L, 1, maxdeg=8)

        def thp(t):
            return -mp.log(mp.pi) / 2 + mp.re(mp.digamma(mp.mpf(1) / 4 + 1j * t / 2)) / 2

        for n in (0, 1):
            wr = 2 * gamma_[n] - 2 * beta[n]
            pn = 2 * mp.pi * n / L

            def f2(t):
                d = t - pn
                if abs(d) < mp.mpf("1e-9"):
                    return L  # removable limit (2-2cos(dL))/(L d^2) -> L
                return (2 - 2 * mp.cos(t * L)) / (L * d * d)

            Tinf = mp.mpf(200)
            h = 2 * mp.pi / L
            total = mp.mpf(0)
            t = mp.mpf(-Tinf)
            # integrate over R: symmetric range in per-period cells
            while t < Tinf - h / 2:
                total += mp.quad(lambda u: f2(u) * thp(u), [t, min(t + h, Tinf)],
                                 maxdegree=6)
                t += h
            # smoothed tails (|fhat|^2 ~ mean 2/(L (t-pn)^2)); osc part recorded
            tail_p = (2 / L) * mp.quad(lambda u: thp(u) / (u - pn) ** 2,
                                       [Tinf, mp.inf])
            tail_m = (2 / L) * mp.quad(lambda u: thp(-u) / (u + pn) ** 2,
                                       [Tinf, mp.inf])
            spectral = -(total + tail_p + tail_m) / mp.pi
            tol = mp.mpf(REG["st2_tol"]) * max(1, abs(wr))
            ok = abs(spectral - wr) <= tol
            sign_flip = abs(-spectral - wr) <= tol
            ok_all = ok_all and ok
            print(f"ST2 n={n}: WR_diag(rho-integrals)={mp.nstr(wr, 10)} "
                  f"spectral(theta')={mp.nstr(spectral, 10)} -> "
                  f"{'PASS' if ok else 'FAIL'}"
                  + ("  [OPPOSITE SIGN MATCHES: assembly sign convention "
                     "wrong — halt]" if (not ok and sign_flip) else ""))

        # --- ST2b (added by adversarial verification 2026-08-05): the
        # off-diagonal entry WR(0,1), which ST1/ST2 diagonals cannot see.
        # Assembly convention (Prop 4.3): WR(0,1) = (al(1)-al(0))/(0-1)
        # = -alpha_L(1).  Independent check: polarized (3.19),
        # WR(n,m) = -(1/pi) Int fhat_n(t) fhat_m(t) theta'(t) dt with the
        # symmetric log-interval basis.  From U_n = L^{-1/2} e^{2 pi i n x/L}
        # (eq 2.6), V_n(u) = U_n(log(lam u)) (3.21) and Fhat(s) = Int F u^{-is}
        # d*u (3.5), with u = e^{x-L/2}, one gets for EVERY n
        #     fhat_n(t) = 2 sin(tL/2)/(sqrt(L) (t - p_n)),
        # real, with no n-dependent phase (the e^{i p_n L/2} = (-1)^n cancels
        # against sin(pi n - tL/2) = -(-1)^n sin(tL/2)).  Hence
        # fhat_0*fhat_1 = +(2-2cos(tL))/(L t (t-p1)), removable at 0 and p1
        # (both limits are 0) — the SAME convention as the |fhat_n|^2 used on
        # the diagonal above.  A minus sign here was a defect of this
        # REFERENCE (not of the assembly); repaired 2026-08-06, design.md
        # amendment A2.  A sign-flipped WR off-diagonal block FAILS
        # here with the [OPPOSITE SIGN MATCHES] banner -> halt, re-derive
        # the basis convention; never auto-flip.
        wr01 = (alpha[1] - alpha[0]) / (0 - 1)
        p1 = 2 * mp.pi / L

        def g01(t):
            if abs(t) < mp.mpf("1e-9") or abs(t - p1) < mp.mpf("1e-9"):
                return mp.mpf(0)  # removable points, limit 0
            return (2 - 2 * mp.cos(t * L)) / (L * t * (t - p1))

        Tinf = mp.mpf(200)
        h = 2 * mp.pi / L
        total = mp.mpf(0)
        t = mp.mpf(-Tinf)
        while t < Tinf - h / 2:
            total += mp.quad(lambda u: g01(u) * thp(u),
                             [t, min(t + h, Tinf)], maxdegree=6)
            t += h
        tail_p = (2 / L) * mp.quad(lambda u: thp(u) / (u * (u - p1)),
                                   [Tinf, mp.inf])
        tail_m = (2 / L) * mp.quad(lambda u: thp(-u) / (u * (u + p1)),
                                   [Tinf, mp.inf])
        spectral01 = -(total + tail_p + tail_m) / mp.pi
        tol01 = mp.mpf(REG["st2_tol"]) * max(1, abs(wr01))
        ok01 = abs(spectral01 - wr01) <= tol01
        flip01 = abs(-spectral01 - wr01) <= tol01
        ok_all = ok_all and ok01
        print(f"ST2b (0,1): WR_offdiag(assembly conv)={mp.nstr(wr01, 10)} "
              f"spectral(theta')={mp.nstr(spectral01, 10)} -> "
              f"{'PASS' if ok01 else 'FAIL'}"
              + ("  [OPPOSITE SIGN MATCHES: WR off-diagonal sign flipped "
                 "— halt]" if (not ok01 and flip01) else ""))
    return ok_all


def st3_info(rec):
    """Informational: distance of the lowest zeros to zeta ordinates."""
    if rec is None or "base" not in rec:
        return
    with mp.workdps(30):
        zs = [mp.mpf(s) for s in rec["base"]["zeros_pos"]][:3]
        for k, z in enumerate(zs):
            g = mp.mpf(HARDCODED_ZEROS[k])
            print(f"ST3 info: z_{k+1}={mp.nstr(z, 12)}  gamma_{k+1}="
                  f"{mp.nstr(g, 12)}  diff={mp.nstr(z - g, 5)}  "
                  f"[no gate: source publishes no numbers at pilot scale]")


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="T3 kill-test probe (design.md)")
    ap.add_argument("--lambdas", type=str, default=None,
                    help="comma list, e.g. 2,sqrt8,3,sqrt13 (exact lambda^2)")
    ap.add_argument("--sizes", type=str, default=None,
                    help="comma list of N, e.g. 20,40,80,120")
    ap.add_argument("--x0", type=str, default=REG["x0"])
    ap.add_argument("--pilot", action="store_true",
                    help="self-tests + registered pilot points (lambda=2, N=6,8)")
    ap.add_argument("--build-zeros", type=float, default=None, metavar="TMAX",
                    help="build zeta zero cache up to TMAX and exit")
    ap.add_argument("--verdict-only", action="store_true",
                    help="aggregate checkpoints and print the verdict line")
    ap.add_argument("--force", action="store_true",
                    help="recompute existing checkpoints")
    args = ap.parse_args()

    print(f"# t3_probe start  sha256={script_sha256()[:16]}...  "
          f"reg={REG_HASH[:16]}...  mpmath={mp.__version__}")

    if args.build_zeros is not None:
        build_zero_cache(args.build_zeros)
        return 0

    if args.verdict_only:
        aggregate_verdict()
        return 0

    if args.pilot:
        t0 = time.time()
        spec = parse_lambda(REG["pilot"]["lambdas"][0])[1]
        print("== pilot: self-tests (design.md 7.4) ==")
        ok1 = st1_pole_block(spec)
        ok2 = st2_archimedean(spec)
        if not (ok1 and ok2):
            print("PILOT-GATE: FAIL (ST self-tests). Production runs are NOT "
                  "licensed; fix assembly and re-register if formulas change.")
            print("T3-VERDICT: INCONCLUSIVE conv=S-half;x0=1;grid=pilot "
                  "detail={\"reason\": \"ST self-test failure\"}")
            return 1
        print("== pilot: points ==")
        last = None
        for N in REG["pilot"]["sizes"]:
            last = run_point(spec, N, args.x0, args,
                             dps_base=REG["pilot"]["dps_base"],
                             dps_hi=REG["pilot"]["dps_hi"])
        st3_info(last)
        st, why = judge_point(last)
        print(f"pilot J2 status of last point: {st} {why}")
        print(f"pilot wall total: {round(time.time() - t0, 1)} s "
              f"(owner rule: measure wall/RSS externally before treating the "
              f"pilot as local-light)")
        print("T3-VERDICT: INCONCLUSIVE conv=S-half;x0=1;grid=pilot "
              "detail={\"reason\": \"pilot never yields a verdict; grid "
              "incomplete by construction\"}")
        return 0

    lam_toks = (args.lambdas.split(",") if args.lambdas
                else REG["grid_lambdas"])
    sizes = ([int(s) for s in args.sizes.split(",")] if args.sizes
             else REG["grid_sizes"])
    specs = [parse_lambda(t)[1] for t in lam_toks]

    # fail early if the zero cache cannot cover the largest window
    tmax_needed = max(
        math.pi * N / float(mp.log(lam_value(s))) for s in specs for N in sizes)
    if tmax_needed > float(HARDCODED_ZEROS[-1]):
        cache = load_zero_cache()
        if cache is None or float(cache[-1]) <= tmax_needed:
            print(f"ERROR: zero cache missing/short; run "
                  f"--build-zeros {int(tmax_needed) + 20} first")
            return 2

    for s in specs:
        for N in sizes:
            run_point(s, N, args.x0, args)
    aggregate_verdict()
    return 0


if __name__ == "__main__":
    sys.exit(main())
