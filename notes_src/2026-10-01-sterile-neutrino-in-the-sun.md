---
title: "A fourth state in the solar Hamiltonian: what a sterile neutrino changes"
date: 2026-10-01
summary: "How a 3+1 extension enters the matter Hamiltonian, and why the ratio of mass splittings decides which approximation is valid."
tags: [sterile-neutrinos, MSW, theory]
draft: false
---

Context: [the MSW post](/notes/msw-survival-probability-sun/) derived $P_{ee}$ for three active flavours. Adding a light sterile state changes the structure of the problem in a specific way, and the details determine which approximations survive.

## What changes in the Hamiltonian...

In the flavour basis $(\nu_e,\nu_x,\nu_s)$, with $\nu_x$ the active combination orthogonal to $\nu_e$, the Hamiltonian is

$$H(r)=U\,\frac{\mathrm{diag}(0,\Delta m^2_{21},\Delta m^2_{01})}{2E}\,U^T+\mathrm{diag}\!\left(V_e\cos^2\theta_{13}+V_n,\;V_n,\;0\right),$$

with $V_e=\sqrt2G_Fn_e$ and $V_n=-G_Fn_n/\sqrt2$.

Three things stand out.

1. The sterile state has no matter potential at all, since it does not take part in any Standard Model interaction.
2. The electron flavour carries both the charged-current and the neutral-current term.
3. The remaining active combination carries only the neutral-current term. A neutral-current potential is common to all active flavours, so it drops out of active-active oscillations. It does not drop out once a state exists that does not feel it.

## A second resonance

Equating the $(\nu_e,\nu_e)$ and $(\nu_s,\nu_s)$ diagonal entries gives a sterile resonance condition of the form

$$\Delta m^2_{01}\cos2\alpha=2V_{\rm eff}E_{\rm res},\qquad V_{\rm eff}=V_e\cos^2\theta_{13}+|V_n|,$$

where $\alpha$ is the sterile mixing angle. The sterile resonance and the standard 1-2 resonance sit at different energies in general. How far apart they are is the whole story.

## The regime parameter

Define $R_\Delta\equiv\Delta m^2_{01}/\Delta m^2_{21}$. Two limits are well understood.

- **Mass dominance** ($\Delta m^2_{01}\gg\Delta m^2_{21}$): the sterile oscillation is fast and averages away. What remains is an effective 2-level Hamiltonian, and $P_{ee}(E)$ is modified smoothly and monotonically, with no resonance feature.
- **Coupled regime** ($R_\Delta\sim O(1)$): the two resonances overlap in density and cannot be treated one at a time. The full three-level problem has to be solved, and the energy dependence can show a broad feature.

Published global analyses of solar data have focused largely on the first regime. The coupled regime is harder to treat analytically, which is part of why it deserves a numerical treatment (see the [post on eigenvector tracking](/notes/two-bugs-in-one-hamiltonian/) for what that numerical treatment looked like and what went wrong on the way).

## What is still unclear

Which published constraints already cover the coupled regime, and at what mixing angles, needs to be checked carefully against the literature before this post goes live. A table of regimes with references would make that explicit.

