# Publish History Page Design

> **Route:** `/publish-history`
> **Purpose:** Review past publishing records, analyze success rates, export data

---

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Page Header                                                     │
│  "Publish History"                             [Export CSV]      │
│  "Review your publishing records and analytics"                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Success Rate Trend (30 days)                              │ │
│  │  ════════════════════════════════════════════════════════  │ │
│  │  100%│▓▓▓▓▓▓▓▓▓▓▓░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │ │
│  │   80%│                                                     │ │
│  │   60%│                                                     │ │
│  │      └──────────────────────────────────────────────────    │ │
│  │       Apr 8  Apr 15  Apr 22  Apr 29  May 6  May 8         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Date Range: Last 30 days ▼]  [Platform: All ▼]                │
│  [Status: All ▼]  [Account: All ▼]  [Search: _________]        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  History Table                                           │   │
│  │                                                          │   │
│  │  Date ▲ │ Platform │ Account │ Title    │ Status │ Actions│   │
│  │  ───────┼──────────┼─────────┼──────────┼────────┼────────│   │
│  │  May 8  │ [Douyin] │ user1   │ My Video │ ✓ Done │ [...]  │   │
│  │  14:30  │          │         │          │        │        │   │
│  │  ───────┼──────────┼─────────┼──────────┼────────┼────────│   │
│  │  May 8  │ [XHS]    │ user2   │ Another  │ ✗ Fail │ [...]  │   │
│  │  14:28  │          │         │          │        │        │   │
│  │  ───────┼──────────┼─────────┼──────────┼────────┼────────│   │
│  │  May 8  │ [Bili]   │ user3   │ Third V  │ ✓ Done │ [...]  │   │
│  │  14:25  │          │         │          │        │        │   │
│  │  ...more rows...                                        │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  [Showing 1-20 of 156]  [< 1 2 3 ... 8 >]                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Success Rate Chart

- Chart type: Area chart (line + fill)
- 30-day view by default, toggle to 7-day / 90-day
- X-axis: dates, Y-axis: success rate percentage
- Green area for success, red area for failures
- Dark theme: grid `rgba(51,65,85,0.3)`, axis text `var(--color-text-secondary)`

## Filter Bar

- All filters inline, horizontally arranged
- `el-date-picker type="daterange"` with quick presets: Today / 7 days / 30 days / Custom
- Platform filter: multi-select with platform brand color dots
- Status filter: multi-select (Success / Failed)
- Account filter: searchable dropdown
- Search: text input for title match
- Filters persist in URL query params for bookmarking

## History Table

- Element Plus `el-table` with dark theme, striped rows
- Row hover: `background: rgba(34,197,94,0.05)`

### Column Definitions

| Column | Width | Content | Alignment |
|--------|-------|---------|-----------|
| Date | 140px | `YYYY-MM-DD HH:mm` | Left |
| Platform | 100px | Platform tag with brand color | Left |
| Account | 120px | Avatar (24px) + name | Left |
| Title | flex | Truncated text with tooltip | Left |
| Duration | 80px | "3m 22s" | Center |
| Status | 80px | Status badge | Center |
| Actions | 80px | "..." dropdown | Center |

### Actions Dropdown

- **View Detail:** Opens task detail drawer (same as TaskCenter)
- **Open URL:** Opens published content in browser (success only)
- **Copy URL:** Copy published URL to clipboard
- **Retry:** Re-create the task (failed only)
- **Delete:** Remove from history (with confirmation)

## Export CSV

- Button in header: "Export CSV"
- Exports current filtered view (respects date range, platform, status filters)
- CSV columns: Date, Platform, Account, Title, Status, Duration, URL, Error
- File download via `Blob` + `URL.createObjectURL`

## Pagination

- Element Plus `el-pagination`
- Page size: 20 (default), options: 20 / 50 / 100
- Show total: "Showing 1-20 of 156 records"

## Empty State

- "No publishing history"
- "Your publishing records will appear here after your first task"
- [Go to Publish Center] button

## Interaction Details

- **Click row:** Expand to show detail inline (error message, URL, timeline)
- **Sort:** Click column headers to sort (date, platform, status, duration)
- **Batch select:** Checkbox on each row, bulk actions (delete, retry failed)
- **Refresh:** Auto-refresh every 60s if tasks are running
