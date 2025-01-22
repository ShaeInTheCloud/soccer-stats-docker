# Containerized Soccer Stats App

## Project Overview
Part of the 30 Days DevOps Challenge - Week 2: Containers & Microservices. This project implements a containerized soccer statistics application using Docker, Python, and the Football API.

## Architecture
```mermaid
flowchart LR
    API[Football API] -->|Match Data| DC[Docker Container]
    
    subgraph Docker Container
        App[Python App]
        Config[Config Files]
        Cache[Data Cache]
    end
    
    DC -->|Process| Stats[Stats Processing]
    Stats -->|Store| Results[(Results Storage)]
```

## Technologies Used
- Docker
- Python/FastAPI
- Soccer API (api-football-v1.p.rapidapi.com)
- pytest for testing

## Project Structure
```bash
soccer-stats-docker/
├── src/
│   ├── __init__.py
│   └── soccer_stats.py
├── tests/
│   └── test_soccer_stats.py
├── Dockerfile
├── requirements.txt
└── .env
```

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repo-url>
cd soccer-stats-docker
```

2. Create a `.env` file with your API key:
```bash
RAPID_API_KEY=your_api_key_here
```

3. Build the Docker image:
```bash
docker build -t soccer-stats .
```

4. Run the container:
```bash
docker run -p 8000:8000 --env-file .env soccer-stats
```

## API Endpoints
- `/` - Welcome message and available endpoints
- `/health` - Health check endpoint
- `/player/{player_id}` - Get player statistics
- `/topscorers/{league_id}` - Get top scorers for a league (default: Premier League)

## Debugging Tips

### Common Issues and Solutions

1. Docker Permission Issues
```bash
# If you get permission denied errors:
sudo usermod -aG docker $USER
newgrp docker
```

2. API Key Issues
- Ensure your RAPID_API_KEY is correctly set in .env
- Verify the API key is valid at RapidAPI
- Check if the key is being properly passed to the container

3. Container Access Issues
```bash
# Check if container is running
docker ps

# View container logs
docker logs <container-id>

# Access container shell
docker exec -it <container-id> /bin/bash
```

## Resource Cleanup

Clean up Docker resources when you're done:

```bash
# Stop the container
docker stop $(docker ps -q --filter ancestor=soccer-stats)

# Remove the container
docker rm $(docker ps -aq --filter ancestor=soccer-stats)

# Remove the image
docker rmi soccer-stats

# Remove all unused containers, networks, images (use with caution)
docker system prune
```

## Contributing
Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)