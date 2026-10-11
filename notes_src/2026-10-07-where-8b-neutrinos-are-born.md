---
title: "Where are the 8B neutrinos born? Production-zone averaging in P_ee"
date: 2026-10-07
summary: "A single production radius is a simplification. How much it matters depends on how fast n_e changes across the zone."
tags: [solar-neutrinos, solar-model, numerics]
draft: false
---

Context: the [MSW post](/notes/msw-survival-probability-sun/) evaluated $P_{ee}$ with $\theta_m$ at one production radius. The $^8$B neutrinos are emitted from an extended region of the solar core, and the matter potential varies across it.

## How much does the density change?

For the exponential profile $n_e\propto e^{-10.54\,r/R_\odot}$, a shift of $0.025\,R_\odot$ in production radius changes the density by a factor of $e^{10.54\times0.025}\approx1.3$. Since $\varepsilon\propto n_e$, the resonance energy shifts by the same 30%. For a smooth, broad feature in $P_{ee}(E)$ this is a modest effect. For a feature that depends on two resonances sitting close together, it is not obviously negligible.

## The averaging

The fix is to average $P_{ee}$ over the production distribution $w(r)$:

$$\langle P_{ee}(E)\rangle=\frac{\int w(r)\,P_{ee}(E;\,r_{\rm prod}=r)\,dr}{\int w(r)\,dr}.$$

Three choices for $w(r)$ appear in practice.

- **A Gaussian** centred near $0.05\,R_\odot$ with a width of about $0.025\,R_\odot$, an analytic fit calibrated to a solar model.
- **A tabulated profile** from a standard solar model, such as the BS05 tables with 610 radial zones, used directly as quadrature weights.
- **A tabulated profile for a different composition**, for example the low-metallicity variant of the same model, as a systematic cross-check.

## Some imp points

- Using the tabulated weights directly avoids resampling onto Gauss-Legendre nodes, so no information is lost.
- A fitted Gaussian should be compared against the tabulated profile before being trusted. Narrower and more sharply peaked tabulated profiles shift the average, and the direction of that shift cannot be guessed in advance.
- When the sterile solver is expensive, a reduced set of nodes (for instance 30 quantile-sampled nodes from the 610 zones) can be validated against the full tabulation, first with a cheap proxy and then with the expensive solver at one point.

## What is still unclear

The residual solar-model uncertainty that the two tabulated compositions do not span (opacity or diffusion treatment, for example) is not addressed here.

