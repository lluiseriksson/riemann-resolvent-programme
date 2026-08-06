# A4 supplemental pass — Colab cells (run AFTER the registered grid, same runtime)

Companion to `design.md` (registered campaign), `colab_notebook.md` (registered
runbook, cells 1–9), and `a4_completeness.py` (the A4 witness instrument).
Plane: the same Colab Pro+ Linux runtime that finished the registered grid
(`/content/t3-kill-test` with `t3_probe.py` sha
`b173fec9e6dc8447f99c7e6a79abfe1eede38d418de4ee90f64eccf849d87b34`, REG
`215ba8033b77c03d…`, and a complete `results/`). If the runtime was recycled,
re-run registered cells 2–3 (upload + zero cache) first; the checkpoints resume.

## Discipline (house rules, binding — read before executing anything)

1. **Registered verdict first and verbatim.** Cell A4-1 prints the registered
   aggregator's `T3-VERDICT:` line BEFORE any A4 output exists, and that line is
   THE verdict of the campaign. Nothing in this pass can change it, and nothing
   in this pass is allowed to try: judges and REG are UNTOUCHABLE.
2. **A4 is a supplemental LABELED pass.** Its output is witness evidence only
   (`a4-*.txt`), deposited alongside the checkpoints. It gets its own
   amendment-log entry A4 in `design.md` §13 — documentation of the witness run,
   no judge/threshold/REG/grid change. Any future re-aggregation after any
   future probe amendment must carry the post-A4 label and never replaces the
   registered verdict silently.
3. **A3 precedent.** A widened/structural search can only find MORE zeros; every
   zero the witness reports is a verified root of the source's own polynomial
   `Det(D''−s) = Σ_j ξ_j Π_{i≠j}(i−s)` (Lemma 5.4 iii, degree 2N, even), built
   from the probe's own registered ξ. `mp.polyroots` has no window and no
   sampling density — completeness is structural (the adjudicator's recommended
   mitigation for open risk #2).
4. `a4_completeness.py` GATES NOTHING, writes NO checkpoint, and never prints a
   `T3-VERDICT:` line. `(3, N=40)` remains INVALID for the registered verdict
   (J2 requires both replicas) regardless of what the witness finds — correctly.

Wall-time notes are estimates, not promises. All runs single-process.

---

## Cell A4-1 — code (registered verdict, VERBATIM, before any A4 output)

```python
# The registered aggregator. Its T3-VERDICT line is THE campaign verdict.
# With the live evidence as of 2026-08-06 ((3,40) base found 39/40 => INVALID
# under J2.a), the expected line is INCONCLUSIVE with '3:40' in detail.invalid.
# Whatever it prints is reported verbatim; A4 cannot and does not alter it.
!python t3_probe.py --verdict-only 2>&1 | tee results/a4-00-registered-verdict-20260806.txt
```

Expected wall: seconds.

## Cell A4-2 — code (upload the A4 instrument + integrity)

```python
import hashlib
from google.colab import files
up = files.upload()   # upload a4_completeness.py from the desk
h = hashlib.sha256(open("a4_completeness.py", "rb").read()).hexdigest()
print("a4 sha256:", h)
# explicit check, not assert (house rule: decisions must survive -O)
if h != "2221bab35074fef2b15ee02db6ed2b3b148cc4dbef15a7de9c431e4b5b14f7c9":
    raise SystemExit("SHA MISMATCH — this is not the designed A4 witness; STOP")
h2 = hashlib.sha256(open("t3_probe.py", "rb").read()).hexdigest()
if h2 != "b173fec9e6dc8447f99c7e6a79abfe1eede38d418de4ee90f64eccf849d87b34":
    raise SystemExit("PROBE SHA MISMATCH — not the registered probe; STOP")
```

## Cell A4-3 — code (A4 witness at the flagged point, base replica settings)

```python
# (lambda=3, N=40) at the base replica's registered settings (dps 149,
# maxdeg 12). Rebuilds tau and xi with the probe's own registered functions,
# builds the exact degree-80 Lemma-5.4(iii) polynomial, finds ALL roots by
# mp.polyroots, compares against BOTH replicas' zeros_pos lists in
# results/point_L3_N40.json, prints the mechanical cause verdict for the
# scan-missed root. WITNESS lines only; gates nothing.
!python a4_completeness.py --lam 3 --N 40 --mode base --dps 149 2>&1 | tee results/a4-L3_N40-base-dps149-20260806.txt
```

Expected wall: ~20–60 min (dominated by the registered assembly+eig rebuild at
dps 149+40; the degree-80 polyroots stage itself is ~1–10 min).

**Registered expectations for this cell** (written on the desk before the cell
runs; a deviation is itself news): degree 80, 80 roots, all real to
`imag_tol_rel = 1e-15`, 40 positive / 40 negative; leading coeff = Σξ; P(0) ≠ 0;
Newton rel resid small; against the BASE scan list, 39/40 matched and exactly
ONE missed root with z ≈ 80–85 (the ~1.5e-4 S_IR deficit = the missing zero's
1/(z²+1) weight); against the HI scan list, 40/40 matched; zero spurious scan
hits in both directions. Mechanical cause verdict for the missed root: expected
in {DEDUP-MERGE, BASE-RESOLUTION, SCAN-DEFECT-OTHER with the BASE-RESOLUTION
flag}; EVEN-MULTIPLICITY expected NOT to fire (hi found the root — a genuine
multiplicity-≥2 root is invisible to any sign-change scan, hi included) and
OUT-OF-WINDOW expected NOT to fire (both replicas run the same ceiling logic).
The script decides mechanically; these expectations do not.

## Cell A4-4 — code (hi cross-check, same point)

```python
# Same point at the hi replica's registered settings (dps 209, maxdeg 14):
# confirms the polynomial root list is precision-stable and that the hi scan
# list is complete against it (expected 40/40 both directions).
!python a4_completeness.py --lam 3 --N 40 --mode hi --dps 209 2>&1 | tee results/a4-L3_N40-hi-dps209-20260806.txt
```

Expected wall: ~30–90 min (dps 209+40).

## Cell A4-5 — markdown (the OPTIONAL msamp-doubled re-scan: CLI check result)

```markdown
CLI CHECK (performed against the registered probe, sha b173fec9…, before this
pass was written): t3_probe.py's argparse exposes ONLY
  --lambdas, --sizes, --x0, --pilot, --build-zeros, --verdict-only, --force.
msamp is taken exclusively from REG["msamp_base"]/REG["msamp_hi"] inside
run_point -> run_mode; there is NO per-point msamp/dps/maxdeg override.
--force merely recomputes a checkpoint at the SAME registered settings, so it
cannot express "msamp doubled" and would only spend budget reproducing the
same 39.

CONSEQUENCE: the optional re-scan of (3, N=40) base with msamp doubled
REQUIRES an A4.1 probe amendment (a new, registered override flag, under
design.md §7.4's own clause "fix and re-register if formulas change" — a scan
parameter is a registered replica setting, so the override must be registered,
and any point recomputed under an override is a post-A4-labeled artifact that
NEVER feeds the registered verdict).

THIS PASS STOPS HERE. No probe edit is designed in this pass.
```

## Cell A4-6 — code (registered aggregator re-print — expected identical)

```python
# A4 wrote no checkpoints, so this MUST print a verdict line identical to
# cell A4-1's. It is a RE-PRINT for the zip transcript, not a re-verdict.
# Any difference between the two lines is itself news: stop and investigate
# before anything ships.
!python t3_probe.py --verdict-only 2>&1 | tee results/a4-99-registered-verdict-reprint-20260806.txt
```

## Cell A4-7 — code (results zip, now including the a4-*.txt evidence)

```python
import shutil, time
stamp = time.strftime("%Y%m%d-%H%M%S")
zipname = f"t3-kill-test-results-postA4-{stamp}"
shutil.make_archive(f"/content/{zipname}", "zip",
                    "/content/t3-kill-test/results")
from google.colab import files
files.download(f"/content/{zipname}.zip")
```

Unzip into
`C:/Users/lluis/Documents/Codex/2026-08-05/sol/outputs/t3-kill-test/results/`
on the desk and commit; the commit message quotes (i) the registered
`T3-VERDICT:` line VERBATIM from `a4-00-…`, then (ii) the A4-CAUSE line(s)
verbatim as separate labeled evidence, with hash context per the repo hash
rule. Transcripts do not exist until committed.

## Cell A4-8 — markdown (runtime closeout)

```markdown
Runtime log (owner rule 2026-08-01): record NOW, then DISCONNECT —
runtime type, open/close time, connected duration, cells executed,
compute-unit balance before/after. An idle connected runtime is a violation.
```

---

## Amendment-log entry A4 (paste into design.md §13 AFTER the cells above ran;
## documentation of the witness run ONLY — no judge/REG change)

> **A4 (2026-08-06, supplemental completeness-witness pass, POST-GRID —
> documentation of a labeled witness run; NO judge, threshold, REG, or grid
> change; `reg_sha256 = 215ba8033b77c03d…` unchanged; probe sha `b173fec9…`
> unchanged; the registered verdict was printed verbatim BEFORE any A4 output
> and is quoted below unaltered).**
>
> *Live evidence that motivated it* (Colab, 2026-08-06, probe `b173fec9…`):
> at (λ=3, N=40) the base replica found 39/40 positive zeros
> (`invalid=['count_mismatch:39!=40']` — INVALID under J2.a, correctly), the
> hi replica found 40/40; `S_IR` differs by ~1.5e-4, locating the missing
> zero's 1/(z²+1) weight at z ≈ 80–85. Discrimination available before A4:
> not even-multiplicity (hi would be equally blind), not out-of-window (same
> ceiling logic); base-resolution / coarse-dedup class.
>
> *Instrument:* `a4_completeness.py` (v1.1) sha256 =
> `2221bab35074fef2b15ee02db6ed2b3b148cc4dbef15a7de9c431e4b5b14f7c9` —
> v1.1 = adversarial-verifier fix applied BEFORE any A4 run: the
> EVEN-MULTIPLICITY / DEDUP-MERGE criteria now measure nearest-neighbour
> distances against the STORED root list, dropping the exact-0 self match
> (v1.0 recomputed `twopiL·s` at lower precision, which turned the self
> root into a fake ~1e-30 twin and would have misclassified EVERY missed
> root as EVEN-MULTIPLICITY — reproduced in a toy before the fix; an
> exactly-equal numerical twin, the true-multiplicity case, is now seen
> as distance 0 instead of being filtered out) —
> implements A3 open item (i): the Lemma 5.4 iii polynomial
> `Det(D''−s) = Σ_j ξ_j Π_{i≠j}(i−s)` (degree 2N, even, P(0)≠0) built
> integer-exactly from the probe's OWN registered ξ (assemble +
> bottom_cluster, registered settings), ALL roots via mp.polyroots (no
> window, no sampling density — structural completeness; the adjudicator's
> recommended mitigation for open risk #2). GATES NOTHING; witness lines
> only; its A4REG witness constants are hashed in every transcript's
> provenance header.
>
> *Evidence deposited:* `results/a4-00-registered-verdict-20260806.txt`
> (registered verdict, verbatim, printed first),
> `a4-L3_N40-base-dps149-20260806.txt`, `a4-L3_N40-hi-dps209-20260806.txt`,
> `a4-99-registered-verdict-reprint-20260806.txt` (verdict line re-print,
> identical — A4 wrote no checkpoints).
>
> *Registered verdict (verbatim):* `<paste the T3-VERDICT line from a4-00>`
>
> *Witness findings:* `<paste the A4-CAUSE and A4-COMPLETENESS lines verbatim>`
>
> *Status of (3, N=40):* remains INVALID for the registered verdict — J2
> requires both replicas and A4 does not and cannot amend J2. The
> msamp-doubled re-scan is NOT expressible in the registered CLI (checked:
> no per-point override exists); if pursued it is a separate A4.1 probe
> amendment with a registered override flag, its outputs labeled post-A4,
> never replacing the registered verdict.
