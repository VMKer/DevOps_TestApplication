# Test Application

A FastAPI REST API backed by PostgreSQL, with CRUD endpoints.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- A `.env` file in the project root


---

## Local development

### 1. Create and activate a virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Start the database

You need a running PostgreSQL instance. The easiest way is to start just the `db` service from Compose:

```
docker compose up -d db
```

Then set `DATABASE_URL` in your `.env`:

```
APP_ENV=local
LOG_LEVEL=INFO
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/postgres
```

### 4. (Optional) Initialise the schema manually

In local mode (`APP_ENV=local`) the app auto-creates tables on startup.
You can also run the init script directly:

```
python -m app.scripts.init_db
```

### 5. Run the API

```
uvicorn app.main:app --reload --env-file .env
```

### 6. Verify

```
curl http://localhost:8000/health
```

Expected: `{"ok": true}`

```
curl http://localhost:8000/health/db
```

Expected: `{"ok": true}`

---

## Local development with Docker Compose

Run the full stack (API + Postgres) in containers:

```
docker compose up --build
```

The API is available at `http://localhost:8000`.

To stop and remove volumes:

```
docker compose down -v
```

---

## Running on EC2

The `docker-compose.ec2.yml` file is a slimmed-down Compose file for EC2 deployment. It runs only the API container and expects an external database (e.g. Amazon RDS).



### Configure environment variables

Create a `.env` file on the instance pointing to your RDS (or other external) database:

```
APP_ENV=prod
LOG_LEVEL=INFO
DATABASE_URL=postgresql+psycopg://<user>:<password>@<rds-endpoint>:5432/<dbname>
```

### Initialise DB

```
python3 -m app.scripts.init_db
```

### Start the application

```
docker-compose -f docker-compose.ec2.yml up --build -d
```

The API is served on port **80**.

### Verify

```
curl http://<ec2-public-ip>/health
curl http://<ec2-public-ip>/health/db
```

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | App health check |
| GET | `/health/db` | Database connectivity check |
| POST | `/students` | Create a student |
| GET | `/students` | List students (query: `limit`, `offset`) |
| GET | `/students/{student_id}` | Get a student by student_id |
| DELETE | `/students/{student_id}` | Delete a student by student_id |
