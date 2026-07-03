# ROADMAP — commit sequence

Merge gate for every commit: `lake build` clean + axiom audit + sorry grep
+ `HYPOTHESIS_FRONTIER.md` updated in the same commit.

- **C1 (this release, v0.1.0).** Programme objects against Mathlib's zeta
  (`riemannXi`, `xiResolventTarget`, `SlitPlaneStieltjesExtension`,
  `PrimeResolventData`), assemblies with named carried inputs, and the
  fully proved Hankel-positivity falsifier bridge with the zero-model
  instances. DONE.
- **C2 — `primeTail_bound`.** Formalize the omitted-prime tail
  `X^{-δ}(log X/δ + 1/δ²)/(1+2δ)` by sum–integral comparison. Blocked on
  re-extracting source §6 verbatim (AGENTS rule 6): the sum being bounded
  and each inequality step must come from the source, not be reverse-
  engineered from the displayed constant.
- **C3 — discharge `bridgeA`.** Slit-plane extension ⇒ RH via the
  completed zeta, identity principle and the reflection structure; Mathlib
  provides the functional equation and locally uniform holomorphic limits.
  Source estimate 2–4 months.
- **C4 — Stieltjes compactness.** Compactness of Stieltjes families from
  a single pointwise bound (Helly/normal-families layer). 4–8 months; the
  hardest abstract block.
- **C5 — discharge `bridgeC`.** C2 + C4 + locally uniform limits assemble
  Theorem C's analytic core; abstract spectral-operator interface only
  (no `D_{λ,N}`). Abstract core complete at 8–16 months total.
- **C6+ — concrete operators.** Weil-form operators `D_{λ,N}` under gates
  V4 (CCM; Connes–van Suijlekom), tasks T1–T4, with T3 as kill switch.
  Second project; +2–4 years. Numerical falsifier support: extend the
  `hausdorff-certificates` pipeline (more zeros → refutation-grade depth
  grows like log T / T).
