# Advanced Python Async API Service

A production-style asynchronous REST API demonstrating FastAPI, async SQLAlchemy, Pydantic validation, dependency injection, pagination, structured error handling, and health checks.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `/docs` for the interactive API documentation.

## Concepts
- Async I/O
- API validation
- Repository/service separation
- Dependency injection
- Pagination
- Health/readiness endpoints
- Testable architecture
