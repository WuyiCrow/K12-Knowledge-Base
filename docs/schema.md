# K12知识库数据结构文档

## 概述

K12知识库采用JSON格式存储各学科的结构化知识点数据。每个学科独立一个目录，包含`knowledge_points.json`文件。

## 顶层结构

```json
{
  "subject": "学科名称",
  "grade_range": "适用年级范围",
  "version": "数据版本号",
  "knowledge_points": [...]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| subject | string | 学科名称（中文） |
| grade_range | string | 适用年级范围，如"高一-高三" |
| version | string | 语义化版本号，如"1.0.0" |
| knowledge_points | array | 知识点数组 |

## 知识点结构 (KnowledgePoint)

```json
{
  "id": "math_001",
  "title": "函数的概念与性质",
  "category": "函数",
  "grade": "高一",
  "difficulty": 3,
  "description": "理解函数的定义...",
  "key_concepts": ["定义域", "值域", "单调性"],
  "formulas": ["y = f(x)"],
  "examples": [...],
  "common_mistakes": ["忽略定义域限制"],
  "related_points": ["math_002"]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | ✓ | 唯一标识符，格式：`{学科缩写}_{序号}` |
| title | string | ✓ | 知识点标题 |
| category | string | ✓ | 知识点分类 |
| grade | string | ✓ | 适用年级 |
| difficulty | int | ✓ | 难度等级（1-5，5最难） |
| description | string | ✓ | 知识点描述（200字以内） |
| key_concepts | string[] | ✓ | 核心概念关键词列表 |
| formulas | string[] | - | 重要公式列表（文科可为空） |
| examples | object[] | ✓ | 典型例题列表 |
| common_mistakes | string[] | ✓ | 常见错误/易错点列表 |
| related_points | string[] | - | 关联知识点ID列表 |

## ID命名规范

| 学科 | 前缀 | 示例 |
|------|------|------|
| 数学 | math_ | math_001 |
| 物理 | phy_ | phy_001 |
| 化学 | chem_ | chem_001 |
| 生物 | bio_ | bio_001 |
| 语文 | cn_ | cn_001 |
| 英语 | eng_ | eng_001 |
| 历史 | hist_ | hist_001 |
| 地理 | geo_ | geo_001 |
| 政治 | pol_ | pol_001 |

## 难度等级定义

| 等级 | 含义 | 说明 |
|------|------|------|
| 1 | 入门 | 基本概念认知 |
| 2 | 基础 | 基础知识掌握 |
| 3 | 中等 | 理解应用层面 |
| 4 | 进阶 | 综合分析能力 |
| 5 | 困难 | 深度推理与综合 |

## 例题结构 (Example)

```json
{
  "problem": "题目描述",
  "solution": "解题过程和答案"
}
```

## SQLite表结构

导入SQLite后的表结构：

### knowledge_points 表

| 列名 | 类型 | 说明 |
|------|------|------|
| id | TEXT PK | 知识点ID |
| subject | TEXT | 学科 |
| title | TEXT | 标题 |
| category | TEXT | 分类 |
| grade | TEXT | 年级 |
| difficulty | INTEGER | 难度 |
| description | TEXT | 描述 |
| key_concepts | TEXT | JSON数组字符串 |
| formulas | TEXT | JSON数组字符串 |
| examples | TEXT | JSON数组字符串 |
| common_mistakes | TEXT | JSON数组字符串 |
| related_points | TEXT | JSON数组字符串 |
| grade_range | TEXT | 适用年级范围 |

### subjects 表

| 列名 | 类型 | 说明 |
|------|------|------|
| name | TEXT PK | 学科名称 |
| grade_range | TEXT | 年级范围 |
| version | TEXT | 版本号 |
| point_count | INTEGER | 知识点数量 |

## 扩展指南

### 添加新学科

1. 在 `knowledge_base/` 下创建新目录
2. 创建 `knowledge_points.json`，遵循上述结构
3. 添加 `README.md` 说明文件
4. 运行导入工具更新数据库

### 添加新知识点

1. 在对应学科的 `knowledge_points.json` 的 `knowledge_points` 数组中追加
2. 确保 `id` 全局唯一
3. 更新 `related_points` 中的关联关系
4. 重新运行导入工具

## 版本历史

- **v1.0.0** (2026-06) — 初始版本，9大学科共91个核心知识点
