from datetime import datetime
from typing import List
from common.connect_db import get_postgres_client

def get_videos_after_date(date: datetime) -> List[dict]:
    """
    특정 날짜 이후에 생성된 영상 정보들을 가져옵니다.
    채널 정보는 제외합니다.
    
    Args:
        date (datetime): 기준이 되는 날짜
        
    Returns:
        List[dict]: 영상 정보 리스트
    """
    with get_postgres_client() as cur:
        cur.execute("""
            SELECT * FROM ba_torment.named_users 
            WHERE created_at >= %s 
            AND raid_id IS NOT NULL
        """, (date,))
        return cur.fetchall()

def has_channel(user_id: int) -> bool:
    """
    특정 유저 ID에 대한 채널 정보가 있는지 확인합니다.
    
    Args:
        user_id (int): 확인할 유저 ID
        
    Returns:
        bool: 채널 정보 존재 여부
    """
    with get_postgres_client() as cur:
        cur.execute("""
            SELECT COUNT(*) FROM ba_torment.named_users 
            WHERE user_id = %s 
            AND raid_id IS NULL
        """, (user_id,))
        return cur.fetchone()[0] > 0

def update_user_channel(user_id: int, channel_name: str, channel_url: str) -> bool:
    """
    특정 유저의 채널 정보를 업데이트합니다.
    
    Args:
        user_id (int): 업데이트할 유저 ID
        channel_name (str): 채널 사용자명
        channel_url (str): 채널 URL
        
    Returns:
        bool: 업데이트 성공 여부
    """
    try:
        with get_postgres_client() as cur:
            sql = """
                INSERT INTO ba_torment.named_users (user_id, raid_id, description, youtube_url, created_at, updated_at, score)
                VALUES (%s, NULL, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)
            """
            cur.execute(sql, (user_id, channel_name, channel_url))
            return cur.rowcount > 0
    except Exception as e:
        raise e
