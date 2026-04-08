# fastapi-backend-template

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Async-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Async-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io/)
![Template](https://img.shields.io/badge/Project-Backend_Template-6F42C1?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-2EA44F?style=flat-square)

一个面向二次开发的 FastAPI 后端模板，提供清晰、可扩展、适合继续演进的后端基础架构。仓库内置了认证、用户、资源管理、管理员、日志、异常处理等常见能力，适合作为前后端分离项目、管理后台或内部服务的起点。

## 项目定位

`fastapi-backend-template` 的重点不是某个垂直业务，而是一套可复用的后端工程骨架。

当前仓库已经包含：

- 一套完整的认证与鉴权流程
- 一套可直接运行的用户与资源管理接口
- 一套管理员管理与恢复机制
- 一套适合继续扩展的分层目录结构

你可以直接基于这套结构继续开发自己的业务模块，而不需要从零搭后端基础设施。

## 核心能力

### 基础设施

- FastAPI 路由组织与 OpenAPI 文档
- SQLAlchemy Async 异步数据库访问
- PostgreSQL 持久化存储
- Redis 缓存与验证码存储
- Alembic 数据库迁移
- Pydantic v2 请求与响应校验
- JWT 鉴权与 OAuth2 Password Flow
- 中间件级请求日志与请求上下文
- 统一异常处理与结构化错误响应
- 启动生命周期管理与管理员初始化

### 内置模块

- 用户注册、登录、重置密码
- 当前用户资料查询与更新
- 资源模块的增删改查
- 普通用户与管理员权限分离
- 软删除与恢复流程

当前资源模块路由为 `/v1/pets`，后续可以按同样结构替换成你自己的领域模型。

## 为什么适合作为模板

- 目录结构稳定，适合持续维护
- 路由、服务、CRUD、Schema、模型职责边界清晰
- 已经具备真实项目常见的认证、权限、日志、异常、迁移能力
- 可以直接启动调试，也适合作为脚手架继续演进
- 代码规模适中，便于理解和二次改造

## 技术栈

| 类别 | 技术 |
| --- | --- |
| Web Framework | FastAPI |
| Server | Uvicorn |
| ORM | SQLAlchemy Async |
| Database | PostgreSQL + asyncpg |
| Cache | Redis |
| Validation | Pydantic v2 |
| Authentication | JWT / OAuth2 Password Flow |
| Migration | Alembic |
| Logging | Loguru |

## 架构设计

项目采用比较典型的分层结构：

- `router`：接收请求、定义接口、声明依赖
- `service`：承载业务逻辑与事务控制
- `crud`：负责数据库读写
- `schema`：负责输入输出校验
- `model`：定义数据库模型
- `core`：集中放配置、依赖注入、安全、生命周期

这种结构的优势是接口层不会过重，业务逻辑不会和数据库细节强耦合，新增模块时也更容易保持一致的组织方式。

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

建议优先检查以下配置：

| 变量名 | 说明 |
| --- | --- |
| `DB_URL` | PostgreSQL 异步连接串 |
| `REDIS_URL` | Redis 连接串 |
| `INIT_ADMIN` | 启动时自动初始化的管理员用户名 |
| `INIT_ADMIN_PASSWORD` | 启动时自动初始化的管理员密码 |
| `SECRET_KEY` | JWT 签名密钥 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 有效期 |
| `RETURN_CODE` | 是否在接口响应中直接返回验证码，生产环境应为 `false` |

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

## 内置 API 概览

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

### Resource Module

| Method | Path | 说明 |
| --- | --- | --- |
| `POST` | `/v1/pets` | 创建资源 |
| `GET` | `/v1/pets` | 获取当前用户资源列表 |
| `GET` | `/v1/pets/{pet_id}` | 获取单个资源 |
| `PATCH` | `/v1/pets/{pet_id}` | 修改资源 |
| `DELETE` | `/v1/pets/{pet_id}` | 软删除资源 |

### Admin

| Method | Path | 说明 |
| --- | --- | --- |
| `GET` | `/v1/admin/users` | 获取全部用户，包含软删除数据 |
| `PATCH` | `/v1/admin/users/{user_id}` | 修改用户 |
| `DELETE` | `/v1/admin/users/{user_id}` | 软删除用户 |
| `POST` | `/v1/admin/users/{user_id}/restore` | 恢复用户 |
| `GET` | `/v1/admin/pets` | 获取全部资源，包含软删除数据 |
| `PATCH` | `/v1/admin/pets/{pet_id}` | 修改资源 |
| `DELETE` | `/v1/admin/pets/{pet_id}` | 软删除资源 |
| `POST` | `/v1/admin/pets/{pet_id}/restore` | 恢复资源 |

## 权限与认证

### 用户角色

- `role = 0`：普通用户
- `role = 1`：管理员

### 认证方式

所有受保护接口都使用 Bearer Token：

```http
Authorization: Bearer <access_token>
```

Swagger UI 中推荐通过右上角 `Authorize` 授权，它会调用 `/v1/auth/token`。

## 通用机制

### 统一错误响应

项目统一返回结构化错误，方便前端按 `error_code` 做分流处理：

```json
{
  "error_code": "USER_NOT_FOUND",
  "message": "User not found.",
  "details": null
}
```

### 日志与请求追踪

- 请求日志默认写入 `app/logs`
- 日志按天切分，默认保留 30 天
- 每个请求自动生成 `X-Request-ID`
- 每个响应自动返回 `X-Process-Time-Ms`

### 验证码机制

验证码流程基于 Redis，实现了：

- 验证码摘要存储
- 有效期控制
- 重复发送冷却控制

当前仓库默认没有接入真实短信服务。在开发或联调阶段，可以通过 `RETURN_CODE=true` 或请求体中的 `return_code=true` 直接在响应中获取验证码；生产环境建议关闭该能力并接入真实短信平台。

### 启动时初始化管理员

应用启动时会根据以下环境变量自动初始化管理员账号：

- `INIT_ADMIN`
- `INIT_ADMIN_PASSWORD`

如果对应用户名已经存在，系统会自动提升其管理员权限，并恢复软删除状态。

## 二次开发建议

如果你要把它改造成自己的项目，通常可以按这个顺序推进：

1. 保留 `auth`、`core`、`middlewares`、`exceptions` 这些通用基础设施。
2. 参考现有 `users` 与资源模块的实现方式，替换成你自己的业务模型。
3. 延续 `router -> service -> crud -> schema -> model` 的分层方式新增模块。
4. 继续补充测试、CI、部署脚本和更细粒度的权限控制。

如果你的业务并不是宠物场景，通常只需要替换资源模块对应的模型、Schema、CRUD、Service 和 Router 层即可。

## requirements.txt 说明

当前 `requirements.txt` 已按用途分组：

- 核心框架
- 数据库与迁移
- 缓存与配置
- 鉴权与安全
- 日志
- 开发测试依赖

后续如果项目继续增长，可以再拆分成：

- `requirements.txt`
- `requirements-dev.txt`

或者迁移到 `pyproject.toml`。

## 适用场景

- 个人 FastAPI 后端项目起步
- 管理后台 API
- SaaS 后台原型
- 内部工具服务
- 需要 JWT + PostgreSQL + Redis 的中小型后端项目

