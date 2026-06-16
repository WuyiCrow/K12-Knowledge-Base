# K12 Knowledge Base

K12教育知识库结构化数据仓库，涵盖初中至高中9大学科核心知识点。

## 目录结构

```
K12-Knowledge-Base/
├── knowledge_base/          # 各学科知识点数据
│   ├── math/                # 数学
│   ├── physics/             # 物理
│   ├── chemistry/           # 化学
│   ├── biology/             # 生物
│   ├── chinese/             # 语文
│   ├── english/             # 英语
│   ├── history/             # 历史
│   ├── geography/           # 地理
│   └── politics/            # 政治
├── import_tools/            # 数据导入工具
├── docs/                    # 文档
└── README.md
```

## 学科覆盖

| 学科 | 知识点数量 | 适用年级 |
|------|-----------|---------|
| 数学 | 12 | 高一-高三 |
| 物理 | 10 | 高一-高三 |
| 化学 | 10 | 高一-高三 |
| 生物 | 12 | 高一-高三 |
| 语文 | 9 | 高一-高三 |
| 英语 | 8 | 高一-高三 |
| 历史 | 10 | 高一-高三 |
| 地理 | 10 | 高一-高三 |
| 政治 | 10 | 高一-高三 |

## 数据结构

每个学科的 `knowledge_points.json` 包含标准化的知识点数据，详见 [docs/schema.md](docs/schema.md)。

## 快速开始

```bash
# 导入到SQLite
python import_tools/import_to_sqlite.py --source knowledge_base/ --db k12.db

# 导入到向量数据库（用于语义搜索）
python import_tools/import_to_vector_db.py --source knowledge_base/ --db k12_vectors.db
```

## 数据来源

基于抢救的原始 K12 知识点数据（all_knowledge_points.json, for_edu_app_import.json）进行结构化整理和扩充。

## 版本

v1.0.0 — 初始版本

## License

MIT
