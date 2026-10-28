---
title: "A 2.5% bug in ten lines: rebinning, conservation tests, and a Monte Carlo that disagreed"
date: 2026-10-28
summary: "A rebinning helper silently dropped slivers at every bin edge. The conservation test passed because it tested the wrong function."
tags: [workflow, numerics, Monte-Carlo, verification]
draft: false
---

Context: an event-rate pipeline of the type described in the [kinematics post](/notes/from-neutrino-energy-to-electron-energy/) ends by summing a continuous spectrum into a handful of analysis bins. That last step hid a bug that survived several rounds of review.

## The cross-check that exposed it

A second pipeline was written on purpose to be different. Instead of Gauss-Legendre quadrature, weighted production averaging and grid convolution, it drew individual pseudo-events: $E_\nu$ by inverse-CDF sampling, $T_e$ by sampling the tabulated kernel, and the reconstructed energy by per-event Gaussian smearing, then histogrammed into the same bins. Both pipelines shared the validated $P_{ee}$ solver, flux, cross section and production profile, so the comparison tested the binning machinery and nothing else.

The two disagreed, by far more than the Monte Carlo's own statistical error. The first suspects were checked and ruled out: the coarseness of the kernel bucketing in the Monte Carlo, and a resolution floor applied in the deterministic code. Neither changed the answer.

## The pattern in the numbers

A bin-by-bin comparison showed the Monte Carlo running uniformly 2.3 to 2.6% above the deterministic result in every bin. A uniform offset is a normalization problem, not a shape problem. A single unbroken trapezoidal integral of the post-convolution spectrum reproduced the pre-convolution total to 0.000%, so the convolution was fine. The loss was in the last step.

## The bug

```python
def _rebin(x, y, edges):
    out = np.zeros(len(edges) - 1)
    for i in range(len(edges) - 1):
        m = (x >= edges[i]) & (x <= edges[i + 1])
        out[i] = np.trapezoid(y[m], x[m]) if m.sum() >= 2 else 0.0
    return out
```

This integrates only the grid points that fall inside each bin, and never evaluates the spectrum at the bin edges. The spectrum grid and the bin edges are independent samplings of the same range, so their points almost never coincide. At each internal boundary a sliver of area between the true edge and the nearest grid point is thrown away.

A self-contained reproduction, with a smooth test spectrum, 400 grid points and 10 bins:

```python
x = np.linspace(0.05, 5.0, 400); y = x**2 * np.exp(-x / 1.2)
edges = np.linspace(0.05, 5.0, 11)
# total by one trapezoid pass: 2.7140
# sum over bins with the buggy _rebin: 2.6486   (2.4% lost)
# sum over bins with the fixed _rebin: 2.7140
```

The fix interpolates the spectrum at each edge and integrates over `[edge_low, interior points, edge_high]`:

```python
def _rebin(x, y, edges):
    out = np.zeros(len(edges) - 1)
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        m = (x > lo) & (x < hi)
        x_bin = np.concatenate(([lo], x[m], [hi]))
        y_bin = np.concatenate(([np.interp(lo, x, y)], y[m], [np.interp(hi, x, y)]))
        out[i] = np.trapezoid(y_bin, x_bin)
    return out
```

## Why the conservation test missed it

The earlier conservation test integrated the convolved spectrum in one piece. That checks the kernel, which was correct. It did not exercise `_rebin` at its production resolution. A test that passes for the wrong function gives confidence that does not belong to the code it was written for.

## Three habits from this

1. **Test the path production uses.** Conservation should be checked from the first array to the last number that gets reported.
2. **A different method finds bugs that a re-run cannot.** Had the Monte Carlo reused any of the deterministic binning, it would have reproduced the bug and agreed.
3. **Copy-pasted helpers multiply bugs.** The same function had been pasted into three other scripts, and a separate recurrence turned up later in a different comparison script. A shared module would have meant one fix.

After the fix, the deterministic and Monte Carlo pipelines agreed to within the Monte Carlo's own noise.

## What is still unclear

Whether the remaining small differences between pipelines are purely statistical can only be settled with more replicates. The comparison to date is consistent with statistical noise, not proof of it.
