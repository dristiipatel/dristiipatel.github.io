---
title: "Where does 'N sigma' come from in a counting experiment?"
date: 2026-10-11
summary: "Asimov datasets, chi-squared with nuisance parameters, and why normalization pulls act on the prediction."
tags: [statistics, sensitivity, methods]
draft: false
---

A sensitivity forecast ends with a single number such as "N sigma". This post lays out where that number comes from for a binned counting experiment, and where it is easy to fool oneself.

## The Asimov shortcut

To forecast, there is no real data. Instead, the expected counts under the hypothesis taken as true replace the data (the "Asimov dataset"), and the test statistic is evaluated on those:

$$\chi^2=\sum_i\frac{\left(N_i^{\rm std}-N_i^{\rm alt}\right)^2}{\sigma_i^2},\qquad\text{significance}\approx\sqrt{\chi^2}.$$

For a simple-versus-simple comparison, $\sqrt{\chi^2}$ is a good estimate of the median significance when the counts per bin are large enough for the Gaussian approximation to hold. At low counts a Poisson likelihood ratio is the safer choice, and the difference should be checked on a bin-by-bin basis.

## Adding nuisance parameters

Flux and cross-section normalizations are never known exactly. A standard pull-term form is

$$\chi^2(\vec\epsilon)=\sum_i\frac{\left(N_i^{\rm std}-N_i^{\rm alt}(\vec\epsilon)\right)^2}{\sigma_i^2}+\sum_j\epsilon_j^2,\qquad N_i^{\rm alt}(\vec\epsilon)=N_i^{\rm alt}\Big(1+\sum_j\epsilon_jf_{ij}\Big),$$

where $f_{ij}$ is the fractional effect of nuisance $j$ on bin $i$ at $\epsilon_j=1$.

Two details are easy to get wrong.

1. **Only the alternative prediction floats.** $N_i^{\rm std}$ plays the role of the reference data and stays fixed. A normalization pull then acts by letting the alternative prediction partly mimic the standard spectrum's overall scale. That is the correct way for a normalization systematic to reduce discovery significance. If the same pull were applied to both sides, it would cancel.
2. **The minimum is analytic.** Since $N_i^{\rm alt}(\vec\epsilon)$ is linear in $\vec\epsilon$, the profiled $\chi^2$ is a quadratic form with a closed-form minimum. It is still worth checking against a numerical minimizer, which in this case agreed to better than $10^{-11}$.

## Why the prior on the flux can dominate

A 16% flux uncertainty from a solar model is large compared to a spectral distortion of a few percent. If the flux prior is treated as external and independent of the detector, the significance can drop dramatically. If the detector can measure the flux itself, for example through a neutral-current channel as discussed in the [deuterium post](/notes/deuterium-cc-nc-es/), the picture changes. The size of that swing is a major point in any honest forecast, and deserves its own post once the numbers are cleared.

## What is still unclear

Gaussian pulls for non-Gaussian systematics, and the treatment of backgrounds with shape uncertainties, are simplifications that have not been tested against a full likelihood analysis.

