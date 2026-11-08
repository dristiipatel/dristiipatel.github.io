---
title: "A numerical artifact that looks like physics: step-size resonance in a Magnus integrator"
date: 2026-10-25
summary: "A piecewise-constant propagator gave wrong answers at isolated step counts. How it was found and what the fix was."
tags: [workflow, numerics, TDSE]
draft: false
---

Context: the [cross-check post](/notes/when-the-cross-check-disagrees/) mentioned a direct time-dependent Schrodinger integration used as an independent solver. This post is about a problem found in that integrator.

## The method

Starting from a pure $\nu_e$ state in the flavour basis, the wave function is evolved with

$$i\frac{d\psi}{dr}=H(r)\,\psi$$

using piecewise-constant steps: over each step $H$ is frozen at its midpoint value and the state is multiplied by $e^{-iH\,\Delta r}$. This is a Magnus integrator of order one. It is cheap and keeps the state normalized exactly.

Two practical details:

- **Scale disparity.** Near the production point the matter potential is orders of magnitude larger than the off-diagonal couplings. Subtracting the instantaneous minimum eigenvalue from $H$ before exponentiating removes a global phase. That phase cancels in every final probability, so this is an exact acceleration and not an approximation.
- **Observable.** The surface state is projected on the vacuum mass eigenstates, and the probabilities are summed incoherently. This is justified because the Sun-Earth vacuum phase accumulated over about 1 AU averages to zero for any realistic detector.

## The artifact

With uniform steps, the step size can land close to a rational multiple of the local oscillation half-period. Phase errors then add up coherently across many steps instead of averaging out. The result is a wrong answer at specific, isolated step counts, and a correct one at the neighbouring counts. A scan over $N$ in the 1 to 8 MeV range showed bad values at $N=2000,\,4000,\,5000,\,6000,\,8000,\,10000$ and $12000$ (at one or more energies each), and a stable result at $N=14\,000$.

This has nothing to do with the physical MSW resonance. It is a property of the numerical scheme. The two are easy to confuse because both appear as features at specific energies.

## How it was found

By running the same physical point at many step counts, not only at "a large number". A sketch of the diagnostic:

```python
import numpy as np

def scan_steps(pee_func, energies, n_list):
    """pee_func(E, n_steps) -> P_ee.  Returns array [len(n_list), len(energies)]."""
    return np.array([[pee_func(E, n) for E in energies] for n in n_list])

# Then look for rows (values of N) that deviate from their neighbours:
# results = scan_steps(my_tdse, np.linspace(1, 8, 36), [2000, 2500, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 14000])
# spread = np.ptp(results, axis=0)       # per-energy spread across N
# np.argmax(np.abs(results - np.median(results, axis=0)), axis=0)   # which N is the outlier at each energy
```

## What to take away

- A convergence study that doubles $N$ from one starting point can miss bad values and still look converged.
- A smooth-looking result as a function of energy at one fixed $N$ is not evidence that $N$ is safe.
- Higher-order Magnus terms or a non-uniform step grid would be better fixes. Here a fixed $N$ that was checked to be stable was used instead, and the choice is documented.

## What is still unclear

The chosen value of $N$ was confirmed over the energy range and parameters tested. A new region of parameter space calls for a new scan.
