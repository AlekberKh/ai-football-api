import requests 

API_KEY  = "dce0605cf426404096200d4c7f3efa23"
BASE_URL = "https://api.football-data.org/v4"

headers = {
    "X-Auth-Token": API_KEY
}

def get_team_matches(team_id, limit=5):
    url = f"{BASE_URL}/teams/{team_id}/matches?status=FINISHED&limit={limit}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def get_teams_in_competition(competition_id=2021):
    url = f"{BASE_URL}/competitions/{competition_id}/teams"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["teams"]
    else:
        return {"error": response.text}

def find_team_id_by_name(team_name, competition_id=2021):
    teams = get_teams_in_competition(competition_id)
    for team in teams:
        if team_name.lower() in team["name"].lower():
            return team["id"]
    return None