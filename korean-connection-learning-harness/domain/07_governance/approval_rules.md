# Approval Rules

## Purpose

Defines when the parent agent can write output directly and when human approval is required.

## Parent-Owned Writes

The parent agent may write:

- generated lesson blueprints
- practice plans
- material specs
- review reports
- workspace handoffs
- proposed domain updates

## Human Approval Required

Human approval is required before:

- changing approved files under `domain/`
- changing artifact contracts under `contracts/`
- promoting research insight to a default rule
- changing agent responsibilities
- relaxing privacy restrictions
- marking a learner target as stable without evidence

## Approval State

Every approved change should reference an `approval_state` contract record or a clear user instruction in the session transcript.

## Partial Rerun Rule

If a rerun affects only one artifact, rerun the owning agent and any downstream reviewer. Do not rerun unrelated upstream agents unless their input changed.
