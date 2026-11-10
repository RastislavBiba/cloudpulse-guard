import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Overenie health check endpointu."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "cloudpulse-guard"}

def test_index_dashboard():
    """Overenie načítania webového UI."""
    response = client.get("/")
    assert response.status_code == 200
    assert "CloudPulse Guard & LLMOps" in response.text
    assert "NOTIX" in response.text

@patch("app.auditor.get_azure_client")
def test_audit_api_mocked(mock_get_client):
    """Overenie audítora cez mockované volanie Azure OpenAI."""
    fake_client = MagicMock()
    mock_response = MagicMock()
    
    mock_response.choices = [
        MagicMock(message=MagicMock(content='''{
            "summary": "Mocked test summary",
            "compliance_score": 85,
            "severity": "LOW",
            "findings": [
                {
                    "severity": "LOW",
                    "issue": "Test issue",
                    "recommendation": "Test fix"
                }
            ],
            "remediated_snippet": "apiVersion: v1"
        }'''))
    ]
    mock_response.usage = MagicMock(prompt_tokens=50, completion_tokens=100, total_tokens=150)
    fake_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = fake_client

    payload = {
        "code_snippet": "apiVersion: v1\nkind: Pod",
        "code_type": "kubernetes"
    }

    response = client.post("/api/audit", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["compliance_score"] == 85
    assert data["severity"] == "LOW"
    assert data["total_tokens"] == 150
    assert data["cost_usd"] > 0
    assert len(data["findings"]) == 1
