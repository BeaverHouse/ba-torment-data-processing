import requests
from collections import defaultdict
import polars as pl

def parse_arona_ai_party_data(arona_ai_data: dict) -> dict:
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
    for idx, rank_data in enumerate(arona_ai_data["d"]):
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
            "USER_ID": -(idx + 1),
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

def parse_arona_ai_summary_data(arona_ai_data: dict) -> dict:
    """Arona AI 데이터를 BA Torment 총력전 요약 데이터 형식으로 변환합니다.
    
    Args:
        arona_ai_data (dict): Arona AI에서 제공하는 총력전 데이터
        
    Returns:
        dict: BA Torment 총력전 요약 데이터 형식으로 변환된 데이터
    """
    # 데이터프레임 생성 및 점수로 정렬
    df = pl.DataFrame(arona_ai_data["d"]).sort("s", descending=True)
    
    # 토먼트/루나틱 데이터 분리
    lunatic_df = df.filter(pl.col("s") >= 44000000)
    lunatic_count = len(lunatic_df)
    torment_df = df.filter((pl.col("s") >= 31076000) & (pl.col("s") < 44000000))
    torment_count = len(torment_df)
    
    def get_thresholds(lunatic_count: int, torment_count: int, is_torment: bool) -> list:
        """클리어 수에 따라 적절한 임계값 목록을 반환합니다.
        
        Args:
            lunatic_count (int): 루나틱 클리어 수
            torment_count (int): 토먼트 클리어 수
            is_torment (bool): 토먼트 난이도 여부
            
        Returns:
            list: 임계값 목록
        """
        # 전체 임계값 목록
        all_thresholds = [100, 200, 500, 1000, 2000, 5000, 10000, 20000]
        
        if is_torment:
            # 토먼트는 루나틱 클리어 수보다 큰 임계값들만 사용
            thresholds = [t for t in all_thresholds if lunatic_count < t <= (lunatic_count + torment_count)]
            if not thresholds or thresholds[-1] != (lunatic_count + torment_count):
                thresholds.append(lunatic_count + torment_count)
        else:
            # 루나틱은 100부터 시작하고 루나틱 클리어 수까지
            thresholds = [t for t in all_thresholds if t <= lunatic_count]
            if not thresholds or thresholds[-1] != lunatic_count:
                thresholds.append(lunatic_count)
        
        return thresholds
    
    def process_level_data(df: pl.DataFrame, level: str) -> dict:
        """각 레벨(토먼트/루나틱)의 데이터를 처리합니다."""
        # 클리어 수 계산
        clear_count = len(df)
        
        # 파티 수 통계 계산
        party_counts = {}
        
        # 임계값 계산
        thresholds = get_thresholds(lunatic_count, torment_count, level == "torment")
        
        # 각 임계값에 대해 파티 수 통계 계산
        for threshold in thresholds:
            # 해당 임계값까지의 데이터만 사용
            filtered_df = df.filter((pl.col("r") <= threshold))

            party_count = [0] * 4  # [1파티, 2파티, 3파티, 4파티 이상]
            
            for row in filtered_df.iter_rows():
                num_parties = len(row[2]) # t 필드의 길이 = 파티 수
                if num_parties >= 4:
                    party_count[3] += 1
                elif num_parties > 0:  # 0파티는 카운트하지 않음
                    party_count[num_parties - 1] += 1
            
            if any(party_count):  # 모든 값이 0이 아닌 경우만 저장
                party_counts[f"in{threshold}"] = party_count
        
        # 필터 데이터 계산
        filters = defaultdict(lambda: [0] * 9)
        assist_filters = defaultdict(lambda: [0] * 9)
        
        # 각 파티의 캐릭터 정보 처리
        for row in df.iter_rows():
            for party in row[2]:  # row[2]는 "t" 필드
                for char in party["m"] + party["s"]:  # 스트라이커와 서포터 모두 처리
                    if not char:
                        continue
                        
                    char_id = str(char["id"])
                    star = char["star"]
                    weapon_star = char["weaponStar"] if char["hasWeapon"] else 0
                    is_assist = char["isAssist"]
                    
                    # 필터 데이터 업데이트
                    if star < 5:
                        filters[char_id][star] += 1
                        if is_assist:
                            assist_filters[char_id][star] += 1
                    else:
                        filters[char_id][5 + weapon_star] += 1
                        if is_assist:
                            assist_filters[char_id][5 + weapon_star] += 1
        # 사용량이 1% 미만인 필터 제거
        filters_to_remove = []
        for key in filters.keys():
            if sum(filters[key]) < 0.01 * clear_count:
                filters_to_remove.append(key)
        for key in filters_to_remove:
            del filters[key]
            
        assist_filters_to_remove = []
        for key in assist_filters.keys():
            if sum(assist_filters[key]) < 0.01 * clear_count:
                assist_filters_to_remove.append(key)
        for key in assist_filters_to_remove:
            del assist_filters[key]
        
        # 상위 5개 파티 계산
        top5_partys = []
        party_usage = defaultdict(int)
        
        for row in df.iter_rows():
            total_char_ids = []
            for party in row[2]:
                char_ids = []
                for char in party["m"] + party["s"]:
                    if char:
                        char_ids.append(str(char["id"]))
                total_char_ids.extend(sorted(char_ids))
            party_key = "_".join(total_char_ids)
            party_usage[party_key] += 1
        
        # 상위 5개 파티 선택
        for party_key, count in sorted(party_usage.items(), key=lambda x: x[1], reverse=True)[:5]:
            top5_partys.append([party_key, count])
        
        return {
            "clear_count": clear_count,
            "party_counts": party_counts,
            "filters": dict(filters),
            "assist_filters": dict(assist_filters),
            "top5_partys": top5_partys
        }
    
    # 최종 데이터 구성
    result = {
        "torment": process_level_data(torment_df, "torment"),
        "lunatic": process_level_data(lunatic_df, "lunatic")
    }
    
    return result


def upload_json_data_to_oracle(json_data: dict):
    pass


if __name__ == "__main__":
    season = 74
    
    arona_ai_data_url = f"https://media.arona.ai/data/v3/raid/{season}/team-in20000"
    json_data = requests.get(arona_ai_data_url).json()

    parse_arona_ai_party_data(json_data)
    parse_arona_ai_summary_data(json_data)
    upload_json_data_to_oracle(json_data)
