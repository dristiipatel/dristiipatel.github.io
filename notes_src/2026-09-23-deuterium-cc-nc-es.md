---
title: "Why deuterium? Three reaction channels for solar 8B"
date: 2026-09-23
summary: "Thresholds, flavour sensitivity and the role of the neutral-current channel in a deuterated detector."
tags: [detectors, deuterium, SNO]
draft: false
---

Context: the [gap post](/notes/solar-neutrinos-2-5-mev-gap/) argued that a low-threshold, spectroscopic charged-current channel would be useful in the 2 to 5 MeV range. Deuterium offers that, and it offers more. A deuterated detector sees three reactions at once.

## The three channels

$$\nu_e+d\to p+p+e^-\qquad(\text{CC})$$
$$\nu_x+d\to\nu_x+p+n\qquad(\text{NC})$$
$$\nu_x+e^-\to\nu_x+e^-\qquad(\text{ES})$$

**CC.** Only $\nu_e$ participates. The threshold follows directly from rest masses,

$$Q_{CC}=2m_p+m_e-m_d\approx1.44~\text{MeV},$$

which is below the entire 2 to 5 MeV window, and the outgoing electron carries energy information about the neutrino (with a smearing discussed in [a later post](/notes/from-neutrino-energy-to-electron-energy/)).

**NC.** All active flavours contribute with equal strength. The threshold is the deuteron binding energy, 2.2246 MeV. The signature is a neutron, not an electron, so it carries almost no spectral information, but its rate measures the total active flux.

**ES.** All flavours contribute, with $\nu_e$ weighted more heavily than $\nu_{\mu,\tau}$ because of the extra charged-current diagram. Directional information is available in Cherenkov detectors but is largely lost in scintillator, and spectral information is limited by the kinematics.

## Why the combination is useful

CC measures $\nu_e$ only, NC measures the total active flux. A ratio of the two is independent of the absolute flux normalization, which is how SNO established flavour conversion without relying on a solar model. For a sensitivity study the same logic suggests a built-in calibration: if the flux uncertainty is large (the $^8$B flux has an uncertainty of order 15% from solar models), a simultaneous NC measurement can in principle constrain it.

Near threshold, the CC cross section exceeds the NC cross section by more than two orders of magnitude because of Coulomb enhancement of the outgoing electron. So at 2 to 3 MeV the CC channel dominates the event count even though the NC channel has the better calibration properties.

## Cross sections

Event rates need the deuteron cross sections as functions of energy. The standard calculation (Nakamura, Sato, Gudkov and Kubodera, 2001) is the one used in SNO analyses, and it is tabulated on a fine grid.

## What is still unclear

The practical feasibility of a loaded or deuterated scintillator, and its backgrounds, is a separate engineering question this post does not address. The in-situ NC calibration idea also depends on neutron detection efficiency, which has to be known.

