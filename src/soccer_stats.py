# src/soccer_stats.py
import os
import json
import requests
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Soccer Stats API")

class SoccerStats:
    def __init__(self):
        self.api_key = os.getenv('RAPID_API_KEY')
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

    async def get_player_stats(self, player_id: int, season: int = 2023):
        """Fetch player statistics for a given season"""
        try:
            url = f"{self.base_url}/players"
            params = {
                "id": player_id,
                "season": season
            }
            
            response = requests.get(
                url, 
                headers=self.headers, 
                params=params
            )
            response.raise_for_status()
            
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch player stats: {str(e)}"
            )

    async def get_top_scorers(self, league_id: int = 39, season: int = 2023):
        """Fetch top scorers for a league (default: Premier League)"""
        try:
            url = f"{self.base_url}/players/topscorers"
            params = {
                "league": league_id,
                "season": season
            }
            
            response = requests.get(
                url, 
                headers=self.headers, 
                params=params
            )
            response.raise_for_status()
            
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch top scorers: {str(e)}"
            )

# Initialize our stats class
stats = SoccerStats()

# API Routes
@app.get("/")
async def root():
    return {
        "message": "Welcome to Soccer Stats API!",
        "endpoints": [
            "/player/{player_id}",
            "/topscorers/{league_id}"
        ]
    }

@app.get("/player/{player_id}")
async def get_player(player_id: int, season: int = 2023):
    """Get stats for a specific player"""
    return await stats.get_player_stats(player_id, season)

@app.get("/topscorers/{league_id}")
async def get_top_scorers(league_id: int = 39, season: int = 2023):
    """Get top scorers for a league"""
    return await stats.get_top_scorers(league_id, season)

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": str(exc.detail),
        "status_code": exc.status_code
    }