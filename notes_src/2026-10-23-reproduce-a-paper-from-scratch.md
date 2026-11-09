---
title: "Reproduce a paper from scratch: what it teaches that reading does not"
date: 2026-10-23
summary: "A practical guide for undergraduates who want to get into research through a published result."
tags: [research, students, methods]
section: general
draft: false
---

> Rebuilding a published calculation from the text alone, without the original code, is a good way for an undergraduate to learn a research field. It brings out the assumptions that a paper only mentions in passing. A mismatch is still useful, as long as it is written down clearly.

## Why it helps

A paper presents a final table. Behind it sit dozens of choices about cross sections, interpolation, integration ranges, units and normalization, and many appear only as a citation or a half sentence. Reading can give a feeling of understanding. Rebuilding means every assumption has to be written down in code, which shows what was not understood yet.

It is also a safe way to learn. The answer is known, so the result can be graded against the paper. Nobody has to wonder whether the physics is right, only whether the implementation is.

## A starter recipe

1. **Pick a paper with a table or figure of numbers.** Event rates, a sensitivity table, a cross-section plot. Numbers can be compared. A qualitative argument cannot.
2. **Choose the smallest reproducible piece.** One row of the table, one curve. Not the whole paper.
3. **Write down every input and where it comes from.** Anything that is only named in the paper needs a primary source.
4. **Implement the simplest version first.** Check that it lands in the right ballpark.
5. **Compare, then investigate any gap before touching anything.** Never adjust a parameter just to make a number match.
6. **Write up what matched, what did not, and what is still unknown.**

## What it looked like in practice

A supernova-neutrino event-rate paper for a deuterated detector was rebuilt from its published description. Neutral-current rates came out within 1 to 3% of the published tables, while the charged-current rates started 17 to 20% too high. A coding mistake was a natural suspect, so an independent re-implementation was built, and it gave the same answer. The cause turned out to be that the published cross-section tables are printed with coarse energy sampling, and integrating over a coarse table is not the same as integrating over the underlying calculation. Using the original finer tables brought the gap below 4%.

In another reproduction, a detection-sensitivity table for two detectors was matched to rounding precision, but about 15% of discrepancy remained in a signal rate. It was documented in the write-up, and no parameter was tuned to hide it. A clearly labelled mismatch is more useful to the next reader than a match that was forced.

## Why it can help when applying for research

A reproduction can show that someone has read a paper carefully, implemented it and checked their own result. Sharing the code and a short note about mismatches may say more about this than a list of courses.

## Going deeper

The [checking habits post](/notes/five-habits-for-checking-a-calculation/) lists tests that help during a reproduction.
