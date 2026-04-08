# Fastapi-Backend-Template

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Async-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Async-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Verification_Code-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io/)
![Template](https://img.shields.io/badge/Project-Template-6F42C1?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-2EA44F?style=flat-square)

一个可复用的 FastAPI 后端模板，内置认证鉴权、验证码流程、用户与宠物管理、管理员接口、软删除恢复、统一异常处理和日志追踪，适合作为前后端分离项目或个人后台项目的起点。

## 项目亮点

- 基于 FastAPI + SQLAlchemy Async + PostgreSQL + Redis 构建
- 提供注册、登录、重置密码、JWT 鉴权和 OAuth2 Password Flow
- 内置普通用户与管理员两套权限路径
- 支持用户和宠物的软删除与管理员恢复
- 统一错误响应格式，方便前端处理
- 提供 Swagger UI、ReDoc 和 OpenAPI JSON
- 启动时自动初始化管理员账号
- 项目结构清晰，适合继续扩展成业务系统

## 技术栈

| 类别 | 技术 |
| --- | --- |
| Web Framework | FastAPI |
| Server | Uvicorn |
| ORM | SQLAlchemy Async |
| Database | PostgreSQL + asyncpg |
| Cache | Redis |
| Validation | Pydantic v2 |
| Auth | JWT / OAuth2 Password Flow |
| Migration | Alembic |
| Logging | Loguru |

## 功能概览

### 认证模块

- 发送验证码
- 用户注册
- 用户登录
- Swagger OAuth2 授权登录
- 验证码重置密码

### 用户模块

- 获取当前用户资料
- 修改当前用户资料

### 宠物模块

- 创建当前用户的宠物
- 查看当前用户的宠物列表
- 查看单个宠物
- 修改宠物信息
- 软删除宠物

### 管理员模块

- 管理所有用户
- 管理所有宠物
- 查看已软删除数据
- 恢复被软删除的用户和宠物

## 项目结构

```text
.
├── app
│   ├── api                 # 路由层
│   │   ├── router.py
│   │   └── v1
│   │       ├── router.py
│   │       └── routers
│   ├── core                # 配置、依赖注入、安全组件、生命周期
│   ├── crud                # 数据访问层
│   ├── db                  # 数据库与 Redis 连接
│   ├── exceptions          # 自定义异常与异常处理
│   ├── middlewares         # 中间件
│   ├── models              # SQLAlchemy 模型
│   ├── schemas             # Pydantic 请求/响应模型
│   ├── services            # 业务逻辑层
│   ├── utils               # 工具函数
│   └── main.py             # 应用入口
├── migrations              # Alembic 迁移脚本
├── tests                   # 测试目录
├── .env.example            # 环境变量模板
├── requirements.txt        # 项目依赖
├── alembic.ini             # Alembic 配置
└── README.md
```

## 快速开始

### 环境要求

- Python 3.11+
- PostgreSQL 14+
- Redis 6+

### 1. 克隆项目

```bash
git clone https://github.com/<your-username>/fastapi-backend-template.git
cd fastapi-backend-template
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

Windows:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

推荐优先检查这些配置：

| 变量名 | 说明 |
| --- | --- |
| `DB_URL` | PostgreSQL 异步连接串 |
| `REDIS_URL` | Redis 连接串 |
| `INIT_ADMIN` | 启动时自动初始化的管理员用户名 |
| `INIT_ADMIN_PASSWORD` | 启动时自动初始化的管理员密码 |
| `SECRET_KEY` | JWT 签名密钥 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 有效期 |
| `RETURN_CODE` | 是否直接在接口响应中返回验证码，生产环境应为 `false` |

### 5. 执行数据库迁移

```bash
alembic upgrade head
```

### 6. 启动服务

```bash
uvicorn app.main:app --reload
```

启动后可访问：

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
- Health Check: `http://127.0.0.1:8000/health`

## API 概览

### Auth

| Method | Path | 说明 |
| --- | --- | --- |
| `POST` | `/v1/auth/send-code` | 发送验证码 |
| `POST` | `/v1/auth/register` | 用户注册 |
| `POST` | `/v1/auth/login` | JSON 登录 |
| `POST` | `/v1/auth/token` | OAuth2 Password Flow 登录 |
| `POST` | `/v1/auth/reset-password` | 重置密码 |

### Current User

| Method | Path | 说明 |
| --- | --- | --- |
| `GET` | `/v1/users/me` | 获取当前用户资料 |
| `PATCH` | `/v1/users/me` | 修改当前用户资料 |

### Pets

| Method | Path | 说明 |
| --- | --- | --- |
| `POST` | `/v1/pets` | 创建宠物 |
| `GET` | `/v1/pets` | 获取当前用户宠物列表 |
| `GET` | `/v1/pets/{pet_id}` | 获取单个宠物 |
| `PATCH` | `/v1/pets/{pet_id}` | 修改宠物 |
| `DELETE` | `/v1/pets/{pet_id}` | 软删除宠物 |

### Admin

| Method | Path | 说明 |
| --- | --- | --- |
| `GET` | `/v1/admin/users` | 获取全部用户，包含软删除数据 |
| `PATCH` | `/v1/admin/users/{user_id}` | 修改用户 |
| `DELETE` | `/v1/admin/users/{user_id}` | 软删除用户 |
| `POST` | `/v1/admin/users/{user_id}/restore` | 恢复用户 |
| `GET` | `/v1/admin/pets` | 获取全部宠物，包含软删除数据 |
| `PATCH` | `/v1/admin/pets/{pet_id}` | 修改宠物 |
| `DELETE` | `/v1/admin/pets/{pet_id}` | 软删除宠物 |
| `POST` | `/v1/admin/pets/{pet_id}/restore` | 恢复宠物 |

## 权限与业务说明

### 用户角色

- `role = 0`：普通用户
- `role = 1`：管理员

### 软删除机制

用户和宠物删除接口默认都是软删除，数据库记录不会被物理移除，而是将 `is_deleted` 标记为 `true`。管理员接口可以查询这些数据，并通过恢复接口将其恢复为正常状态。

### 验证码机制

当前验证码实现采用 Redis 缓存：

- 生成验证码
- 保存验证码摘要
- 控制验证码有效期
- 控制重复发送冷却时间

当前模板默认没有接入真实短信服务。在开发或联调阶段，可以通过 `RETURN_CODE=true` 或请求体中的 `return_code=true` 直接在响应中获取验证码；生产环境建议关闭该能力并接入真实短信平台。

## 认证方式

所有受保护接口都使用 Bearer Token：

```http
Authorization: Bearer <access_token>
```

如果使用 Swagger UI 调试接口，推荐通过右上角 `Authorize` 完成授权，Swagger 会调用 `/v1/auth/token`。

## 错误响应格式

项目统一返回结构化错误响应，便于前端直接根据 `error_code` 处理：

```json
{
  "error_code": "USER_NOT_FOUND",
  "message": "User not found.",
  "details": null
}
```

## 日志与可观测性

- 请求日志默认写入 `app/logs`
- 日志按天切分，默认保留 30 天
- 每个请求会自动生成 `X-Request-ID`
- 每个响应都会返回 `X-Process-Time-Ms`

这对于联调、定位异常和排查线上问题都很有帮助。

## 默认管理员初始化

应用启动时会根据以下环境变量自动初始化管理员账号：

- `INIT_ADMIN`
- `INIT_ADMIN_PASSWORD`

如果指定用户名已经存在，系统会自动确保其角色为管理员，并恢复其软删除状态。


