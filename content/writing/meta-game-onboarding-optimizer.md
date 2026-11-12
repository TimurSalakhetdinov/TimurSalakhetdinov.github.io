---
title: "Meta Game Onboarding Optimizer: closed-loop onboarding playtests with Meta Muse"
date: 2026-11-12
description: "A Meta Global AI Developer Hackathon project that uses agents to play a browser game, identify onboarding friction, propose a change and test it after human approval."
slug: meta-game-onboarding-optimizer
tags:
  - AI Agents
  - Evals
  - Game Development
related_projects:
  - /projects/meta-game-onboarding-optimizer.html
---

I submitted the project to the indie developer track under the theme *Build for Your World*. The game under test is an original Celtic village builder, Hearths of the Glen, created for the project so that proposed changes can be played and tested.

## The problem

The first minutes of a free-to-play game can influence whether a player stays. Finding onboarding friction through playtests and funnel analysis takes time, and each proposed fix needs another round of testing.

I wanted to build a loop that playtests, diagnoses, proposes a change, waits for a human decision and checks whether the change helped.

## How the loop works

The system separates playtesting, diagnosis, design and experimentation:

1. **Playtester agents** use Muse Spark to run sessions and record screenshots, actions and events.
2. **An analyst agent** uses SAM 3.1 and Muse Spark to build an onboarding funnel and rank friction points.
3. **A designer agent** proposes a configuration change or a feature patch.
4. **A human** reviews the proposal before anything is applied.
5. **An experiment agent** reruns the playtesters on the original and changed configurations and produces a report.

The human approval step is part of the workflow. A proposed change does not become a tested change until it has been reviewed.

## Playtesting and diagnosis

The playtester agents use Muse Spark to inspect the screen, click through onboarding and maintain a short working-memory scratchpad. Five literature-grounded personas cover different player types: Rush-Clicker, Story-Guided, Strategist, Tinkerer and Hoarder.

The analyst uses SAM 3.1 to mark UI elements in gameplay screenshots and Muse Spark to reason over the session. It builds an onboarding funnel and ranks friction points with linked evidence, including a distractor-to-goal visual salience note from the SAM masks.

The designer can propose an onboarding configuration patch or turn a free-text feature idea into a schema-validated feature plugin. After human approval, the experiment agent runs a paired comparison using the baseline and patched configurations. It produces a report and a side-by-side replay.

Bug hunting diagnoses one run. Feature Forge evaluates one frozen experiment. The two paths remain separate.

## Evaluating the diagnosis pipeline

I compared the agent pipeline with a single-turn LLM baseline on seven predefined onboarding scenarios. Two scenarios contained no seeded issue, three contained a known bottleneck, and two tested how the system handled damaged or noisy telemetry.

Each scenario ran three times with `muse-spark-1.3-contributor`. A scenario passed only if all three runs passed and their classifications agreed. The checks covered the diagnosis, the presence or absence of a patch, and, for the agent pipeline, the sequence of tool calls. A separate LLM judge evaluated responses against a rubric.

| Metric | Single-turn baseline | Agent pipeline |
|---|---:|---:|
| Scenarios passed | 7/7 | 6/7 |
| Precision | 1.00 | 1.00 |
| Recall | 1.00 | 1.00 |
| Median latency | 7.29 s | 9.84 s |
| 95th-percentile latency | 9.27 s | 19.55 s |
| Total estimated cost | $0.0096 | $0.0121 |

The agent pipeline failed one scenario because one of its three runs produced a patch response that did not pass schema validation. The analyst identified the locked-interface issue, but the resulting diagnosis contained no usable patch. The other two runs of that scenario passed.

On this small test set, the single-turn baseline passed every scenario and was faster. The agent pipeline did not improve precision or recall. Its tool sequence made the steps of the diagnosis visible, but it also introduced another point of failure.

Precision and recall were calculated using the first run of each scenario, while the pass rate required all three runs to succeed. Seven scenarios are not enough to establish how either approach performs across games or real player sessions. A broader evaluation would need more onboarding problems and telemetry patterns.

## Models and credits

| Model | Role |
|---|---|
| Muse Spark | Playtester decisions, diagnosis and report summaries |
| Muse Wonder | Coding help, optional playtester and feature ideas |
| SAM 3.1 | UI segmentation and visual analysis |
| Muse Image | Game art and feature emblems |
| Muse Voice Transcribe | Optional transcription of in-game voice lines |

The soundtrack, voices and sound effects were generated with ElevenLabs.

## Limits

Agent playtests are a smoke test, not a sample of real players. Persona findings are hypotheses to check with people. SAM 3.1 marks detected regions; it does not prove what a human would notice. Recorded bot commentary is not a window into hidden model motives.

The evaluation covers seven predefined scenarios. Its results do not establish performance on unseen games, onboarding flows or real player sessions.

Runtime changes are schema-validated JSON patches, and every patch stops at the human approval gate.

## Demo and repository

[Play Hearths of the Glen](https://hearths-of-the-glen.onrender.com) · [Watch the demo video](https://youtu.be/K9RStD75dBM) · [View the repository](https://github.com/TimurSalakhetdinov/meta-ai-hackathon)
