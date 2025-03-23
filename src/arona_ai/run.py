import requests

def parse_arona_ai_data(arona_ai_data: dict) -> dict:
    return arona_ai_data

def upload_json_data_to_oracle(json_data: dict):
    pass


if __name__ == "__main__":
    season = 74
    
    arona_ai_data_url = f"https://media.arona.ai/data/v3/raid/{season}/team-in20000"
    json_data = requests.get(arona_ai_data_url).json()

    parse_arona_ai_data(json_data)
    upload_json_data_to_oracle(json_data)
