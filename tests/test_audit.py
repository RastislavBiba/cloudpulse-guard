from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Overenie health endpointu."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_index_dashboard():
    """Overenie načítania webového UI."""
    response = client.get("/")
    assert response.status_code == 200
    assert "CloudPulse Guard" in response.text


@patch("app.auditor.execute_agent_run")
def test_audit_api_mocked(mock_execute_run):
    """Overenie orchestrácie cez mockované volania Azure AI Agent Service (0 tokenov, bez 429)."""
    mock_execute_run.side_effect = [
        # 1. Mock Triage Agenta
        (
            '{"severity": "LOW", "component": "Kubernetes Pod", "clean_summary": "Test pod spec"}',
            10,
            20,
        ),
        # 2. Mock Remediation Agenta
        (
            '{"findings": [{"severity": "LOW", "issue": "Chýba limit", "recommendation": "Pridať resources"}], "remediated_snippet": "resources:\\n  limits:\\n    cpu: 100m"}',
            25,
            40,
        ),
        # 3. Mock Safety Agenta
        (
            '{"compliance_score": 95, "safety_verdict": "SCHVÁLENO", "audit_comment": "Bezpečný manifest"}',
            15,
            10,
        ),
    ]

    payload = {
        "code_snippet": "apiVersion: v1\nkind: Pod\nmetadata:\n  name: test-pod",
        "code_type": "kubernetes",
    }

    response = client.post("/api/audit", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["severity"] == "LOW"
    assert data["compliance_score"] == 95
    assert "Test pod spec" in data["summary"]
    assert "Bezpečný manifest" in data["summary"]
    assert "remediated_snippet" in data
    assert data["total_tokens"] == 120
    assert mock_execute_run.call_count == 3
