#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mc_moments.py -- (MC) moment-convergence WITNESS (T3 kill-test, supplemental)
=============================================================================

STATUS AND DISCIPLINE (house rules, binding)
  * This script GATES NOTHING.  It is READ-ONLY: it never writes or modifies
    a checkpoint, never prints a T3-VERDICT line (or any verdict line), and
    nothing it prints may feed J1/J2/J3.  Every line it prints begins with
    "MC-WITNESS".  The registered verdict is whatever the registered
    aggregator (t3_probe.py --verdict-only) prints, verbatim, independently
    of this output.
  * It is STANDALONE: no import of t3_probe.  It consumes only the deposited
    per-point checkpoints (results/point_L{tag}_N{N}.json), the zeta zero
    cache (results/zeta_zeros_cache.json), and its own arithmetic.  The
    checkpoint's own stored strings (zeros_pos, S_IR, S_Xi_anchor, x0, N,
    lambda_sq) are the only inputs from the campaign.

WHAT IT COMPUTES ((MC) route, Codex desk, under audit)
  For each VALID replica (base/hi) of each per-point checkpoint, the finite
  moment sequence of the compressed operator D'' at (lambda, N):

      b_n^(m) = (1/(2*x0)) * Tr T^(n+1),   T = x0 * (D''^2 + x0 I)^(-1),
              = (1/(2*x0)) * sum_{full spectrum} t_i^(n+1),
      t_i = x0 / (z_i^2 + x0),   n = 0..NMAX.

  [conv:MC-double]  The checkpoint deposits ONLY the positive IR zeros
  ([conv:S-half], N of them).  The spectrum of D'' is symmetric under
  z -> -z (Det(D''-s) is an even polynomial, Lemma 5.4 iii / Thm 5.10 iii)
  and t_i depends on z_i^2 only, so the FULL-spectrum sum is exactly TWICE
  the positive-zero sum:

      b_n^(m) = (1/(2*x0)) * 2 * sum_{z in zeros_pos} (x0/(z^2+x0))^(n+1)
              = (1/x0)     *     sum_{z in zeros_pos} (x0/(z^2+x0))^(n+1).

  SELF-CHECK built into the convention: at n = 0 the doubling and the
  1/(2*x0) prefactor cancel to
      b_0^(m) = sum_{z in zeros_pos} 1/(z^2+x0) = S_IR
  exactly as stored in the checkpoint [conv:S-half].  The script recomputes
  b_0^(m) from the zeros list and prints PASS/FAIL of that reconciliation
  per replica (tolerance recon_tol_rel below: the checkpoint stores S_IR at
  15 significant digits).  Two convention caveats (verifier findings,
  2026-08-06 cross-audit):
    * b_0^(m) = S_IR is exact ONLY when 0 is not an eigenvalue of D''
      (xi_0 != 0); a zero eigenvalue would add mult_0/(2*x0).  Such a point
      fails the registered count gate (N positive zeros found), so on every
      J2-valid point the identity is exact; the count_found flag echoed on
      the POINT line is the reader's signal.
    * [conv:S-half] means b_0^(m) equals the checkpoint's S_IR, which is
      HALF the prose-T3 trace Tr((D''^2+x0)^{-1}) (design U9 factor-2
      note).  Anyone reconciling against the prose trace instead of the
      stored S_IR string will see a spurious factor 2.

  TARGETS, two routes:
  (a) zero-side benchmark, per point, truncated HONESTLY at the point's own
      window T = pi*N/log(lambda) (same truncation as the registered J1
      benchmark B_zero):
          b_n^Xi,zero(x0; T) = x0^n * sum_{gamma_j <= T} 1/(gamma_j^2+x0)^(n+1)
      over the cached zeta ordinates [conv:zeros].  This equals
      (1/(2*x0)) * 2 * sum_j v_j^(n+1) with v_j = x0/(x0+gamma_j^2): the SAME
      weighting as the finite side, doubled over +-gamma the same way.  The
      truncation is printed per point (n_zeros used, gamma_max, T, and a flag
      if the cache ran out before T).  The omitted tail is POSITIVE, so every
      printed target is a strict lower bound of the full sum; for n >= 1 the
      tail is O(T^(-2n-1) log T) -- decreasing rapidly in n BECAUSE higher
      moments weight low zeros more: the summand x0^n/(gamma^2+x0)^(n+1)
      suppresses gamma > T by an extra factor ~ (x0/T^2)^n per unit of n,
      so the truncated benchmark gets MORE accurate, not less, as n grows.
  (b) the S_Xi anchor route, n = 0 ONLY (already the registered J1 anchor):
          b_0^Xi = S_Xi(x0) = (xi'/xi)(1/2+sqrt(x0)) / (2*sqrt(x0)),
      recomputed here independently with mpmath and cross-checked against
      the checkpoint's stored S_Xi_anchor string.  No closed form for
      n >= 1 is claimed by this witness.

  TREND: for each mode and each n, the per-point gap |b_n^(m) - b_n^Xi,zero|
  is tabulated across the grid, and the script prints whether the gap is
  monotone non-increasing along N at fixed lambda and along lambda at fixed
  N (descriptive lines only; NOT a kill/survive statement -- the registered
  judges do not read moments).

VALIDITY RULE (this witness's own, gates nothing)
  A replica is consumed iff it is present in the checkpoint and carries a
  non-empty "zeros_pos" list.  A checkpoint (or replica) lacking the zeros
  list draws a polite MC-WITNESS REFUSE line and is skipped -- nothing is
  invented.  void/invalid flags from the registered probe are echoed on the
  point line so no reader mistakes a flagged point for a clean one.

SELF-TEST (--selftest, single process, < 5 s)
  Builds a synthetic in-memory checkpoint with 5 fake zeros {2,3,5,7,11},
  x0 = 1, and verifies (explicit checks that raise in BOTH normal and -O
  modes -- no Python assert anywhere on the acceptance path):
    * b_0 reconciliation against the synthetic S_IR string (PASS required);
    * b_1 and b_2 against DIRECT INDEPENDENT arithmetic: exact rationals via
      the fractions module (t = 1/(z^2+1) exact), compared to the mpmath
      route at 1e-30 relative;
    * the refusal path: a synthetic replica without zeros_pos must be
      politely refused, not computed.
  An explicit counter of executed checks is printed; the self-test reports
  FAIL and exit code 3 if any check fails or the counter is short.

USAGE
  python mc_moments.py --selftest
  python mc_moments.py [--results-dir PATH] [--nmax 8]
  # default results dir: ./results next to this script

Honesty label: everything this script prints is VERIFIED NUMERICS (repo
tricotomy); nothing is exact or certified (the self-test's rational
reference values are exact, but they certify only the script's own
arithmetic, not any campaign quantity).  Exit codes: 0 = witness produced;
2 = polite refusal (no consumable input); 3 = self-test failure or internal
failure (reported as a witness line, never a verdict).
"""

import os
import re
import sys
import json
import time
import hashlib
import argparse
from fractions import Fraction

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# MCREG: witness constants for THIS pass.  WITNESS parameters only: they gate
# nothing, feed no judge, and the registered REG (t3_probe.py) is untouched.
# Their hash travels in the provenance header of every transcript.
# ----------------------------------------------------------------------------

MCREG = {
    "mc": "MC moment witness v1.0 2026-08-06 (gates nothing; standalone; "
          "doubling convention conv:MC-double documented in docstring)",
    "nmax_default": 8,             # moments n = 0..nmax
    "work_dps": 60,                # zeros stored at 25 digits; 60 is ample
    "recon_tol_rel": "1e-12",      # b_0 vs stored S_IR (stored at 15 sig digits)
    "anchor_tol_rel": "1e-10",     # recomputed S_Xi vs stored anchor string
    "selftest_tol_rel": "1e-30",   # mpmath route vs exact-rational route
    "print_digits": 15,
    "trend_slack_rel": "0",        # trend lines use strict non-increase
}

MCREG_HASH = hashlib.sha256(
    json.dumps(MCREG, sort_keys=True).encode("utf-8")).hexdigest()

# First 10 zeta ordinates, standard tables, ~18 digits [conv:zeros] --
# fallback benchmark when the cache is absent (honestly flagged).
HARDCODED_ZEROS = [
    "14.134725141734693790", "21.022039638771554993",
    "25.010857580145688763", "30.424876125859513210",
    "32.935061587739189690", "37.586178158825671257",
    "40.918719012147495187", "43.327073280914999519",
    "48.005150881167159727", "49.773832477672302181",
]


def wl(tag, msg):
    print(f"MC-WITNESS {tag}: {msg}", flush=True)


def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def parse_x0(tok):
    """Registered x0 strings are '1', '1/2', '2', ... -> mpf, exactly."""
    tok = str(tok).strip()
    if "/" in tok:
        a, b = tok.split("/")
        return mp.mpf(int(a)) / mp.mpf(int(b))
    return mp.mpf(tok)


# ----------------------------------------------------------------------------
# the moment map (the only mathematics this script owns)
# ----------------------------------------------------------------------------

def moments_from_positive_zeros(zeros_pos, x0, nmax):
    """b_n^(m), n = 0..nmax, per [conv:MC-double]:
    b_n = (1/(2*x0)) * 2 * sum_{z>0} t^(n+1),  t = x0/(z^2+x0).
    Written with the doubling and the prefactor EXPLICIT so the printed
    convention and the executed arithmetic cannot drift apart."""
    ts = [x0 / (z * z + x0) for z in zeros_pos]
    out = []
    for n in range(nmax + 1):
        full_trace = 2 * mp.fsum(t ** (n + 1) for t in ts)  # +-z doubled
        out.append(full_trace / (2 * x0))
    return out


def zero_side_targets(gammas, x0, nmax):
    """b_n^Xi,zero = x0^n * sum_j 1/(gamma_j^2+x0)^(n+1), truncated to the
    supplied list (truncation is the caller's, printed honestly)."""
    out = []
    for n in range(nmax + 1):
        s = mp.fsum(1 / (g * g + x0) ** (n + 1) for g in gammas)
        out.append((x0 ** n) * s)
    return out


def s_xi_anchor(x0):
    """Independent recomputation of the registered n=0 anchor:
    S_Xi(x0) = (xi'/xi)(1/2+sqrt(x0)) / (2*sqrt(x0))."""
    def xi_completed(s):
        return (s * (s - 1) / 2 * mp.pi ** (-s / 2)
                * mp.gamma(s / 2) * mp.zeta(s))
    s0 = mp.mpf(1) / 2 + mp.sqrt(x0)
    return mp.diff(xi_completed, s0) / xi_completed(s0) / (2 * mp.sqrt(x0))


# ----------------------------------------------------------------------------
# inputs (read-only)
# ----------------------------------------------------------------------------

def load_zero_bench(results_dir):
    """Returns (gammas list of mpf, source string)."""
    path = os.path.join(results_dir, "zeta_zeros_cache.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [mp.mpf(s) for s in data["gammas"]], f"cache:{path}"
    return ([mp.mpf(s) for s in HARDCODED_ZEROS],
            "hardcoded-10-anchors (cache absent)")


POINT_RE = re.compile(r"^point_L(?P<tag>[A-Za-z0-9]+)_N(?P<N>\d+)\.json$")


def discover_points(results_dir):
    pts = []
    if not os.path.isdir(results_dir):
        return pts
    for name in sorted(os.listdir(results_dir)):
        m = POINT_RE.match(name)
        if m:
            pts.append((m.group("tag"), int(m.group("N")),
                        os.path.join(results_dir, name)))
    return pts


def lam_log_from_replica(rr, tag):
    """log(lambda) from the replica's exact lambda_sq (log(lam2)/2)."""
    lam2 = rr.get("lambda_sq")
    if lam2 is None:
        # fall back to the tag: 'sqrtK' or integer K
        if tag.startswith("sqrt"):
            lam2 = int(tag[4:])
        else:
            lam2 = int(tag) ** 2
    return mp.log(mp.mpf(lam2)) / 2


# ----------------------------------------------------------------------------
# per-replica witness
# ----------------------------------------------------------------------------

def witness_replica(tag, N, mode, rr, x0_str, gammas, bench_src, nmax):
    """Returns a record for the trend table, or None on polite refusal."""
    zp = rr.get("zeros_pos")
    if not isinstance(zp, list) or len(zp) == 0:
        wl("REFUSE", f"[{tag} N={N} {mode}] checkpoint replica lacks a "
           f"non-empty zeros_pos list -- the (MC) moments are sums over "
           f"the deposited zeros and cannot be computed without them.  "
           f"Nothing was computed for this replica.")
        return None
    x0 = parse_x0(x0_str)
    zeros = [mp.mpf(s) for s in zp]
    loglam = lam_log_from_replica(rr, tag)
    T = mp.pi * N / loglam
    gam = [g for g in gammas if g <= T]
    truncated_early = bool(gammas and gammas[-1] <= T)
    flags = []
    if rr.get("void"):
        flags.append(f"void={rr['void']}")
    if rr.get("invalid"):
        flags.append(f"invalid={rr['invalid']}")
    if rr.get("count_found") is not None and rr.get("count_found") != N:
        flags.append(f"count_found={rr['count_found']}!={N}")
    pd = MCREG["print_digits"]
    wl("POINT", f"lam={tag} N={N} mode={mode} x0={x0_str} "
       f"[conv:S-half + conv:MC-double] n_zeros_m={len(zeros)} "
       f"T_window={mp.nstr(T, 12)} benchmark_zeros_used={len(gam)} "
       f"gamma_max_used={mp.nstr(gam[-1], 12) if gam else 'none'} "
       f"benchmark_src={bench_src} "
       f"benchmark_truncated_before_T={truncated_early} "
       f"(zero-side targets are TRUNCATED sums over gamma<=T: strict lower "
       f"bounds, tail positive and SHRINKING in n -- higher moments weight "
       f"low zeros more)"
       + (f"  PROBE-FLAGS: {'; '.join(flags)}" if flags else ""))

    bm = moments_from_positive_zeros(zeros, x0, nmax)
    bt = zero_side_targets(gam, x0, nmax)

    # b_0 reconciliation against the checkpoint's own S_IR (the self-check
    # the doubling convention was designed to make exact)
    sir_str = rr.get("S_IR")
    if sir_str is None:
        wl("RECON", f"[{tag} N={N} {mode}] checkpoint has no S_IR field -- "
           f"reconciliation SKIPPED (b_0 printed uncorroborated)")
        recon = "SKIPPED"
    else:
        sir = mp.mpf(sir_str)
        rel = abs(bm[0] - sir) / max(mp.mpf(1), abs(sir))
        recon = "PASS" if rel <= mp.mpf(MCREG["recon_tol_rel"]) else "FAIL"
        wl("RECON", f"[{tag} N={N} {mode}] b_0^(m)={mp.nstr(bm[0], pd)} "
           f"S_IR(checkpoint)={mp.nstr(sir, pd)} rel_diff={mp.nstr(rel, 5)} "
           f"tol={MCREG['recon_tol_rel']} => {recon}")

    # anchor route (b) for n=0 only
    anchor = s_xi_anchor(x0)
    astr = rr.get("S_Xi_anchor")
    if astr is not None:
        arel = abs(anchor - mp.mpf(astr)) / max(mp.mpf(1), abs(anchor))
        anote = (f"checkpoint_anchor={astr} rel_diff={mp.nstr(arel, 5)} "
                 f"agree={bool(arel <= mp.mpf(MCREG['anchor_tol_rel']))}")
    else:
        anote = "checkpoint carries no S_Xi_anchor field"
    wl("ANCHOR", f"[{tag} N={N} {mode}] b_0^Xi via S_Xi route = "
       f"{mp.nstr(anchor, pd)} (independent mpmath recomputation; {anote}) "
       f"-- n=0 ONLY; no closed form claimed for n>=1")

    gaps = []
    for n in range(nmax + 1):
        gap = bm[n] - bt[n]
        gaps.append(abs(gap))
        extra = f"  b_target_anchor={mp.nstr(anchor, pd)}" if n == 0 else ""
        wl("MOMENT", f"lam={tag} N={N} mode={mode} n={n} "
           f"b_n_m={mp.nstr(bm[n], pd)} "
           f"b_n_target_zero={mp.nstr(bt[n], pd)} "
           f"diff={mp.nstr(gap, 6)}{extra}")
    return {"tag": tag, "N": N, "mode": mode, "recon": recon,
            "loglam": loglam, "gaps": gaps, "bm": bm, "bt": bt}


# ----------------------------------------------------------------------------
# trend across the grid (descriptive only)
# ----------------------------------------------------------------------------

def _mono_noninc(vals):
    return all(vals[i + 1] <= vals[i] for i in range(len(vals) - 1))


def trend_lines(records, nmax):
    modes = sorted({r["mode"] for r in records})
    for mode in modes:
        rs = [r for r in records if r["mode"] == mode]
        tags = sorted({r["tag"] for r in rs},
                      key=lambda t: min(float(r["loglam"]) for r in rs
                                        if r["tag"] == t))
        sizes = sorted({r["N"] for r in rs})
        idx = {(r["tag"], r["N"]): r for r in rs}
        for n in range(nmax + 1):
            along_N, along_lam = [], []
            for tg in tags:
                seq = [(N, idx[(tg, N)]["gaps"][n]) for N in sizes
                       if (tg, N) in idx]
                if len(seq) >= 2:
                    along_N.append((tg, [s[0] for s in seq],
                                    _mono_noninc([s[1] for s in seq])))
            for N in sizes:
                seq = [(tg, idx[(tg, N)]["gaps"][n]) for tg in tags
                       if (tg, N) in idx]
                if len(seq) >= 2:
                    along_lam.append((N, [s[0] for s in seq],
                                      _mono_noninc([s[1] for s in seq])))
            if not along_N and not along_lam:
                wl("TREND", f"mode={mode} n={n}: fewer than 2 comparable "
                   f"points in every direction -- no trend statement")
                continue
            dn = ", ".join(f"lam={tg}(N={Ns}):"
                           f"{'toward' if ok else 'NOT-monotone-toward'}"
                           for (tg, Ns, ok) in along_N) or "n/a"
            dl = ", ".join(f"N={N}(lams={tgs}):"
                           f"{'toward' if ok else 'NOT-monotone-toward'}"
                           for (N, tgs, ok) in along_lam) or "n/a"
            wl("TREND", f"mode={mode} n={n} |b_n^(m)-b_n^target| "
               f"along N: {dn}; along lambda: {dl} "
               f"(descriptive; 'toward' = strictly non-increasing gap; "
               f"NOT a judge, NOT a verdict)")


# ----------------------------------------------------------------------------
# self-test (--selftest): explicit checks, no assert, normal-and-O identical
# ----------------------------------------------------------------------------

def selftest():
    t0 = time.time()
    checks_done = 0
    failures = []

    def check(name, cond, detail=""):
        nonlocal checks_done
        checks_done += 1
        if cond:
            wl("SELFTEST", f"check {checks_done} [{name}] PASS {detail}")
        else:
            failures.append(name)
            wl("SELFTEST", f"check {checks_done} [{name}] FAIL {detail}")

    with mp.workdps(MCREG["work_dps"]):
        fake = [2, 3, 5, 7, 11]
        x0 = mp.mpf(1)
        # synthetic checkpoint replica, exactly the deposited shape
        sir_exact = sum(Fraction(1, z * z + 1) for z in fake)
        rr = {
            "zeros_pos": [mp.nstr(mp.mpf(z), 25) for z in fake],
            "S_IR": mp.nstr(mp.mpf(sir_exact.numerator)
                            / sir_exact.denominator, 15),
            "lambda_sq": 4, "count_found": 5,
            "void": [], "invalid": [],
        }
        nmax = 2
        zeros = [mp.mpf(s) for s in rr["zeros_pos"]]
        bm = moments_from_positive_zeros(zeros, x0, nmax)

        # (1) b_0 reconciliation: doubled trace / (2 x0) == S_IR
        sir = mp.mpf(rr["S_IR"])
        rel0 = abs(bm[0] - sir) / abs(sir)
        check("b0-reconciliation-vs-synthetic-S_IR",
              rel0 <= mp.mpf(MCREG["recon_tol_rel"]),
              f"b_0={mp.nstr(bm[0], 15)} S_IR={rr['S_IR']} "
              f"rel={mp.nstr(rel0, 5)}")

        # (2)+(3) n=1,2 against direct INDEPENDENT arithmetic: exact
        # rationals, t = 1/(z^2+1), b_n = (1/(2*1)) * 2 * sum t^(n+1)
        for n in (1, 2):
            exact = sum(Fraction(1, (z * z + 1)) ** (n + 1) for z in fake)
            ref = mp.mpf(exact.numerator) / mp.mpf(exact.denominator)
            rel = abs(bm[n] - ref) / abs(ref)
            check(f"b{n}-vs-exact-rational",
                  rel <= mp.mpf(MCREG["selftest_tol_rel"]),
                  f"b_{n}={mp.nstr(bm[n], 20)} exact={mp.nstr(ref, 20)} "
                  f"rel={mp.nstr(rel, 5)}")

        # (4) the full witness path on the synthetic replica must PASS recon
        gammas = [mp.mpf(s) for s in HARDCODED_ZEROS]
        recrec = witness_replica("2", 5, "base", rr, "1", gammas,
                                 "selftest-hardcoded", nmax)
        check("witness-path-runs-and-recon-PASS",
              recrec is not None and recrec["recon"] == "PASS",
              f"recon={recrec['recon'] if recrec else 'None'}")

        # (5) refusal path: replica without zeros_pos must be refused
        refused = witness_replica("2", 5, "hi", {"S_IR": "0.1"}, "1",
                                  gammas, "selftest-hardcoded", nmax)
        check("refusal-on-missing-zeros-list", refused is None)

        # (6) python -O guard: the five checks above must have executed.
        # The condition is evaluated at argument time, BEFORE check() bumps
        # the counter for this line itself, so the expected value is 5.
        check("explicit-counter", checks_done == 5,
              f"prior_counter={checks_done} expected=5 "
              f"(this line itself makes the total 6)")

    ok = (not failures) and checks_done == 6
    wl("SELFTEST", f"result: {checks_done} checks executed, "
       f"{len(failures)} failed {failures if failures else ''} "
       f"wall={round(time.time() - t0, 2)}s => "
       f"{'SELF-TEST PASS' if ok else 'SELF-TEST FAIL'} "
       f"(a self-test outcome; gates nothing, feeds no judge)")
    return 0 if ok else 3


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="(MC) moment witness -- gates nothing; see docstring")
    ap.add_argument("--results-dir", default=os.path.join(HERE, "results"))
    ap.add_argument("--nmax", type=int, default=MCREG["nmax_default"])
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    prov = {
        "mc_script_sha256": sha256_of(os.path.abspath(__file__)),
        "mcreg_sha256": MCREG_HASH,
        "mpmath": mp.__version__,
        "python": sys.version.split()[0],
        "platform": sys.platform,
        "argv": vars(args),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    wl("PROVENANCE", json.dumps(prov, sort_keys=True))
    wl("STATUS", "supplemental (MC) moment witness -- READ-ONLY, GATES "
       "NOTHING; prints MC-WITNESS lines only, never a verdict; the "
       "registered verdict is whatever the registered aggregator prints "
       "[conv:S-half; conv:MC-double; verified numerics]")

    if args.selftest:
        return selftest()

    if args.nmax < 0:
        wl("REFUSE", f"--nmax {args.nmax} < 0 makes no moment sequence.  "
           f"Nothing was computed.")
        return 2

    pts = discover_points(args.results_dir)
    if not pts:
        wl("REFUSE", f"no point_L*_N*.json checkpoints found under "
           f"{args.results_dir} -- the (MC) moments are computed from the "
           f"deposited per-point zero lists and cannot run without them.  "
           f"Nothing was computed.")
        return 2

    with mp.workdps(MCREG["work_dps"]):
        gammas, bench_src = load_zero_bench(args.results_dir)
        records = []
        for (tag, N, path) in pts:
            with open(path, "r", encoding="utf-8") as f:
                rec = json.load(f)
            wl("CHECKPOINT", f"path={path} sha256={sha256_of(path)} "
               f"reg_sha256={rec.get('reg_sha256')} "
               f"replicas_present={[r for r in ('base', 'hi') if r in rec]}")
            x0_str = rec.get("x0", "1")
            got_any = False
            for mode in ("base", "hi"):
                if mode not in rec:
                    continue
                got_any = True
                r = witness_replica(tag, N, mode, rec[mode], x0_str,
                                    gammas, bench_src, args.nmax)
                if r is not None:
                    records.append(r)
            if not got_any:
                wl("REFUSE", f"[{tag} N={N}] checkpoint has neither base "
                   f"nor hi replica -- skipped, nothing computed")
        if not records:
            wl("REFUSE", "no valid replica carried a zeros_pos list; no "
               "moments were computed anywhere")
            return 2
        trend_lines(records, args.nmax)
    wl("DONE", f"{len(records)} replica(s) witnessed, n=0..{args.nmax}; "
       f"this pass gated nothing and wrote nothing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
