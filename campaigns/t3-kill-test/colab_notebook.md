# T3 kill-test — Colab notebook (cell-by-cell)

Companion to `design.md` (pre-registered campaign) and `t3_probe.py`
(self-contained probe; **no repo clone needed**). Plane: Colab Pro+ Linux,
CPU/high-RAM default runtime (no GPU — this is not a numerical campaign that
justifies one). Owner rule discipline: one runtime per thread, never shared;
record runtime open/close, type, and connected time in the thread log;
disconnect when the execution unit finishes; prepare everything below while
disconnected.

Script integrity: `t3_probe.py` sha256 =
`b173fec9e6dc8447f99c7e6a79abfe1eede38d418de4ee90f64eccf849d87b34`
(cell 2 verifies; a mismatch means the registered probe is not what you are
about to run — stop). This hash supersedes `b3ab8b20…` after the PRE-RUN
scan-domain repair of 2026-08-06 (design.md Amendment A3: the count gate's
expectation N is CORRECT and unchanged — `dim E'_N = 2N`, `D''` selfadjoint,
`Det(D''−s)` even and nonvanishing at 0 — but the scan searched only the pole
hull, and two of the N positive eigenvalues provably lie above `p_{N+1}`;
`positive_zeros` now scans two regimes under an exact Newton ceiling).
`b3ab8b20…` in turn superseded `125bef5d…` after the PRE-RUN formula repair of
the same day (Amendment A2: γ_L(n) double-counted c(L); the ST2b reference
carried a spurious global minus), and `125bef5d…` superseded the
pre-verification value `0a912031…` (x0 registration gate in `judge_point`). The
REG block was not touched in any of these edits, so
`reg = 215ba8033b77c03d…` is unchanged throughout.

Wall-time notes are ESTIMATES pending the cell-4 smoke calibration; they are
scheduling aids, not promises. All runs are single-process (the script pins
BLAS to 1 thread itself).

---

## Cell 1 — markdown (header)

```markdown
# T3 kill-test probe — CCM operators D_log^{(lambda,N)} (arXiv:2511.22755)
Registered design: design.md v1.0 2026-08-05. Judges J1/J2/J3 frozen before
any run. Conventions: [conv:S-half], x0 = 1. This notebook only executes the
registered grid; it decides nothing — the verdict line is mechanical.
```

## Cell 2 — code (setup, upload, integrity)

```python
# mpmath and numpy ship with Colab; pin-check versions, upload the probe.
import sys, subprocess, hashlib, os
subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                "mpmath>=1.3.0"], check=True)
import mpmath, numpy
print("mpmath", mpmath.__version__, "| numpy", numpy.__version__,
      "| python", sys.version.split()[0])

os.makedirs("/content/t3-kill-test", exist_ok=True)
os.chdir("/content/t3-kill-test")
from google.colab import files
up = files.upload()   # upload t3_probe.py from the desk
h = hashlib.sha256(open("t3_probe.py", "rb").read()).hexdigest()
print("sha256:", h)
# explicit check, not assert (house rule: acceptance decisions must survive -O)
if h != "b173fec9e6dc8447f99c7e6a79abfe1eede38d418de4ee90f64eccf849d87b34":
    raise SystemExit("SHA MISMATCH — this is not the registered probe; STOP")
```

Expected wall: < 1 min.

## Cell 3 — code (zeta zero cache, once per runtime lineage)

```python
# Zero-side benchmark data [conv:zeros]: ordinates to T_max = 543.9 (+ margin).
# Largest window on the grid: T(lambda=2, N=120) = 120*pi/log(2) = 543.9.
!python t3_probe.py --build-zeros 560
```

Expected wall: ~10–25 min (mpmath.zetazero to k ≈ 305 at dps 30). The cache
lands in `results/zeta_zeros_cache.json`; if you split the grid across two
runtimes, run this cell in BOTH (or copy the JSON), it is deterministic.

## Cell 4 — code (pilot-scale smoke = self-test gates + calibration)

```python
# ST1/ST2 assembly gates + two tiny points (lambda=2, N=6,8; dps 60/90).
# HALT the campaign if any ST gate prints FAIL (design.md section 7.4).
!python t3_probe.py --pilot
```

**Registered predictions for this cell after Amendment A3** (made on the desk
before this probe ran on the plane; a deviation is itself news): all five ST
gates PASS unchanged; both points return `invalid=[]` with `count_found` = 6
and 8 respectively and `refine_rounds = 0`; `scan_diag.V_consistent = true`
with V = 3 (N=6) and V = 5 (N=8); `S_IR = 0.010505643138843` (N=6) and
`0.011964124720552` (N=8) at x0 = 1 [conv:S-half]; `n_spur = 0` and
`S_low = 0` at both, unchanged from the A2 pilot.

Expected wall: ~1–5 min on Colab. This cell is also the calibration anchor:
scale its per-stage timings (assembly / eig / scan printed per point) by
(dim/17)^3 and the dps ratio to sanity-check the estimates below before
committing runtime hours. NOTE: the same `--pilot` invocation is the
local-light candidate for the Windows desk — but under the owner rule it must
be MEASURED there (< 30 s wall, single process, < 512 MiB peak RSS) before
being treated as local-light; until measured, it runs here.

## Cell 5 — code (production, lambda = 2 and sqrt8)

```python
# Grid columns lambda in {2, sqrt8}, all N in {20,40,80,120}, both J2 replicas.
# Checkpoints are resume-safe: re-running skips completed points.
!python t3_probe.py --lambdas 2,sqrt8 --sizes 20,40,80,120
```

Expected wall: ~2–6 h total (dps 93/153 and 138/198; N=120 dominates).

## Cell 6 — code (production, lambda = 3 and sqrt13)

```python
# The published-anchor columns (CCM ran lambda=3 and sqrt13 at N=120).
!python t3_probe.py --lambdas 3,sqrt13 --sizes 20,40,80,120
```

Expected wall: ~6–18 h total (dps 149/209 and 195/255; the sqrt13, N=120
replicas are the heaviest points, ~1.5–3 h each pair).

**Parallelization (budget permitting):** cells 5 and 6 may run in two SEPARATE
thread-owned runtimes (each with cells 1–3 executed first). Never share a
runtime between threads; serialize only for compute-unit budget, never for a
fictitious one-session limit; if Colab rejects a runtime, record the literal
message and distinguish session-limit from exhausted units. If a runtime is
recycled mid-column, re-upload, re-run cell 3, and re-run the same command —
checkpointing resumes.

## Cell 7 — code (aggregate + machine-readable verdict)

```python
# Prints the J1 table and exactly one T3-VERDICT line (J3). INCONCLUSIVE
# unless the registered 4x4 grid is complete with all J2 gates passed.
!python t3_probe.py --verdict-only
```

Expected wall: seconds. The verdict line format (design.md section 8):
`T3-VERDICT: {KILL|SURVIVE-AT-PROBED-SCALES|AMBIGUOUS|INCONCLUSIVE} conv=S-half;x0=1;grid=L{2,sqrt8,3,sqrt13}xN{20,40,80,120} detail={...}`

## Cell 8 — code (download results back to the desk)

```python
# Bring EVERYTHING home: per-point JSON checkpoints (the audit artifacts),
# the zero cache, and a run log. Transcripts do not exist until committed.
import shutil, time
stamp = time.strftime("%Y%m%d-%H%M%S")
zipname = f"t3-kill-test-results-{stamp}"
shutil.make_archive(f"/content/{zipname}", "zip",
                    "/content/t3-kill-test/results")
from google.colab import files
files.download(f"/content/{zipname}.zip")
```

Instruction: unzip into
`C:/Users/lluis/Documents/Codex/2026-08-05/sol/outputs/t3-kill-test/results/`
on the desk, commit alongside `design.md` + `t3_probe.py` (verdict line quoted
in the commit message with its hash context per the repo hash rule), and only
then treat the run as existing.

## Cell 9 — markdown (runtime closeout)

```markdown
Runtime log (owner rule 2026-08-01): record NOW, then DISCONNECT this runtime —
* runtime type (CPU/high-RAM), open time, close time, connected duration;
* which cells executed (grid columns owned by this runtime);
* compute-unit balance observed before/after (needed before authorizing >2
  concurrent sessions on any future round).
An idle connected runtime is a violation, not a convenience.
```
