# AIJIAOYU
<p align="center">
基于 AI Agent 与知识孪生地图的个性化学习系统
</p>
<p align="center">
<img src="https://img.shields.io/badge/Python-3.10-blue">
<img src="https://img.shields.io/badge/Flask-Web-green">
<img src="https://img.shields.io/badge/AI-Agent-orange">
<img src="https://img.shields.io/badge/Education-Tech-red">
</p>
🎓 AIJIAOYU

> 基于 AI Agent 与知识孪生地图的个性化学习系统

## 📖 项目简介

AIJIAOYU 是一个融合人工智能代理（AI Agent）、知识图谱和动态学习路径规划的智能教育系统。
系统能够根据学生输入的学习目标：
- 自动拆解知识体系
- 智能生成学习路径
- 自动出题测评
- 实时计算掌握度
- 动态调整学习路线
- 可视化展示知识孪生地图

帮助学生实现个性化学习。
---

## ✨ 核心功能
### 🎯 学习目标解析

输入：

```text
Python变量
```
系统自动分析相关知识点并构建学习路径。

---

### 🧠 AI智能学习规划

自动生成：

```text
变量与数据类型
↓
输入输出
↓
条件判断
↓
循环结构
↓
函数
```

---

### 📝 AI自动测评

系统根据当前知识点自动生成测试题。

示例：

```text
在Python中，哪个数据类型表示整数？

A. int
B. str
C. float
D. bool
```
---

### 📊 掌握度分析

根据答题情况动态计算：

```text
变量模块

50%
↓
75%
```

实时更新学习状态。

---

### 🗺️ 知识孪生地图

不同颜色表示不同掌握状态：
🔴 未掌握（0-30%）
🟡 部分掌握（30-70%）
🟢 已掌握（70%以上）
---

### 🔄 学习路径重规划
针对薄弱知识点：
- 自动识别
- 自动补强
- 自动跳过已掌握内容
实现因材施教。

---

## 🏗️ 系统架构
```text
学生输入学习目标
          │
          ▼
    AI Agent分析
          │
          ▼
      知识点拆解
          │
          ▼
      路径规划
          │
          ▼
      AI自动出题
          │
          ▼
      掌握度评估
          │
          ▼
    知识孪生地图
          │
          ▼
      路径重规划
```
---
## 📂 项目结构

```text
AIJIAOYU
│
├── backend.py
├── main_agent.py
├── llm_utils.py
├── learning_progress.json
├── main.js
│
├── data/
│
└── templates/
    ├── index.html
    └── knowledge_map.html
```

---
## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/changan113/AIJIAOYU.git
cd AIJIAOYU
```

### 2. 创建虚拟环境

Windows
```bash
python -m venv venv

venv\Scripts\activate
```

Linux / Mac
```bash
python3 -m venv venv

source venv/bin/activate
```

---
### 3. 安装依赖
```bash
pip install flask
pip install requests
```
---

### 4. 配置大模型接口

修改：
```text
llm_utils.py
```
填写：
```python
API_KEY = "你的API_KEY"
BASE_URL = "模型接口地址"
```
---
### 5. 启动后端
```bash
python backend.py
```

运行成功：
```text
Running on http://127.0.0.1:5000
```
---
### 6. 启动前端
使用 VSCode：

```text
Live Server
```

打开：
```text
templates/knowledge_map.html
```

访问：
```text
http://127.0.0.1:5500
```

## 🛠 技术栈
### 前端
- HTML
- CSS
- JavaScript
### 后端
- Python
- Flask
### AI能力
- AI Agent
- 大语言模型
- 自动出题
- 路径规划
### 数据存储
- JSON

## 💡 项目创新点
### 知识孪生地图
学习过程可视化。
### AI Agent学习规划
自动制定学习路线。
### 动态掌握度评估
实时反馈学习效果。
### 薄弱点重规划
精准补强知识漏洞。

## 🎯 应用场景
- 中小学教育
- 大学课程学习
- 考研复习
- 职业技能培训
- 企业培训

## 📌 未来规划
- 多学生管理系统
- 数据库持久化
- Three.js三维知识图谱
- RAG知识库增强
- AI学习助手
