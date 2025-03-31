from delete_season_data.db import get_old_raid_ids, delete_raid_by_id, delete_named_users_by_raid_id

def delete_old_raid_data(days: int = 200) -> None:
    """
    200일 이상 된 총력전 데이터를 삭제합니다.
    
    Args:
        days (int): 삭제할 데이터의 경과 일수 (기본값: 200)
    """
    old_raid_ids = get_old_raid_ids(days)
    print(f"삭제할 총력전 ID 목록: {old_raid_ids}")
    
    for raid_id in old_raid_ids:
        print(f"총력전 ID {raid_id} 삭제 중...")
        delete_raid_by_id(raid_id)
        delete_named_users_by_raid_id(raid_id)
        print(f"총력전 ID {raid_id} 삭제 완료")

if __name__ == "__main__":
    delete_old_raid_data()
