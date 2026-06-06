# 环游中国 - 儿童地理学习应用

基于 Vue 3 + Django + MySQL + Docker + Element Plus 构建的儿童地理学习应用。

## 功能特性

- 🏠 首页 - 展示应用功能入口
- 🗺️ 地图探索 - 浏览中国34个省级行政区
- 🧩 拼图游戏 - 省份拼图挑战
- ✏️ 答题闯关 - 地理知识问答
- 🏆 积分系统 - 收集徽章和积分
- 📷 图片探索 - 查看省份风景图片

## 技术栈

### 前端
- Vue 3
- Element Plus
- Vite
- Axios

### 后端
- Django 4.2
- Django REST Framework
- MySQL 8.0

### 容器化
- Docker
- Docker Compose

## 快速开始

### 使用 Docker Compose（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 手动运行

#### 后端

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_data.json
python manage.py runserver 0.0.0.0:8000
```

#### 前端

```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
china-app/
├── backend/                 # Django 后端
│   ├── china_app/          # 项目配置
│   ├── provinces/          # 省份管理应用
│   ├── game/              # 游戏管理应用
│   ├── quiz/              # 答题管理应用
│   ├── score/             # 积分管理应用
│   ├── fixtures/          # 初始数据
│   └── requirements.txt
├── frontend/              # Vue 前端
│   ├── src/
│   │   ├── components/    # Vue 组件
│   │   ├── api/          # API 接口
│   │   ├── stores/       # 状态管理
│   │   ├── App.vue       # 主应用组件
│   │   └── main.js       # 入口文件
│   ├── package.json
│   └── vite.config.js
├── images/               # 省份图片
├── png-images/           # PNG 图标
└── docker-compose.yml
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/provinces/` | GET | 获取省份列表 |
| `/api/provinces/{id}/` | GET | 获取单个省份 |
| `/api/quiz/questions/random/` | GET | 获取随机题目 |
| `/api/score/` | POST | 创建积分记录 |
| `/api/score/visit/` | POST | 打卡省份 |
| `/api/score/add_score/` | POST | 增加积分 |

## 徽章系统

| 徽章 | 条件 |
|------|------|
| 🌟 初次探索 | 探索第一个省份 |
| 🗺️ 探索十省 | 探索10个省份 |
| 🏆 走遍中国 | 探索全部34个省份 |
| ⭐ 百分达人 | 积分达到100 |
| 👑 地理王者 | 积分达到500 |

## 开发说明

- 前端开发服务器：http://localhost:5173
- 后端 API：http://localhost:8000
- 数据库：MySQL 8.0 (端口 3306)
- 管理员界面：http://localhost:8000/admin
