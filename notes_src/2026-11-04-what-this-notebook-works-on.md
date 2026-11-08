---
title: "What this notebook works on, in plain language"
date: 2026-11-04
summary: "A one-page overview for anyone who wants to know what the projects here are about before reading the details."
tags: [overview, intro]
draft: false
---

> The work here is about neutrinos from the Sun and from exploding stars, and about how well future detectors could measure them. Most of it is computation: building event-rate and sensitivity calculations, reproducing published results, and checking everything against independent methods.

## The questions

**What do solar neutrinos look like between 2 and 5 MeV?** This is an energy range where the survival probability is sensitive to extra neutrino states, and where current detectors have trouble. A detector based on deuterium could in principle cover it. The first questions are how its spectrum would look and how much exposure would be needed to test a modification. See the [overview post on the gap](/notes/solar-neutrinos-2-5-mev-gap/). A manuscript on this is in preparation.

**What can the neutrinos from a supernova tell us about the neutrino mass ordering?** This is the sensitivity of several detector designs, from water to heavy water to doped scintillators, in several reaction channels.

**What does the background of all past supernovae look like?** The diffuse supernova neutrino background is being added to an open-source package that turns supernova models into detector event rates.

## The way of working

Published results are rebuilt from scratch, without the original code, which helps find details that papers skip over. Important numbers are then checked with a second method that shares as little code as possible. When something does not match, the mismatch is written down, not tuned away.

## Smaller side projects

A simulation of a technique for extracting the direction of solar neutrinos in a scintillator detector. A pipeline that recovers the first gravitational-wave event from public data. A live muon-detection demonstration for the public at an open day.

## Where to start

For students: the [reproduction post](/notes/reproduce-a-paper-from-scratch/) and the [checking habits post](/notes/five-habits-for-checking-a-calculation/) are the most practical. For anyone curious about the physics, start with [the Sun's neutrinos](/notes/sun-neutrinos-that-change-identity/).

Corrections and questions are welcome by email.
