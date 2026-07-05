# Mother Interface Digest

Snapshot: v0.1.0 interface, last audited against public `main` HEAD
`a08dbe82bcaa9e9d17ce112ae671b3473c99e867`.

CI heartbeat for that audited HEAD: workflow `ci`, run
`28755325020`, conclusion `success` on 2026-07-05.

Purpose: give THE-ERIKSSON-PROGRAMME and the knowledge-tree tooling a
small, exact interface map for this sibling repository. This is an
infrastructure digest only. It does not claim RH, Yang-Mills progress,
operator construction, bridge discharge, or any dependency edge from the
mother repo to this repo.

## Import Surface

Lean entrypoint:

```lean
import RiemannResolvent
```

Namespace:

```lean
namespace RiemannResolvent
```

Files:

- `RiemannResolvent/HankelPositivity.lean`: atomic moment and Hankel PSD
  infrastructure.
- `RiemannResolvent/Program.lean`: Riemann-xi objects, programme data, and
  the two carried-input assemblies.
- `RiemannResolvent.lean`: public import aggregator.

## Programme Objects

Defined in `RiemannResolvent/Program.lean` (ASCII names below; source
uses the standard Lean notations `ℂ`, `ℝ`, `ℕ`, and `→`):

- `riemannXi (s : Complex) : Complex`
- `xiResolventTarget (x : Real) : Complex`
- `SlitPlaneStieltjesExtension : Prop`
- `PrimeResolventData : Type`

`PrimeResolventData` fields, transcribed from the source:

```lean
S : ℕ → ℝ → ℝ
P : ℕ → ℝ → ℝ
x₀ : ℝ
hx₀ : 0 < x₀
δ : ℝ
hδ : 0 < δ
B : ℝ
hB : (1 / 2 + δ) ^ 2 < B
uniform_bound : ∃ C : ℝ, ∀ j : ℕ, S j x₀ ≤ C
approx : ∀ ε : ℝ, 0 < ε → ∃ N : ℕ, ∀ j : ℕ, N ≤ j →
  ∀ x : ℝ, x ∈ Set.Icc ((1 / 2 + δ) ^ 2) B → |S j x - P j x| ≤ ε
```

The marked point is named `x₀` in the Lean structure. Do not erase it in
downstream summaries.

## Carried-Input Assemblies

Defined in `RiemannResolvent/Program.lean`:

```lean
theorem riemannHypothesis_of_slitPlaneExtension
    (bridgeA : SlitPlaneStieltjesExtension → RiemannHypothesis)
    (h : SlitPlaneStieltjesExtension) : RiemannHypothesis
```

```lean
theorem riemannHypothesis_of_primeResolventApproximation
    (bridgeC : PrimeResolventData → SlitPlaneStieltjesExtension)
    (bridgeA : SlitPlaneStieltjesExtension → RiemannHypothesis)
    (d : PrimeResolventData) : RiemannHypothesis
```

Consumption rule: these theorems are compiled assemblies with explicitly
named carried inputs. They are useful as dependency-graph anchors, not as
discharges of `bridgeA` or `bridgeC`.

## Hankel/Falsifier Interface

Defined in `RiemannResolvent/HankelPositivity.lean`:

- `atomicMoment (s : Finset ι) (u v : ι → ℝ) (n : ℕ) : ℝ`
- `hankelForm (b : ℕ → ℝ) (N : ℕ) (c : Fin (N + 1) → ℝ) : ℝ`
- `hankelForm_atomic_eq_sum_sq`
- `hankelForm_nonneg_of_atomic`
- `theta_shift_eq_atomicMoment`
- `hankelForm_theta_nonneg_of_support`

Defined in `RiemannResolvent/Program.lean`:

- `zeroModelWeight`
- `zeroModelAtom`
- `hankelForm_nonneg_of_zeroModel`
- `hankelForm_L_nonneg_of_zeroModel`

Mother-facing use: cite these as the discrete atomic direction behind the
Hausdorff moment falsifier interface, especially the direction "positive
atomic measure implies Hankel PSD". This is a local infrastructure result,
not a proof of the analytic prime-resolvent criterion.

## Frontier Not To Repackage

The following must stay as explicit frontier items, not structure fields,
renamed hypotheses, or wrapper criteria:

- `bridgeA : SlitPlaneStieltjesExtension → RiemannHypothesis`
- `bridgeC : PrimeResolventData → SlitPlaneStieltjesExtension`
- `primeTail_bound`
- source tasks T1, T2, T3, T4 from `HYPOTHESIS_FRONTIER.md`

`T3` is the kill switch: a failure of the uniform one-point bound kills the
concrete operator route while leaving the abstract bookkeeping honest.

## Suggested Knowledge-Tree Consumption

- Register this repository as `programme.riemann_resolvent`, a sibling
  programme repo, not as a Yang-Mills satellite.
- Keep relation to THE-ERIKSSON-PROGRAMME as `shares_method` only.
- Use the assemblies as compiled graph anchors with carried inputs named
  in the edge metadata.
- Use the Hankel interface as a partial discharge for the discrete atomic
  form of the Hausdorff PSD falsifier semantics.
- Do not promote confidence labels from this digest alone.

Verification expected for consumers:

```bash
lake build
./scripts/check_axioms.sh
! grep -rnE "\bsorry\b|\badmit\b|\bnative_decide\b" --include="*.lean" RiemannResolvent RiemannResolvent.lean
```
