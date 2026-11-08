---
title: "An event count twice the literature value: a fiducial-volume story"
date: 2026-11-01
summary: "A sanity check against a published event count flagged a missing fiducial cut, and a swapped-argument bug hid in the same script."
tags: [workflow, event-rates, JUNO, verification]
draft: false
---

Context: an event-rate pipeline ([architecture post](/notes/verification-first-architecture/)) was extended to a comparison against JUNO's elastic-scattering channel for $^8$B neutrinos. Before comparing anything, the pipeline's absolute event count was checked against a published feasibility study.

## The warning sign

JUNO's own feasibility study quotes roughly 60,000 elastic-scattering signal events over ten years for the full analysis range with a 2 MeV threshold. The idealized calculation (full 20 kt target, no cuts) gave 126,489 events in the narrower 2 to 5 MeV window alone, a factor of about 2.1 above the full-range literature number. A sub-window cannot exceed the full range, so the direction of the discrepancy was already suspicious.

## Ruling out the usual suspects

- **Cross section:** the elastic-scattering cross section reproduced the Bahcall (1989) benchmark to 0.01%.
- **Target electrons:** the electron count for 20 kt of LAB scintillator matched the expected $6$ to $7\times10^{33}$.
- **Flux shape:** the tabulated spectrum integrated to 1.000004 over its range.

None of these moved the answer.

## The root cause

The calculation used the full target mass. Published analyses apply a fiducial cut to reject backgrounds near the vessel wall. JUNO's published analysis uses a 13 m fiducial radius inside a 17.7 m detector radius, which keeps

$$f_{\rm FV}=\left(\frac{13.0}{17.7}\right)^3\approx0.40$$

of the mass. With that correction the 2 to 5 MeV total drops to about 50,000 events per ten years, about 0.84 of the full-range literature figure, and now correctly below one for a sub-window.

## Treating both detectors the same way

A comparison between two detectors has to treat both the same way. For the deuterated-detector side, the analogous number was taken from SNO, the only D$_2$O detector built so far: 550 cm fiducial radius inside a 600 cm vessel,

$$f_{\rm FV}=\left(\frac{550}{600}\right)^3\approx0.77.$$

The factor was threaded through the target-mass term inside the pipeline, not applied afterwards to cached headline numbers, so that every downstream method picks it up automatically.

## A second bug in the same script

The same comparison script called a solver as

```python
pee_sterile_3x3(E, DM2_01, SIN2_2ALPHA, n_steps=N_STEPS, check_convergence=False)
```

while the function expects the mixing angle in its second position and the mass splitting in the third. The values were passed in swapped order, so the mixing angle was about $10^{-5}$ rad and the curve collapsed onto the standard one. A diagnostic print showed the problem: the "feature" minimum sat at the very edge of the energy grid with a depth of $10^{-4}$, which is what `argmin` returns on numerical noise.

The fix converts $\sin^2 2\alpha$ to $\alpha$ explicitly and passes both parameters as keywords:

```python
alpha = 0.5 * np.arcsin(np.sqrt(SIN2_2ALPHA))
pee_sterile_3x3(E, alpha=alpha, dm2_01=DM2_01, n_steps=N_STEPS, check_convergence=False)
```

## Habits

1. Compare an absolute number to the literature before comparing anything relative.
2. A discrepancy in the wrong direction (a part larger than the whole) is more informative than one in the plausible direction.
3. Use keyword arguments for physical parameters that share a type and a rough scale.
4. Apply every correction to both sides of a comparison, or say explicitly that it was not.

## What is still unclear

An efficiency correction was available in the literature for one detector and not for the other, so the comparison remains asymmetric in that respect. Any quoted margin should carry that caveat.
