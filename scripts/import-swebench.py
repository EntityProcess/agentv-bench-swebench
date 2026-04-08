#!/usr/bin/env python3
"""Import SWE-bench Verified examples into agentv eval format.

Usage: uv run scripts/import-swebench.py [--limit N] [--output evals/swebench-verified/]
"""
import json
import yaml
import sys
from pathlib import Path

def swebench_to_agentv(instance: dict) -> dict:
    """Convert a SWE-bench instance to agentv eval YAML format."""
    instance_id = instance["instance_id"]
    repo = instance["repo"]
    problem = instance["problem_statement"]

    return {
        "description": f"SWE-bench Verified: {instance_id}",
        "workspace": {
            "docker": {
                "image": f"swebench/sweb.eval.x86_64.{instance_id.replace('/', '__').replace('-', '_')}:latest",
                "timeout": 1800,
                "memory": "4g",
            }
        },
        "tests": [{
            "id": instance_id,
            "criteria": f"Resolve the GitHub issue in {repo}. Apply a patch that makes all FAIL_TO_PASS tests pass without breaking PASS_TO_PASS tests.",
            "input": [{
                "role": "user",
                "content": f"Fix the following GitHub issue in the {repo} repository:\n\n{problem}"
            }],
            "assertions": [{
                "type": "code-grader",
                "command": ["bash", "-c", "cd /workspace && python -m pytest -x -q"]
            }]
        }]
    }

def main():
    try:
        from datasets import load_dataset
    except ImportError:
        print("Install datasets: uv pip install datasets")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output", default="evals/swebench-verified/")
    args = parser.parse_args()

    ds = load_dataset("SWE-bench/SWE-bench_Verified", split="test")
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, instance in enumerate(ds):
        if i >= args.limit:
            break
        eval_data = swebench_to_agentv(instance)
        filename = instance["instance_id"].replace("/", "__").replace("-", "_")
        with open(output_dir / f"{filename}.EVAL.yaml", "w") as f:
            yaml.dump(eval_data, f, default_flow_style=False, sort_keys=False)
        print(f"Wrote {filename}.EVAL.yaml")

if __name__ == "__main__":
    main()
