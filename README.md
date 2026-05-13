<!-- Built by AbilitySoft | abilitysoft.net -->

<div align="center">
<img src="banner.png" alt="AbilitySoft FastAPI Banner" width="100%">

# 🚀 FastAPI Production Boilerplate

**Built with ❤️ by [AbilitySoft](https://abilitysoft.net)**

A production-ready FastAPI boilerplate with JWT authentication, role-based access control, PostgreSQL, Redis, Docker, and clean architecture.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Quick Start (5 minutes)](#-quick-start-5-minutes)
- [Manual Setup (without Docker)](#-manual-setup-without-docker)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [Database Migrations](#-database-migrations)
- [Environment Variables](#-environment-variables)
- [API Endpoints](#-api-endpoints)
- [Architecture](#-architecture)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Development](#-development)
- [About AbilitySoft](#-about-abilitysoft)

---

## ✨ Features

| Category | Details |
|----------|---------|
| **Architecture** | Clean architecture with routers → services → repositories → models |
| **Authentication** | JWT login & register with access + refresh tokens |
| **Security** | bcrypt password hashing, role-based access control (admin/user) |
| **Database** | PostgreSQL with async SQLAlchemy ORM + Alembic migrations |
| **Validation** | Pydantic v2 request/response schemas with full type hints |
| **API Features** | Pagination, filtering, sorting, global error handling |
| **DevOps** | Docker + docker-compose (App + PostgreSQL + Redis) |
| **Monitoring** | Health check endpoint, structured JSON logging, request timing |
| **Testing** | Comprehensive test suite with Pytest & AsyncClient |
| **Code Quality** | Linting (Ruff), Type Checking (Mypy), Pre-commit hooks |
| **CI/CD** | GitHub Actions workflow for automated testing & linting |
| **Middleware** | CORS, request ID tracking, process time headers |
| **Docs** | Auto-generated Swagger UI & ReDoc |

---

## 📁 Project Structure

```
fastapi-boilerplate/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application factory & entry point
│   ├── core/
│   │   ├── config.py           # Environment configuration (pydantic-settings)
│   │   ├── database.py         # Async SQLAlchemy engine & session
│   │   ├── security.py         # JWT & bcrypt utilities
│   │   ├── dependencies.py     # Auth dependencies & role checker
│   │   ├── exceptions.py       # Custom exceptions & global handlers
│   │   ├── middleware.py       # CORS, request timing, request ID
│   │   └── logging_config.py   # Structured JSON logging
│   ├── models/
│   │   ├── base.py             # Declarative base with shared columns
│   │   └── user.py             # User ORM model
│   ├── schemas/
│   │   ├── common.py           # Pagination, health, message schemas
│   │   ├── auth.py             # Login, register, token schemas
│   │   └── user.py             # User CRUD schemas
│   ├── repositories/
│   │   └── user.py             # User data access layer
│   ├── services/
│   │   ├── auth.py             # Authentication business logic
│   │   └── user.py             # User CRUD business logic
│   └── routers/
│       ├── health.py           # Health check endpoint
│       ├── auth.py             # Auth endpoints (login, register, refresh)
│       └── users.py            # User CRUD endpoints
├── alembic/
│   ├── env.py                  # Async migration environment
│   ├── script.py.mako          # Migration template
│   └── versions/               # Generated migration files
├── alembic.ini                 # Alembic configuration
├── .env.example                # Environment template
├── .gitignore
├── .dockerignore
├── Dockerfile                  # Multi-stage production build
├── docker-compose.yml          # App + PostgreSQL + Redis
├── requirements.txt            # Pinned dependencies
└── README.md                   # You are here!
```

---

## 🚀 Quick Start (5 minutes)

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/) installed

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/Ability-Soft/fastapi-production-boilerplate.git
cd fastapi-boilerplate
```

**2. Create your `.env` file**

```bash
cp .env.example .env
```

> ⚠️ **Important**: Change `SECRET_KEY` in `.env` for production:
> ```bash
> # Generate a secure key
> openssl rand -hex 32
> ```

**3. Start all services**

```bash
docker-compose up -d --build
```

This starts:
- 🟢 **FastAPI app** on `http://localhost:8000`
- 🐘 **PostgreSQL 16** on `localhost:5432`
- 🔴 **Redis 7** on `localhost:6379`

**4. Run database migrations**

```bash
docker-compose exec app alembic upgrade head
```

> 💡 If this is your first time, generate the initial migration first:
> ```bash
> docker-compose exec app alembic revision --autogenerate -m "Initial migration"
> docker-compose exec app alembic upgrade head
> ```

**5. Open the API docs**

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- Health Check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

**🎉 You're up and running!**

---

## 🔧 Manual Setup (without Docker)

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- Redis 6+ (optional, for caching)

### Steps

**1. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Create your `.env` file**

```bash
cp .env.example .env
```

Edit `.env` and set your database URL:

```
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/fastapi_db
```

**4. Create the database**

```bash
createdb fastapi_db
# or via psql:
psql -U postgres -c "CREATE DATABASE fastapi_db;"
```

**5. Run migrations**

```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

**6. Start the development server**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📖 API Documentation

Once the server is running, visit:

| URL | Description |
|-----|-------------|
| `/docs` | Swagger UI — interactive API playground |
| `/redoc` | ReDoc — clean API reference documentation |
| `/openapi.json` | Raw OpenAPI 3.1 specification |

---

## 🔐 Authentication

### Register a new user

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Use the access token

```bash
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <your-access-token>"
```

### Refresh the token

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<your-refresh-token>"
  }'
```

### Role-Based Access

| Role | Permissions |
|------|-------------|
| `user` | View own profile (`/users/me`) |
| `admin` | Full CRUD on all users, list/filter/sort |

> 💡 To promote a user to admin, update the `role` column in the database:
> ```sql
> UPDATE users SET role = 'admin' WHERE email = 'john@example.com';
> ```

---

## 🗄️ Database Migrations

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "Describe your change"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current revision
alembic current
```

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | FastAPI Boilerplate | Application name shown in docs |
| `APP_VERSION` | 1.0.0 | API version |
| `DEBUG` | false | Enable debug mode |
| `ENVIRONMENT` | production | `development` / `staging` / `production` |
| `DATABASE_URL` | (see .env.example) | PostgreSQL async connection string |
| `DB_POOL_SIZE` | 20 | Connection pool size |
| `DB_MAX_OVERFLOW` | 10 | Max overflow connections |
| `REDIS_URL` | redis://localhost:6379/0 | Redis connection URL |
| `SECRET_KEY` | ⚠️ **Change this!** | JWT signing secret |
| `JWT_ALGORITHM` | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | 7 | Refresh token lifetime |
| `CORS_ORIGINS` | ["*"] | Allowed CORS origins |
| `LOG_LEVEL` | INFO | Logging level |

---

## 📡 API Endpoints

### Health

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/health` | Health check | ❌ |

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/auth/register` | Register new user | ❌ |
| `POST` | `/api/v1/auth/login` | Login | ❌ |
| `POST` | `/api/v1/auth/refresh` | Refresh access token | ❌ |

### Users

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/v1/users/me` | Get current user | ✅ | any |
| `GET` | `/api/v1/users` | List users (paginated) | ✅ | admin |
| `GET` | `/api/v1/users/{id}` | Get user by ID | ✅ | admin |
| `POST` | `/api/v1/users` | Create user | ✅ | admin |
| `PATCH` | `/api/v1/users/{id}` | Update user | ✅ | admin |
| `DELETE` | `/api/v1/users/{id}` | Delete user | ✅ | admin |

### Pagination & Filtering

The `GET /api/v1/users` endpoint supports:

```
?page=1&page_size=20        # Pagination
?search=john                 # Search by email, first name, or last name
?role=admin                  # Filter by role
?is_active=true              # Filter by active status
?sort_by=created_at          # Sort by any column
?sort_order=desc             # asc or desc
```

---

## 🧪 Testing

We use **Pytest** with `pytest-asyncio` for testing.

```bash
# Run all tests
make test

# Run with coverage
pytest --cov=app tests/
```

Tests use an in-memory SQLite database by default (`tests/conftest.py`), ensuring they are fast and don't require a running PostgreSQL instance.

---

## 💎 Code Quality

To maintain high standards, we use several tools:

- **Ruff**: Extremely fast Python linter and formatter.
- **Mypy**: Static type checker for Python.
- **Pre-commit**: Runs checks automatically before every commit.

```bash
# Run linting manually
make lint

# Run formatting
make format

# Install pre-commit hooks
pre-commit install
```

---

## 🎡 CI/CD

This boilerplate includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:
1. Sets up Python 3.12.
2. Starts PostgreSQL and Redis services.
3. Installs dependencies.
4. Runs Ruff linting and Mypy type checks.
5. Executes the full test suite.

---

## 🛠️ Development

### Adding a New Module

1. **Model**: Create `app/models/your_model.py` (extend `Base`)
2. **Schema**: Create `app/schemas/your_model.py` (Pydantic v2)
3. **Repository**: Create `app/repositories/your_model.py`
4. **Service**: Create `app/services/your_model.py`
5. **Router**: Create `app/routers/your_model.py`
6. **Register**: Add the router in `app/main.py`
7. **Migrate**: Run `alembic revision --autogenerate -m "Add your_model"`

### Useful Commands

```bash
# Start with Docker
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v

# Run locally (development)
uvicorn app.main:app --reload

# Run migrations
alembic upgrade head
```

---

## 🏗️ Architecture

The project follows a modular clean architecture to ensure scalability and maintainability.

```mermaid
graph TD
    Client[Web/Mobile Client] --> Router[API Routers]
    Router --> Service[Business Services]
    Service --> Repo[Data Repositories]
    Repo --> DB[(PostgreSQL)]
    Service --> Cache[(Redis)]
    
    subgraph Core
        Config[App Settings]
        Auth[JWT Security]
        Logs[JSON Logging]
    end
    
    Router -.-> Auth
    Service -.-> Config
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **DB Connection Refused** | Ensure Docker services are running: `docker-compose ps` |
| **JWT Invalid Token** | Check `SECRET_KEY` matches in `.env` and tokens aren't expired. |
| **Migration Errors** | Run `alembic current` to check your version vs database. |
| **ModuleNotFoundError** | Ensure you are in the virtual environment: `source venv/bin/activate` |

---

## 🗺️ Roadmap

- [ ] Sentry Integration for error tracking.
- [ ] Prometheus/Grafana monitoring dashboard.
- [ ] Social Login (Google/GitHub/Microsoft).
- [ ] WebSocket support for real-time notifications.
- [ ] Documentation site with MkDocs.

---

## 🏢 About AbilitySoft

This boilerplate was built by **[AbilitySoft](https://abilitysoft.net)** — a software company specialising in building high-quality, scalable web applications and digital solutions.

- 🌐 **Website**: [abilitysoft.net](https://abilitysoft.net)
- 📧 **Contact**: [support@abilitysoft.net](mailto:support@abilitysoft.net)

---

## 🤝 Community & Support

- **[Contributing Guide](CONTRIBUTING.md)**: Learn how to contribute to this project.
- **[Security Policy](SECURITY.md)**: How to report security vulnerabilities.
- **[Changelog](CHANGELOG.md)**: Track recent changes and updates.
- **[License](LICENSE)**: This project is licensed under the MIT License.

---

<div align="center">

**Built with ❤️ by [AbilitySoft](https://abilitysoft.net)**

</div>
