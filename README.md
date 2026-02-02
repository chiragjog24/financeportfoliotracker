# Finance Portfolio Tracker

A full-stack application for tracking and managing investment portfolios.

## Tech Stack

### Backend
- **FastAPI** - Python web framework
- **SQLModel** - SQL database ORM
- **Alembic** - Database migrations
- **PostgreSQL** - Database
- **AWS Cognito** - Authentication

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router** - Routing
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Docker and Docker Compose (optional)

### Backend Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Create a `.env` file in the root directory. See `.env.example` for all available configuration options.
   Minimum required for local development:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/portfolio_tracker
   AWS_REGION=us-east-1
   COGNITO_USER_POOL_ID=your_pool_id
   COGNITO_APP_CLIENT_ID=your_client_id
   ```

3. Start the local PostgreSQL database:
   ```bash
   docker-compose up -d db
   ```
   The database will be available at `localhost:5432` with:
   - Username: `postgres`
   - Password: `postgres`
   - Database: `portfolio_tracker`

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the API server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000` with docs at `http://localhost:8000/api/v1/docs`.

#### Database Management

**Reset the local database:**
```bash
./scripts/db-reset.sh
```
This script stops the database, removes all data, and restarts it with a fresh instance.

**Stop the database:**
```bash
docker-compose stop db
```

**View database logs:**
```bash
docker-compose logs -f db
```

**Connect to the database directly:**
```bash
docker-compose exec db psql -U postgres -d portfolio_tracker
```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`.

See [frontend/README.md](frontend/README.md) for more frontend-specific documentation.

### Docker Setup

Run the entire stack with Docker Compose:

```bash
# Start all services
docker-compose up

# Start with development profile (includes frontend)
docker-compose --profile dev up
```

Services:
- **API**: `http://localhost:8000`
- **Frontend**: `http://localhost:5173` (dev profile)
- **Database**: `localhost:5432`

## Project Structure

```
.
├── alembic/              # Database migrations
├── app/                  # Backend application
│   ├── api/             # API routes
│   ├── core/            # Core configuration
│   ├── db/              # Database setup
│   ├── models/          # Data models
│   └── services/        # Business logic
├── frontend/            # Frontend application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   └── lib/         # Utilities
│   └── package.json
├── docker-compose.yml
└── requirements.txt
```

## Development

### Backend Development

- API documentation: `http://localhost:8000/api/v1/docs`
- Run migrations: `alembic upgrade head`
- Create migration: `alembic revision --autogenerate -m "description"`

### Frontend Development

- Development server: `http://localhost:5173`
- Build: `npm run build`
- Lint: `npm run lint`
- Format: `npm run format`

## License

MIT
