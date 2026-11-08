---
title: "Five habits for checking whether a calculation is right"
date: 2026-10-19
summary: "Practical checks, with small worked examples, that work for a lab report, a problem set or a research code."
tags: [methods, computational-physics, intro]
draft: false
---

> A calculation that runs without errors can still be wrong. Five checks help catch many problems: test a limit with a known answer, wiggle each input and see whether the output moves, check conservation through the whole pipeline, compare with a different method, and compare one absolute number with the literature.

## 1. Test a limit where the answer is known

Set a parameter to zero or infinity and see whether the code collapses to a textbook formula. In a solver for a three-state neutrino problem, setting the mixing with the extra state to zero must reproduce the standard two-flavour result exactly. A residual of 0.1 to 0.6% remained, and it did not shrink when the grid was refined. Numerical error shrinks with a finer grid and a modelling mistake does not. That difference pointed to a missing factor in the Hamiltonian.

## 2. Wiggle every input

Change each input by 10% and check that the output moves in a sensible way. An input that changes nothing is a warning.

```python
def wiggle(f, params, name, rel=0.1):
    """Change in output when one parameter is changed by rel."""
    base = f(**params)
    p2 = dict(params); p2[name] = params[name] * (1 + rel)
    return f(**p2) - base
```

A cross-check function once accepted a mass-splitting argument and never used it. It agreed with the standard curve only because it could not represent anything else. One call to `wiggle` would have shown a zero response.

## 3. Check conservation in the code the analysis uses

If a step only redistributes things (events into bins, probability across energies), the total must be unchanged. It is important to test the function that the analysis calls, at the resolution it uses. A rebinning helper lost about 2.4% of events at every bin edge, while a conservation test written for a different step still passed.

## 4. Use a completely different method to validate

A second calculation is only useful if it can fail in a different way. An event-by-event Monte Carlo that sampled the same distributions agreed with a deterministic integration everywhere except by a uniform 2.5%, and that exposed the rebinning bug. A second run of the same integration code would have reproduced the bug.

## 5. Compare one absolute number with the literature

Relative comparisons hide normalization mistakes. A predicted event count was twice the published value for a whole energy range, even though it was for a narrower range. A part larger than the whole was a sign that something, here a missing fiducial-volume cut, was not accounted for.

## When a check disagrees

The check needs the same care as the main calculation. In one case a new cross-check disagreed by a large amount, and the error turned out to be in the check, a mixing angle computed with `arctan` instead of `arctan2` that failed at the crossing. In another, the main code was wrong. Disagreement says that one of them is off and does not say which.

## Try it

Try habits 1 and 2 on a recent piece of problem-set code. It takes about ten minutes, and it often finds something.

## Going deeper

Longer write-ups of these cases: [two bugs in one Hamiltonian](/notes/two-bugs-in-one-hamiltonian/), [when a cross-check disagrees](/notes/when-the-cross-check-disagrees/), and [a bug in ten lines](/notes/a-two-percent-bug-in-ten-lines/).
