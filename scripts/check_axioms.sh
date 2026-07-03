#!/usr/bin/env bash
# Every public declaration must depend only on propext / Classical.choice /
# Quot.sound: no sorry, no extra axioms. Run from repo root or scripts/.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=$(lake env lean --stdin << 'LEAN'
import RiemannResolvent
open RiemannResolvent
#print axioms hankelForm_atomic_eq_sum_sq
#print axioms hankelForm_nonneg_of_atomic
#print axioms theta_shift_eq_atomicMoment
#print axioms hankelForm_theta_nonneg_of_support
#print axioms riemannHypothesis_of_slitPlaneExtension
#print axioms riemannHypothesis_of_primeResolventApproximation
#print axioms hankelForm_nonneg_of_zeroModel
#print axioms hankelForm_L_nonneg_of_zeroModel
LEAN
)
echo "$OUT"
if echo "$OUT" | grep -Eq "sorryAx|ofReduceBool|ofReduceNat"; then
  echo "FORBIDDEN AXIOM DETECTED"; exit 1
fi
echo "AXIOM CHECK OK: only propext / Classical.choice / Quot.sound"
