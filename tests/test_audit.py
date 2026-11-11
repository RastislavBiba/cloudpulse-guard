# tests/test_audit.py
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


@patch("app.agents.triage.execute_agent_run")
@patch("app.agents.remediation.execute_agent_run")
@patch("app.agents.safety.execute_agent_run")
def test_audit_api_mocked(mock_safety_run, mock_remed_run, mock_triage_run):
    """Overenie orchestrácie cez mockované volania Azure AI Agent Service (0 tokenov, bez 429)."""

    # 1. Mock Triage Agenta
    mock_triage_run.return_value = (
        '{"severity": "LOW", "component": "Kubernetes Pod", "stack_category": "K8s", "clean_summary": "Test pod spec"}',
        10, 20
    )

    # 2. Mock Remediation Agenta
    mock_remed_run.return_value = (
        '{"findings": [{"severity": "LOW", "issue": "Chýba limit", "recommendation": "Pridať resources"}], "remediated_snippet": "resources:\\n  limits:\\n    cpu: 100m"}',
        25, 40
    )

    # 3. Mock Safety Agenta
    mock_safety_run.return_value = (
        '{"compliance_score": 95, "safety_verdict": "SCHVÁLENO", "audit_comment": "Bezpečný manifest"}',
        15, 10
    )

    payload = {
        "code_snippet": "apiVersion: v1\nkind: Pod\nmetadata:\n  name: test-pod",
        "code_type": "kubernetes"
    }

    response = client.post("/api/audit", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["severity"] == "LOW"
    assert data["compliance_score"] == 95
    assert "Test pod spec" in data["summary"]
    assert "Bezpečný manifest" in data["summary"]
    assert "remediated_snippet" in data

    # Overenie, že všetci traja sub-agenti boli zavolaní presne raz
    assert mock_triage_run.call_count == 1
    assert mock_remed_run.call_count == 1
    assert mock_safety_run.call_count == 1
