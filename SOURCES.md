# Sources and verification gates

## Primary source

`source.ideas5_2026_07` (ideas5.txt, 130425 bytes, sha256
`28f00d12ff6cfa5228400d70fe92d3bee530ac2e6c0078939da5b09e489aabd8`,
curated in `batch-2026-07-03-ym-unblock`): the prime-resolvent Stieltjes
criterion — Theorems A/B/C, the four open tasks, the Lean architecture
recommendation and the 7.40/10 self-assessment. Theorem statements in this
repository's docstrings are transcribed from §2–§3 and §7 of that source.
Section §6 (omitted-prime bound derivation) is pending verbatim
re-extraction before C2 (AGENTS rule 6).

## Gates (nothing promotes to `literature` without them)

- **V4 — CCM / Connes–van Suijlekom** (`verify.ccm_operators`): the
  Connes–Consani–Moscovici operators `D_log^{(λ,N)}` (ground-state
  simplicity and parity hypotheses; determinant-to-Ξ convergence status)
  and the Connes–van Suijlekom reality theorem (lower-bounded self-adjoint
  operator, simple isolated minimal eigenvalue, even eigenfunction).
  These sustain tasks T1–T2. Resolve against the arXiv papers before any
  operator-layer commit.
- **V3 — novelty of the single-point criterion**
  (`verify.hausdorff_novelty`, owned by node
  `bridge.hausdorff_moment_certificates`): moment-problem RH criteria
  already exist; nothing in this repository depends on novelty.
- **Falsifier gates V-A / V-B** (owned by `hausdorff-certificates`):
  Trudgian constants and zero-table cross-check condition any refutation
  claim coming from the numerical arm.

## Classical background (no gate)

Hausdorff moment problem (Shohat–Tamarkin 1943); Hadamard factorization
and the completed zeta (as formalized in Mathlib v4.31.0).
