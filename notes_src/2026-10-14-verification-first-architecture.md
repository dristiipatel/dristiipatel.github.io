---
title: "Building a solver you can trust: the architecture of a verification-first project"
date: 2026-10-14
summary: "How a solar P_ee and sensitivity codebase is organised so that every number has an independent check."
tags: [workflow, scientific-python, verification]
draft: false
---

Context: the earlier posts covered the physics (the [MSW formula](/notes/msw-survival-probability-sun/), the [sterile extension](/notes/sterile-neutrino-in-the-sun/), [production averaging](/notes/where-8b-neutrinos-are-born/), [event kinematics](/notes/from-neutrino-energy-to-electron-energy/), [significance](/notes/where-does-n-sigma-come-from/)). This post and the next few describe how the code behind a $P_{ee}$ and sensitivity study was organised, and what the verification process caught.

## Rule 1: nothing is tuned

The first version of the project used a fixed-density formula with a hand-tuned $\tanh$ for the standard curve, and a Gaussian bump with chosen amplitude, centre and width for a new-physics feature. Both produce plausible-looking plots, and neither has any predictive content: changing an oscillation parameter would not change the curve correctly, because the curve was never derived from a Hamiltonian. Replacing both with numerical solutions of the evolution equation was the first change made, before any other verification work.

## Rule 2: several solvers, shared only where it is safe

| Method | Role | What it shares with the others |
|---|---|---|
| Closed-form adiabatic formula | Standard three-flavour $P_{ee}$ | Inputs only |
| Full $3\times3$ diagonalization with eigenvector tracking | Primary sterile solver | The Hamiltonian |
| Effective $2\times2$ solver | Mass-dominance regime | Inputs only |
| Direct time-dependent Schrodinger integration | Independent check of the primary solver | The Hamiltonian function only |
| Reduced-Hamiltonian method of de Holanda and Smirnov | Independent check in the coupled regime | Inputs only |

The direct integrator deliberately shares nothing with the primary solver except the function that builds $H(r)$. No diagonalization, no eigenvector permutation, no tracking. Agreement between them is therefore evidence, not a self-consistency test.

## Rule 3: separate the pipeline stages

The repository separates what a physicist would think of as stages: $P_{ee}$ solvers, flux and cross-section modules, production-zone averaging, the $E_\nu\to T_e$ kernel, detector response, then analysis scripts that only import from the modules above. Superseded implementations go to an `archive/` folder and are not deleted, so that a rejected approach remains visible and explained.

## Rule 4: every script reproduces a number

A final pass that runs every script end to end, instead of trusting each script's own header comment, turned out to be worthwhile. Several scripts were still importing a solver from before the first round of fixes, so they reproduced the project's very first significance number and none of the later corrections. That is a synchronization problem, not a physics error, and it only shows up by running everything.

## What is still unclear

A verification-first structure does not remove the need for judgement about which approximations matter. It only makes it harder for an error to survive unnoticed. The next four posts are specific cases where it caught something.
