# T3 kill-test — pre-registered campaign design

Version: 1.0 (2026-08-05). Status: **REGISTERED BEFORE ANY RUN.** No matrix of the
target family has been assembled and no spectrum computed at the time this file is
written. Every judge constant below is frozen here; any change after full-grid data
exists constitutes a NEW registration and voids any kill/survive verdict computed
under the old one. Designer: Claude Fable 5 (this session). Inputs: (a) source
extraction of arXiv:2511.22755 (CCM "Zeta Spectral Triples"); (b) source extraction
of the prolate/Sonin line (arXiv:2112.05500, PNAS 2022 via PMC, arXiv:2310.18423);
(c) repo T3 specification extract (riemann-resolvent-programme /
riemann-prime-resolvent); (d) charter = `barrido-idea-genuina-18-repos.md`,
"Recomendación operativa" item 1: *the T3 kill-test first; days-scale Colab
campaign; implement the published CCM operators and measure the sup of the
resolvent trace at one point over (λ,N); it is THE kill switch the repo itself
declares and nobody has run it.*

Companion script: `t3_probe.py` (same directory). Results: `results/` (JSON
checkpoints). Colab runbook: `colab_notebook.md`.

Convention discipline: every number in this file travels with its convention.
Global conventions used throughout:

* **[conv:CCM]** — arXiv:2511.22755 conventions: Fourier duality
  `F(s) = ∫ f(u) u^{-is} d*u` on `R*_+`, `d*u = du/u`; interval `[λ^{-1}, λ]`;
  `L = 2 log λ`; convolution = unnormalized Lebesgue after `x = log u`; von
  Mangoldt sum over ALL prime powers `1 < n ≤ λ²`; θ = Riemann–Siegel angular
  function with principal `log Γ` branch; spectral cut `(-1)^{-z} := e^{-iπz}`.
* **[conv:S-half]** — the repo's operational trace convention
  (spectral-construction.md / 06-positive-approximants.md / FiniteStieltjes.lean):
  `S_{λ,N}(x) = (1/2) Tr((D_{λ,N}² + xI)^{-1}) = Σ_{z_k>0} 1/(z_k² + x)` over the
  paired ±z finite spectrum. All headline numbers here are in S-half. The prose T3
  writes `Tr` (no 1/2); the factor 2 is harmless for boundedness and is carried
  explicitly wherever both appear.
* **[conv:zeros]** — ζ ordinates: `γ_j` with `ζ(1/2 + iγ_j) = 0`, `γ_1 =
  14.134725…` (known zero data, "verified" label; sourced from mpmath.zetazero at
  dps 30 plus 10 hardcoded anchors, never from this probe).
* Tricotomy labels: everything this campaign produces is **verified numerics**.
  Nothing here is "exact" or "certified". The judges are designed so that the
  verdict is robust to that label.

---

## 1. The target statement (what is being probed)

Quoted from the repo extraction (three layers, NOT identical in strength):

1. **Prose (canonical kill switch)** — riemann-resolvent-programme
   `HYPOTHESIS_FRONTIER.md:35-38`: *"T3 (uniform low-energy bound) — KILL SWITCH.
   `sup_{λ,N} Tr (D_{λ,N}² + x₀ I)⁻¹ < ∞`. If spectral mass accumulates at low
   energy, criterion C is empty and the operator route dies; the abstract core
   survives, the programme's concrete arm does not."*
2. **Lean** — `Program.lean:79-81`: `uniform_bound : ∃ C, ∀ j, S j x₀ ≤ C` with
   `S j x = (1/2) Tr(D j² + xI)⁻¹` abstracted to a real function family over a
   single index `j`.
3. **Operational** — `spectral-construction.md:3-8`: *"For a concrete finite or
   Galerkin operator `D_{λ,N}`, define `S_{λ,N}(x) = (1/2) Tr (D_{λ,N}² +
   xI)⁻¹."*

`D_{λ,N}` is identified by the repo (SOURCES.md gate V4) as *"the
Connes–Consani–Moscovici operators `D_log^{(λ,N)}`"* of arXiv:2511.22755. Neither
repo defines the operator concretely anywhere (verified in the extraction); the
repos' own rule (V4) requires extraction from the source paper with exact equation
numbers. That extraction is input (a) and is what Section 3 instantiates.

The repo declares **no numeric threshold** for "T3 looks dead": the kill criterion
is qualitative (boundedness). Therefore the quantitative kill rule in Section 8 is
a **NEW registration made by this campaign**, not a repo-derived criterion — the
repo spec extract explicitly demands this labeling.

A caveat carried from the extraction: the literal quantifier text of T3's satellite
atom (`riemann-prime-resolvent` `three_step_triangle` / `riemann.error_budget`)
was re-read only through the repo-spec extraction, whose prose statement (layer 1)
is treated as canonical here. If the satellite text diverges, this design binds to
layer 1 + layer 3.

## 2. Fidelity analysis, including a vacuity trap in the literal reading

### 2.1 The literal whole-operator sup is trivially infinite (pen-and-paper note)

The full operator `D_log^{(λ,N)}` acts on all of `L²([λ^{-1},λ], d*u)` and its
spectrum contains the unperturbed lattice `{2πj/L : |j| > N}` (Thm 5.10 of the
source). Hence, in [conv:S-half],

    S_full ≥ Σ_{j>N} 1/((2πj/L)² + x₀).

For `j ≤ L√x₀/(2π)` each term is ≥ 1/(2x₀), and the number of such j exceeding N
grows like `L√x₀/(2π) − N → ∞` as `λ → ∞` at **fixed** N (L = 2 log λ). So
`sup_{λ,N} S_full = +∞` **unconditionally**, driven purely by the unperturbed UV
lattice thickening with λ — a property of the free periodic Dirac operator, with
no arithmetic content and nothing to do with "spectral mass accumulating at low
energy". A "kill" read off this literal quantifier would be vacuous: it would
kill every operator family on a growing interval.

**Consequence (registered reading).** The probe targets the repo's OWN operational
layer (layer 3): `S_{λ,N}(x₀) = (1/2)Tr((D''² + x₀)⁻¹)` where `D''` is the
**finite** (2N-dimensional, infrared) part of `D_log^{(λ,N)}` — the compressed
operator on `E'_N` whose 2N real eigenvalues are what the source compares to zeta
zeros. This matches "concrete finite or Galerkin operator" verbatim. The exact UV
lattice tail `Σ_{j>N} 1/((2πj/L)²+x₀)` is computed in closed form and **reported
separately** at every grid point (it is exactly known, it is not evidence about
the arm, and folding it in would manufacture the vacuous kill above). The kill
rule (Section 8) is keyed, exactly as the prose gloss demands, to **low-energy
accumulation** in the finite spectrum.

This finding is itself a deliverable: the repo's prose T3, read with the sup over
the two-parameter family and the trace over the full operator, is vacuously false
for the CCM family for free-Dirac reasons. The defensible T3 is the operative
low-energy reading probed here. (Also: under RH plus the numerically observed
spectral matching, the natural finite benchmark `Σ_j 1/(γ_j²+x₀) = S_Ξ(x₀) < ∞`
is what boundedness would look like; Section 6.)

### 2.2 Is this instantiation faithful or a proxy?

Per extraction (a), `D_log^{(λ,N)}` **is reproducible from the paper alone**
("moderate transcription risk and mandatory very-high-precision arithmetic"); all
matrix entries are exact special-function/elementary expressions, no mesh exists.
So this campaign implements the **operator itself, not a proxy** — with the
underspecification choices and risk ledger of Section 3.4 and the compromises
ledger of Section 11. The one place fidelity is *chosen* rather than forced is the
registered reading of Section 2.1 (finite/IR trace), which follows the repo's own
operational definition.

The prolate/Sonin line (input (b)) is **context only**: T3 names `D_log^{(λ,N)}`,
not `W_sa`. No prolate operator is implemented here. (Had the CCM operator been
unimplementable, the prolate Route B would have been the fallback proxy; it is not
needed.)

## 3. The operator, exactly as implemented

All equation numbers are arXiv:2511.22755 [conv:CCM].

### 3.1 The truncated Weil matrix `QW_λ^N`

`(2N+1)×(2N+1)` real symmetric matrix `τ_{nm} = QW_λ(V_n, V_m)`, indices
`n,m ∈ {-N,…,N}`, `V_n` the orthonormal exponential eigenbasis (eqs. 2.6/3.21),
`L = 2 log λ`. Assembly `τ = W02 − WR − Wp` (Ψ = W_{0,2} − W_R − Σ_p W_p,
eq. 3.10):

* **Pole block** (Lemma 4.1, eq. 4.2), closed form as printed:
  `W02(n,m) = 32 L sinh²(L/4) (L² − 16π²mn) / ((L²+16π²m²)(L²+16π²n²))`.
* **Prime block** (eq. 4.3 + Lemma 2.3): with `y = log k`,
  `Wp(n,m) = Σ_{1<k≤λ²} Λ(k) k^{-1/2} q_{nm}(y)`, sum over ALL prime powers
  (λ = √13 ⇒ k ∈ {2,3,4,5,7,8,9,11,13}); `q_{nn}(y) = 2(1−y/L)cos(2πny/L)`;
  `q_{nm}(y) = [sin(2πmy/L) − sin(2πny/L)]/(π(n−m))` for `n≠m`. Exact
  elementary evaluation; the prime cutoff is **slaved to λ** (`x = λ²`), so the
  λ-grid must consist of values with exact integer λ² (Section 5).
* **Archimedean block** (Prop. 4.3): `WR(n,m) = (α_L(m) − α_L(n))/(n−m)` for
  `n≠m`; `WR(n,n) = 2γ_L(n) − 2β_L(n)`; with `ρ(x) = e^{x/2}/(e^x − e^{-x})`,
  `α_L(n) = (1/π)∫₀^L sin(2πnx/L)ρ(x)dx`,
  `β_L(n) = (1/L)∫₀^L x cos(2πnx/L)ρ(x)dx`,
  `γ_L(n) = ∫₀^L (cos(2πnx/L) − 1)ρ(x)dx + c(L)+w(L)`
  (equivalently `∫₀^L (cos(2πnx/L) − e^{-x/2})ρ(x)dx + w(L)`; eq. (4.14) as
  PRINTED carries the `e^{-x/2}` subtraction *and* `+c(L)`, which double-counts
  `c(L)` by (4.11) — see amendment A2),
  `c(L)+w(L) = ½log((e^{L/2}−1)/(e^{L/2}+1)) + arctan(e^{L/2}) − π/4 + γ_E/2 +
  ½log(8π)`. Parities used: α odd in n, β and γ even in n.

**Registered implementation choice:** the archimedean entries are computed by
**direct high-precision quadrature of these defining integrals**, NOT by the
paper's 2F1/digamma/trigamma/Hurwitz-Lerch closed forms (Prop. 4.2). Rationale
(from the extraction's own risk analysis): the closed forms carry many silent
sign/branch conventions and are the single highest transcription risk; the
defining integrals are more primary and the extraction itself names direct
quadrature as "the natural independent check … which is cheap". The transcription
surface that remains is the integral definitions above plus `c(L)+w(L)`; it is
covered by self-test ST2 (Section 7.4), which checks the assembled `WR` diagonal
against the **independent** spectral representation of the archimedean term
(eq. 3.19: `−W_R(f,f) = ∫_R |f̂(t)|² θ'(t)/π dt`, `θ'(t) = −½log π +
½Re ψ(¼+it/2)`), a formula sharing no code path and no special function with the
ρ-integrals.

### 3.2 The perturbed operator and its finite spectrum

Per Thm 1.1/5.10 (CONDITIONAL on the bottom eigenvalue of `QW_λ^N` being simple
with even eigenvector — checked per point, Section 7.2):

* `ε_N` = smallest (algebraic) eigenvalue of `τ`, `ξ` its eigenvector.
* `D_log^{(λ,N)} = D_log^{(λ)} − |D_log^{(λ)}ξ⟩⟨δ_N|` with the coupling rigidly
  fixed by `δ_N(ξ) = L^{-1/2} Σ_j ξ_j = 1`. **No free coupling constant exists.**
* Spectrum (Prop. 5.9 / Thm 5.10 iii): real zeros of the entire function
  `ξ̂(z) = 2L^{-1/2} sin(zL/2) Σ_{|j|≤N} ξ_j/(z − 2πj/L)`; equal to
  `{2πj/L : |j|>N}` (UV lattice) ∪ {2N real IR eigenvalues of the compressed
  `D''` on `E'_N`}.

**Registered spectral route:** the IR spectrum is computed as the real zeros of
`ξ̂` (the source's own explicit formula), via the pole-stable term-wise identity
`sin(zL/2)/(z−p_j) = (−1)^j sin((z−p_j)L/2)/(z−p_j)`, `p_j = 2πj/L`. Zeros of
`ξ̂` are invariant under scaling of ξ, so the δ_N-normalization is **not needed**
for the spectrum (only its non-degeneracy `Σξ_j ≠ 0` is checked — if
`Σξ_j ≈ 0` the normalization `δ_N(ξ)=1` is impossible and the perturbation is
undefined: the point is VOID). Since ξ is even (checked), `ξ̂` is even; only the
N positive zeros are scanned and the spectrum is the symmetric closure — which is
exactly the paired ±γ structure that [conv:S-half] counts once.

### 3.3 The probed observable

Per grid point `(λ, N)` and `x₀`:

* `S_IR(λ,N;x₀) = Σ_{k=1..N} 1/(z_k² + x₀)` over the positive IR zeros
  [conv:S-half] — **the probe's instantiation of the repo's `S_{λ,N}(x₀)`**.
* `S_tail(λ,N;x₀) = Σ_{j>N} 1/((2πj/L)² + x₀)` in closed form
  (`Σ_{j≥1} 1/(j²+a²) = (π/2a)coth(πa) − 1/(2a²)`, `a = L√x₀/2π`) — reported
  separately per Section 2.1.
* Low-energy diagnostics: `n_spur = #{k : z_k ≤ t_c}` and
  `S_low = Σ_{z_k ≤ t_c} 1/(z_k²+x₀)` with **t_c = 10** (registered; the first
  zeta ordinate is γ₁ = 14.13…, so the band (0, 10] contains no zero-side mass
  at all — anything there is exactly the "spectral mass at low energy" T3 fears).

### 3.4 Underspecification choices and risks (everything the sources leave open)

| # | Choice | Registered resolution | Risk |
|---|---|---|---|
| U1 | Archimedean entries: closed forms vs defining integrals | Defining integrals by quadrature | Quadrature error (guarded: dual settings, J2; ST2 cross-representation check) |
| U2 | "smallest eigenvalue" if a negative eigenvalue of large modulus exists | ε_N = smallest **algebraic** eigenvalue; located by float64 pre-scan + high-precision inverse-iteration cluster refinement (Section 4.2) | Misidentification if float64 blind; mitigated by cluster block + refinement of any float64-visible negative |
| U3 | Eigenvalue↔zero pairing (unpublished in source) | **Not needed**: judges compare traces (sums), never paired differences; informational nearest-pairing printed only in pilot ST3 | none for verdict |
| U4 | Whole-operator vs finite trace | Finite `D''` trace per repo layer 3; UV tail reported separately; literal-sup vacuity documented (2.1) | A reader wanting the literal prose sup gets it: it is +∞, proven above, no computation needed |
| U5 | x₀ | x₀ = 1 (repo precedent: the only prior numerical run, Hausdorff falsifier, used x₀ = 1; Lean requires only x₀ > 0). Secondary displays x₀ ∈ {1/2, 2} (free: same spectrum) | none |
| U6 | (λ,N) enumeration to Lean's single j | Never diagonalized: 2-D grid, both directions reported independently (repo two-parameter caution, HYPOTHESIS_FRONTIER.md:45-50) | none |
| U7 | Even-simplicity (assumed by source Thm 5.10) | Checked per point; failure ⇒ point VOID (outside the theorem: the operator is not the theorem's object there). VOID is itself reportable news but never a kill | Conflating hypothesis-failure with T3-failure — excluded by construction |
| U8 | Precision | dps schedule tied to the known ε_λ ~ e^{−4πλ²+9logλ} scale (Fig. 4 + Fuchs asymptotic), Section 5; J2 dual-precision gate | Insufficient dps produces garbage — caught by J2 disagreement, never silently trusted |
| U9 | Trace vs half-trace factor 2 | [conv:S-half] everywhere; noted at every printed number | none if convention travels |

## 4. Discretization and its own convergence check (pollution vs real IR accumulation)

There is **no mesh**: matrix entries are exact expressions evaluated in
arbitrary-precision arithmetic (mpmath). "Discretization" therefore means the four
numerical knobs, each with a dual-resolution counterpart so that spectral
pollution is distinguishable from real IR accumulation:

| Knob | base | hi (J2 replica) |
|---|---|---|
| working precision dps | schedule(λ) (Section 5) | schedule(λ) + 60 |
| quadrature maxdegree (tanh-sinh) | 12 | 14 |
| quadrature working dps | dps + 40 | (dps+60) + 40 |
| ξ̂ root-scan samples per pole gap | 9 | 17 |

**J2 (Section 7.2)** re-runs every grid point at both settings. Disagreement ⇒
numerics invalid ⇒ no verdict. Additional structural anti-pollution gates:

* **Count gate:** the source's structure fixes the positive IR zero count at
  exactly N; found ≠ N ⇒ INVALID.
  *Derivation, added by amendment A3 — the registered number N is UNCHANGED, it
  is here stated together with the source argument that forces it:*
  `dim E'_N = dim(E_N/Cξ) = (2N+1) − 1 = 2N` (Thm 5.10 i); `D''` is selfadjoint
  for the `T`-inner product (Lemma 5.4 ii), so
  `Det(D''−s) = Det(D−s)·Σ_j (j−s)^{-1}ξ_j = Σ_j ξ_j Π_{i≠j}(i−s)`
  (Lemma 5.4 iii, eq. 5.5) has exactly 2N real roots, counted with
  multiplicity; that polynomial is **even** in `s`, because `ξ_j = ξ_{−j}` and
  the index set is symmetric; and `Det(D''−0) = ξ_0·Π_{i≠0} i`, which is
  nonzero precisely when `ξ_0 ≠ 0`. Hence exactly N positive and N negative.
  *The scan DOMAIN is a separate matter and is not implied by the count.*
  Nothing in Prop. 5.9 or Thm 5.10 confines those roots to the pole hull
  `[p_{−N}, p_N]`; one-root-per-gap interlacing would need all `ξ_j` to share a
  sign, and they do not. Per A3 the scan therefore runs in two regimes: the
  pole gaps `(p_j, p_{j+1})`, j = 0..N−1, on `ξ̂` with the lattice ENDPOINTS
  sampled, plus an upward cell walk above `p_N` on the pole-free
  `g(z) = Σ_{|j|≤N} ξ_j/(z − p_j)` (on which the UV lattice zeros `p_k`,
  `|k| > N`, of `ξ̂` — which belong to `E_N^⊥`, not to `D''` — are absent),
  under the exact ceiling `Z_max = (2π/L)·√(Σ_k s_k²)` of A3. Up to two
  refinement rounds (×4, ×16 sampling), as registered.
* **Persistence gate (in the kill rule):** an eigenvalue counted as spurious
  low-energy mass must persist (within |Δz| ≤ 0.5) between the two largest N at
  the same λ. Pollution jumps with the truncation; genuine IR accumulation
  persists and strengthens.
* **Cancellation depth is budgeted, not hoped away:** locating a zero to 10^-10
  when `ξ̂` is flat at the 10^-|log ε| scale requires dps > |log₁₀ ε| + margin;
  the schedule provides ≈ 2.2× that depth (Section 5), and J2's +60-digit replica
  would expose any residual starvation.

### 4.1 Eigenpair extraction (bottom of `QW_λ^N`)

float64 copy of τ → full `eigvalsh` pre-scan (locates the near-zero cluster and
any large-modulus negative eigenvalue) → high-precision LU (shift 0) → subspace
inverse iteration on a deterministic start block of size (cluster size + 2, min 4,
cap 40) → Rayleigh–Ritz at working precision → ε₁, ε₂, ξ. Any float64-visible
eigenvalue < −10⁻⁴ is additionally refined by shifted inverse iteration and
included in the algebraic minimum. Deterministic throughout (start vectors are
fixed cosine patterns; no RNG anywhere in the script).

## 5. Grid, x₀, and precision schedule

**Registered grid** (independent directions, no diagonal; repo caution U6):

* λ ∈ {2, √8, 3, √13} — tags `2, sqrt8, 3, sqrt13`; exact λ² = {4, 8, 9, 13}
  keeps the prime cutoff exact. Includes the published anchors λ = 3 and λ = √13
  (the "primes ≤ 13 / 2.5e-55" case) and two smaller values for the λ-direction.
  λ ≤ √13 keeps dps ≤ ~200, the precision the authors themselves used; larger λ
  is out of this campaign's budget (documented compromise C5).
* N ∈ {20, 40, 80, 120} — includes the published N = 120.
* x₀ = 1 [conv:S-half]; secondary x₀ ∈ {1/2, 2} report-only.
* Window edge per point: `T(λ,N) = p_N = πN/log λ`.

**Precision schedule** (registered formula): with λ² = m exactly,
`digits(λ) = (4πm − 4.5 log m)/log 10` (the known ε_λ decay scale),
`dps_base(λ) = 50 + ceil(2.2·digits)`, `dps_hi = dps_base + 60`:

| λ | λ² | dps_base | dps_hi |
|---|---|---|---|
| 2 | 4 | 93 | 153 |
| √8 | 8 | 138 | 198 |
| 3 | 9 | 149 | 209 |
| √13 | 13 | 196 | 256 |

(Consistent with the source's stated 200 digits at λ ≤ √14, N = 120.)

**Pilot (registered separately):** λ = 2, N ∈ {6, 8}, dps 60/90, plus the ST
self-tests. This is the local-light candidate: presumed < 30 s wall, single
process, ≪ 512 MiB — **presumed only; under the owner rule of 2026-08-01 it must
be MEASURED (wall, single-process, peak RSS) before being relied on**. If the
measurement exceeds any limit, the pilot too goes to the Colab plane. Pilot
results never produce a verdict (grid incomplete by construction).

## 6. J1 — trace curve vs the zero-side benchmarks (registered before any run)

Per grid point, computed from independently known zero data [conv:zeros]:

* **B_zero(λ,N;x₀) = Σ_{0<γ_j ≤ T(λ,N)} 1/(γ_j² + x₀)** — the zero-side
  benchmark (mpmath.zetazero cache at dps 30; first 10 ordinates additionally
  hardcoded in the script for the offline pilot).
* **B_smooth(λ,N;x₀) = ∫_{2π}^{T} (2π)^{-1}max(0, log(t/2π))/(t²+x₀) dt** — the
  Riemann–von Mangoldt smooth-density integral (secondary display; the RvM count
  `N̄(T) = (T/2π)log(T/2πe) + 7/8` is also printed per point).
* **Anchor: S_Ξ(x₀) = (1/(2√x₀))(ξ'/ξ)(1/2+√x₀)** — the repo's target at the
  probe point; at x₀ = 1 this is (ξ'/ξ)(3/2)/2 ≈ 0.0231 [verified; recomputed by
  the script, never hardcoded into a judge]. Under RH it equals
  `Σ_{j≥1} 1/(γ_j²+1)`, the full-sum ceiling of B_zero.
* **Edge budget** (registered tolerance model): the eigenvalue count in the
  window (N positive) and the zero count `N̄(T)` need not agree; the mismatch is
  a UV-edge effect. Modeling it as confined to `[T/2, T]`,
  `tol_edge(λ,N) = (|N − N̄(T)| + 2)/((T/2)² + x₀)`.
* **Excess: E(λ,N) = S_IR − B_zero** — the J1 observable.

**Expected curve under "T3 holds (operative reading)":** E stays within
`max(0.1·B_zero, 5·tol_edge)` across the grid; S_IR increases in N at fixed λ
toward ≤ S_Ξ(x₀) + edge slack, and is flat-to-slowly-varying in λ at fixed N;
n_spur = 0 everywhere (no spectrum below 10 — mirroring the source's observed
tables, whose first eigenvalue sits at γ₁ ≈ 14.13). Every accumulating low-energy
eigenvalue would contribute up to 1/x₀ = 1 ≈ 43× the ENTIRE true benchmark
S_Ξ(1) ≈ 0.0231 — the kill signal, if real, is enormous relative to the signal
floor, which is why trace-at-one-point is a good kill instrument.

**Expected curve under "T3 fails":** E positive and growing along λ↑ and/or N↑,
carried by n_spur ≥ 1 modes below t_c = 10 whose weights 1/(z²+1) dominate S_IR;
S_low grows toward and past S_Ξ(1) and keeps growing with the family.

J1 outcome bands (registered): per point, `J1-PASS` if `|E| ≤ max(0.1·B_zero,
5·tol_edge)`, else `J1-NOTE` (with sign and magnitude). **J1 alone never kills**
(mid-window density mismatch between the lattice-dense and zero-dense regimes is
unmeasured territory — the probe measures it); the kill is J3's, keyed to the
low-energy band. J1 is the curve that makes the verdict interpretable.

## 7. J2 — numerics validity gates (no verdict without them)

Per grid point, both replicas (base, hi) must satisfy ALL of:

* **J2.a count:** exactly N positive zeros found in each replica.
* **J2.b zero stability:** sorted positive zeros agree:
  `max_k |z_k^base − z_k^hi| ≤ 10^-8 · max(1, z_k)`.
* **J2.c trace stability:** `|S_IR^base − S_IR^hi| ≤ 10^-8` (same for S_low).
* **J2.d even-simplicity (source hypothesis, Def. 5.3):** relative gap
  `(ε₂−ε₁)/(|ε₁|+|ε₂|) > 10^-6` AND even-defect
  `max_j |ξ_j − ξ_{-j}|/max|ξ| ≤ 10^-10` AND `|Σ_j ξ_j| ≥ 10^{-dps/2}·‖ξ‖`.
  Failure ⇒ **VOID** (hypothesis fails; not a numerics failure, not a kill;
  reported as its own headline — the source itself lists even-simplicity as open).
* **J2.e sanity:** all entries finite; quadrature error estimates recorded.

Any J2.a–c/e failure ⇒ point INVALID ⇒ global verdict INCONCLUSIVE (per the task
brief: disagreement > tolerance = numerics invalid, no verdict). VOID likewise
blocks kill/survive (but is separately headlined).

### 7.4 Assembly self-tests (pilot-stage gates, run before any production point)

* **ST1 (pole block):** `W02(n,n)` closed form (eq. 4.2) vs the (3.19) pole term
  `2Re(f̂(i/2)f̂(−i/2))` with `f̂(±i/2)` computed by direct quadrature; n ∈
  {0,1}; tol 10^-8 relative (both conjugation conventions evaluated; the one
  matching 4.2 is recorded).
* **ST2 (archimedean block, the load-bearing one):** assembled diagonal
  `WR(n,n) = 2γ_L(n) − 2β_L(n)` vs the independent spectral representation
  `−∫_R |f̂_n(t)|² θ'(t)/π dt`, `|f̂_n(t)|² = (2−2cos(tL))/(L(t−p_n)²)`
  (removable singularity guarded), integrated per pole-gap cell to T∞ = 200 plus
  smoothed tail; n ∈ {0,1}; tol `2×10^-3·max(1,|WR(n,n)|)` (registered; the tail
  oscillation bound is recorded alongside). **Sign is part of the test**: if the
  opposite sign matches, the assembly convention is wrong ⇒ ST2 FAIL ⇒ halt, no
  production run.
* **ST2b (archimedean OFF-diagonal; added by adversarial verification, pre-run):**
  the assembled `WR(0,1) = (α_L(1) − α_L(0))/(0−1) = −α_L(1)` (Prop. 4.3 with
  the `(n−m)` denominator) vs the polarized (3.19) form
  `−(1/π)∫_R f̂_0(t) f̂_1(t) θ'(t) dt` with the symmetric log-interval basis
  (`f̂_n(t) = 2sin(tL/2)/(√L(t−p_n))` for every n — real, no relative phase, by
  (2.6)+(3.5)+(3.21); hence `f̂_0 f̂_1 = +(2−2cos(tL))/(L·t·(t−p_1))`,
  removable at 0 and p_1), same per-cell scheme, T∞ and tolerance as ST2. This
  is the only gate that can see a global sign flip of the WR off-diagonal
  block (the `/(m−n)` transcription caught in draft): diagonal-only ST1/ST2
  are blind to it. FAIL with the opposite-sign banner ⇒ halt and re-derive the
  basis convention; never auto-flip.
* **ST3 (informational only):** at pilot (λ=2, N=8), print `z_k − γ_k` for
  k = 1..3. No gate — the source publishes no numbers at this (λ,N) and matching
  quality there is unknown.

ST failure ⇒ production runs are not licensed; fix and re-register if formulas
change.

## 8. J3 — the kill rule (mechanical, registered) and scope clause

Let the registered grid be complete with all points J2-valid and none VOID.
All quantities from base replicas, x₀ = 1, [conv:S-half], t_c = 10.

**KILL** (the repo's concrete T3 arm, as instantiated here, is dead) iff
**count-form OR trace-form** fires:

* Count-form (all four):
  * (K1) persistence at λ_max: n_spur(λ_max, N=120) and n_spur(λ_max, N=80)
    agree within ±1 and each z ≤ 10 at N=120 has a partner within 0.5 at N=80;
  * (K2) `n_spur(λ_max, N_max) ≥ 4`;
  * (K3) monotone: n_spur non-decreasing in λ along each fixed N ∈ {40,80,120},
    and non-decreasing in N along each fixed λ ∈ {√8, 3, √13};
  * (K4) growth in BOTH directions independently:
    `n_spur(λ_max,N_max) ≥ n_spur(λ_min,N_max) + 2` and
    `≥ n_spur(λ_max,N_min) + 2`.
* Trace-form (all three):
  * (T1) `S_low(λ_max,N_max) ≥ 0.25` (≈ 10× the entire true benchmark S_Ξ(1));
  * (T2) `S_low(λ_max,N_max) ≥ 2·max(S_low(λ_min,N_max), 0.02)` and
    `≥ 2·max(S_low(λ_max,N_min), 0.02)`;
  * (T3g) S_low non-decreasing (slack 10^-6) along the N_max row (in λ) and the
    λ_max column (in N).

**SURVIVES-AT-PROBED-SCALES** iff all of: `n_spur ≤ 1` at every grid point;
`S_low ≤ 0.02` at every grid point; `S_IR ≤ 0.030` at every grid point
(= S_Ξ(1) ≈ 0.0231 plus a generous registered margin).

**AMBIGUOUS** otherwise (e.g. spurious modes present but non-monotone, or S_IR
over 0.030 without low-energy mass — a mid-window surplus, reported with the J1
curves for diagnosis; no verdict claimed either way). Two named scenarios the
grid can plausibly produce, registered here so they are read mechanically as
AMBIGUOUS and not narrated into something stronger: (i) **lattice-like low
band** — the compressed spectrum below t_c sits near the unperturbed lattice
`2πj/L` (spacing shrinks like 1/log λ, so n_spur grows ~log λ but is flat in
N); this fails K4's N-direction growth and (at probed λ) stays below T1, hence
AMBIGUOUS — honest, because log-in-λ growth cannot be separated from saturation
on a λ ≤ √13 box; (ii) **CCM mechanism engaging late** — low-band mass at small
λ that empties as λ grows (clean at λ_max): fails the strict SURVIVE (which
demands cleanliness across the whole box) and lands in AMBIGUOUS with the
diagnostic detail label `trend=low-band-decreasing-in-lambda(clean-at-lambda-max)`
printed by the aggregator (detail only, never a verdict).

**INCONCLUSIVE** whenever the registered grid is incomplete, any point is
INVALID, or any point is VOID (VOID additionally headlined: "even-simplicity
hypothesis failed at (λ,N) = …" — news about the source's open hypothesis, not
about T3).

The script prints exactly one machine-readable line, only from the aggregator:
`T3-VERDICT: {KILL|SURVIVE-AT-PROBED-SCALES|AMBIGUOUS|INCONCLUSIVE} conv=S-half;x0=1;grid=L{2,sqrt8,3,sqrt13}xN{20,40,80,120} detail={…}`.
(The `--pilot` and self-test-failure paths print an `INCONCLUSIVE` line tagged
`grid=pilot`; a registered-grid verdict carries the full grid string above and
is printed only by the aggregator. Checkpoints computed at any x₀ other than
the registered x₀ = 1 are gated INVALID by the aggregator and can never feed
the x0=1-labeled verdict.)

### 8.1 Scope clause (what a verdict does and does not mean)

* **A KILL kills exactly:** the repo's concrete T3 arm **as instantiated here** —
  the CCM family `D_log^{(λ,N)}` per arXiv:2511.22755, finite/IR trace
  [conv:S-half], x₀ = 1, on and beyond the probed box in the measured growth
  pattern. Per the repo's own words, "the abstract core survives, the programme's
  concrete arm does not."
* **A KILL does NOT refute:** (i) the CCM papers' own claims — they claim a
  conditional real-zeros theorem (Thm 5.10), closed-form matrices, and numerical
  matching of low-lying eigenvalues to zeros; they claim **no trace bound and no
  T3**; low-energy accumulation elsewhere in the spectrum is perfectly compatible
  with everything they publish; (ii) RH; (iii) the repo's abstract Lean core
  (`PrimeResolventData` remains consistent — its `uniform_bound` field simply has
  no CCM instantiation); (iv) other conceivable instantiations of `D_{λ,N}`
  (e.g. prolate `W_sa`-based families) — those would need their own probe.
* **A SURVIVAL licenses exactly:** "no low-energy accumulation at the probed
  scales (λ ≤ √13, N ≤ 120, x₀ = 1)". It does **not** establish
  `sup_{λ,N} < ∞`, does not discharge the Lean `uniform_bound`, does not verify
  T1/T2/T4, and does not upgrade any numerical observation of the source to a
  theorem. Per the repo's own rules: "Numerical spectral agreement alone does not
  complete this item"; the accepted trust path for anything promoted beyond
  verified-numerics is interval certificates → Lean, which this campaign does not
  claim to enter.
* If the campaign had been forced to a proxy operator, a kill would have been
  weaker evidence and a survival would license nothing; per Section 2.2 the
  operator is the source's own, so the kill carries at the "as instantiated"
  strength above — the residual wedge is the risk ledger (3.4, 11), all of it
  guarded by ST/J2 gates.

## 9. Environments and execution plan

Per the owner rule of 2026-08-01: **all production points run on the Colab Pro+
Linux plane** (`colab_notebook.md`; single-process runs, one runtime per thread,
runtimes closed after each execution unit). Windows is limited to the pilot
**only after** it is measured to satisfy the local-light contract (< 30 s wall,
one process, < 512 MiB peak RSS); the measurement itself is the license — until
it exists the pilot also runs on Colab. No Lean, no oven, no sustained local
computation is involved in this campaign.

Wall-time budget (estimates, to be calibrated by the smoke cell; not promises):
per point both replicas — λ=2: ~10–25 min at N=120; λ=3: ~40–90 min; √13:
~1.5–3 h. Full 16-point grid ≈ 12–30 h ⇒ split the λ-values across 2 runtimes
(each runtime owns its λ's; never shared). Zeros cache build: ~10–20 min once.

## 10. Deliverables and trust path

Each grid point checkpoints to `results/point_L{tag}_N{N}.json` (atomic
temp+rename writes; resume-safe; carries the full REG block hash, script sha256,
mpmath/python versions, per-stage timings, both replicas, all judge inputs).
These JSONs are the audit artifacts; the repo's certificate schema
(`certificate.schema.json`, exact-rational) is NOT claimed — this campaign's
output is verified-numerics JSON, and any later promotion to the repo's
exact-rational certificate format is separate work.

## 11. Compromises ledger (complete)

1. **Operative low-energy reading** of T3 instead of the literal whole-operator
   sup (which is proven trivially infinite in Section 2.1 — the literal reading
   is vacuous, and the repo's own operational layer defines S over the finite
   operator). Anyone auditing this choice starts at Section 2.1.
2. **Archimedean block by quadrature of defining integrals**, not the printed
   closed forms (risk swap: transcription → quadrature; guarded by ST2 + J2 dual
   settings). The closed-form route was NOT implemented; if ST2 fails, that route
   becomes the fallback and this design must be re-registered.
3. **ξ̂-zero route** for the IR spectrum (Prop. 5.9) instead of building the
   compressed matrix `D''` via Lemma 5.4 (whose η-normalization is a transcription
   risk the extraction flags). The two are equivalent by Thm 5.10 iii; the count
   gate + dual-precision replicas stand in for a second independent spectral
   route. A Lemma-5.4 cross-check is explicitly NOT implemented (documented gap).
4. **Even-simplicity** is checked numerically, not proved (the source itself
   leaves it open); VOID handling per U7/J2.d.
5. **Grid ceiling λ ≤ √13, N ≤ 120**: precision cost grows like e^{4πλ²}; the
   sup is only probed on a box. The verdict names are chosen accordingly
   ("SURVIVES-AT-PROBED-SCALES", never "T3 holds").
6. **x₀ = 1 only** for the verdict (secondary x₀ displays are report-only).
7. **Zero data at dps 30** from mpmath (verified label), not an independent
   second source; the first 10 ordinates are double-anchored (hardcoded + mpmath).
8. **No prolate arm**: the (b) extraction's `W_sa`/Sonin line is out of scope for
   T3 (different operator); its Route A/Route B fidelity fork is recorded there
   for any future probe, and none of it is used here.
9. **Verified-numerics only**: no interval arithmetic; the kill rule's margins
   (t_c = 10 vs γ₁ = 14.13; kill thresholds 10–40× above tolerance scales) are
   chosen so the verdict does not live near numerical noise, and J2's replicas
   bound the noise empirically.

## 12. What this campaign does not test

T1 (self-adjointness/domain bookkeeping of the family), T2 (the ±γ pairing
normalization as an open task for the concrete family), T4 (prime-resolvent
convergence — "the genuine frontier"), the Hausdorff falsifier (refutes RH, not
the arm), the CCM λ→∞ program (k_λ vs ξ_λ, "the main remaining obstacle"), and
everything in Part I/Part II of the host repo. A SURVIVE here reopens exactly one
decision: whether the abstract bridgeC block (4–8 months per the charter) is
worth buying, knowing the operator layer would still require proving what Connes
has not proved.

---

## 13. Amendment log

**A1 (2026-08-06, adversarial verifier pass, PRE-RUN — no matrix assembled, no
spectrum computed; the Section-0 freeze clause is not triggered).** Edits by the
independent verification desk (Claude Fable 5):

1. Section 5 dps table, √13 row: 195/255 → **196/256**. The registered formula
   `50 + ceil(2.2·(4π·13 − 4.5·log 13)/log 10)` evaluates to 196 (the script
   was already correct; the table was off by one against its own formula).
2. Section 7.4: **ST2b registered in the design text** (it existed in the
   script since 2026-08-05 but was undocumented here — a load-bearing gate must
   not live only in code).
3. Section 8: pilot/self-test-failure `grid=pilot` INCONCLUSIVE lines
   acknowledged; x₀ registration gate documented.
4. `t3_probe.py`: **x₀ registration gate added to `judge_point`** — any
   checkpoint whose stored x₀ differs from the registered x₀ = 1 is INVALID
   (S_low scales like 1/x₀; an off-registration x₀ could otherwise manufacture
   or mask a kill under an `x0=1` label). New script sha256 =
   `125bef5d0a3a9bd4b79e98627e67a99b57d09a03da9b96a88795d4bc84cf4bec`
   (supersedes `0a912031…`; REG hash unchanged — the REG block was not touched).
5. `colab_notebook.md`: sha updated to match; integrity check converted from
   `assert` to an explicit `raise` (house `-O` rule); T_max comment corrected
   543.7 → 543.9 (= 120π/log 2).

No judge constant, threshold, grid point, or kill-rule clause was changed.

**A2 (2026-08-06, ST-gate repair desk, PRE-RUN — the pilot's ST gates fired and
halted the run, so NO production point of the registered grid was ever computed,
no matrix of the target family was assembled and no spectrum computed; the
Section-0 freeze clause is not triggered).** Two independent transcription
defects, one on each side of gate ST2/ST2b, found by two independent diagnosis
desks and re-verified here against the source PDF and by independent numerics.

*The measured failure that bought this amendment* (Colab, 2026-08-06, probe
sha256 `125bef5d…`, reg `215ba8033b77c03d`, mpmath 1.3.0, python 3.12.13,
λ = 2 ⇒ L = 2log2):

    ST2 n=0: WR_diag=2.811166705   spectral(θ')=2.062327857  -> FAIL
    ST2 n=1: WR_diag=1.061074172   spectral(θ')=0.3122354665 -> FAIL
    ST2b   : WR_offdiag=-0.2313394171 spectral(θ')=+0.2313165751 -> FAIL
             [OPPOSITE SIGN MATCHES banner]
    PILOT-GATE: FAIL (ST self-tests).  Production NOT licensed.

1. **γ_L(n) double-counted c(L) — the ASSEMBLY was wrong (defect 1).** Eq. (4.14)
   as PRINTED reads `γ_L(n) := ∫₀^L (cos(2πnx/L) − exp(−x/2))ρ dx + c(L) + w(L)`,
   and the probe transcribed it verbatim (design.md §3.1, `t3_probe.py`
   `archimedean_tables`). But (4.11) states
   `∫(cos − e^{−x/2})ρ = ∫(cos − 1)ρ + c(L)`, so the printed (4.14) applies the
   `e^{−x/2}` subtraction *and* adds `c(L)`: `c(L)` is counted twice. Deriving
   the diagonal straight from the paper's own primary display (3.15)/(4.4) —
   `W_R = (ω(0)/2)(γ + log 4π) + ∫₀^L [e^{x/2}ω(x) − ω(0)]/(e^x−e^{−x})dx
   − ω(0)∫_L^∞ dx/(e^x−e^{−x})`, with `ω = q(U_n,U_n)`, `ω(0) = 2` (Lemma 2.3,
   eq. 2.10) and the exact identity `e^{−x/2}ρ(x) = 1/(e^x−e^{−x})` — forces
      `WR(n,n) = 2[∫₀^L(cos − e^{−x/2})ρ dx + w(L)] − 2β_L(n)`
              `= 2[∫₀^L(cos − 1)ρ dx + c(L) + w(L)] − 2β_L(n)`,
   i.e. `γ_L(n) = ∫(cos − 1)ρ + c(L) + w(L)`, with NO second `c(L)`. Note the
   paper's own closed form (4.7) computes `∫₀^L(cos − 1)ρ dx`, so the intended
   pipeline ((4.7) + c + w) is correct; only the display (4.14) mis-states the
   integrand. **Change:** `t3_probe.py` line 246 integrand
   `(cos(a·x) − exp(−x/2))·ρ(x)` → `(cos(a·x) − 1)·ρ(x)`, the constant `cw`
   (the p.15 closed form of `c(L)+w(L)`) left untouched — this puts the
   quadrature on exactly the integral the paper gives in closed form and lets
   `c(L)` enter exactly rather than by quadrature. §3.1 of this design amended to
   match. The equivalent form (keep the integrand, replace `cw` by `w(L)` alone)
   was verified to agree to all printed digits and was not used.
   *Verification of the constant, done here at 4 values of L (2log2, 3,
   2log√13, 1/2, dps 40):* `cw(p.15) − w(L) = ∫₀^L(1−e^{−x/2})ρ dx = c(L)` to
   ≤2.3e-41 — an identity in L, so the coded `cw` really is `c+w` and the bug is
   that `c` must not also sit inside the integrand. At L = 2log2,
   `c(L) = 0.3744308122255553`, so every diagonal entry of `WR` was too large by
   exactly `2c(L) = 0.7488616244511107`, independent of n — which is why the two
   pilot offsets (0.748838848 and 0.748838705) agreed to 1.4e-7.
   *Consequence had this shipped:* `τ_buggy = τ_true − 2c(L)·I`. A multiple of
   the identity leaves ξ, `ξ̂`, its zeros and hence `S_IR` — the actual T3
   observable — completely unchanged, while shifting EVERY eigenvalue by
   0.749, i.e. destroying `ε_N`, the J2.d relative-gap/even-simplicity gate and
   any statement about `μ_λ`. The gate caught a defect that would have voided
   the hypothesis check while leaving the headline number deceptively intact.
   *Second, harmless source typo recorded in passing:* the p.14 display of
   `c(L)` prints the integrand `(1−e^{−x/2})/(e^x−e^{−x})`, i.e. missing the
   `e^{x/2}` that ρ carries; it evaluates to 0.2690702965677290 at L = 2log2 and
   is self-consistent with its own printed closed form, but it is NOT the `c(L)`
   forced by (4.11) nor the one inside the (correct) p.15 combined display.
   Nothing in the probe used it.
2. **The ST2b REFERENCE carried a spurious global minus — the ASSEMBLY was right
   (defect 2).** This is the outcome §7.4 explicitly provides for ("never
   auto-flip"), and it is argued from the source, not from a wish to pass.
   From `U_n(x) = L^{−1/2}exp(2πinx/L)` (2.6), `V_n(u) = U_n(log λu)` (3.21) and
   `F̂(s) = ∫F(u)u^{−is}d*u` (3.5), substituting `u = e^{x−L/2}` gives, for
   EVERY n, `V̂_n(t) = 2sin(tL/2)/(√L(t−p_n))` — real, no n-dependent phase (the
   `e^{ip_nL/2} = (−1)^n` cancels against `sin(πn − tL/2) = −(−1)^n sin(tL/2)`).
   Hence `V̂_0V̂_1 = +(2−2cos(tL))/(L·t·(t−p_1))`, a PLUS sign; the probe's `g01`
   and both of its smoothed tails carried a minus, which also contradicted the
   `|f̂_n|² = (2−2cos(tL))/(L(t−p_n)²)` used four lines above in the same
   function. *Verified here* by direct quadrature of the defining integral
   against the closed form at five (n,t) pairs: agreement 1.9e-39…3.0e-31, imag
   part ≤1.4e-37. The assembly line `wr = (α_L(m) − α_L(n))/(n − m)` is Prop. 4.3
   character-for-character (corroborated independently by Lemma 5.1 and its
   proof, p.16, which displays the same crossed index order) and was NOT touched.
   **Change:** `t3_probe.py` `st2_archimedean`, three signs in the ST2b block
   (`g01` return, `tail_p`, `tail_m`) and the comment that encoded the wrong
   derivation. §7.4 of this design amended to match.
3. **Which side was wrong, stated plainly:** the diagonal failure was the
   ASSEMBLY (defect 1, a real matrix bug); the off-diagonal failure was the ST
   REFERENCE (defect 2, a self-test bug that left τ bit-identical). Both
   diagnosis desks reached the same verdict on both sides; this desk re-derived
   both from the PDF and re-measured both before acting.
4. **Arbitration of the residual ~2.3e-5** (measured here, not asserted): it is
   the ST reference's own truncation, not physics and not quadrature. Running
   the probe's θ' scheme for the n=0 diagonal at T∞ = 200/400/800/1600 gives
   2.06232785677 / 2.06231367729 / 2.06230521800 / 2.06230515607, i.e. residual
   against the REPAIRED assembly value 2.062305080262 of
   2.28e-5 → 8.60e-6 → 1.38e-7 → 7.6e-8, collapsing like C/T∞², while the
   distance to the BUGGY value stays pinned at 0.7489. The reference integrates
   the exact oscillatory integrand only to T∞ = 200 and then splices tails in
   which `(2−2cos(tL))` is replaced by its mean 2; the dropped oscillatory
   remainder is the whole effect. So the repaired assembly is the thing the
   independent representation converges to.

**ST numbers before / after** (λ = 2, registered settings, tolerance
`2e-3·max(1,|WR|)` UNCHANGED):

| gate | assembly BEFORE | assembly AFTER | reference (T∞=200) | residual AFTER | tol | verdict |
|---|---|---|---|---|---|---|
| ST2 n=0 | 2.811166705 | **2.06230508** | 2.062327857 | 2.28e-5 | 4.12e-3 | PASS (181× margin) |
| ST2 n=1 | 1.061074172 | **0.3122125473** | 0.3122354665 | 2.29e-5 | 2.0e-3 | PASS (87× margin) |
| ST2b (0,1) | −0.2313394171 (unchanged) | −0.2313394171 | −0.2313165751 (was +) | 2.28e-5 | 2.0e-3 | PASS (88× margin) |

ST1 unchanged and still PASS (n=0 plain, n=1 conj). Measured on the Windows desk
by a wrapper that runs ONLY the ST portion (single process, no pools, no
checkpoint written): **ST1 0.0 s, ST2+ST2b 63.5 s, total 63.5 s wall**. That
exceeds the owner rule's 30 s local-light ceiling, so the ST block is NOT
local-light; it is recorded here as a one-off diagnostic measurement and the
gate is to be re-run on the Colab plane as part of `--pilot` before any
production point. Peak RSS was not captured by the wrapper's probe.

**No judge was weakened.** `REG` is byte-identical (`reg_sha256 =
215ba8033b77c03d5948da990197862eb8fcaa3548ee527b354ea093d8c1955c`, unchanged);
`st2_tol` stays `2e-3`; ST2's "sign is part of the test" and ST2b's
halt-on-opposite-sign banner stay as registered; J1, J2.a–e and the J3 kill/
survive rule are untouched. Only two mis-transcribed FORMULAS changed. Per §7.4's
own clause ("fix and re-register if formulas change") this is a re-registration:
new `t3_probe.py` sha256 =
`b3ab8b200d230cf9da2d72bcca9158d997da16bd78af78c5e7fe9e91ef49b716`
(supersedes `125bef5d…`); `colab_notebook.md` header and cell-2 integrity check
updated to match.

**A3 (2026-08-06, adjudication desk, PRE-RUN — verified at the time of writing:
`results/` contains exactly one file, `pilot-A2-colab-20260806.txt`; there is no
`point_L{tag}_N{N}.json`, no zero cache, and no other artifact, so NO production
point of the registered grid has ever been computed and the Section-0 freeze
clause is not triggered).** This is a **PROBE fix, not a gate amendment**. The
registered count expectation stays exactly `N`; `REG` is byte-identical
(`reg_sha256 = 215ba8033b77c03d5948da990197862eb8fcaa3548ee527b354ea093d8c1955c`).

*The measured pilot evidence that triggered it* (Colab, 2026-08-06, probe
sha256 `b3ab8b20…`, reg `215ba8033b77c03d`, mpmath 1.3.0; transcript
`results/pilot-A2-colab-20260806.txt`):

    [lambda=2 N=6 base] S_IR=0.0098878733756455  n_spur=0 J1=PASS  invalid=['count_mismatch:4!=6']
    [lambda=2 N=6 hi  ] identical numbers,                        invalid=['count_mismatch:4!=6']
    [lambda=2 N=8 base] S_IR=0.011537087628295   n_spur=0 J1=PASS  invalid=['count_mismatch:6!=8']
    [lambda=2 N=8 hi  ] identical numbers,                        invalid=['count_mismatch:6!=8']

Deficit exactly 2 at both N and identical at both precision replicas — so not a
precision effect. All five ST gates PASS, and the found zeros reproduce γ₁, γ₂,
γ₃ to 4.8e-9 / 1.4e-6 / 3.0e-5, so the assembly is not in question.

1. **Ruling: the registered number was always right; the SEARCH DOMAIN was
   wrong.** The house rule permits amending a registered judge only on a
   source-grounded proof that the number was never the right number. There is no
   such proof — the opposite is provable, and was proved here from the PDF
   before anything was edited: `dim E'_N = 2N` (Thm 5.10 i); `D''` selfadjoint
   (Lemma 5.4 ii) so all 2N roots of `Det(D''−s) = Σ_j ξ_j Π_{i≠j}(i−s)`
   (Lemma 5.4 iii, eq. 5.5) are real; that polynomial is even (`ξ_j = ξ_{−j}`,
   symmetric index set); and `Det(D''−0) = ξ_0 Π_{i≠0} i ≠ 0` since
   `ξ_0 ≈ 0.7048` (N=6) / `0.7021` (N=8) is the DOMINANT component of ξ.
   Therefore exactly N positive roots. **J2.a is not amended.**
2. **Discriminating evidence, not plausibility** (this desk's own computation,
   single process, 4.6 s, from the probe's own ξ; it shares no code path with
   the gap scan): `Det(D''−s)` was built by exact polynomial arithmetic and
   handed to `mp.polyroots`, which has no window and no sampling density —
   completeness is structural. Result: **N=6 → deg 12, 12 real roots, 6
   positive / 6 negative, max|Im| = 0, `P(0) = 3.65e5`; N=8 → deg 16, 8
   positive / 8 negative, max|Im| = 0.** Leading coefficient `= Σ_j ξ_j`
   (1.84e-5 and 7.63e-6), as the degree-2N claim requires. The positive roots
   are, in `z = (2π/L)s`:
   `14.1347251866514, 21.0220577410478, 25.011444793654, 30.7878166388224,
   42.4608534163468, 125.563623887962` (N=6) and
   `14.1347251465511, 21.0220410258056, 25.0108878507087, 30.4271794661733,
   32.9467808139053, 37.6852322342288, 51.0378657150143, 151.988591710161`
   (N=8). The old scan's right edge is `p_{N+1}` = 31.7265 / 40.7912; exactly
   two roots lie beyond it in each case, reproducing the measured deficit of 2
   with no free parameter. Evaluating the probe's OWN `make_phi` at the two
   allegedly-missing roots gives `|φ|/ref ≈ 1e-102` at dps 60 — they are zeros
   of `ξ̂` itself, not artifacts. Had the registered number been wrong, the
   polynomial route would have returned complex roots or an asymmetric split; it
   returned neither. A spec defect is therefore **excluded**, not merely deemed
   unlikely. Two further hypotheses were excluded by measurement rather than
   argument: density is irrelevant (base and hi replicas print identical
   numbers, and the ×4/×16 refinement rounds never changed the count), and no
   zero sits at or near a lattice point at the pilot (`φ(p_j) = (−1)^j ξ_j L/2`,
   bounded away from 0).
3. **What changed in `t3_probe.py` (`positive_zeros`, plus two new helpers
   `make_g` and `newton_root_sum_sq`).** All three changes strictly WIDEN the
   search; none can make the gate easier to pass.
   * **Two-regime scan.** Below `p_N`, unchanged gap scan of `ξ̂`. Above `p_N`,
     scan `g(z) = Σ_j ξ_j/(z − p_j)` and **not** `ξ̂`. This is load-bearing and
     is the trap in the naive repair: above `p_N` the factor `sin(zL/2)` makes
     `ξ̂` vanish at every lattice point `p_k` with `|k| > N`, and those are the
     `E_N^⊥` / UV spectrum of Thm 5.10 iii, **not** eigenvalues of `D''`; a
     merely-widened `ξ̂` scan would count them and overshoot N. `g` is
     holomorphic above `p_N`, so every sign change of `g` there is an escaped
     `D''` eigenvalue.
   * **Ceiling derived, not invented.** `Z_max = (2π/L)·√(Σ_k s_k²)` with
     `Σ_k s_k² = 2·Σ_{j=1..N} j² − 2·(Σ_j j² ξ_j)/(Σ_j ξ_j)` — Newton's
     relation on the top three coefficients of `Det(D''−s)` (`c_{2N} = Σ_j ξ_j`,
     `c_{2N−1} = Σ_j j ξ_j = 0` by evenness, `c_{2N−2} = −c_{2N}S/2 + Σ_j j²ξ_j`
     with `S = Σ_i i²`), valid as a bound because all roots are real. Verified
     against the directly computed roots to all printed digits: 1926.20478012154
     (N=6) and 2960.15094256007 (N=8); `Z_max` = 198.92 / 246.59 versus true top
     zeros 125.56 / 151.99. Its denominator `Σ_j ξ_j = √L·δ_N(ξ)` is the very
     quantity whose vanishing is already the registered VOID condition, so the
     ceiling is finite exactly where the point is admissible at all. The walk
     stops as soon as the source's N zeros are accounted for, so the ceiling is
     paid for only by a point that is going to fail anyway (measured: 22 and 26
     cells walked at the pilot, scan time 0.13–0.42 s).
   * **Lattice endpoints are now sampled.** `ξ̂(p_j) = (−1)^j ξ_j L/2` exactly,
     and `Det(D''−j) = ξ_j Π_{k≠j}(k−j)`, so `p_j` with `|j| ≤ N` is itself a
     `D''` eigenvalue precisely when `ξ_j = 0` — a root the old interior-only
     sampling could never see. Latent second defect; it did not bite at the
     pilot (`min |ξ_j|` is 3.1e-5 at N=6) but the `ξ_j` shrink fast with `|j|`.
   * Coincident hits are merged with a tolerance of a quarter sample step. This
     can only LOWER a count, never raise one, so it cannot manufacture a pass;
     an undercount falls into the existing ×4/×16 refinement, which tightens the
     tolerance along with the sampling.
   * **Diagnostics only, no new gate** (recorded per point in `scan_diag`):
     `V` = number of sign changes of `((−1)^j ξ_j)_{j=0..N}`, which must equal
     the number of zeros found in `(0, p_N)` (measured V = 3 at N=6 and 5 at
     N=8, both consistent); the `Z_max` used and the cells walked; and
     `Σ_k s_k²` from the Newton identity against the same sum rebuilt from the
     zeros actually found. A mismatch means the scan is still incomplete.
4. **Verification after the change** (this desk, Windows, single process,
   6.5 s total, pilot POINTS logic only — the ST block was NOT re-run here, it
   was measured at 63.5 s in A2 and is not local-light; it goes to Colab):
   **count = 6/6 and 8/8, both replicas, `refine_rounds = 0`, `invalid = []`.**
   Base and hi print identical zeros, so J2.b/J2.c are satisfied by inspection.
   `S_IR` rises from 0.0098878733756455 to **0.010505643138843** (N=6, +6.3%)
   and from 0.011537087628295 to **0.011964124720552** (N=8, +3.7%). These
   match, to every printed digit, the predictions BOTH diagnosis desks
   registered before the repaired probe was run.
5. **`n_spur` and `S_low` are UNCHANGED (0 and 0 at both points): every
   recovered zero is high-energy (z ≥ 42), so the J3 kill instrument never saw
   this defect.** The defect blocked the run at J2.a; it did not bias the kill
   in either direction. J1 remains PASS at both points. Recorded for the
   fabrication desk, needing no re-registration: `S_IR` is registered as a sum
   over all N positive eigenvalues while `B_zero` is registered over
   `(0, T = p_N]`; with eigenvalues now measured genuinely above `p_N`, that
   asymmetry is a measured fact rather than a hypothetical, and it is the §6
   edge budget that absorbs it (added mass 6.2e-4 at N=6 versus `5·tol_edge`).
   §6 already anticipated this in the registered tolerance model ("the
   eigenvalue count in the window (N positive) and the zero count N̄(T) need not
   agree").
6. **Had this not been caught:** the gate would have fired `count_mismatch` at
   every one of the 16 production points, each point would have been INVALID,
   and §8's own rule ("any point is INVALID ⇒ INCONCLUSIVE") would have returned
   a **global INCONCLUSIVE after the entire 12–30 h grid budget had been spent**
   — the exact failure the pilot exists to prevent. The alternative failure, had
   the desk instead taken the easy road and amended J2.a to `N−2`, would have
   been worse: the deficit 2 is a coincidence of these two points, not a law
   (the true out-of-window count is `N − V` minus however many escapees land in
   the extra gap `(p_N, p_{N+1})`, which happened to be one at both pilot
   points), so an `N−2` gate would have hard-coded a coincidence, silently
   discarded the top of the spectrum at every production point, and understated
   `S_IR`. That is the concrete cost of a desk weakening its own judge.
7. **No judge was weakened, and none was touched.** J1, J2.a–e, J2's dual
   replica scheme, ST1/ST2/ST2b/ST3, and the entire J3 kill/survive rule are
   byte-identical; `REG` is byte-identical, so `reg_sha256` is unchanged.
   §4's count-gate paragraph was rewritten to remove a false auxiliary premise
   it stated as if the source implied it ("the scan runs over the N+1 pole
   gaps"): the count is forced by the source, the LOCATION is not, and at λ = 2
   two of the N positive eigenvalues provably lie outside the pole hull. That is
   a design-TEXT defect, corrected here; the gate clause `found ≠ N ⇒ INVALID`
   is unchanged. Per §7.4's own clause ("fix and re-register if formulas
   change") this is a re-registration: new `t3_probe.py` sha256 =
   `b173fec9e6dc8447f99c7e6a79abfe1eede38d418de4ee90f64eccf849d87b34`
   (supersedes `b3ab8b20…`); `colab_notebook.md` header and cell-2 integrity
   check updated to match.

**Open items recorded by A3 (not done, not required for the gate):**
(i) §11 item 3 still stands — the full Lemma-5.4 compressed-matrix route is NOT
implemented as a second spectral route in the probe; A3 imports only one exact
scalar consequence of Lemma 5.4 iii (the Newton ceiling) plus diagnostics, and
the polynomial-root route was used by this desk as an audit instrument, not
wired into the probe. Wiring it in as a pilot/small-N completeness witness is
recommended and would also catch even-multiplicity roots, to which any
sign-change scan is structurally blind. (ii) **Production cost warning:**
`Σ_j ξ_j` is 1.84e-5 at N=6 and 7.63e-6 at N=8 and shrinking, and the top pair
runs away like `√(|Σ_j j²ξ_j / Σ_j ξ_j|)`; at N = 120, λ = √13 the ceiling and
the number of cells walked are unmeasured, and the early stop is what keeps the
cost sane. `--pilot` must be re-run on the Colab plane with this probe before
any production point is licensed, and the printed `cells_walked_above_pN` should
be read as the cost signal. (iii) The `zero_thresh` branch still appends a
sample point without bisection when `|ξ̂|` is already below threshold; at a
lattice endpoint that value is exact, elsewhere it is accurate only to a sample
step. It did not fire at the pilot; left as registered behaviour rather than
changed in the same pass as a defect repair.

**Open item, not required for the gate (recorded, not done):** Prop. 4.2's
closed forms (4.5)–(4.7) are still not implemented, so the repaired γ_L(n) has
not been cross-checked against the paper's hypergeometric/digamma route. Now
that the quadrature sits on exactly the integral (4.7) evaluates, that check is
free and is recommended as an extra witness before production. Tightening T∞
from 200 (residual 2.3e-5) to 800 (1.4e-7) is likewise available and would make
ST2/ST2b bite harder; it is a tightening, never a weakening, and was NOT applied
here because changing a registered gate parameter is not this desk's call.
