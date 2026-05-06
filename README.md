# AI Designer Stack

A curated list of [Claude Code](https://claude.com/claude-code) skills built for designers who work with AI.

Strategy. Motion. Execution. Quality.

> This is a **curator repo** — it doesn't redistribute skills. It points you to the original public sources and tells you how to install them in one command.

---

## Quick install

Open Claude Code and run these commands (one time):

```bash
/plugin marketplace add anthropics/skills
/plugin marketplace add yahav123147/paid-ads-cro-skills
/plugin marketplace add obra/superpowers
/plugin marketplace add dangogit/workshop-setup-plugin
```

Then install:

```bash
/plugin install skills@anthropics
/plugin install paid-ads-cro-skills@yahav123147
/plugin install superpowers@obra
/plugin install workshop-setup@dangogit
```

That's it. Every skill below is now available — just type `/<skill-name>` or describe what you want and Claude Code will load the right one.

---

## The skills

### 🧠 Design Strategy & Systems

| Skill | What it does |
|---|---|
| `design-strategist` | Analyzes product, audience, and copy to recommend visual style, color palette, and design direction. |
| `ui-ux-expert` | User-centered design, WCAG 2.2 accessibility, design systems, responsive interfaces. |
| `ux-design-systems` | Design tokens, components, theming, component libraries. |
| `responsive-design-system` | Mobile-first breakpoints, container queries, fluid typography, adaptive layouts. |
| `mobile-responsiveness` | Responsive layouts, touch interactions, mobile navigation. |
| `brand-guidelines` | Anthropic's official brand colors and typography for branded artifacts. |

### ✨ Animation & Motion

| Skill | What it does |
|---|---|
| `framer-motion-animator` | Page transitions, gestures, scroll-based animations, orchestrated sequences. |
| `framer-motion-best-practices` | Performance optimization for React animations with Framer Motion. |
| `emilkowal-animations` | Emil Kowalski's animation best practices — one of the most iconic motion designers in the field. |
| `gsap` | GSAP for complex animations (HUD transitions, advanced effects). |
| `animation-micro-interaction-pack` | Ready-made interaction patterns: hover effects, gesture feedback, entrance animations, reduced motion support. |
| `tailwind-gradient-builder` | Modern CSS gradients: linear, radial, conic, mesh, animated, glassmorphism, gradient text. |

### 🎨 Design Execution & QA

| Skill | What it does |
|---|---|
| `design-shotgun` | Generates multiple AI design variants in parallel, opens a comparison board, collects feedback, and iterates. Killer for exploration. |
| `design-consultation` | Researches the landscape and proposes a complete design system (aesthetic, typography, color, layout, spacing, motion). |
| `design-html` | Generates production-quality HTML/CSS from approved mockups. |
| `design-review` | Designer's eye QA: catches visual inconsistency, spacing issues, hierarchy problems, AI slop patterns. |
| `taste-skill` | Senior UI/UX engineer that overrides default LLM biases. Enforces metric-based rules, strict component architecture. |
| `yahav-design-agent` | Landing Page Design Maestro for high-converting Next.js pages with WOW-factor animations. |
| `frontend-design` | Distinctive, production-grade frontend interfaces (web components, pages, artifacts, posters). |

---

## Recommended workflow

A real designer flow using these skills, end-to-end:

1. **Direction** → `/design-strategist` — get a recommended visual style and palette from your product/audience/copy.
2. **Exploration** → `/design-shotgun` — generate 5-10 variants in parallel and pick a winner.
3. **System** → `/design-consultation` + `/ux-design-systems` — turn the winning variant into a full design system.
4. **Build** → `/yahav-design-agent` or `/frontend-design` — ship it as production code.
5. **Motion** → `/framer-motion-animator` + `/emilkowal-animations` — add the polish that makes it feel premium.
6. **QA** → `/design-review` + `/taste-skill` — catch AI slop before shipping.

---

## Credits

This stack stands on the shoulders of public work by:

- **[Anthropic](https://github.com/anthropics/skills)** — official Claude Code skills (`brand-guidelines`, `algorithmic-art`, `canvas-design`, and many more).
- **[Yahav Robin](https://github.com/yahav123147/paid-ads-cro-skills)** — `yahav-design-agent` and the Yahav marketing skill suite.
- **[Jesse Vincent (`obra`)](https://github.com/obra/superpowers)** — design system & taste skills (`taste-skill`, `design-review`).
- **[Dan Gontovnik (`dangogit`)](https://github.com/dangogit/workshop-setup-plugin)** — the workshop setup plugin.

All credit goes to the original authors. This repo is just a recommended bundle for designers.

---

## License

MIT — for the curation and recommendations only. Each skill is governed by its own upstream license.

---

Curated by [Talya Northrop](https://talyanorthrop.com) · [Claude Academy](https://talyanorthrop.com)
