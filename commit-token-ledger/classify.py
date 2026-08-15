#!/usr/bin/env python3
import json
from pathlib import Path


def load_config(path="config.json"):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def classify(repository, commit_message="", readme_text="", config=None):
    config = config or load_config()
    rules = config["classification"]
    repo_l = repository.lower()
    msg_l = (commit_message or "").lower()
    readme_l = (readme_text or "").lower()

    if repository in rules.get("manual_non_space_x_repositories", []):
        return {
            "classification": "NON_SPACEX",
            "score": 0,
            "evidence": ["manual NON_SPACEX repository override"],
            "evidence_level": "CONFIRMED"
        }

    if repository in rules.get("manual_space_x_repositories", []):
        return {
            "classification": "SPACE_X",
            "score": 100,
            "evidence": ["manual SPACE_X repository override"],
            "evidence_level": "CONFIRMED"
        }

    score = 0
    evidence = []
    for term, weight in rules.get("term_weights", {}).items():
        term_l = term.lower()
        locations = []
        if term_l in repo_l:
            locations.append("repository")
        if term_l in msg_l:
            locations.append("commit_message")
        if term_l in readme_l:
            locations.append("readme")
        if locations:
            score += int(weight)
            evidence.append({"term": term, "weight": int(weight), "locations": locations})

    threshold = int(rules.get("space_x_threshold", 4))
    classification = "SPACE_X" if score >= threshold else "NON_SPACEX"
    return {
        "classification": classification,
        "score": score,
        "evidence": evidence,
        "evidence_level": "INFERRED"
    }


def is_administrative(commit_message, config):
    message = (commit_message or "").strip().lower()
    prefixes = config.get("classification", {}).get("administrative_message_prefixes", [])
    return any(message.startswith(prefix.lower()) for prefix in prefixes)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("repository")
    p.add_argument("--message", default="")
    p.add_argument("--readme", default="")
    p.add_argument("--config", default="config.json")
    args = p.parse_args()
    cfg = load_config(args.config)
    print(json.dumps(classify(args.repository, args.message, args.readme, cfg), indent=2))
