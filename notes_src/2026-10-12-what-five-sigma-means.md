---
title: "What does 5 sigma actually mean? A coin-flip explanation"
date: 2026-10-12
summary: "A discovery threshold explained with something anyone can imagine: tossing a fair coin."
tags: [statistics, intro, methods]
section: general
draft: false
---

> "5 sigma" means that a result at least this extreme would happen by chance, if there were no effect at all, about once in 3.5 million tries. Roughly the same odds as tossing a fair coin and getting 22 heads in a row. It is a statement about the data under the no-signal assumption, not about the probability that the signal exists.

## The coin version

Suppose a coin is claimed to be biased. A fair coin is the "nothing is going on" hypothesis. If it is tossed 10 times and lands heads 9 times, this is unusual but not very surprising: it happens for a fair coin about 1% of the time. At 20 heads in 20 tosses, a fair coin would almost never do that, and most people would stop believing the coin is fair.

Particle physicists do the same thing, with numbers of detected events replacing coin tosses. They ask: if there were no new effect and the background alone were present, how often would a statistical fluctuation produce a result this far from the expected count? That probability is the p-value.

## Turning a p-value into sigma

"Sigma" is a way to quote the p-value using the Gaussian distribution. The one-sided numbers are:

| Significance | Chance of a fluctuation this large |
|---|---|
| 1 sigma | about 1 in 6 |
| 2 sigma | about 1 in 44 |
| 3 sigma | about 1 in 740 |
| 4 sigma | about 1 in 32,000 |
| 5 sigma | about 1 in 3.5 million |

3 sigma is called "evidence" and 5 sigma is called "discovery". The 2012 Higgs announcement used 5 sigma. For comparison, 22 fair-coin heads in a row has odds of 1 in about 4 million, close to 5 sigma.

## Why the bar is so high

Physicists look at many places, with many kinds of analysis, so a rare fluctuation will be found somewhere eventually. A high threshold protects against being fooled by one of them. Some 3 sigma anomalies have come and gone over the decades.

## Two common mistakes

1. **It is not the probability that the effect exists.** The p-value says how surprising the data are if there is no effect. It does not give the chance of the effect being true. That needs a prior and a different kind of analysis.
2. **It is only as good as the model.** If the background is underestimated or the detector response is misjudged, the sigma value can be wrong even though it looks precise.

## For sensitivity forecasts

When a paper says that a future detector would reach "7 sigma" in some measurement, no data exist yet. The number is computed from expected counts, with a stand-in dataset equal to the prediction, and it depends strongly on assumptions about backgrounds and systematic uncertainties. Part of reading such a claim sensibly is asking which assumptions it is sensitive to. A [more technical post](/notes/where-does-n-sigma-come-from/) shows how this is calculated.

## A question to take away

If an experiment reports 3 sigma, and 100 such experiments are done on unrelated questions, how many 3 sigma results should be expected from fluctuations alone?
