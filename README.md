# riemann-resolvent-programme

A **sibling programme** to [THE-ERIKSSON-PROGRAMME](https://github.com/lluiseriksson/THE-ERIKSSON-PROGRAMME)
(Yang–Mills), not an appendix of it: same discipline — a sorry-free,
axiom-audited Lean core of *assemblies*, explicitly named *carried inputs*
playing the role `hRpoly` plays there, an honest `HYPOTHESIS_FRONTIER.md`,
mandatory falsifiers — applied to the **prime-resolvent Stieltjes
criterion for the Riemann Hypothesis** (knowledge-tree node
`problem.prime_resolvent_stieltjes_criterion`, Bridge Card 9; source:
ideas5, self-assessed 7.40/10).

The two programmes are related by `shares_method` **only**. Any
implication RH ⇒ YM or YM ⇒ RH was explicitly rejected at curation
(`discard.rh_ym_equivalence`): what is shared is a formal library of
resolvents, Stieltjes transforms, complete monotonicity and moment
certificates — plus the abstract endpoint "base positivity minus
accumulated multiscale defect > 0".

## The observable

Replace the convergence of full spectral determinants by the positive,
one-point observable

```
S_j(x) = (1/2) Tr (D_j² + x I)⁻¹,        𝒮_Ξ(x) = (1/(2√x)) (ξ'/ξ)(1/2 + √x),
```

where under RH the Hadamard factorization gives
`𝒮_Ξ(x) = ∑_{γ>0} 1/(γ² + x)` for `x > 1/4` — the Stieltjes transform of
the positive zero measure `ν_Ξ = ∑ δ_{γ²}`. Why this endpoint is better
than determinants (source §9): it eliminates determinant normalizations,
turns the problem into a **positive** one, damps the ultraviolet spectrum,
and admits perturbation estimates.

## The two theorems the programme rests on (source §3, §7)

**Theorem A (Stieltjes extension criterion).** With
`Ω = ℂ ∖ (-∞, 0]`: RH is equivalent to `𝒮_Ξ` being the restriction to
`x > 1/4` of a Stieltjes function `S(w) = ∫ dν(t)/(t+w)` with `ν ≥ 0` and
`∫ dν/(1+t) < ∞`. For the **decisive direction toward RH it suffices**
that `𝒮_Ξ` admits *any* holomorphic extension to `Ω` agreeing with it on
an open interval `I ⊂ (1/4, ∞)`.

**Theorem C (prime-resolvent criterion).** Let `D_j` be self-adjoint with
discrete symmetric spectrum, `S_j` as above, `X_j → ∞`, `δ > 0`,
`B > (1/2 + δ)²`, `I_{δ,B} = [(1/2+δ)², B]`. If `sup_j S_j(x₀) < ∞` for
some `x₀ > 0` and `sup_{x ∈ I_{δ,B}} |S_j(x) − P_{X_j}(x)| → 0`, then RH —
via `sup |S_j − 𝒮_Ξ| ≤ sup |S_j − P_{X_j}| + X_j^{−δ}(log X_j/δ + 1/δ²)/(1+2δ)`.

## What is proved vs carried in v0.1.0

| item | status |
|---|---|
| `hankelForm_atomic_eq_sum_sq`, `hankelForm_nonneg_of_atomic` | **proved** (0 sorry): atomic Hausdorff direction — the formal half of the falsifier |
| `theta_shift_eq_atomicMoment`, `hankelForm_theta_nonneg_of_support` | **proved**: `L_N^θ ⪰ 0` support test (`θ = 1` gives `L_N`; YM coercivity dictionary via `θ = x₀/(c+x₀)`) |
| `hankelForm_nonneg_of_zeroModel`, `hankelForm_L_nonneg_of_zeroModel` | **proved**: Card-8 truncated-zero-model certificates, `H_N`/`L_N` halves |
| `riemannXi`, `xiResolventTarget`, `SlitPlaneStieltjesExtension`, `PrimeResolventData` | **defined** against Mathlib's `completedRiemannZeta`, `Complex.slitPlane`, `RiemannHypothesis` |
| `riemannHypothesis_of_slitPlaneExtension` | **assembly proved**; carried input: `bridgeA` |
| `riemannHypothesis_of_primeResolventApproximation` | **assembly proved**; carried inputs: `bridgeC`, `bridgeA` |
| `bridgeA`, `bridgeC`, tasks T1–T4, `primeTail_bound` | **frontier** — see `HYPOTHESIS_FRONTIER.md` and `ROADMAP.md`; never encoded as vacuous `Prop`s |

Axiom audit: every public declaration depends only on `propext`,
`Classical.choice`, `Quot.sound` (`scripts/check_axioms.sh`, repeated in CI).

## Scope contract (non-negotiable)

This repository proves **assemblies and finite certificates**. It does not
claim RH, any spectral-operator construction, the analytic bridges A/C, or
any progress on the Yang–Mills front. Distance to RH after this release:
unchanged. Every conditional theorem names its carried inputs in its
signature; the anti-wrapper audit of `AGENTS.md` forbids repackaging them.

## Falsifier arm

The numerical falsifier of this programme is the satellite
[hausdorff-certificates](https://github.com/lluiseriksson/hausdorff-certificates)
(node `bridge.hausdorff_moment_certificates`): exact/interval `H_N`, `L_N`,
`L_N^θ` certificates whose "positive measure ⇒ PSD" direction is *proved*
here (`HankelPositivity.lean`). Its executed zeta pipeline (run ledger
`run.2026_07_03.hausdorff_certificates_v0_1_0`) found consistency
`PSD_CERTIFIED` to depth `N = 14` at `x₀ = 1` (truncated measure, Lemma S)
and no refutation; an interval-certified negative eigenvalue of the true
`b_n(x₀)` at any `(N, c)` would refute RH — modulo that satellite's gates
V-A (Trudgian constants) and V-B (zero-table cross-check).

## Build

```bash
lake exe cache get        # toolchain pinned: Lean 4.31.0 + Mathlib v4.31.0
lake build                # 0 errors, 0 sorry (compiles any cache-gap files from source)
./scripts/check_axioms.sh
```

Verified locally against the pinned manifest before the initial commit.

## Source timeline (for calibration, from ideas5 §12)

Abstract core (Ξ + slit-plane criterion + finite Stieltjes transforms +
prime formula and remainder + locally uniform convergence + Stieltjes
compactness): **8–16 months** for one expert; concrete Weil-form operators
`D_{λ,N}`: **+2–4 years**, deliberately deferred (`ROADMAP.md` C6+).

## License

Apache-2.0. See `CITATION.cff`.
