import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "reports.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database with reports table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                sources TEXT NOT NULL,
                summary TEXT NOT NULL,
                key_points TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_report(self, query: str, sources: List[Dict], summary: str, key_points: List[str]) -> int:
        """Save a research report to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO reports (query, sources, summary, key_points)
            VALUES (?, ?, ?, ?)
        """, (query, json.dumps(sources), summary, json.dumps(key_points)))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return report_id
    
    def get_all_reports(self) -> List[Dict]:
        """Get all reports from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM reports ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        reports = []
        for row in rows:
            reports.append({
                'id': row[0],
                'query': row[1],
                'sources': json.loads(row[2]),
                'summary': row[3],
                'key_points': json.loads(row[4]),
                'created_at': row[5]
            })
        
        return reports
    
    def get_report(self, report_id: int) -> Optional[Dict]:
        """Get a specific report by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'query': row[1],
                'sources': json.loads(row[2]),
                'summary': row[3],
                'key_points': json.loads(row[4]),
                'created_at': row[5]
            }
        
        return None