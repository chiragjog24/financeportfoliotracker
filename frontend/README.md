# Finance Portfolio Tracker - Frontend

This is the frontend application for the Finance Portfolio Tracker, built with React, TypeScript, Vite, and shadcn/ui.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Component library
- **ESLint & Prettier** - Code quality and formatting

## Getting Started

### Prerequisites

- Node.js 18+ and npm (or yarn/pnpm)

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

The Vite dev server is configured to proxy API requests to `http://localhost:8000/api/v1`.

### Building for Production

Build the application:

```bash
npm run build
```

The production build will be in the `dist/` directory.

Preview the production build:

```bash
npm run preview
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/     # React components
│   │   ├── ui/        # shadcn/ui components
│   │   └── layout/    # Layout components
│   ├── pages/         # Page components
│   ├── hooks/         # Custom React hooks
│   ├── utils/         # Utility functions
│   ├── lib/           # Library configurations
│   ├── types/         # TypeScript type definitions
│   ├── App.tsx        # Main app component
│   ├── main.tsx       # Entry point
│   └── index.css      # Global styles
├── components.json     # shadcn/ui configuration
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Using shadcn/ui Components

This project uses [shadcn/ui](https://ui.shadcn.com/) for UI components. To add new components:

```bash
npx shadcn-ui@latest add [component-name]
```

Components are installed in `src/components/ui/` and can be imported like:

```tsx
import { Button } from '@/components/ui/button'
```

## Path Aliases

The project uses path aliases for cleaner imports:

- `@/` maps to `src/`

Example:
```tsx
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
```

## Styling

The project uses Tailwind CSS with shadcn/ui's design system. CSS variables are defined in `src/index.css` for theming.

## Docker Development

You can also run the frontend in Docker:

```bash
docker-compose --profile dev up frontend
```

This will start the frontend service with hot module replacement enabled.

## Code Quality

- **ESLint**: Configured with TypeScript and React rules
- **Prettier**: Code formatting with consistent style
- **TypeScript**: Strict type checking enabled

Run linting and formatting:

```bash
npm run lint
npm run format
```
