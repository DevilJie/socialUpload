# Dashboard Page Design

> **Route:** `/`
> **Purpose:** Overview of all accounts, tasks, and publishing activity

---

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Page Header                                                     │
│  "Dashboard"                                          [Refresh] │
│  "Overview of your content distribution"                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Total    │ │ Active   │ │ Tasks    │ │ Success  │           │
│  │ Accounts │ │ Accounts │ │ Today    │ │ Rate     │           │
│  │   12     │ │    9     │ │    15    │ │   93%    │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│                                                                  │
│  ┌────────────────────────────┐ ┌────────────────────────────┐  │
│  │  Publishing Trend (7 days) │ │  Platform Distribution     │  │
│  │  ▁▂▃▅▇▆▅ (Area Chart)     │ │  ┌─────────────────────┐  │  │
│  │                            │ │  │  Douyin    ████  45%  │  │  │
│  │  Mon Tue Wed Thu Fri Sat   │ │  │  Bilibili  ███   25%  │  │  │
│  │                            │ │  │  XHS       ██    18%  │  │  │
│  │                            │ │  │  Kuaishou  █     12%  │  │  │
│  └────────────────────────────┘ └────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Recent Activity                                         │   │
│  │                                                          │   │
│  │  ┌─────────────────────────────────────────────────────┐│   │
│  │  │ [Douyin] [user1] "My Video Title"  SUCCESS  2m ago  ││   │
│  │  │ [XHS]    [user2] "Another Title"   RUNNING  just now ││   │
│  │  │ [Bili]   [user3] "Third Video"     FAILED   5m ago  ││   │
│  │  └─────────────────────────────────────────────────────┘│   │
│  │                                          [View All ->]   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Stat Cards Row

- **4 cards** in a row (CSS Grid: `grid-template-columns: repeat(4, 1fr)`)
- Each card: `min-height: 100px`, left border accent color
- Card 1 (Accounts): accent `var(--color-info)`
- Card 2 (Active): accent `var(--color-cta)`
- Card 3 (Tasks Today): accent `var(--color-warning)`
- Card 4 (Success Rate): accent `var(--color-cta)` or `var(--color-error)` based on value

### Stat Card Structure

```
┌──────────────────────┐
│  [Icon]               │
│  Label (text-muted)   │
│  12                   │  <- var(--text-h1) 28px bold
│  +3 this week         │  <- var(--text-small) 12px, text-secondary
└──────────────────────┘
```

## Charts Section

- **Left (60%):** Publishing Trend — Area chart (Chart.js / ECharts)
  - 7-day or 30-day toggle
  - Stacked by platform (each platform a different color)
  - Dark theme: grid lines `rgba(51,65,85,0.5)`, no background fill on chart area
- **Right (40%):** Platform Distribution — Horizontal bar chart
  - Each bar uses platform brand color
  - Show percentage + count on right

## Recent Activity Table

- Element Plus `el-table` with dark theme
- Columns: Platform (tag with brand color), Account, Title, Status (badge), Time
- Max 10 rows, "View All" link to PublishHistory page
- Row hover: `background: rgba(34,197,94,0.05)`
- Status uses badge component with status-specific colors

## Empty States

- If no accounts: "Add your first account to get started" + [Go to Accounts] button
- If no tasks: "No publishing activity yet" + [Create First Post] button

## Interaction Details

- **Auto-refresh:** Poll stats every 30s via `setInterval`
- **Refresh button:** Manual refresh with spin animation on icon
- **Chart hover:** Tooltip with exact numbers, platform name, date
- **Table row click:** Navigate to task detail in TaskCenter
