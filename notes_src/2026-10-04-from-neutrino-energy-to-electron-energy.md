---
title: "Bins in neutrino energy are not observable: from E_nu to the detected electron"
date: 2026-10-04
summary: "Why a CC event-rate analysis has to convert E_nu into electron kinetic energy and then into reconstructed energy."
tags: [detectors, kinematics, event-rates]
draft: false
---

Context: the [deuterium post](/notes/deuterium-cc-nc-es/) described the CC channel. A first-pass event-rate calculation typically bins events in neutrino energy, because the flux, the cross section and $P_{ee}$ are all functions of $E_\nu$. A detector does not measure $E_\nu$. It measures light from an electron.

## Why the map is a continuum

$\nu_e+d\to e^-+p+p$ has three bodies in the final state. A fixed $E_\nu$ therefore does not give a single electron energy. It gives a continuum, bounded above by roughly $E_\nu-Q_{CC}$ (with $Q_{CC}\approx1.44$ MeV, and small recoil corrections), and the shape inside that envelope depends on the nuclear physics.

The cleanest way to carry this through is a normalized kernel,

$$\frac{dN}{dT_e}=\int dE_\nu\,\frac{dN}{dE_\nu}\,K(E_\nu,T_e),\qquad\int K(E_\nu,T_e)\,dT_e=1,$$

where the normalization condition expresses that the kernel redistributes events and neither creates nor destroys them. The kernel can be built from tabulated electron-momentum distributions $d\sigma/dP_e$ (the NSGK calculation provides them), converted to $T_e$ with the appropriate Jacobian, and interpolated between tabulated neutrino energies.

## Resolution as a second step

The detector then blurs $T_e$. A single stochastic term,

$$\sigma(E)=a\sqrt{E},$$

is the simplest model, with $a$ of order 5 to 6% at 1 MeV for large scintillator detectors. Convolving the $T_e$ spectrum with a Gaussian of this width gives the reconstructed-energy spectrum that analysis bins actually refer to.

## Why that is imp for a sensitivity forecast

A spectral distortion in $P_{ee}(E_\nu)$ gets spread over a range of $T_e$ by the three-body kinematics, and spread again by resolution. Which of the two dominates depends on the detector and on the feature being searched for, but the conversion cannot be left out either way. A resolution sweep alone gives an incomplete picture.

## But...

The kernel is only as good as its input tables, and tabulated electron spectra exist only at discrete neutrino energies. Interpolating on the fractional envelope coordinate $x=T_e/T_{e,\max}(E_\nu)$ respects the energy-dependent endpoint, but how well it does so between tabulated points has to be checked and not assumed.

