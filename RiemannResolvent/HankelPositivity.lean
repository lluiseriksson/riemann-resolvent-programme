/-
Copyright (c) 2026 Lluis Eriksson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Lluis Eriksson
-/
import Mathlib.Analysis.SpecificLimits.Basic

/-!
# Hankel positivity for atomic moment sequences

The finite, fully proved layer of the prime-resolvent programme: moments of
a finite atomic measure with nonnegative weights have positive semidefinite
Hankel quadratic forms, and a support bound `v ≤ θ` makes the shifted form
`θ b_{i+j} - b_{i+j+1}` PSD as well.

This is the formal bridge to the numerical falsifier satellite
`hausdorff-certificates` (knowledge-tree node
`bridge.hausdorff_moment_certificates`): its exact/interval `H_N`, `L_N`,
`L_N^θ` certificates compute exactly these quadratic forms, and this file
proves the direction "positive measure ⇒ PSD" that makes a certified
negative eigenvalue a genuine finite falsifier of the measure's existence.
It also discharges the discrete (atomic) form of that node's Lean target
`hankelPSD_of_coercive`.
-/

namespace RiemannResolvent

open Finset

variable {ι : Type*}

/-- Moments of a finite atomic measure `μ = ∑_{k ∈ s} u k · δ_{v k}`:
`atomicMoment s u v n = ∑ k ∈ s, u k * v k ^ n`. -/
def atomicMoment (s : Finset ι) (u v : ι → ℝ) (n : ℕ) : ℝ :=
  ∑ k ∈ s, u k * v k ^ n

/-- Hankel quadratic form `∑ i j, c i * c j * b (i + j)` of a moment
sequence `b` at depth `N`. -/
def hankelForm (b : ℕ → ℝ) (N : ℕ) (c : Fin (N + 1) → ℝ) : ℝ :=
  ∑ i : Fin (N + 1), ∑ j : Fin (N + 1), c i * c j * b (i.1 + j.1)

/-- Structure identity: the Hankel form of atomic moments is a weighted sum
of squares, `∑ k ∈ s, u k * (∑ i, c i * v k ^ i) ^ 2`. -/
theorem hankelForm_atomic_eq_sum_sq (s : Finset ι) (u v : ι → ℝ) (N : ℕ)
    (c : Fin (N + 1) → ℝ) :
    hankelForm (atomicMoment s u v) N c
      = ∑ k ∈ s, u k * (∑ i : Fin (N + 1), c i * v k ^ i.1) ^ 2 := by
  unfold hankelForm atomicMoment
  calc ∑ i : Fin (N + 1), ∑ j : Fin (N + 1),
          c i * c j * ∑ k ∈ s, u k * v k ^ (i.1 + j.1)
      = ∑ i : Fin (N + 1), ∑ j : Fin (N + 1), ∑ k ∈ s,
          c i * c j * (u k * v k ^ (i.1 + j.1)) := by
        refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
        rw [Finset.mul_sum]
    _ = ∑ i : Fin (N + 1), ∑ k ∈ s, ∑ j : Fin (N + 1),
          c i * c j * (u k * v k ^ (i.1 + j.1)) := by
        refine Finset.sum_congr rfl fun i _ => ?_
        exact Finset.sum_comm
    _ = ∑ k ∈ s, ∑ i : Fin (N + 1), ∑ j : Fin (N + 1),
          c i * c j * (u k * v k ^ (i.1 + j.1)) := Finset.sum_comm
    _ = ∑ k ∈ s, u k * (∑ i : Fin (N + 1), c i * v k ^ i.1) ^ 2 := by
        refine Finset.sum_congr rfl fun k _ => ?_
        rw [sq, Finset.sum_mul_sum, Finset.mul_sum]
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [Finset.mul_sum]
        refine Finset.sum_congr rfl fun j _ => ?_
        rw [pow_add]
        ring

/-- **Hankel PSD from positivity** (atomic Hausdorff direction): if all
weights are nonnegative, every Hankel quadratic form of the atomic moment
sequence is nonnegative.  A certified negative value at any single `(N, c)`
therefore refutes the existence of the representing positive measure. -/
theorem hankelForm_nonneg_of_atomic (s : Finset ι) {u : ι → ℝ} (v : ι → ℝ)
    (hu : ∀ k ∈ s, 0 ≤ u k) (N : ℕ) (c : Fin (N + 1) → ℝ) :
    0 ≤ hankelForm (atomicMoment s u v) N c := by
  rw [hankelForm_atomic_eq_sum_sq]
  exact Finset.sum_nonneg fun k hk => mul_nonneg (hu k hk) (sq_nonneg _)

/-- Weight-shift identity behind the support test:
`θ * b n - b (n+1)` is the `n`-th moment of the reweighted atoms
`u k * (θ - v k)` at the same positions. -/
theorem theta_shift_eq_atomicMoment (s : Finset ι) (u v : ι → ℝ) (θ : ℝ)
    (n : ℕ) :
    θ * atomicMoment s u v n - atomicMoment s u v (n + 1)
      = atomicMoment s (fun k => u k * (θ - v k)) v n := by
  unfold atomicMoment
  rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [pow_succ]
  ring

/-- **Support certificate direction** (`L_N^θ ⪰ 0`): if the weights are
nonnegative and every atom satisfies `v k ≤ θ`, the shifted Hankel form
`∑ i j, c i * c j * (θ * b (i+j) - b (i+j+1))` is nonnegative.  The case
`θ = 1` is the classical `L_N` of the Hausdorff pair; on the Yang–Mills
side, `θ = x₀ / (cclaim + x₀)` turns this into the finite coercivity test
of the `hausdorff-certificates` satellite. -/
theorem hankelForm_theta_nonneg_of_support (s : Finset ι) {u v : ι → ℝ}
    {θ : ℝ} (hu : ∀ k ∈ s, 0 ≤ u k) (hv : ∀ k ∈ s, v k ≤ θ) (N : ℕ)
    (c : Fin (N + 1) → ℝ) :
    0 ≤ hankelForm
        (fun n => θ * atomicMoment s u v n - atomicMoment s u v (n + 1)) N c := by
  have hshift : (fun n => θ * atomicMoment s u v n - atomicMoment s u v (n + 1))
      = atomicMoment s (fun k => u k * (θ - v k)) v := by
    funext n
    exact theta_shift_eq_atomicMoment s u v θ n
  rw [hshift]
  exact hankelForm_nonneg_of_atomic s v
    (fun k hk => mul_nonneg (hu k hk) (sub_nonneg.mpr (hv k hk))) N c

end RiemannResolvent
