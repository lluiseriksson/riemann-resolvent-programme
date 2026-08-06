# HYPOTHESIS FRONTIER — riemann-resolvent-programme

Checkpoint: 2026-07-03 (v0.1.0). Mirror of the sibling programme's
frontier file: every conditional theorem's carried inputs, listed with
what discharging each one requires. **Nothing below may be repackaged as a
structure field, a renamed hypothesis or an abstract "criterion" — it must
be discharged** (anti-wrapper rule, `AGENTS.md`).

## Carried analytic inputs (the `hRpoly`-analogues)

### bridgeA : SlitPlaneStieltjesExtension → RiemannHypothesis
The decisive direction of Theorem A. Discharging it = formalizing: from a
holomorphic extension of `𝒮_Ξ` to `ℂ ∖ (-∞,0]` agreeing with
`xiResolventTarget` on an open subinterval of `(1/4, ∞)`, exclude zeros of
`Ξ` off the real axis (identity principle + Hadamard/reflection structure
of `ξ`), then conclude Mathlib's `RiemannHypothesis`. Mathlib already has
the completed zeta, its functional equation and locally uniform limits of
holomorphic functions. Source estimate: 2–4 months (ROADMAP C3).

### bridgeC : PrimeResolventData → SlitPlaneStieltjesExtension
The analytic core of Theorem C: from the uniform one-point bound (T3
shape) plus uniform prime-approximant convergence on `I_{δ,B}`, produce
the slit-plane Stieltjes extension. Needs: compactness of Stieltjes
families from a single pointwise bound (source: 4–8 months, the hardest
abstract block) + locally uniform holomorphic limits + the omitted-prime
tail (`primeTail_bound`, ROADMAP C2). Total abstract core: 8–16 months.

## Operator tasks (source §11) — deliberately NOT in Lean yet

- **T1 (simplicity + parity).** Uniform simplicity and parity of the
  ground state used to build `D_{λ,N}` (Connes–Consani–Moscovici
  construction). Gate `verify.ccm_operators` (V4) open.
- **T2 (trace class and ±γ counting).** `(D_{λ,N}² + xI)⁻¹` trace class;
  the `1/2` normalization counts the `±γ` pairs correctly.
- **T3 (uniform low-energy bound) — KILL SWITCH.**
  `sup_{λ,N} Tr (D_{λ,N}² + x₀ I)⁻¹ < ∞`. If spectral mass accumulates at
  low energy, criterion C is empty and the operator route dies; the
  abstract core survives, the programme's concrete arm does not.
- **T4 (prime-resolvent convergence) — the genuine frontier.**
  `E_{λ,N}(δ,B) → 0`. Approximating the first ten or hundred eigenvalues
  is not enough: the whole spectrum must be controlled under the weight
  `1/(γ² + x)`.

### Campaign refinement (2026-08-06): the critical spectral rate

The T3 campaign isolates a sufficient, still open route from the concrete
CCM ground state to the required transform convergence.  For normalized
ground state `ξ_λ`, explicit approximant `k_λ`, ground energy `E_λ`, spectral
gap `Δ_λ > 0`, and normalized Rayleigh excess

`r_λ = QW_λ[k_λ / ‖k_λ‖] - E_λ`,

the spectral theorem and Cauchy--Schwarz on
`L²([λ⁻¹,λ], du/u)` give a scalar `a_λ` with

`‖a_λ ξ_λ - k_λ‖₁ ≤ 2 ‖k_λ‖₂ sqrt(log λ * r_λ / Δ_λ)`.

Consequently, a bound

`‖k_λ‖₂ sqrt(2 r_λ / Δ_λ) = O(λ^{-q})` for some `q > 1/2`

beats the Mellin substrip loss for every `|Im z| ≤ η < 1/2`.  This identifies
the mathematical role of `BeatsHalfThreshold` and `rayleighGapDefect` in the
`riemann-prime-resolvent` sibling.  It does **not** discharge T1 or T4: no
current satellite proves the required gap/rate for the concrete `QW_λ`, and
the independent convergence of the explicit approximant to `Xi` is still
required.  Full derivation and falsifier are recorded in
`campaigns/t3-kill-test/frontera-analitica.md`.

## Inherited cautions

- **Two-parameter (R, N) caution** (from the Weil/W-Schur route, Card 2):
  the arithmetic cutoff `R` and the resolution `N` behave differently —
  raising `R` adds `V_{R,R',N}`, not a block extension. Any future
  `D_{λ,N}` interface must keep both parameters explicit and never take a
  diagonal limit silently.
- **Marked infinity**: the interior point `x₀` is the marker of the
  programme (same move as the root in Appendix F); no statement may erase
  it before the uniform bound is extracted.

## Falsifier status

`hausdorff-certificates` run `run.2026_07_03.hausdorff_certificates_v0_1_0`:
zeta pipeline at `x₀ = 1`, 60 zeros — consistency `PSD_CERTIFIED` to
`N = 14` (`H` and `L`, truncated measure via Lemma S), refutation-grade
enclosure honestly `INCONCLUSIVE` at small `N` (tail width ~4.3e-3
dominates); derivative cross-check `all_inside = true`. No falsifier
fired. Refutation semantics conditional on that satellite's gates V-A/V-B.

## What would change this file

Discharging `bridgeA` (C3) removes one carried input and promotes
`riemannHypothesis_of_slitPlaneExtension` to a single-input theorem.
Discharging `bridgeC` (C4–C5) leaves RH reduced, inside Lean, to
exhibiting one `PrimeResolventData` — which is exactly T1–T4.
