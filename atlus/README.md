# Atlus Frontend

This is the React + TypeScript frontend for Atlus, a web application that parses US addresses and phone numbers into OpenStreetMap tagging format.

## Tech Stack

- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework

## Development

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Build for production:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

## Deployment

The frontend is deployed to GitHub Pages. The build output (`dist/` directory) is served as static files.

## Project Structure

- `src/` - Source code
  - `components/` - React components
  - `App.tsx` - Main application component
  - `main.tsx` - Application entry point
- `public/` - Static assets
- `index.html` - HTML template

## API Integration

The frontend communicates with the FastAPI backend hosted on AWS Lambda via API Gateway. API endpoints are configured to point to the production backend at `api.atlus.dev/`.
