---
title: "The Sun makes one kind of neutrino. Detectors on Earth see another."
date: 2026-10-02
summary: "A short, math-free tour of how the Sun's own matter changes the identity of the particles leaving it."
tags: [neutrinos, Sun, intro]
section: general
draft: false
---

> Fusion in the Sun produces only electron neutrinos. By the time they reach Earth, most of the high-energy ones have changed flavour, and the Sun's own dense core is part of the reason. The effect (MSW) explained a decades-old puzzle and it is still a useful place to look for new physics.

## A puzzle from the 1960s

The Sun fuses hydrogen into helium and releases neutrinos while doing it. Roughly 60 billion of them pass through every square centimetre of the Earth each second, and almost none interact. In the late 1960s, Ray Davis built a detector deep underground to catch a few of them. It counted about a third of the number that solar models predicted.

Either the Sun models were wrong, or the neutrinos were doing something on the way. The second explanation turned out to be right, and it took until the early 2000s to settle it.

## What the neutrinos do

Neutrinos come in three flavours, and a neutrino born as one flavour is a quantum mixture of three mass states. As the mass states travel they drift out of step, and the flavour changes. In a vacuum this gives the familiar oscillation.

Inside the Sun there is one more effect. Its core is packed with electrons, and only electron neutrinos can scatter forward off electrons by the charged-current interaction. The other flavours do not feel this. The result is something like a headwind that only one flavour experiences, and it modifies how the mixing works. As a neutrino climbs out of the dense core, the effective mixing slides smoothly from "mostly one mass state" to the vacuum picture. If the density changes gently enough, the neutrino follows along, and it emerges as a particular mass state, not as the electron neutrino it started as.

That is the Mikheyev-Smirnov-Wolfenstein (MSW) effect. For the high-energy neutrinos from boron-8 decay it converts about two thirds of the electron neutrinos into other flavours, which accounts for the deficit Davis saw.

## Why it is still interesting

Low-energy neutrinos barely feel the Sun's matter and oscillate as in a vacuum. High-energy ones feel it fully. In between there is a transition, around a few MeV, where the two effects compete, and that region is hard to measure with current detectors. Anything that changes the matter effect (an extra neutrino state, a new interaction) would show up there first. This is the kind of question the work in this notebook looks at.

## Try it yourself

For anyone who wants to try this: write the two-flavour Hamiltonian with a density that falls exponentially, evolve a pure electron-neutrino state numerically for a few energies, and plot the survival probability against energy. About fifty lines of Python should be enough, and the two limits (vacuum and matter-dominated) should show up in the plot.

## Going deeper

The [formula and its derivation](/notes/msw-survival-probability-sun/) are in a more technical post, and [how adiabatic the Sun is](/notes/adiabaticity-landau-zener/) is covered there too.
