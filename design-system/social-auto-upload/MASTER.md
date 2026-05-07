# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** Social Auto Upload
**Updated:** 2026-05-08
**Category:** Content Distribution Dashboard (Desktop-first)
**Stack:** Vue 3 + Element Plus + Vite

---

## Global Rules

### Layout Shell

```
┌─────────────────────────────────────────────────────────────────┐
│  Top Bar (height: 56px)                                         │
│  [Logo] [Social Auto Upload]          [Theme Toggle] [Settings] │
├──────────┬──────────────────────────────────────────────────────┤
│          │                                                      │
│  Sidebar │  Main Content Area                                   │
│  (200px  │  (padding: 24px)                                     │
│  collapsed:                                        │
│   64px)  │                                                      │
│          │  ┌──────────────────────────────────────────────┐   │
│  [Home]  │  │  Page Header (title + description + actions)  │   │
│  [Acct]  │  ├──────────────────────────────────────────────┤   │
│  [Mate]  │  │                                              │   │
│  [Pub]   │  │  Content Grid / Cards                        │   │
│  [Task]  │  │                                              │   │
│  [Hist]  │  │                                              │   │
│  [Set]   │  │                                              │   │
│          │  └──────────────────────────────────────────────┘   │
│          │                                                      │
└──────────┴──────────────────────────────────────────────────────┘
```

- **Min width:** 1024px (desktop only, no mobile)
- **Sidebar:** Collapsible, icon-only mode at 64px
- **Content max-width:** None (fluid), but cards max-width 1600px
- **Grid:** CSS Grid or Element Plus `el-row`/`el-col`

### Color Palette

| Role | Hex | CSS Variable | Usage |
|------|-----|--------------|-------|
| Background Base | `#020617` | `--color-bg-base` | App background |
| Background Elevated | `#0F172A` | `--color-bg-elevated` | Cards, sidebar |
| Background Surface | `#1E293B` | `--color-bg-surface` | Inputs, wells |
| Border | `#334155` | `--color-border` | Card borders, dividers |
| Border Light | `#1E293B` | `--color-border-light` | Subtle separators |
| Text Primary | `#F8FAFC` | `--color-text-primary` | Headings, body text |
| Text Secondary | `#94A3B8` | `--color-text-secondary` | Descriptions, labels |
| Text Muted | `#64748B` | `--color-text-muted` | Placeholder, hints |
| CTA / Success | `#22C55E` | `--color-cta` | Primary buttons, success states |
| CTA Hover | `#16A34A` | `--color-cta-hover` | Button hover |
| Warning | `#F59E0B` | `--color-warning` | Warnings, pending states |
| Error | `#EF4444` | `--color-error` | Errors, failed states |
| Info | `#3B82F6` | `--color-info` | Info, links, running states |
| Platform-Douyin | `#FE2C55` | `--color-douyin` | Douyin brand accent |
| Platform-Bilibili | `#00A1D6` | `--color-bilibili` | Bilibili brand accent |
| Platform-XHS | `#FF2442` | `--color-xiaohongshu` | XiaoHongShu brand accent |
| Platform-Kuaishou | `#FF4906` | `--color-kuaishou` | Kuaishou brand accent |
| Platform-WeChat | `#07C160` | `--color-wechat` | WeChat Video brand accent |

### Typography

- **Font Family:** Plus Jakarta Sans, system-ui, -apple-system, sans-serif
- **Font Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
```

| Token | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| `--text-h1` | 28px | 700 | 1.3 | Page title |
| `--text-h2` | 22px | 600 | 1.4 | Section title |
| `--text-h3` | 16px | 600 | 1.5 | Card title |
| `--text-body` | 14px | 400 | 1.6 | Body text, descriptions |
| `--text-small` | 12px | 400 | 1.5 | Labels, captions, tags |
| `--text-mono` | 13px | 400 | 1.6 | Monospace for logs, paths |

### Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 4px | Tight gaps, icon padding |
| `--space-sm` | 8px | Inline spacing |
| `--space-md` | 16px | Standard padding, card internal |
| `--space-lg` | 24px | Section padding, content area |
| `--space-xl` | 32px | Card gaps, section margins |
| `--space-2xl` | 48px | Page-level spacing |

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | 6px | Buttons, inputs, tags |
| `--radius-md` | 8px | Cards, modals |
| `--radius-lg` | 12px | Large cards, panels |
| `--radius-full` | 9999px | Avatars, pills |

### Shadows

| Level | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.3)` | Subtle cards |
| `--shadow-md` | `0 4px 12px rgba(0,0,0,0.4)` | Elevated cards |
| `--shadow-lg` | `0 8px 24px rgba(0,0,0,0.5)` | Modals, dropdowns |
| `--shadow-glow-green` | `0 0 12px rgba(34,197,94,0.3)` | Active/success glow |
| `--shadow-glow-blue` | `0 0 12px rgba(59,130,246,0.3)` | Running task glow |

### Transitions

```css
--transition-fast: 150ms ease;
--transition-normal: 200ms ease;
--transition-slow: 300ms ease;
```

### Element Plus Dark Theme Override

```javascript
// main.js
import { ElConfigProvider } from 'element-plus'

// Dark mode CSS variables override
const themeOverrides = {
  '--el-bg-color': '#020617',
  '--el-bg-color-overlay': '#0F172A',
  '--el-bg-color-page': '#020617',
  '--el-text-color-primary': '#F8FAFC',
  '--el-text-color-regular': '#CBD5E1',
  '--el-text-color-secondary': '#94A3B8',
  '--el-text-color-placeholder': '#64748B',
  '--el-border-color': '#334155',
  '--el-border-color-light': '#1E293B',
  '--el-fill-color-blank': '#0F172A',
  '--el-color-primary': '#22C55E',
  '--el-color-success': '#22C55E',
  '--el-color-warning': '#F59E0B',
  '--el-color-danger': '#EF4444',
  '--el-color-info': '#3B82F6',
}
```

### Icon Rules

- **Icon set:** Element Plus Icons (`@element-plus/icons-vue`)
- **Fallback:** Lucide Icons for missing icons
- **No emojis** as UI icons ever
- **Icon size:** 16px inline, 20px navigation, 24px feature, 32px empty state
- **Platform icons:** Use official SVG brand logos from Simple Icons

---

## Component Specs

### Cards

```css
.card {
  background: var(--color-bg-elevated);       /* #0F172A */
  border: 1px solid var(--color-border);      /* #334155 */
  border-radius: var(--radius-md);            /* 8px */
  padding: var(--space-lg);                   /* 24px */
  transition: box-shadow var(--transition-normal), border-color var(--transition-normal);
}

.card:hover {
  border-color: #475569;
  box-shadow: var(--shadow-md);
}

.card-stat {
  /* For stat/overview cards */
  border-left: 3px solid var(--color-cta);
}
```

### Buttons

```css
/* Primary CTA */
.btn-cta {
  background: var(--color-cta);
  color: #FFFFFF;
  padding: 10px 24px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: var(--text-body);
  cursor: pointer;
  transition: all var(--transition-normal);
}
.btn-cta:hover { background: var(--color-cta-hover); }

/* Ghost / Secondary */
.btn-ghost {
  background: transparent;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
  padding: 10px 24px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-normal);
}
.btn-ghost:hover {
  border-color: var(--color-text-secondary);
  color: var(--color-text-primary);
}
```

### Status Badges

| Status | Background | Text Color | Border |
|--------|-----------|------------|--------|
| Success | `rgba(34,197,94,0.15)` | `#22C55E` | `rgba(34,197,94,0.3)` |
| Running | `rgba(59,130,246,0.15)` | `#3B82F6` | `rgba(59,130,246,0.3)` |
| Warning | `rgba(245,158,11,0.15)` | `#F59E0B` | `rgba(245,158,11,0.3)` |
| Failed | `rgba(239,68,68,0.15)` | `#EF4444` | `rgba(239,68,68,0.3)` |
| Pending | `rgba(100,116,139,0.15)` | `#94A3B8` | `rgba(100,116,139,0.3)` |

### Form Inputs (Dark)

```css
.el-input__wrapper,
.el-textarea__inner {
  background-color: var(--color-bg-surface) !important;  /* #1E293B */
  border-color: var(--color-border) !important;          /* #334155 */
  color: var(--color-text-primary) !important;           /* #F8FAFC */
  box-shadow: none !important;
}

.el-input__wrapper:hover {
  border-color: #475569 !important;
}

.el-input__wrapper.is-focus {
  border-color: var(--color-cta) !important;
  box-shadow: 0 0 0 2px rgba(34,197,94,0.2) !important;
}
```

### Empty States

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-3xl);
  color: var(--color-text-muted);
}

.empty-state__icon {
  width: 64px;
  height: 64px;
  opacity: 0.3;
  margin-bottom: var(--space-md);
}

.empty-state__title {
  font-size: var(--text-h3);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-sm);
}

.empty-state__action {
  margin-top: var(--space-lg);
}
```

---

## Anti-Patterns (Do NOT Use)

- **Emojis as icons** - Use SVG icons only
- **Light mode default** - This is a dark-first application
- **Missing cursor:pointer** on clickable elements
- **Layout-shifting hovers** - No scale transforms on interactive elements
- **Low contrast text** - Maintain 4.5:1 minimum contrast ratio
- **Instant state changes** - Always use transitions (150-300ms)
- **Invisible focus states** - Focus rings must be visible
- **Decorative animations** - Infinite animations only for loading states
- **Platform-colored borders on non-platform elements** - Brand colors reserved for platform indicators only

---

## Pre-Delivery Checklist

Before delivering any page, verify:

- [ ] No emojis used as icons (use Element Plus Icons / Lucide SVG)
- [ ] `cursor: pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Dark theme: text contrast 4.5:1 minimum against dark backgrounds
- [ ] Focus states visible for keyboard navigation
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive at 1024px, 1280px, 1440px, 1920px
- [ ] No horizontal scroll
- [ ] Loading skeletons for async content
- [ ] Empty states with CTA actions
- [ ] Platform brand colors used consistently
