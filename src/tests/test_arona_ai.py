import json
import os
from arona_ai.run import parse_arona_ai_data

def test_arona_ai():
    """This function test can be run using the following command:
    
    python -m pytest tests/arona_ai_test.py::test_arona_ai -v
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

    parsed_data = parse_arona_ai_data(arona_ai_data)

    # 두 데이터를 정렬된 문자열로 변환하여 비교
    parsed_json_str = json.dumps(parsed_data, sort_keys=True)
    expected_json_str = json.dumps(ba_torment_party_data, sort_keys=True)
    assert parsed_json_str == expected_json_str, "JSON 데이터가 일치하지 않습니다."

if __name__ == "__main__":
    test_arona_ai()

