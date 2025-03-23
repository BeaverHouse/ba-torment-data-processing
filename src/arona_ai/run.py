import requests
from collections import defaultdict

def parse_arona_ai_data(arona_ai_data: dict) -> dict:
    """Arona AI 데이터를 BA Torment 파티 데이터 형식으로 변환합니다.
    
    Args:
        arona_ai_data (dict): Arona AI에서 제공하는 총력전 데이터
        
    Returns:
        dict: BA Torment 파티 데이터 형식으로 변환된 데이터
    """
    # 필터 데이터 초기화
    filters = defaultdict(lambda: [0] * 9)
    assist_filters = defaultdict(lambda: [0] * 9)
    parties = []
    
    # 각 파티 데이터 처리
    for rank_data in arona_ai_data["d"]:
        rank = rank_data["r"]
        score = rank_data["s"]
        
        # 파티 데이터 생성
        party_data = defaultdict(list)
        
        # 각 파티 처리
        for i, party in enumerate(rank_data["t"], 1):
            # 파티 멤버 초기화 (6개의 0으로)
            party_members = [0] * 6
            member_idx = 0
            
            # 스트라이커 처리
            for char in party["m"]:
                if not char:  # None 체크
                    member_idx += 1
                    continue
                    
                char_id = str(char["id"])
                star = char["star"]
                weapon_star = char["weaponStar"] if char["hasWeapon"] else 0
                is_assist = 1 if char["isAssist"] else 0
                
                # 캐릭터 ID 생성 (8자리)
                char_id_full = f"{char_id:0>5}{star}{weapon_star}{is_assist}"
                party_members[member_idx] = int(char_id_full)
                member_idx += 1
                
                # 필터 데이터 업데이트
                filter_list = assist_filters if char["isAssist"] else filters
                if star < 5:
                    filter_list[char_id][star] += 1  # 1성~4성
                else:
                    filter_list[char_id][5 + weapon_star] += 1  # 5성(전용무기 1성~3성)
            
            # 서포터 처리
            for char in party["s"]:
                if not char:  # None 체크
                    member_idx += 1
                    continue
                    
                char_id = str(char["id"])
                star = char["star"]
                weapon_star = char["weaponStar"] if char["hasWeapon"] else 0
                is_assist = 1 if char["isAssist"] else 0
                
                # 캐릭터 ID 생성 (8자리)
                char_id_full = f"{char_id:0>5}{star}{weapon_star}{is_assist}"
                party_members[member_idx] = int(char_id_full)
                member_idx += 1
                
                # 필터 데이터 업데이트
                filter_list = assist_filters if char["isAssist"] else filters
                if star < 5:
                    filter_list[char_id][star] += 1  # 1성~4성
                else:
                    filter_list[char_id][5 + weapon_star] += 1  # 5성(전용무기 1성~3성)
            
            # 파티 데이터 저장
            party_data[f"party_{i}"] = party_members
        
        # 파티 정보 추가
        party_info = {
            "FINAL_RANK": rank,
            "SCORE": score,
            "USER_ID": -1,
            "LEVEL": "L" if score >= 44000000 else "T" if score >= 31076000 else "I",
            "PARTY_DATA": dict(party_data),
            "TORMENT_RANK": rank
        }
        parties.append(party_info)
    
    # 최종 데이터 구성
    result = {
        "filters": dict(filters),
        "assist_filters": dict(assist_filters),
        "min_partys": 1,
        "max_partys": 15,
        "parties": parties
    }
    
    return result

def upload_json_data_to_oracle(json_data: dict):
    pass


if __name__ == "__main__":
    season = 74
    
    arona_ai_data_url = f"https://media.arona.ai/data/v3/raid/{season}/team-in20000"
    json_data = requests.get(arona_ai_data_url).json()

    parse_arona_ai_data(json_data)
    upload_json_data_to_oracle(json_data)
