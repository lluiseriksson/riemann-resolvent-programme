#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
a4_completeness.py -- A4 supplemental completeness WITNESS (T3 kill-test)
=========================================================================

STATUS AND DISCIPLINE (house rules, binding)
  * This script GATES NOTHING.  It prints "A4-..." witness lines only.  It
    never writes or modifies a checkpoint, never prints a T3-VERDICT line,
    and nothing it prints may feed J1/J2/J3.  The registered verdict is
    whatever the registered aggregator (t3_probe.py --verdict-only) prints,
    verbatim, and it is printed BEFORE any A4 output in the runbook.
  * Judges and REG are UNTOUCHABLE.  This script imports the registered
    probe (t3_probe.py, same directory, sha printed in the provenance
    header) and uses ONLY its registered functions to rebuild the operator
    and the bottom eigenvector; on top it adds a structural root-finding
    WITNESS: the source polynomial of Lemma 5.4 iii (eq. 5.5),
        P(s) = sum_j xi_j * prod_{i != j} (i - s),   i, j in [-N, N],
    degree 2N, even, P(0) != 0, ALL roots by mp.polyroots -- no window and
    no sampling density, so completeness is structural.  This is the
    adjudicator's recommended mitigation for open risk #2 (design.md,
    amendment A3, open item (i)).
  * A3 precedent: a widened/structural search can only find MORE zeros,
    and every reported zero is verified against the source's own objects
    (here: roots of Det(D''-s) built from the probe's own xi, plus the
    reverse check that every scan-reported zero has a polynomial
    counterpart).
  * Output is deposited as a4-*.txt evidence (supplemental LABELED pass;
    design.md amendment-log entry A4 documents this witness run only -- no
    judge, threshold, REG, or grid change).

WHAT IT DOES, for one (lambda, N, mode/dps) point
  1. Rebuilds tau and (eps1, xi) with the probe's registered assemble()
     and bottom_cluster() at the replica's registered settings
     (maxdeg from REG per mode; dps from the registered schedule unless
     overridden on the command line for the record).
  2. Builds P(s) exactly: integer-exact product
     G(s) = prod_{i=-N..N}(s - i) and exact synthetic division
     H_j = G/(s - j) (integer remainder checked to be 0), then
     P = sum_j xi_j H_j by mpmath fsum -- H_j integer-exact; the xi_j*H_j
     products and their fsum are correctly rounded at working precision
     (dps + workdps_extra), i.e. accurate to ~10^-(dps+40) relative.
     Self-checks (witness only, never a gate):
       - leading coefficient equals sum_j xi_j (delta_N link),
       - evenness of coefficients (odd-power coefficients ~ 0 at the
         even-defect scale of xi),
       - P(0) = xi_0 * (-1)^N * (N!)^2 != 0.
  3. Computes ALL 2N roots via mp.polyroots (maxsteps and extraprec from
     the A4REG block below, generous), verifies each root real to
     tolerance, maps s -> z = (2*pi/L) * s.
  4. Compares the positive-root list against BOTH replicas' scan-found
     'zeros_pos' lists in the results JSON checkpoint (path argument),
     in both directions.
  5. For any scan-missed root prints a MECHANICAL cause verdict, priority
     order (all fired flags are printed alongside):
       EVEN-MULTIPLICITY  polynomial root cluster closer than the
                          registered eps (mult_eps_rel) => multiplicity
                          >= 2; any sign-change scan is structurally
                          blind to it;
       OUT-OF-WINDOW      root beyond that replica's scan ceiling
                          (scan_diag.zmax_newton, cross-checked against
                          this script's own Newton ceiling);
       DEDUP-MERGE        two polynomial roots within that replica's
                          EFFECTIVE dedup tolerance
                          (2*pi/L)/(4*(msamp_eff+1)),
                          msamp_eff = msamp * {1,4,16}[refine_rounds];
       BASE-RESOLUTION    root found by the polynomial AND by the hi
                          replica's scan but not by base;
       SCAN-DEFECT-OTHER  none of the above.
  6. Prints a completeness statement: 2N roots, all real to tol,
     N positive.

COST GUARD
  Reference point: degree 80 (N = 40) at dps ~150 (+40 working digits,
  + extraprec).  Durand-Kerner is ~deg^2 high-precision multiplications
  per step; the A3 adjudication measured the same route at deg 16 in
  4.6 s single-process, which scales to an estimate of ~1-10 min for the
  polyroots stage at degree 80.  The dominant cost of this script remains
  the registered assembly + eigenvector rebuild (tens of minutes at
  lambda=3, N=40).  The script politely refuses above degree 400
  (N > 200): that exceeds the registered grid and belongs to a
  bigger-budget pass with its own registration.

USAGE (Colab plane, after the registered grid is complete in results/)
  python a4_completeness.py --lam 3 --N 40 --mode base --dps 149
  python a4_completeness.py --lam 3 --N 40 --mode hi   --dps 209
  # --checkpoint defaults to the probe's own results/point_L{tag}_N{N}.json

Honesty label: everything this script prints is VERIFIED NUMERICS (repo
tricotomy); nothing is exact or certified.  Exit codes: 0 = witness
produced; 2 = polite refusal (cost guard / missing inputs); 3 = internal
failure while producing the witness (also a witness line, never a verdict).
"""

import os
import sys
import json
import time
import hashlib
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import mpmath as mp

import t3_probe as T3  # the registered probe: registered functions only

# ----------------------------------------------------------------------------
# A4REG: witness constants for THIS pass.  These are WITNESS parameters only:
# they gate nothing, they feed no judge, and REG (t3_probe.REG) is untouched.
# Their hash travels in the provenance header of every a4-*.txt transcript.
# ----------------------------------------------------------------------------

A4REG = {
    "a4": "A4 completeness witness v1.1 2026-08-06 (gates nothing; "
          "v1.1 = adversarial-verifier fix: stored-value self-match "
          "exclusion in the EVEN-MULTIPLICITY / DEDUP-MERGE criteria)",
    "max_degree": 400,             # polite refusal above this (N > 200)
    "polyroots_maxsteps": 1000,    # generous; mp.polyroots default is 50
    "polyroots_extraprec": 200,    # generous extra precision for polyroots
    "workdps_extra": 40,           # poly arithmetic at dps + this (= REG quad_extra_dps)
    "imag_tol_rel": "1e-15",       # |Im s| <= tol*max(1,|s|)  => root is real
    "match_tol_rel": "1e-6",       # |z_poly - z_scan| <= tol*max(1,z) => same zero
    "mult_eps_rel": "1e-8",        # root cluster closer than this => mult >= 2
    "even_note_rel": "1e-8",       # odd-coeff magnitude note threshold (witness)
}

A4REG_HASH = hashlib.sha256(
    json.dumps(A4REG, sort_keys=True).encode("utf-8")).hexdigest()


def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def wl(tag, msg):
    print(f"A4-{tag}: {msg}", flush=True)


# ----------------------------------------------------------------------------
# exact polynomial construction (Lemma 5.4 iii / eq. 5.5)
# ----------------------------------------------------------------------------

def poly_G_desc(N):
    """Integer descending coefficients of G(s) = prod_{i=-N..N}(s - i),
    monic, degree 2N+1.  Exact Python-int arithmetic throughout."""
    c = [1]
    for i in range(-N, N + 1):
        nxt = [0] * (len(c) + 1)
        for k, a in enumerate(c):
            nxt[k] += a
            nxt[k + 1] -= i * a
        c = nxt
    return c


def divide_out_root(desc, r):
    """Exact synthetic division of integer descending poly by (s - r).
    r must be a root; the integer remainder is checked to be exactly 0."""
    out = [desc[0]]
    for a in desc[1:-1]:
        out.append(a + r * out[-1])
    rem = desc[-1] + r * out[-1]
    if rem != 0:
        raise RuntimeError(
            f"synthetic division: nonzero remainder {rem} at root {r} "
            f"(G construction broken)")
    return out


def build_P_desc(xi, N):
    """Descending mpf coefficients of P(s) = sum_j xi_j prod_{i!=j}(i - s).
    Note prod_{i!=j}(i - s) = (-1)^(2N) prod_{i!=j}(s - i) = G(s)/(s - j),
    so each H_j := G/(s-j) is monic integer degree 2N (exact) and
    P = sum_j xi_j H_j with each product and the fsum correctly rounded
    at the caller's working precision."""
    G = poly_G_desc(N)
    Hs = [divide_out_root(G, j) for j in range(-N, N + 1)]
    deg = 2 * N
    return [mp.fsum([xi[j + N] * Hs[j + N][k] for j in range(-N, N + 1)])
            for k in range(deg + 1)]


# ----------------------------------------------------------------------------
# main witness
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="A4 completeness witness (gates nothing; see docstring)")
    ap.add_argument("--lam", required=True,
                    help="lambda tag, e.g. 3 or sqrt13 (exact lambda^2)")
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--mode", choices=["base", "hi"], default="base",
                    help="which replica's registered settings to rebuild at")
    ap.add_argument("--dps", type=int, default=None,
                    help="working dps (default: registered schedule for mode)")
    ap.add_argument("--checkpoint", default=None,
                    help="path to results/point_L{tag}_N{N}.json "
                         "(default: the probe's own results dir)")
    args = ap.parse_args()

    tag, spec = T3.parse_lambda(args.lam)
    N = args.N
    deg = 2 * N

    # ---- cost guard (polite refusal, not a judge) ----
    wl("COST", f"degree {deg} polyroots at requested precision; reference: "
       f"degree 80 at dps ~150(+{A4REG['workdps_extra']} working, "
       f"extraprec {A4REG['polyroots_extraprec']}) est. ~1-10 min "
       f"single-process (Durand-Kerner ~deg^2 mults/step; A3 adjudication "
       f"measured deg 16 in 4.6 s).  Dominant cost is the registered "
       f"assembly+eig rebuild, not polyroots.")
    if deg > A4REG["max_degree"]:
        wl("REFUSE", f"degree {deg} > {A4REG['max_degree']}: this witness "
           f"is scoped to the registered grid (N <= 200).  A larger point "
           f"needs its own registered pass with its own budget.  "
           f"Nothing was computed.")
        return 2

    if args.dps is None:
        dps = T3.dps_schedule(spec) + (
            T3.REG["dps_hi_extra"] if args.mode == "hi" else 0)
    else:
        dps = args.dps
    maxdeg = T3.REG["maxdeg_hi" if args.mode == "hi" else "maxdeg_base"]

    # ---- provenance header (every transcript carries this) ----
    prov = {
        "a4_script_sha256": sha256_of(os.path.abspath(__file__)),
        "t3_probe_path": os.path.abspath(T3.__file__),
        "t3_probe_sha256": sha256_of(T3.__file__),
        "reg_sha256": T3.REG_HASH,
        "a4reg_sha256": A4REG_HASH,
        "mpmath": mp.__version__,
        "python": sys.version.split()[0],
        "platform": sys.platform,
        "argv": vars(args),
        "dps_used": dps, "maxdeg_used": maxdeg,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    wl("PROVENANCE", json.dumps(prov, sort_keys=True))
    wl("STATUS", "supplemental witness pass -- GATES NOTHING; the "
       "registered verdict is whatever the registered aggregator prints, "
       "and it is reported verbatim, before and independently of this "
       "output [conv:S-half; verified numerics]")

    # ---- checkpoint ----
    ckpath = args.checkpoint or T3.point_path(tag, N)
    if not os.path.exists(ckpath):
        wl("REFUSE", f"checkpoint not found: {ckpath} -- the A4 witness "
           f"compares against the registered scan lists and cannot run "
           f"without them.  Nothing was computed.")
        return 2
    with open(ckpath, "r", encoding="utf-8") as f:
        rec = json.load(f)
    reg_match = (rec.get("reg_sha256") == T3.REG_HASH)
    wl("CHECKPOINT", f"path={ckpath} reg_sha256_match={reg_match} "
       f"replicas_present={[r for r in ('base', 'hi') if r in rec]}")
    if not reg_match:
        wl("WITNESS", "checkpoint reg hash differs from the loaded probe's "
           "REG -- comparison lines below are labeled UNRELIABLE")

    try:
        # ---- 1. rebuild with the probe's own registered functions ----
        t0 = time.time()
        wl("STAGE", f"assemble({tag}, N={N}, dps={dps}, maxdeg={maxdeg}) "
           f"via t3_probe.assemble [registered]")
        tau, ameta = T3.assemble(spec, N, dps, maxdeg)
        wl("STAGE", f"assembled in {ameta['assembly_seconds']}s "
           f"quad_err<={ameta['quad_err_max']}")
        eig = T3.bottom_cluster(tau, dps)
        xi = eig["xi"]
        with mp.workdps(30):
            ck = rec.get(args.mode, {})
            wl("REBUILD", f"eps1={mp.nstr(eig['eps1'], 20)} "
               f"(checkpoint {args.mode}: {ck.get('eps1')}) "
               f"even_defect={mp.nstr(eig['even_defect'], 5)} "
               f"sum_xi={mp.nstr(eig['sum_xi'], 10)} "
               f"eig_seconds={eig['seconds']}")

        lam = T3.lam_value(spec)

        # ---- 2-3. exact polynomial + all roots ----
        with mp.workdps(dps + A4REG["workdps_extra"]):
            L = 2 * mp.log(lam)
            twopiL = 2 * mp.pi / L
            tP0 = time.time()
            P = build_P_desc(xi, N)
            wl("STAGE", f"P(s) built exactly: degree {deg}, "
               f"{round(time.time() - tP0, 2)}s")

            # self-checks (witness only)
            lead = P[0]
            sum_xi = mp.fsum(xi)
            wl("SELFCHECK", f"leading coeff = {mp.nstr(lead, 15)}; "
               f"sum_j xi_j = {mp.nstr(sum_xi, 15)}; "
               f"agree_rel={mp.nstr(abs(lead - sum_xi) / max(mp.mpf(1e-300), abs(sum_xi)), 5)}")
            maxabs = max(abs(c) for c in P)
            odd_max = mp.mpf(0)
            for k, c in enumerate(P):
                if (deg - k) % 2 == 1:
                    odd_max = max(odd_max, abs(c))
            even_rel = odd_max / maxabs
            wl("SELFCHECK", f"evenness: max|odd-power coeff|/max|coeff| = "
               f"{mp.nstr(even_rel, 5)} "
               f"({'ok at xi even-defect scale' if even_rel <= mp.mpf(A4REG['even_note_rel']) else 'NOTE: above witness threshold ' + A4REG['even_note_rel']})")
            P0 = P[-1]
            P0_pred = xi[N] * ((-1) ** N) * (mp.factorial(N) ** 2)
            wl("SELFCHECK", f"P(0) = {mp.nstr(P0, 15)}; predicted "
               f"xi_0*(-1)^N*(N!)^2 = {mp.nstr(P0_pred, 15)}; "
               f"nonzero={bool(P0 != 0)}")

            tR0 = time.time()
            roots, rerr = mp.polyroots(
                P, maxsteps=A4REG["polyroots_maxsteps"],
                extraprec=A4REG["polyroots_extraprec"], error=True)
            wl("STAGE", f"polyroots: {len(roots)} roots in "
               f"{round(time.time() - tR0, 2)}s, error estimate "
               f"{mp.nstr(mp.mpf(rerr), 5)}")

            # reality + split
            imag_tol = mp.mpf(A4REG["imag_tol_rel"])
            s_real, n_complex = [], 0
            for r0 in roots:
                re_, im_ = mp.re(r0), mp.im(r0)
                if abs(im_) <= imag_tol * max(mp.mpf(1), abs(r0)):
                    s_real.append(re_)
                else:
                    n_complex += 1
                    wl("REALITY-NOTE", f"root {mp.nstr(r0, 25)} has "
                       f"|Im|>{A4REG['imag_tol_rel']}*scale -- counted via "
                       f"its real part but FLAGGED (a genuinely complex "
                       f"root would contradict Thm 5.10 iii)")
                    s_real.append(re_)
            s_real.sort()
            s_pos = [s for s in s_real if s > 0]
            s_neg = [s for s in s_real if s < 0]
            z_pos = sorted(twopiL * s for s in s_pos)
            # STORED z-mapped list of ALL real roots, built at THIS precision:
            # the cause taxonomy below must compare z against these stored
            # values, never recompute twopiL*s at a lower workdps (a recomputed
            # product rounds differently and turns the self root into a fake
            # ~1e-30 twin -- measured; that would fire EVEN-MULTIPLICITY on
            # every missed root).
            z_all = [twopiL * s for s in s_real]

            # Newton cross-check (registered helper, witness only)
            ssq_newton = T3.newton_root_sum_sq(xi, N)
            ssq_roots = mp.fsum([s * s for s in s_real])
            newton_rel = abs(ssq_roots - ssq_newton) / max(mp.mpf(1),
                                                           abs(ssq_newton))
            zmax_own = twopiL * mp.sqrt(ssq_newton) if ssq_newton > 0 \
                else twopiL * (N + 1)
            if zmax_own < twopiL * (N + 1):
                zmax_own = twopiL * (N + 1)

        # ---- print the full positive list (the witness record) ----
        with mp.workdps(30):
            wl("ROOTS", f"positive polynomial roots z=(2pi/L)s, "
               f"{len(z_pos)} of expected {N}:")
            for k, z in enumerate(z_pos):
                print(f"  a4_z[{k + 1:3d}] = {mp.nstr(z, 25)}", flush=True)
            wl("NEWTON", f"sum s^2 from roots = {mp.nstr(ssq_roots, 15)}; "
               f"Newton identity = {mp.nstr(ssq_newton, 15)}; "
               f"rel resid = {mp.nstr(newton_rel, 5)}; own ceiling "
               f"Z_max = {mp.nstr(zmax_own, 12)}")

            # ---- 4-5. compare against BOTH replicas' scan lists ----
            match_tol = mp.mpf(A4REG["match_tol_rel"])
            mult_eps = mp.mpf(A4REG["mult_eps_rel"])
            factors = [1] + list(T3.REG["scan_refine_factors"])  # [1,4,16]

            scan = {}
            for r in ("base", "hi"):
                if r not in rec:
                    continue
                rr = rec[r]
                ws = [mp.mpf(s) for s in rr["zeros_pos"]]
                rounds = int(rr.get("refine_rounds", 0))
                eff = int(rr["msamp"]) * factors[min(rounds,
                                                     len(factors) - 1)]
                dtol = twopiL / (4 * (eff + 1))
                zmax_r = zmax_own
                sd = rr.get("scan_diag", {})
                if "zmax_newton" in sd:
                    zmax_r = mp.mpf(sd["zmax_newton"])
                scan[r] = {"ws": ws, "dedup_tol": dtol, "zmax": zmax_r,
                           "msamp": rr["msamp"], "rounds": rounds,
                           "eff": eff}
                wl("SCANLIST", f"[{r}] {len(ws)} zeros; msamp={rr['msamp']} "
                   f"refine_rounds={rounds} msamp_eff={eff} "
                   f"dedup_tol={mp.nstr(dtol, 8)} "
                   f"zmax={mp.nstr(zmax_r, 12)}")

            def nearest(z, ws):
                best_d, best_w = None, None
                for w in ws:
                    d = abs(z - w)
                    if best_d is None or d < best_d:
                        best_d, best_w = d, w
                return best_d, best_w

            def matched(z, ws):
                d, w = nearest(z, ws)
                return (d is not None
                        and d <= match_tol * max(mp.mpf(1), abs(z))), d, w

            for r, S in scan.items():
                missed = []
                nmatch = 0
                for z in z_pos:
                    ok, d, w = matched(z, S["ws"])
                    if ok:
                        nmatch += 1
                    else:
                        missed.append((z, d, w))
                wl("COMPARE", f"[{r}] matched {nmatch}/{len(z_pos)} "
                   f"polynomial positive roots in the scan list "
                   f"({len(S['ws'])} scan entries)")
                # reverse direction (A3 precedent: every reported zero must
                # be a root of the source's own objects)
                spur = 0
                for w in S["ws"]:
                    ok, d, z = matched(w, z_pos)
                    if not ok:
                        spur += 1
                        wl("WITNESS", f"[{r}] SPURIOUS-SCAN-HIT: scan zero "
                           f"{mp.nstr(w, 25)} has no polynomial "
                           f"counterpart (nearest root "
                           f"{mp.nstr(z, 25) if z is not None else 'none'}, "
                           f"dist {mp.nstr(d, 5) if d is not None else '-'})")
                if spur == 0:
                    wl("COMPARE", f"[{r}] reverse check: every scan zero "
                       f"has a polynomial counterpart (0 spurious)")

                for (z, d, w) in missed:
                    flags = []
                    # EVEN-MULTIPLICITY: cluster among ALL real roots.
                    # Distances against the STORED z_all (same precision as z,
                    # so the self match is EXACTLY 0 and is dropped as the
                    # single smallest entry); an exactly-equal numerical twin
                    # (true multiplicity) then still shows up as dall[1] = 0.
                    dall = sorted(abs(z - z2) for z2 in z_all)
                    zclu = dall[1] if len(dall) > 1 else None
                    if zclu is not None and \
                            zclu <= mult_eps * max(mp.mpf(1), abs(z)):
                        flags.append("EVEN-MULTIPLICITY")
                    # OUT-OF-WINDOW
                    if z > S["zmax"]:
                        flags.append("OUT-OF-WINDOW")
                    # DEDUP-MERGE: another positive root within dedup tol
                    # (same drop-the-self-0 rule: filtering by `z2 != z` would
                    # also skip an exactly-equal twin, blinding this flag to
                    # the very case it exists for)
                    dpos = sorted(abs(z - z2) for z2 in z_pos)
                    dnn = dpos[1] if len(dpos) > 1 else None
                    if dnn is not None and dnn <= S["dedup_tol"]:
                        flags.append("DEDUP-MERGE")
                    # BASE-RESOLUTION: hi's scan found it, base's did not
                    if r == "base" and "hi" in scan:
                        okh, dh, wh = matched(z, scan["hi"]["ws"])
                        if okh:
                            flags.append("BASE-RESOLUTION")
                    primary = "SCAN-DEFECT-OTHER"
                    for cand in ("EVEN-MULTIPLICITY", "OUT-OF-WINDOW",
                                 "DEDUP-MERGE", "BASE-RESOLUTION"):
                        if cand in flags:
                            primary = cand
                            break
                    wl("CAUSE", f"[{r}] missed root z={mp.nstr(z, 25)} "
                       f"(nearest scan hit {mp.nstr(w, 25) if w is not None else 'none'} "
                       f"at dist {mp.nstr(d, 5) if d is not None else '-'}; "
                       f"nearest other poly root at "
                       f"{mp.nstr(dnn, 5) if dnn is not None else '-'}) "
                       f"=> {primary}  flags={flags or ['none']}")

            # ---- 6. completeness statement ----
            ok_struct = (len(roots) == deg and n_complex == 0
                         and len(s_pos) == N and len(s_neg) == N)
            wl("COMPLETENESS", f"[{tag} N={N} {args.mode} dps={dps}] "
               f"degree {deg}; {len(roots)} roots; "
               f"{len(roots) - n_complex} real to imag_tol_rel="
               f"{A4REG['imag_tol_rel']}; {len(s_pos)} positive / "
               f"{len(s_neg)} negative; P(0) nonzero; polyroots err "
               f"{mp.nstr(mp.mpf(rerr), 5)}; Newton rel resid "
               f"{mp.nstr(newton_rel, 5)}  => "
               + ("STRUCTURAL COMPLETENESS WITNESS OK: 2N real roots, "
                  "N positive (Lemma 5.4 iii + Thm 5.10 iii as expected)"
                  if ok_struct else
                  "STRUCTURAL DEFECT WITNESSED (see lines above) -- this "
                  "is news about the point, still not a gate"))
        wl("DONE", f"total wall {round(time.time() - t0, 1)}s; this pass "
           f"gated nothing and wrote no checkpoint; deposit this transcript "
           f"as a4-*.txt evidence")
        return 0
    except Exception as e:  # witness failure is reported, never silently
        wl("FAILURE", f"internal failure while producing the witness: "
           f"{type(e).__name__}: {e} -- no witness claim is made; the "
           f"registered verdict is unaffected")
        return 3


if __name__ == "__main__":
    sys.exit(main())
