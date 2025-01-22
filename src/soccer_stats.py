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
        if not self.api_key:
            raise ValueError("RAPID_API_KEY environment variable is not set")
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
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"API Error: {response.text}"
                )
            
            data = response.json()
            if not data.get("response"):
                return {"message": "No data found for this player"}
                
            return data
            
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
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"API Error: {response.text}"
                )
            
            return response.json()
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch top scorers: {str(e)}"
            )

# Initialize our stats class
stats = SoccerStats()

@app.get("/")
async def root():
    """Root endpoint showing available endpoints and basic info"""
    return {
        "message": "Welcome to Soccer Stats API!",
        "version": "1.0",
        "endpoints": [
            "/player/{player_id} - Get player statistics",
            "/topscorers/{league_id} - Get top scorers for a league"
        ],
        "default_league": "Premier League (ID: 39)"
    }

@app.get("/player/{player_id}")
async def get_player(player_id: int, season: int = 2023):
    """Get stats for a specific player"""
    return await stats.get_player_stats(player_id, season)

@app.get("/topscorers/{league_id}")
async def get_top_scorers(league_id: int = 39, season: int = 2023):
    """Get top scorers for a league"""
    return await stats.get_top_scorers(league_id, season)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}