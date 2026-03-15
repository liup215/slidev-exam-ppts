# VitePress Documentation Site

This directory contains the VitePress configuration and documentation content for the A-Level Biology study resources.

## Structure

```
docs/
├── .vitepress/
│   └── config.mts          # VitePress configuration
├── cie/                    # CIE Biology 9700 documentation
│   ├── index.md            # CIE overview page
│   └── as/                 # AS Level chapters
│       ├── chapter1.md     # Chapter 1: Cell Structure
│       └── chapter2.md     # Chapter 2: Biological Molecules
├── bio-competition/        # Biology Competition documentation
│   ├── index.md            # Bio Competition overview
│   └── molecular-biology/  # Molecular Biology topics
│       └── chapter7.md     # Chapter 7: Control of Gene Expression
└── index.md                # Homepage
```

## Development

```bash
# Start VitePress dev server
npm run dev

# Build VitePress only
npm run build:vitepress

# Build all (VitePress + Slidev slides)
npm run build
```

## Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch.

## Features

- 📚 Structured documentation with sidebar navigation
- 🎨 Interactive Slidev presentations embedded via iframe
- 🔍 Full-text search (built-in VitePress feature)
- 📱 Responsive design for all devices
- 🌙 Dark/light mode support
