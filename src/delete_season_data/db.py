from datetime import datetime, timedelta
from typing import List

from common.connect_db import get_postgres_client

def get_old_raid_ids(days: int) -> List[str]:
    """
    특정 일수 이상 경과된 총력전 ID 목록을 가져옵니다.
    
    Args:
        days (int): 경과 일수
        
    Returns:
        List[str]: 총력전 ID 목록
    """
    with get_postgres_client() as client:
        query = """
            SELECT raid_id
            FROM ba_torment.raids
            WHERE created_at < NOW() - INTERVAL '%s days'
            AND deleted_at IS NULL
        """
        
        client.execute(query, (days,))
        return [row[0] for row in client.fetchall()]

def delete_raid_by_id(raid_id: str) -> None:
    """
    raids 테이블에서 특정 총력전 ID를 가진 데이터를 삭제합니다.
    
    Args:
        raid_id (str): 삭제할 총력전 ID
    """
    with get_postgres_client() as client:
        query = """
            UPDATE ba_torment.raids
            SET deleted_at = NOW()
            WHERE raid_id = %s
            AND deleted_at IS NULL
        """
        
        client.execute(query, (raid_id,))

def delete_named_users_by_raid_id(raid_id: str) -> None:
    """
    named_users 테이블에서 특정 총력전 ID를 가진 데이터를 삭제합니다.
    
    Args:
        raid_id (str): 삭제할 총력전 ID
    """
    with get_postgres_client() as client:
        query = """
            UPDATE ba_torment.named_users
            SET deleted_at = NOW()
            WHERE raid_id = %s
            AND deleted_at IS NULL
        """
        
        client.execute(query, (raid_id,))

if __name__ == "__main__":
    raid_id = "3S14-1"
    delete_raid_by_id(raid_id)
    delete_named_users_by_raid_id(raid_id)

