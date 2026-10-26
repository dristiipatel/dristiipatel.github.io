---
title: "Finding a black-hole merger in raw noise: matched filtering for beginners"
date: 2026-10-26
summary: "How the first gravitational-wave signal was pulled out of the data, using ideas from a noisy room."
tags: [gravitational-waves, signal-processing, intro]
draft: false
---

> **In one minute:** Gravitational-wave signals are far smaller than the noise in the detector. The way to find them is to know exactly what the signal should look like and to search the data for it, after first flattening the noise. The public data from the first detection can be run through this pipeline by an undergraduate in an afternoon.

## The problem

When two black holes merged and the signal reached LIGO in September 2015, the stretching of space at the detectors was about one part in $10^{21}$. In the raw data it is invisible: the noise is much larger at every moment.

## An analogy: a song in a loud room

Imagine trying to hear one particular song in a noisy cafe. Knowing the tune helps enormously. The brain does a kind of matching: it listens for that pattern, and ignores everything else. It also helps if the room is loud mainly at low frequencies, because the listener can stop paying attention to the rumble.

Those are the two steps of the analysis.

## Step 1: whiten the data

Detector noise is not equal at all frequencies. It is large at very low and very high frequencies and smallest in a band around a hundred hertz. Whitening divides each frequency component by the noise level at that frequency, so the noise becomes flat. This is what makes the signal's structure stand out, and it is why the plot of "whitened strain" looks so different from the raw data.

## Step 2: matched filter

Take a template, a predicted waveform for given black hole masses, and slide it along the whitened data, calculating how well they match at each time. The resulting signal-to-noise ratio (SNR) peaks where the template lines up with a real signal. A bank of templates for different masses is tried, and the best-matching one is chosen.

## Doing it with public data

The data from the detection are public through the Gravitational Wave Open Science Center. A full pipeline (download the data, estimate the noise spectrum, whiten, apply a waveform model, find the SNR peak) can be written with the PyCBC library. Run that way, the signal appears in both detectors, with peak SNRs of about 17.5 in Hanford and 13 in Livingston, and the two peaks are separated by less than the roughly 10 milliseconds that light needs to travel between the two sites.

## Why a neutrino physicist cares

The same logic, a known signal shape against a well-characterized background, appears everywhere in experimental physics. Finding a few supernova neutrinos in a detector, or an energy distortion in a solar neutrino spectrum, relies on knowing what the signal looks like and how the background behaves.

## Try it

PyCBC has tutorials that use exactly this event. Running the whitening step on its own and looking at the before-and-after plot is a good first target.

## A question to take away

What would happen to the SNR if the noise estimate were slightly wrong?
