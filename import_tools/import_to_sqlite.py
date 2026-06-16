#!/usr/bin/env python3
"""
K12知识点导入SQLite工具
将knowledge_base下的JSON文件导入到SQLite数据库

用法:
    python import_to_sqlite.py --source ../knowledge_base/ --db k12.db
"""

import json
import sqlite3
import argparse
import os
import sys
from pathlib import Path


def create_tables(conn):
    """创建数据库表"""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS knowledge_points (
            id TEXT PRIMARY KEY,
            subject TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT,
            grade TEXT,
            difficulty INTEGER,
            description TEXT,
            key_concepts TEXT,
            formulas TEXT,
            examples TEXT,
            common_mistakes TEXT,
            related_points TEXT,
            grade_range TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_subject ON knowledge_points(subject);
        CREATE INDEX IF NOT EXISTS idx_grade ON knowledge_points(grade);
        CREATE INDEX IF NOT EXISTS idx_category ON knowledge_points(category);
        CREATE INDEX IF NOT EXISTS idx_difficulty ON knowledge_points(difficulty);

        CREATE TABLE IF NOT EXISTS subjects (
            name TEXT PRIMARY KEY,
            grade_range TEXT,
            version TEXT,
            point_count INTEGER
        );
    """)


def import_subject(conn, json_path, subject_name):
    """导入单个学科的JSON文件"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    subject = data.get('subject', subject_name)
    grade_range = data.get('grade_range', '')
    version = data.get('version', '1.0.0')
    points = data.get('knowledge_points', [])

    count = 0
    for kp in points:
        conn.execute("""
            INSERT OR REPLACE INTO knowledge_points
            (id, subject, title, category, grade, difficulty, description,
             key_concepts, formulas, examples, common_mistakes, related_points, grade_range)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            kp.get('id', ''),
            subject,
            kp.get('title', ''),
            kp.get('category', ''),
            kp.get('grade', ''),
            kp.get('difficulty', 0),
            kp.get('description', ''),
            json.dumps(kp.get('key_concepts', []), ensure_ascii=False),
            json.dumps(kp.get('formulas', []), ensure_ascii=False),
            json.dumps(kp.get('examples', []), ensure_ascii=False),
            json.dumps(kp.get('common_mistakes', []), ensure_ascii=False),
            json.dumps(kp.get('related_points', []), ensure_ascii=False),
            grade_range
        ))
        count += 1

    conn.execute("""
        INSERT OR REPLACE INTO subjects (name, grade_range, version, point_count)
        VALUES (?, ?, ?, ?)
    """, (subject, grade_range, version, count))

    return count


def main():
    parser = argparse.ArgumentParser(description='导入K12知识点到SQLite')
    parser.add_argument('--source', required=True, help='knowledge_base目录路径')
    parser.add_argument('--db', default='k12.db', help='SQLite数据库文件路径')
    args = parser.parse_args()

    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"错误: 源目录不存在: {source_dir}")
        sys.exit(1)

    conn = sqlite3.connect(args.db)
    create_tables(conn)

    total = 0
    subject_dirs = [d for d in source_dir.iterdir() if d.is_dir()]

    for subj_dir in sorted(subject_dirs):
        json_file = subj_dir / 'knowledge_points.json'
        if json_file.exists():
            count = import_subject(conn, json_file, subj_dir.name)
            print(f"  ✓ {subj_dir.name}: {count} 个知识点")
            total += count
        else:
            print(f"  ⚠ {subj_dir.name}: 未找到 knowledge_points.json")

    conn.commit()
    conn.close()
    print(f"\n完成! 共导入 {total} 个知识点到 {args.db}")


if __name__ == '__main__':
    main()
