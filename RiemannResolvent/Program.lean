/-
Copyright (c) 2026 Lluis Eriksson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Lluis Eriksson
-/
import Mathlib.NumberTheory.LSeries.RiemannZeta
import RiemannResolvent.HankelPositivity

/-!
# The prime-resolvent Stieltjes programme: objects and assemblies

Programme charter objects (knowledge-tree node
`problem.prime_resolvent_stieltjes_criterion`, Bridge Card 9, source
ideas5): the completed xi, the one-point observable
`𝒮_Ξ(x) = (1/(2√x)) (ξ'/ξ)(1/2 + √x)`, the Theorem-A interface
`SlitPlaneStieltjesExtension`, the Theorem-C data bundle
`PrimeResolventData`, and the two **assembly theorems** whose only
nontrivial content lives in the explicitly named carried inputs `bridgeA`
and `bridgeC` (the exact analogue of `hRpoly` in the Yang–Mills sibling:
assemblies compile unconditionally, the analytic bridges are the
frontier — see `HYPOTHESIS_FRONTIER.md`).

**Anti-wrapper rule** (inherited from the sibling programme): `bridgeA`
and `bridgeC` must be *discharged*, never repackaged as fields of a
structure, renamed hypotheses, or "recovery-style" abstractions.  The four
operator tasks T1–T4 of the source live only in `HYPOTHESIS_FRONTIER.md`;
they are deliberately **not** encoded as vacuous `Prop` fields here.
-/

namespace RiemannResolvent

open Complex

/-- The completed xi function `ξ(s) = s (s - 1) / 2 · Λ(s)` built from
Mathlib's completed zeta `completedRiemannZeta` (with its poles at `0, 1`
cancelled by the prefactor); entire, with `ξ(s) = ξ(1 - s)`. -/
noncomputable def riemannXi (s : ℂ) : ℂ :=
  s * (s - 1) / 2 * completedRiemannZeta s

/-- The one-point programme observable
`𝒮_Ξ(x) = (1/(2√x)) · (ξ'/ξ)(1/2 + √x)` for real `x`.  Under RH and for
`x > 1/4`, the Hadamard factorization identifies it with the Stieltjes
transform `∑_{γ>0} 1/(γ² + x)` of the positive zero measure
`ν_Ξ = ∑ δ_{γ²}` (source, §2). -/
noncomputable def xiResolventTarget (x : ℝ) : ℂ :=
  deriv riemannXi (1 / 2 + (Real.sqrt x : ℂ)) /
    riemannXi (1 / 2 + (Real.sqrt x : ℂ)) / (2 * (Real.sqrt x : ℂ))

/-- **Theorem-A interface** (decisive direction): `𝒮_Ξ` admits a
holomorphic extension to the slit plane `ℂ ∖ (-∞, 0]` that agrees with
`xiResolventTarget` on some open subinterval of `(1/4, ∞)`.  Per the
source, this (together with the identity principle and the reflection
structure of `ξ`) already excludes zeros of `Ξ` off the real axis, hence
implies RH; that implication is the carried input `bridgeA` below. -/
def SlitPlaneStieltjesExtension : Prop :=
  ∃ S : ℂ → ℂ, DifferentiableOn ℂ S Complex.slitPlane ∧
    ∃ a b : ℝ, 1 / 4 < a ∧ a < b ∧
      ∀ x : ℝ, a < x → x < b → S (x : ℂ) = xiResolventTarget x

/-- **Theorem-C data bundle**: a family of spectral observables
`S j = (1/2) Tr (D j ^ 2 + x I)⁻¹` (abstracted to plain functions — the
operator layer is deferred to the roadmap), prime-side approximants
`P j`, one interior point `x₀ > 0` with a uniform bound, and uniform
convergence of `S j - P j` on the compact window
`I_{δ,B} = [(1/2 + δ)², B]`.  Exactly the hypotheses of the source's
Theorem C; nothing about RH is smuggled into the fields. -/
structure PrimeResolventData where
  /-- spectral observables `S j x = (1/2) Tr (D j ^ 2 + x I)⁻¹` -/
  S : ℕ → ℝ → ℝ
  /-- prime-side approximants at cutoffs `X j → ∞` -/
  P : ℕ → ℝ → ℝ
  /-- the marked interior point (the "marked infinity" of the programme) -/
  x₀ : ℝ
  hx₀ : 0 < x₀
  δ : ℝ
  hδ : 0 < δ
  B : ℝ
  hB : (1 / 2 + δ) ^ 2 < B
  /-- kill-switch hypothesis (source task T3): the one-point traces do not
  accumulate spectral mass at low energy -/
  uniform_bound : ∃ C : ℝ, ∀ j : ℕ, S j x₀ ≤ C
  /-- prime-resolvent convergence (source task T4), uniformly on the
  compact window -/
  approx : ∀ ε : ℝ, 0 < ε → ∃ N : ℕ, ∀ j : ℕ, N ≤ j →
    ∀ x : ℝ, x ∈ Set.Icc ((1 / 2 + δ) ^ 2) B → |S j x - P j x| ≤ ε

/-- **Assembly (Theorem A, decisive direction).**  Trivial by design: the
entire analytic content is the carried input `bridgeA`, the slit-plane
extension criterion (roadmap C3; source estimate 2–4 months).  Mirrors the
role of `hRpoly` in the Yang–Mills sibling. -/
theorem riemannHypothesis_of_slitPlaneExtension
    (bridgeA : SlitPlaneStieltjesExtension → RiemannHypothesis)
    (h : SlitPlaneStieltjesExtension) : RiemannHypothesis :=
  bridgeA h

/-- **Assembly (Theorem C).**  The carried inputs are `bridgeC` (uniform
one-point boundedness + uniform prime-approximant convergence produce the
slit-plane Stieltjes extension: Stieltjes-family compactness plus locally
uniform limits of holomorphic functions; roadmap C4–C5, the 8–16 month
abstract core of the source) and `bridgeA` as above.  Given both, any
`PrimeResolventData` yields RH. -/
theorem riemannHypothesis_of_primeResolventApproximation
    (bridgeC : PrimeResolventData → SlitPlaneStieltjesExtension)
    (bridgeA : SlitPlaneStieltjesExtension → RiemannHypothesis)
    (d : PrimeResolventData) : RiemannHypothesis :=
  bridgeA (bridgeC d)

section ZeroModelCertificates

variable {ι : Type*}

/-- Truncated-zero-model weights: `u γ = 1 / (γ² + x₀)`. -/
noncomputable def zeroModelWeight (x₀ : ℝ) (γ : ℝ) : ℝ := 1 / (γ ^ 2 + x₀)

/-- Truncated-zero-model positions: `v γ = x₀ / (γ² + x₀) ∈ (0, 1]`. -/
noncomputable def zeroModelAtom (x₀ : ℝ) (γ : ℝ) : ℝ := x₀ / (γ ^ 2 + x₀)

/-- The Hankel forms of any finite truncated zero model are PSD — the
`H_N ⪰ 0` half of the Card-8 certificates, proved (rather than computed)
for the discrete model.  A certified negative Hankel value for the true
`b_n(x₀)` therefore cannot come from any positive atomic configuration. -/
theorem hankelForm_nonneg_of_zeroModel (s : Finset ι) (γ : ι → ℝ) {x₀ : ℝ}
    (hx₀ : 0 < x₀) (N : ℕ) (c : Fin (N + 1) → ℝ) :
    0 ≤ hankelForm
        (atomicMoment s (fun k => zeroModelWeight x₀ (γ k))
          (fun k => zeroModelAtom x₀ (γ k))) N c := by
  refine hankelForm_nonneg_of_atomic s _ (fun k _ => ?_) N c
  unfold zeroModelWeight
  positivity

/-- The `L_N ⪰ 0` half (`θ = 1`): the zero-model atoms satisfy `v ≤ 1`,
so the shifted forms `b_{i+j} - b_{i+j+1}` are PSD as well. -/
theorem hankelForm_L_nonneg_of_zeroModel (s : Finset ι) (γ : ι → ℝ) {x₀ : ℝ}
    (hx₀ : 0 < x₀) (N : ℕ) (c : Fin (N + 1) → ℝ) :
    0 ≤ hankelForm
        (fun n => 1 * atomicMoment s (fun k => zeroModelWeight x₀ (γ k))
              (fun k => zeroModelAtom x₀ (γ k)) n
            - atomicMoment s (fun k => zeroModelWeight x₀ (γ k))
              (fun k => zeroModelAtom x₀ (γ k)) (n + 1)) N c := by
  refine hankelForm_theta_nonneg_of_support s (fun k _ => ?_) (fun k _ => ?_) N c
  · unfold zeroModelWeight
    positivity
  · unfold zeroModelAtom
    rw [div_le_one (by positivity)]
    exact le_add_of_nonneg_left (sq_nonneg (γ k))

end ZeroModelCertificates

end RiemannResolvent
