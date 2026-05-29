# Job Radar — 互联网岗位 & 面经雷达

每日聚合大厂官网招聘岗位，提供技能趋势分析与面经分享平台。

## 快速开始

```bash
# 1. 复制环境变量
cp .env.example .env

# 2. 启动数据库 + 后端 + 前端
docker compose up -d db backend frontend

# 3. 初始化数据库 & 种子数据
docker compose exec backend alembic upgrade head
docker compose exec backend python scripts/seed.py

# 4. 访问
# 前端: http://localhost:3000
# API:  http://localhost:8000/docs

## 已接入数据源

| Adapter | 来源 | 说明 |
|---------|------|------|
| TencentAdapter | careers.tencent.com | 社招公开 API |
| BaiduAdapter | talent.baidu.com | 社招（SOCIAL） |
| JDAdapter | campus.jd.com | 校招/实习公开 API |
```

## 启动爬虫（可选）

```bash
docker compose --profile crawler up crawler
```

## 项目结构

```
job-radar/
├── backend/     FastAPI 后端 + 数据库模型
├── crawler/     爬虫服务（Adapter 模式）
├── frontend/    Next.js 前端
└── scripts/     种子数据脚本
```

## 开发

### 后端

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 爬虫

```bash
cd crawler
pip install -r requirements.txt
python -m adapters.tencent  # 测试单个 Adapter
python scheduler.py           # 启动定时调度
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 合规说明

- 仅抓取各公司官方 Careers 页面公开数据
- JD 只存摘要（≤500 字），详情跳转原站
- 不存储 HR 个人联系方式
- 面经投稿自动过滤手机号/邮箱
