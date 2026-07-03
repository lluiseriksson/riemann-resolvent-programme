# AGENTS.md — rules for agents working on this repository

Mirrored from THE-ERIKSSON-PROGRAMME; deviations require an explicit user
instruction in the task.

1. **Scope contract first.** No commit may claim RH, an operator
   construction, or the analytic bridges. Conditional results name every
   carried input in the signature.
2. **Anti-wrapper audit.** `bridgeA`, `bridgeC`, `primeTail_bound` and
   T1–T4 must be *discharged*, never introduced as fields of structures,
   abstract "criteria", or renamed hypotheses. A PR whose net effect is to
   relocate a carried input is rejected regardless of size.
3. **No confidence promotion without auditable reason.** Evidence labels
   in the knowledge tree change only with a compiled proof, a verified
   source (gates in `SOURCES.md`), or an executed falsifier run.
4. **Falsifiers mandatory.** Any new claim about the programme carries its
   falsifier or abandonment condition. The standing falsifier is the
   `hausdorff-certificates` pipeline: a certified negative `H_N`/`L_N`
   eigenvalue for the true `b_n(x₀)` refutes RH and this programme.
5. **Zero sorry, audited axioms.** `lake build` clean;
   `scripts/check_axioms.sh` must report only `propext`,
   `Classical.choice`, `Quot.sound`. Source-level gate:
   `grep -rnE "\bsorry\b|\badmit\b|\bnative_decide\b" --include="*.lean" .`
   must be empty.
6. **Source fidelity.** Theorem statements A/C are transcribed from the
   curated source (ideas5, sha256 `28f00d12ff6c...9aabd8`); do not
   "improve" a statement without a new curation record. `primeTail_bound`
   (source §6) must be re-extracted verbatim before formalization — never
   reconstructed from the displayed bound alone.
7. **Shared lemmas are vendored, not required.** General lemmas live in
   `physmath-lean-lemmas`; if one is needed here, vendor the single file
   and cite the satellite. No `[[require]]` beyond mathlib.
8. **Sibling etiquette.** Nothing here enters THE-ERIKSSON-PROGRAMME's
   dependency tree, and nothing from there is assumed. The only shared
   objects are methods (`edge.shared_resolvent_library.ym_riemann`).
9. **Before claiming a discharge**, check the declaration against this
   repo's registry (`grep` + `#print axioms`) at current HEAD, update
   `HYPOTHESIS_FRONTIER.md` in the same commit, and record the run in the
   knowledge tree's Reproducible Run Ledger.
