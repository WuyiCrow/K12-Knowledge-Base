#!/usr/bin/env python3
"""
K12知识点导入向量数据库工具
将知识点转换为向量嵌入，支持语义搜索

用法:
    python import_to_vector_db.py --source ../knowledge_base/ --db k12_vectors.db
    
依赖:
    pip install numpy  # 基础向量计算（可选，无依赖时存原始文本）
"""

import json
import sqlite3
import argparse
import os
import sys
import hashlib
from pathlib import Path


def create_vector_tables(conn):
    """创建向量数据库表"""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS vector_store (
            id TEXT PRIMARY KEY,
            subject TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT,
            grade TEXT,
            difficulty INTEGER,
            content_text TEXT,
            content_hash TEXT,
            embedding BLOB
        );

        CREATE INDEX IF NOT EXISTS vs_subject ON vector_store(subject);
        CREATE INDEX IF NOT EXISTS vs_grade ON vector_store(grade);
        CREATE INDEX IF NOT EXISTS vs_hash ON vector_store(content_hash);
    """)


def build_content_text(kp):
    """将知识点构建为可搜索的文本块"""
    parts = []
    parts.append(f"学科: {kp.get('subject', '')}")
    parts.append(f"标题: {kp.get('title', '')}")
    parts.append(f"分类: {kp.get('category', '')}")
    parts.append(f"年级: {kp.get('grade', '')}")
    parts.append(f"描述: {kp.get('description', '')}")

    concepts = kp.get('key_concepts', [])
    if concepts:
        parts.append(f"核心概念: {', '.join(concepts)}")

    formulas = kp.get('formulas', [])
    if formulas:
        parts.append(f"公式: {'; '.join(formulas)}")

    mistakes = kp.get('common_mistakes', [])
    if mistakes:
        parts.append(f"常见错误: {'; '.join(mistakes)}")

    return '\n'.join(parts)


def compute_simple_hash(text):
    """计算内容哈希（用于去重）"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def compute_simple_embedding(text, dim=128):
    """
    简单的伪向量嵌入（基于字符hash）
    实际生产环境应替换为真实的embedding模型
    """
    try:
        import numpy as np
        # 基于字符的简单hash向量
        vec = np.zeros(dim, dtype=np.float32)
        for i, char in enumerate(text):
            idx = ord(char) % dim
            vec[idx] += 1.0 / (1 + i * 0.01)
        # L2归一化
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tobytes()
    except ImportError:
        # 无numpy时存储为text的hash
        return hashlib.md5(text.encode('utf-8')).digest()


def import_to_vectors(conn, json_path, subject_name):
    """导入单个学科到向量数据库"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    points = data.get('knowledge_points', [])
    count = 0

    for kp in points:
        content_text = build_content_text(kp)
        content_hash = compute_simple_hash(content_text)
        embedding = compute_simple_embedding(content_text)

        conn.execute("""
            INSERT OR REPLACE INTO vector_store
            (id, subject, title, category, grade, difficulty, content_text, content_hash, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            kp.get('id', ''),
            data.get('subject', subject_name),
            kp.get('title', ''),
            kp.get('category', ''),
            kp.get('grade', ''),
            kp.get('difficulty', 0),
            content_text,
            content_hash,
            embedding
        ))
        count += 1

    return count


def main():
    parser = argparse.ArgumentParser(description='导入K12知识点到向量数据库')
    parser.add_argument('--source', required=True, help='knowledge_base目录路径')
    parser.add_argument('--db', default='k12_vectors.db', help='向量数据库文件路径')
    parser.add_argument('--dim', type=int, default=128, help='向量维度（默认128）')
    args = parser.parse_args()

    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"错误: 源目录不存在: {source_dir}")
        sys.exit(1)

    conn = sqlite3.connect(args.db)
    create_vector_tables(conn)

    total = 0
    subject_dirs = [d for d in source_dir.iterdir() if d.is_dir()]

    for subj_dir in sorted(subject_dirs):
        json_file = subj_dir / 'knowledge_points.json'
        if json_file.exists():
            count = import_to_vectors(conn, json_file, subj_dir.name)
            print(f"  ✓ {subj_dir.name}: {count} 个知识点已向量化")
            total += count
        else:
            print(f"  ⚠ {subj_dir.name}: 未找到 knowledge_points.json")

    conn.commit()
    conn.close()
    print(f"\n完成! 共向量化 {total} 个知识点到 {args.db}")
    print("提示: 生产环境请替换为真实embedding模型（如text2vec-large-chinese）")


if __name__ == '__main__':
    main()
