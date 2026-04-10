# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Development
npm run dev          # Start dev server at localhost:3000

# Building
npm run build        # Build for production
npm start            # Start production server

# Testing
npm test             # Run all tests with Vitest
npm test -- Navbar   # Run specific test file matching "Navbar"
npm test -- --watch  # Run tests in watch mode

# Linting
npm run lint         # Run ESLint
```

## Architecture Overview

This is a Next.js 16 application using the App Router with a heist-themed task management interface.

### Route Groups and Layouts

The app uses Next.js route groups to separate public and authenticated areas with different layouts:

- **`app/(public)/`** - Unauthenticated pages (login, signup, splash)
  - Layout wraps content in `<main className="public">` for public-specific styling
  - Pages: `/`, `/login`, `/signup`, `/preview`

- **`app/(dashboard)/`** - Protected pages for authenticated users
  - Layout includes `<Navbar>` component and wraps content in `<main>`
  - All heist management pages live here: `/heists`, `/heists/create`, `/heists/[id]`

- **`app/layout.tsx`** - Root layout applies global CSS and metadata

### Path Aliases

The project uses `@/*` path aliases configured in `tsconfig.json`:
```typescript
import Navbar from "@/components/Navbar"
import "@/app/globals.css"
```
Always use `@/` imports instead of relative paths for consistency.

### Styling Approach

The project uses a hybrid CSS approach:

1. **Tailwind CSS 4** - Primary utility framework with custom theme
2. **Custom CSS theme** in `app/globals.css` defines design tokens:
   - Colors: `--color-primary`, `--color-secondary`, `--color-dark`, etc.
   - Applied via `@theme` block for Tailwind compatibility
3. **CSS Modules** - For component-specific styles (e.g., `Navbar.module.css`)
4. **Global utility classes** - Defined in `globals.css`:
   - `.page-content` - Standard page container with max-width
   - `.center-content` - Vertically centered full-height layout
   - `.form-title` - Centered, bold form headings

When styling components, prefer Tailwind utilities. Use CSS Modules only when you need scoped styles that don't fit Tailwind's utility model.

### Testing Setup

Tests use Vitest with React Testing Library:
- Test files live in `tests/` directory (not co-located with components)
- Test file naming: `tests/components/ComponentName.test.tsx`
- Vitest globals are enabled (`describe`, `it`, `expect` available without imports)
- Testing Library matchers available via `vitest.setup.ts`
- Path aliases (`@/*`) work in tests via `vite-tsconfig-paths` plugin

## Key Conventions

- **Component exports**: Default exports for pages and components
- **Icon usage**: Lucide React icons (e.g., `<Clock8>` in branding)
- **TypeScript**: Strict mode enabled, all files should be `.tsx` or `.ts`
- **React**: Using React 19 with modern patterns (no class components)
