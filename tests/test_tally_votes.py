import unittest

from tools.tally_votes import ballot_outcome, tally_votes


class TallyVotesTests(unittest.TestCase):
    def test_latest_human_votes_only(self):
        messages = [
            {"author_id": "owner", "author_type": "human", "content": "DA-VOTE-01 A"},
            {"author_id": "teammate", "author_type": "human", "content": "DA-VOTE-01 B"},
            {"author_id": "app", "author_type": "app", "content": "DA-VOTE-01 B"},
            {"author_id": "webhook", "author_type": "webhook", "content": "DA-VOTE-01 B"},
            {"author_id": "unknown", "content": "DA-VOTE-01 B"},
            {"author_id": "teammate", "author_type": "human", "content": "da-vote-01 a"},
            {"author_id": "teammate", "author_type": "human", "content": "DA-VOTE-02 B"},
            {"author_id": "owner", "author_type": "human", "content": "DA-VOTE-01 B extra"},
        ]
        self.assertEqual(
            tally_votes(messages, "DA-VOTE-01"),
            {"counts": {"A": 2, "B": 0, "MORE INFO": 0}, "votes": {"owner": "A", "teammate": "A"}},
        )

    def test_no_eligible_votes(self):
        self.assertEqual(tally_votes([], "DA-VOTE-01"), {"counts": {"A": 0, "B": 0, "MORE INFO": 0}, "votes": {}})

    def test_follow_up_and_latest_vote(self):
        messages = [
            {"author_id": "one", "author_type": "human", "content": "CASE-R1 A"},
            {"author_id": "one", "author_type": "human", "content": "case-r1 more info"},
            {"author_id": "two", "author_type": "human", "content": "CASE-R1 MORE INFO"},
            {"author_id": "bot", "author_type": "app", "content": "CASE-R1 B"},
        ]
        counts = tally_votes(messages, "CASE-R1")["counts"]
        self.assertEqual(counts, {"A": 0, "B": 0, "MORE INFO": 2})
        self.assertEqual(ballot_outcome(counts, 1), "FOLLOW_UP")

    def test_second_round_decision_or_pending(self):
        self.assertEqual(ballot_outcome({"A": 2, "B": 1, "MORE INFO": 0}, 2), "A")
        self.assertEqual(ballot_outcome({"A": 1, "B": 1, "MORE INFO": 0}, 1), "FOLLOW_UP")
        self.assertEqual(ballot_outcome({"A": 1, "B": 1, "MORE INFO": 0}, 2), "PENDING")
        self.assertEqual(ballot_outcome({}, 2), "PENDING")
