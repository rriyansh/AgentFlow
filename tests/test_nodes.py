from unittest.mock import patch
from app.agents.reviewer import ReviewerAgent
from app.core.state import ReviewDecision


def test_reviewer_structured_output():
    agent = ReviewerAgent()
    mock_decision = ReviewDecision(
        status="APPROVED", feedback="Looks good"
    )

    with patch.object(
        agent.structured_llm, "invoke", return_value=mock_decision
    ):
        result = agent.run(
            {"code_output": "def foo(): pass", "revision_count": 0}
        )

    assert result["review_status"] == "APPROVED"
    assert result["revision_count"] == 1
