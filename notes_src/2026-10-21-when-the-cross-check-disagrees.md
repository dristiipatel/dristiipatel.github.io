---
title: "When the independent cross-check disagrees: arctan2 and a retracted claim"
date: 2026-10-21
summary: "Two episodes where an independent check misled, and the habits that came out of them."
tags: [workflow, verification, numerics]
draft: false
---

Context: the [architecture post](/notes/verification-first-architecture/) listed independent solvers. An independent check is only useful if its disagreements are interpreted correctly, and two episodes showed how that can go wrong.

## Episode 1: a check that disagreed by 0.2

A cross-check following de Holanda and Smirnov's reduced-Hamiltonian method was added. Its first version disagreed with the primary solver by up to about 0.2 in $P_{ee}$ in the feature region. Taken at face value, that would have been serious evidence against the main result.

Before accepting that, the cross-check's own code was audited. The sterile mixing angle was computed as

```python
theta = 0.5 * np.arctan(2 * offdiag / diag_diff)
```

`arctan` returns values in $(-\pi/2,\pi/2)$, so the half-angle sits in $(-\pi/4,\pi/4)$. At the resonance crossing `diag_diff` changes sign, and the true angle passes through $\pi/4$ and continues beyond it. A one-line comparison shows the problem:

```python
import numpy as np
d = np.array([-1, -0.5, 0.5, 1.0])    # diag_diff across the crossing
off = 0.1
print(0.5 * np.arctan(2 * off / d))   # [-0.099 -0.190  0.190  0.099]   sign flips, angle never passes pi/4
print(0.5 * np.arctan2(2 * off, d))    # [ 1.472  1.381  0.190  0.099]   continuous branch
```

This is the same class of bug (continuity through an avoided crossing) that had been fixed in the primary solver's eigenvector tracking ([previous post](/notes/two-bugs-in-one-hamiltonian/)). Switching to `arctan2` brought the two methods into agreement away from the feature, and to within about 0.01 to 0.02 inside it, which is consistent with the cross-check's own stated approximations (fully adiabatic, no coupling to the upper LMA branch).

**The habit:** a new check that disagrees with the main result gets the same scrutiny as the main result. Disagreement does not tell which side is wrong.

## Episode 2: a check that could not have worked

An earlier perturbative check, based on a formula of Giunti and Li, had been used to argue that a feature in the main solver was a numerical artifact. On inspection, the function accepted a `dm2_01` argument and never used it in its resonance condition. It was structurally incapable of representing the sterile resonance at all, so its "agreement" with the standard curve meant nothing.

The claim was retracted in the code, and a runtime warning was added so that the function cannot silently mislead again.

**The habit:** before trusting a check, change each input and confirm the output moves. A cheap sensitivity test would have exposed the unused argument in seconds.

## Episode 3 (shorter): comparing a projected number against an unprojected one

In the transfer-matrix check from the [adiabaticity post](/notes/adiabaticity-landau-zener/), the adiabatic branch applied the outer $\cos^4\theta_{13}/\sin^4\theta_{13}$ projection and the non-adiabatic branch did not. The offset between them was reported as a non-adiabatic correction. Far from any resonance, where the true correction must be about zero, the offset still appeared, and it was reproduced by working out what an unprojected $P_{ee}$ would look like. After the fix the correction shrank by roughly a factor of ten. The off-diagonal transfer-matrix elements themselves were never affected, since the bug lived in how they were converted into a comparable $P_{ee}$.

**The habit:** test a comparison in a regime where the answer is known to be zero.

## What is still unclear

None of this proves the main solver is right. It shows how the checks were interpreted when they gave uncomfortable answers.
