import sqlite3
import os
from typing import List, Dict, Any, Optional

class ManseryukDB:
    """만세력 데이터베이스 연결 및 쿼리 클래스"""
    
    def __init__(self, db_path: str = "./manseryukDB/DB/manseryuk.db"):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.BASE_DIR, "..", "..", db_path)
        
    def get_connection(self):
        """데이터베이스 연결 생성"""
        return sqlite3.connect(self.db_path)
    
    def get_birth_data(self, year: int, month: int, day: int) -> Optional[Dict[str, Any]]:
        """생년월일로 만세력 데이터 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            query = """
                SELECT * FROM calenda_data 
                WHERE cd_sy = ? AND cd_sm = ? AND cd_sd = ?
            """
            cursor.execute(query, (year, month, day))
            result = cursor.fetchone()
            
            if result:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, result))
            return None
            
        finally:
            conn.close()
    
    def get_time_ganzhi(self, time: int) -> tuple:
        """시간을 12지지로 변환"""
        jitime = [
            ('子','자'), ('丑','축'), ('寅','인'), ('卯','묘'), 
            ('辰','진'), ('巳','사'), ('午','오'), ('未','미'),
            ('申','신'), ('酉','유'), ('戌','술'), ('亥','해')
        ]
        
        if time > 23 or time < 0:
            return ('', '')
        
        ptime = time + 1
        if ptime == 24:
            ptime = 0
        
        itime = int(ptime / 2)
        return jitime[itime]
    
    def get_ganzhi_by_date_range(self, start_year: int, end_year: int) -> List[Dict[str, Any]]:
        """특정 연도 범위의 간지 데이터 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            query = """
                SELECT cd_sy, cd_sm, cd_sd, cd_hyganjee, cd_kyganjee, 
                       cd_hmganjee, cd_kmganjee, cd_hdganjee, cd_kdganjee
                FROM calenda_data 
                WHERE cd_sy BETWEEN ? AND ?
                ORDER BY cd_sy, cd_sm, cd_sd
            """
            cursor.execute(query, (start_year, end_year))
            results = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in results]
            
        finally:
            conn.close()

# 싱글톤 인스턴스 생성
manseryuk_db = ManseryukDB()