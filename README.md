# AgentV Bench: SWE-bench

Benchmark repo for SWE-bench coding evaluations using AgentV. Contains imported SWE-bench examples converted to agentv eval format, with Docker workspace configurations for isolated execution.

## Overview

This repository stores SWE-bench-style coding evaluation benchmarks in the [AgentV](https://github.com/EntityProcess/agentv) eval format. Each eval defines:

- A Docker workspace based on the official SWE-bench evaluation images
- A problem statement from a real GitHub issue
- Assertions that verify the fix by running the project's test suite

SWE-bench tasks test an agent's ability to resolve real-world GitHub issues by producing correct code patches. Evals here are imported from the [SWE-bench](https://www.swebench.com/) dataset and converted to AgentV YAML format.

## Structure

```
.agentv/              # AgentV project configuration
  config.yaml         # Studio threshold and settings
  targets.yaml        # Model provider targets
evals/
  swebench-verified/  # SWE-bench Verified examples (curated, human-validated)
  swebench-lite/      # SWE-bench Lite examples (smaller subset)
scripts/
  import-swebench.py  # Import script to pull from HuggingFace datasets
```

## Running Evals

Prerequisites:
- [AgentV](https://github.com/EntityProcess/agentv) installed
- Docker available (SWE-bench images will be pulled automatically)

Run a single eval:

```bash
agentv eval evals/swebench-verified/django-15180.EVAL.yaml
```

Run all SWE-bench Verified evals:

```bash
agentv eval evals/swebench-verified/
```

Run with a specific target:

```bash
agentv eval evals/swebench-verified/ --target claude-opus
```

## Results

Results are stored in `.agentv/results/` (git-ignored). Use `agentv studio` to view and compare results across targets:

```bash
agentv studio
```

The default pass threshold is set to 0.8 in `.agentv/config.yaml`.
