import json
import os
from arona_ai.run import parse_arona_ai_party_data, parse_arona_ai_summary_data

def test_arona_ai_party_data():
    """This function test can be run using the following command:
    
    python -m pytest tests/arona_ai_test.py::test_arona_ai_party_data -v
    """
    season = "S74"
    
    # File position: src/test/files/
    files_dir = os.path.join(os.path.dirname(__file__), "files")
    
    try:
        arona_ai_path = os.path.join(files_dir, f"{season}-arona-ai.json")
        ba_torment_party_path = os.path.join(files_dir, f"{season}-ba-torment-party.json")
    except Exception as e:
        print(e)
        print(f"테스트에 필요한 파일이 없습니다. 다음 파일들이 필요합니다:\n"
            f"- {arona_ai_path}\n"
            f"- {ba_torment_party_path}")
        return
    
    arona_ai_data = json.load(open(arona_ai_path, "r"))
    ba_torment_party_data = json.load(open(ba_torment_party_path, "r"))

    # Arona AI 데이터에는 USER_ID가 없기 때문에
    # 일괄적으로 BA Torment Party 데이터의 USER_ID를 테스트에서는 -1로 변경
    for data in ba_torment_party_data["parties"]:
        data["USER_ID"] = -1

    parsed_data = parse_arona_ai_party_data(arona_ai_data)

    # 각 필드별로 직접 비교하여 성능 개선
    # 필터 데이터를 키로 정렬하여 비교
    sorted_parsed_filters = dict(sorted(parsed_data["filters"].items()))
    sorted_expected_filters = dict(sorted(ba_torment_party_data["filters"].items()))
    assert sorted_parsed_filters == sorted_expected_filters, "필터 데이터가 일치하지 않습니다"

    # 어시스트 필터 데이터를 키로 정렬하여 비교 
    sorted_parsed_assist = dict(sorted(parsed_data["assist_filters"].items()))
    sorted_expected_assist = dict(sorted(ba_torment_party_data["assist_filters"].items()))
    assert sorted_parsed_assist == sorted_expected_assist, "어시스트 필터 데이터가 일치하지 않습니다"
    print("필터 데이터 비교 완료")

    assert parsed_data["min_partys"] == ba_torment_party_data["min_partys"], "최소 파티 수가 일치하지 않습니다"
    assert parsed_data["max_partys"] == ba_torment_party_data["max_partys"], "최대 파티 수가 일치하지 않습니다"
    print("최소, 최대 파티 수 비교 완료")
    
    assert len(parsed_data["parties"]) == len(ba_torment_party_data["parties"]), "파티 데이터 개수가 일치하지 않습니다"
    print("파티 데이터 개수 비교 완료")
    
    for i, (parsed_party, expected_party) in enumerate(zip(parsed_data["parties"], ba_torment_party_data["parties"])):
        assert parsed_party == expected_party, f"{i+1}번째 파티 데이터가 일치하지 않습니다"
        if i % 1000 == 0:
            print(f"{i+1}번째 파티 데이터 비교 완료")

def test_arona_ai_summary_data():
    """This function test can be run using the following command:
    
    python -m pytest tests/arona_ai_test.py::test_arona_ai_summary_data -v
    """
    season = "S74"

    # File position: src/test/files/
    files_dir = os.path.join(os.path.dirname(__file__), "files")

    try:
        arona_ai_path = os.path.join(files_dir, f"{season}-arona-ai.json")
        ba_torment_summary_path = os.path.join(files_dir, f"{season}-ba-torment-summary.json")
    except Exception as e:
        print(e)
        print(f"테스트에 필요한 파일이 없습니다. 다음 파일들이 필요합니다:\n"
            f"- {arona_ai_path}\n"
            f"- {ba_torment_summary_path}")
        
    arona_ai_data = json.load(open(arona_ai_path, "r"))
    ba_torment_summary_data = json.load(open(ba_torment_summary_path, "r"))

    parsed_data = parse_arona_ai_summary_data(arona_ai_data)

    for level in ["torment", "lunatic"]:
        target_data = parsed_data[level]
        expected_data = ba_torment_summary_data[level]

        print(f"{level} 데이터 비교 중...")

        assert target_data["clear_count"] == expected_data["clear_count"], f"{level} 클리어 수가 일치하지 않습니다"
        assert target_data["party_counts"] == expected_data["party_counts"], f"{level} 파티 수가 일치하지 않습니다"

        sorted_parsed_filters = dict(sorted(target_data["filters"].items()))
        sorted_expected_filters = dict(sorted(expected_data["filters"].items()))
        assert sorted_parsed_filters == sorted_expected_filters, f"{level} 필터 데이터가 일치하지 않습니다"

        sorted_parsed_assist = dict(sorted(target_data["assist_filters"].items()))
        sorted_expected_assist = dict(sorted(expected_data["assist_filters"].items()))
        assert sorted_parsed_assist == sorted_expected_assist, f"{level} 어시스트 필터 데이터가 일치하지 않습니다" 

        assert target_data["top5_partys"] == expected_data["top5_partys"], f"{level} 상위 5개 파티 데이터가 일치하지 않습니다"

if __name__ == "__main__":
    test_arona_ai_party_data()

