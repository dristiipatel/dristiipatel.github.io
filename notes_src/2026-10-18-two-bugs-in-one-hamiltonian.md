---
title: "Two bugs in one Hamiltonian: eigenvector tracking and a missing cos^2(theta13)"
date: 2026-10-18
summary: "Overlap-based eigenvector tracking needs the flavour basis and a real one-to-one assignment, and a 0.1% residual that did not shrink with resolution was a modelling error."
tags: [workflow, numerics, verification, sterile-neutrinos]
draft: false
---

Context: the [sterile post](/notes/sterile-neutrino-in-the-sun/) wrote the three-level Hamiltonian, and the [adiabaticity post](/notes/adiabaticity-landau-zener/) explained why the neutrino follows a matter eigenstate. A numerical solver needs a way to say, at every radial step, which eigenvector is "the one that started as $\nu_e$-like". Two bugs lived in that machinery.

## Bug 1a: the wrong basis

Dense diagonalization returns eigenvectors in arbitrary order and phase. Tracking by overlap between successive steps only makes sense if the basis vectors are physical flavour states. An early version built the active sector in a basis ordered by mass content, which makes the question "which eigenvector looks most like $\nu_e$?" meaningless.

**The check that caught it.** In the vacuum limit at the solar surface, the $\nu_e$ content of the lightest eigenstate must be readable off the mixing matrix: $\cos^2\theta_{12}\cos^2\alpha=0.685$. The buggy Hamiltonian gave $0.65$. A difference of $0.035$ is too large for numerical noise, and the tracker was silently mislabelling states near the avoided crossing.

## Bug 1b: greedy assignment is not a permutation

The first tracker matched states with a row-wise `argmax` on the overlap matrix. Nothing stops two rows from choosing the same column:

```python
import numpy as np
from scipy.optimize import linear_sum_assignment

overlap = np.array([[0.90, 0.80, 0.00],
                    [0.85, 0.10, 0.10],
                    [0.00, 0.20, 0.90]])

print(overlap.argmax(axis=1))              # [0 0 2]  state 0 claimed twice, state 1 lost
rows, cols = linear_sum_assignment(-overlap)
print(cols)                                # [1 0 2]  a valid one-to-one assignment
```

The Hungarian algorithm returns the globally best one-to-one assignment. At the benchmark parameters the two methods agreed bit for bit, which is exactly why this bug survived. Away from the benchmark (smaller mixing angle, thinner resonance layer), the greedy method locked onto the wrong branch and reproduced the same wrong value across five consecutive doublings of the step count.

**The lesson about convergence tests.** "The answer does not change when the step count doubles" is not evidence of convergence in general. It only holds in regions that have already been tested. A convergence check that requires several consecutive doublings to agree is better, and still a heuristic. It is documented as one.

## Bug 2: the missing projection

The $(\nu_e,\nu_e)$ entry of $H$ used the bare $V_e$, while the reference standard-model formula used $V_e\cos^2\theta_{13}$ (see the [MSW post](/notes/msw-survival-probability-sun/)).

**The check that caught it.** Setting the sterile mixing angle $\alpha\to0$ must reproduce the standard formula exactly. A residual of $0.1$ to $0.6\%$ in $P_{ee}$ remained. Numerical error shrinks when the grid is refined. This residual did not, which is the signature of a modelling inconsistency.

**Why a 2% potential error matters.** Near a resonance, a small shift in the potential becomes a larger shift in the resonance position. A correction that looks cosmetic can move a spectral feature noticeably, so the fix was a real change to the physics, not a cleanup.

**How the placement was verified.** Instead of copying the factor by analogy, it was checked against the general $N$-neutrino formalism of Giunti and Li: $|U_{e1}|^2-|U_{e2}|^2=\cos^2\theta_{13}\cos2\theta_{12}$, with no suppression on the sterile-row elements, which carry no $\theta_{13}$ rotation. The factor belongs on the $\nu_e$ charged-current term and nowhere else.

## What is still unclear

The automatic convergence check is a heuristic. Anyone extending the parameter grid to smaller mixing angles than the ones tested should compare against a very fine fixed grid directly.
