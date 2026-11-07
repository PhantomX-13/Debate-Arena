#!/usr/bin/env python3
"""Tally votes from one closed ballot's chronological, verified transcript."""

import argparse
import json
from pathlib import Path


def tally_votes(messages, ballot_id):
    """Return counts and latest votes keyed by Discord account ID."""
    latest = {}
    for message in messages:
        author = message.get("author_id")
        if message.get("author_type") != "human" or not author:
            continue
        parts = message.get("content", "").strip().upper().split()
        if len(parts) == 2 and parts[0] == ballot_id.upper() and parts[1] in ("A", "B", "MORE INFO"):
            latest[author] = parts[1]
        elif len(parts) == 3 and parts[0] == ballot_id.upper() and parts[1:] == ["MORE", "INFO"]:
            latest[author] = "MORE INFO"
    counts = {option: sum(vote == option for vote in latest.values()) for option in ("A", "B", "MORE INFO")}
    return {"counts": counts, "votes": latest}


def ballot_outcome(counts, round_number):
    """Require a strict majority of valid votes; permit only one follow-up."""
    if round_number not in (1, 2):
        raise ValueError("round_number must be 1 or 2")
    total = sum(counts.get(option, 0) for option in ("A", "B", "MORE INFO"))
    for option in ("A", "B"):
        if counts.get(option, 0) > total / 2:
            return option
    return "FOLLOW_UP" if round_number == 1 else "PENDING"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ballot_id")
    parser.add_argument("transcript", type=Path, help="JSON array in Discord message order")
    args = parser.parse_args()
    messages = json.loads(args.transcript.read_text(encoding="utf-8"))
    print(json.dumps(tally_votes(messages, args.ballot_id), indent=2))


if __name__ == "__main__":
    main()
