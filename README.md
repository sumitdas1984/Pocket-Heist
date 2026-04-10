# Pocket Heist

A fun, gamified task assignment application where users create and manage "heists" - tiny missions with big office mischief potential.

## Overview

Pocket Heist is a modern web application built with Next.js 16 and React 19 that allows teams to create, assign, and track playful missions or tasks in a gamified way. The app features a heist-themed interface where users can manage active assignments, view expired heists, and create new challenges.

## Features

### Authentication
- **User Sign Up** - Create a new account to start planning heists
- **User Login** - Secure access to your heist dashboard
- **Protected Routes** - Dashboard pages are accessible only to authenticated users

### Heist Management
- **View Active Heists** - Track your ongoing missions and assignments
- **Assigned Heists** - See heists you've created and assigned to others
- **Expired Heists** - Browse historical missions that have completed
- **Create New Heists** - Design and launch new missions with custom details
- **Heist Details** - View comprehensive information about individual heists

### User Interface
- **Responsive Design** - Built with Tailwind CSS for modern, mobile-friendly layouts
- **Icon System** - Lucide React icons for a polished visual experience
- **Navigation** - Intuitive navbar component for easy app navigation
- **Route Groups** - Organized page structure with public and dashboard sections

## Tech Stack

- **Framework**: Next.js 16 with App Router
- **Frontend**: React 19, TypeScript
- **Styling**: Tailwind CSS 4
- **Icons**: Lucide React
- **Testing**: Vitest with Testing Library
- **Linting**: ESLint with Next.js config

## Getting Started

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm test` - Run tests with Vitest

## Project Structure

```
app/
├── (dashboard)/          # Protected dashboard routes
│   ├── heists/          # Heist management pages
│   └── layout.tsx       # Dashboard layout
├── (public)/            # Public routes
│   ├── login/          # Login page
│   ├── signup/         # Signup page
│   └── layout.tsx      # Public layout
└── layout.tsx          # Root layout

components/
└── Navbar/             # Navigation component
```
