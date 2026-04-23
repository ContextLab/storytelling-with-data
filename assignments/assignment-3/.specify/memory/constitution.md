<!--
Sync Impact Report
Version change: 1.0.0 -> 1.1.0
Modified principles:
- I. Working Demo First: clarified demo must be a local static HTML website
- II. Explainable Implementation: unchanged
- III. Workflow Evidence Required: unchanged
- IV. Independently Verifiable Increments: clarified local-browser verification
- V. Simplicity Over Unexplained Complexity: clarified no server/mobile scope
Added sections:
- None
Removed sections:
- None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ✅ .specify/templates/checklist-template.md
- ✅ .specify/templates/commands/*.md (directory not present)
Follow-up TODOs:
- None
-->
# Assignment 3 Constitution

## Core Principles

### I. Working Demo First
Every feature MUST contribute to a runnable local HTML website that does
something visible, interactive, useful, or otherwise demonstrable in a computer
web browser. Deliverables that only create scaffolding, unused abstractions, or
speculative infrastructure are not complete unless they are necessary for the
current local website demo path.

Rationale: The assignment is evaluated on a functional project and the story of
how it was built, not on code volume or architectural polish.

### II. Explainable Implementation
The final implementation MUST be understandable by the author at the level of
major modules, data flow, user interactions, and design choices. AI-generated
code MUST be reviewed, simplified where practical, and kept close enough to the
project goal that the author can explain why it works.

Rationale: The submission requires explaining the code and the decisions behind
it; unexplained complexity weakens both the demo and the workflow story.

### III. Workflow Evidence Required
Work on the demo MUST preserve concrete evidence of the AI-assisted workflow:
important prompts, useful responses, failed attempts, debugging turns, and
iteration decisions. Each feature plan MUST include how this evidence will be
captured for the final video narrative.

Rationale: The video focuses on the workflow more than the final artifact, so
evidence must be gathered while building instead of reconstructed afterward.

### IV. Independently Verifiable Increments
Each user-facing increment MUST define a specific verification path before
implementation begins. Verification MAY be automated tests, manual demo steps,
screenshots, or browser console checks, but it MUST prove the increment works
locally in a computer web browser and does not break earlier demo behavior.

Rationale: Small verifiable slices make AI-assisted iteration easier to debug
and provide stronger material for the workflow explanation.

### V. Simplicity Over Unexplained Complexity
The project MUST prefer the simplest implementation that supports the intended
demo and video. New frameworks, services, data stores, build systems, generated
assets, or multi-file structures MUST be justified by a concrete demo need.
Server-side runtimes, iOS apps, Android apps, and deployment infrastructure are
out of scope.

Rationale: A simple, well-understood demo scores better than a complex project
that cannot be explained or reliably shown.

## Assignment Constraints

The project MUST satisfy the Assignment 3 deliverables:

- A working static HTML website committed to the assignment repository.
- A roughly five-minute YouTube video covering what was built, the AI-assisted
  workflow, and evidence-based tips or lessons.
- Enough local documentation, comments, or notes to answer the assignment's
  "Verify and Explain" questions before submission.

Feature work MUST stay compatible with a local static website delivery format.
The demo MUST open and function from local files in a computer web browser
without a server setup step. HTML, CSS, JavaScript, images, data files, fonts,
and other assets required by the demo MUST be local to the repository. iOS and
Android versions are unnecessary and out of scope.

## Development Workflow

Plans MUST identify the demo format, primary user journey, verification method,
and workflow evidence to capture. Specs MUST prioritize independently testable
user stories that can be demonstrated on their own. Tasks MUST include
verification and workflow-evidence capture, not only implementation steps.

Before submission, the project MUST be opened from a clean checkout in a
computer web browser without starting a local server. The final review MUST
confirm that the demo works, the author can explain the major code sections,
and the video narrative has specific examples of prompts, AI responses,
iterations, and debugging.

## Governance

This constitution supersedes conflicting project practices for Assignment 3
work. Amendments MUST update this file, explain the semantic version change in
the Sync Impact Report, and review dependent Spec Kit templates for consistency.

Versioning follows semantic versioning:

- MAJOR: Removes or redefines a core principle in a way that changes project
  governance.
- MINOR: Adds a principle, required section, or material workflow requirement.
- PATCH: Clarifies wording, fixes errors, or tightens language without changing
  obligations.

Every plan, spec, and task list MUST pass the constitution checks before
implementation proceeds. Any approved exception MUST be documented in the
feature plan's Complexity Tracking table with the concrete reason and the
simpler alternative that was rejected.

**Version**: 1.1.0 | **Ratified**: 2026-04-19 | **Last Amended**: 2026-04-19
