from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from football_api import find_team_id_by_name, get_team_matches

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    team1 = data.get("team1")
    team2 = data.get("team2")

    team1_id = find_team_id_by_name(team1)
    team2_id = find_team_id_by_name(team2)

    if not team1_id or not team2_id:
        return {"error": "Одна из команд не найдена"}

    matches1 = get_team_matches(team1_id)
    matches2 = get_team_matches(team2_id)

    def analyze_performance(matches):
        wins = 0
        goals = 0

        for match in matches["matches"]:
            is_home = match["homeTeam"]["id"] == match["team"]["id"]
            team_score = match["score"]["fullTime"]["home"] if is_home else match["score"]["fullTime"]["away"]
            opponent_score = match["score"]["fullTime"]["away"] if is_home else match["score"]["fullTime"]["home"]
            
            goals += team_score
            if team_score > opponent_score:
                wins += 1
        
        return {
            "wins": wins,
            "goals": goals
        }

    team1_stats = analyze_performance(matches1)
    team2_stats = analyze_performance(matches2)

    team1_score = team1_stats["wins"] * 2 + team1_stats["goals"]
    team2_score = team2_stats["wins"] * 2 + team2_stats["goals"]

    total = team1_score + team2_score
    team1_pct = round((team1_score / total) * 100, 1) if total > 0 else 50
    team2_pct = round((team2_score / total) * 100, 1) if total > 0 else 50

    return {
        "team1": team1,
        "team2": team2,
        "team1_last_matches": matches1,
        "team2_last_matches": matches2,
        "team1_percent": f"{team1_pct}%",
        "team2_percent": f"{team2_pct}%",
        "team1_form": team1_stats,
        "team2_form": team2_stats,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)