# tests/test_soccer_stats.py
import pytest
from fastapi.testclient import TestClient
from src.soccer_stats import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to Soccer Stats API!" in response.json()["message"]

def test_get_player():
    # Using Mohamed Salah's ID as an example
    player_id = 276
    response = client.get(f"/player/{player_id}")
    assert response.status_code == 200