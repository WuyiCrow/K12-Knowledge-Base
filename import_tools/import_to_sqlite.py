#!/usr/bin/env python3
"""K12知识库 SQLite导入工具"""

import json
import sqlite3
import os
import glob

DB_PATH = "knowledge.db"
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge_base")

def create_tables(conn):
    """创建数据表"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT,
            difficulty TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_subject ON knowledge_points(subject)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_difficulty ON knowledge_points(difficulty)
    """)
    conn.commit()

def import_subject(conn, json_path, subject_cn):
    """导入单个学科"""
    with open(json_path, 'r', encoding='utf-8') as f:
        points = json.load(f)
    
    count = 0
    for p in points:
        conn.execute("""
            INSERT INTO knowledge_points (subject, title, content, source, difficulty)
            VALUES (?, ?, ?, ?, ?)
        """, (
            p.get('subject', subject_cn),
            p.get('title', ''),
            p.get('content', ''),
            p.get('source', ''),
            p.get('difficulty', '')
        ))
        count += 1
    return count

def main():
    print(f"📚 K12知识库 → SQLite 导入工具")
    print(f"{'='*50}")
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"🗑️  清除旧数据库")
    
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    
    subjects = {
        'math': '数学', 'physics': '物理', 'chemistry': '化学',
        'biology': '生物', 'chinese': '语文', 'english': '英语',
        'history': '历史', 'geography': '地理', 'politics': '政治'
    }
    
    total = 0
    for en_name, cn_name in subjects.items():
        json_path = os.path.join(KNOWLEDGE_BASE_DIR, en_name, "knowledge_points.json")
        if os.path.exists(json_path):
            count = import_subject(conn, json_path, cn_name)
            total += count
            print(f"✅ {cn_name}: {count}条")
        else:
            print(f"⚠️  {cn_name}: 文件不存在")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"🎉 导入完成！共{total}条知识点")
    print(f"📦 数据库文件: {os.path.abspath(DB_PATH)}")

if __name__ == "__main__":
    main()
