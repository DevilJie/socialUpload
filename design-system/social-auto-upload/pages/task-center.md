# Task Center Page Design

> **Route:** `/task-center`
> **Purpose:** Monitor, manage, and control publishing tasks in real-time

---

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Page Header                                                     │
│  "Task Center"                              [Create New Task]    │
│  "Monitor and manage your publishing tasks"                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Pending  │ │ Running  │ │ Success  │ │ Failed   │           │
│  │    5     │ │    2     │ │    48    │ │    3     │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│                                                                  │
│  [Status Filter: All ▼]  [Platform ▼]  [Date Range]  [Search]  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Task Queue (Real-time)                                  │   │
│  │                                                          │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │ [●] Running  [Douyin] user1 "My Video"    45% ▶   │  │   │
│  │  │     Started: 2m ago  |  Opening upload page...     │  │   │
│  │  ├────────────────────────────────────────────────────┤  │   │
│  │  │ [●] Running  [XHS] user2 "My Video"      20% ▶   │  │   │
│  │  │     Started: 30s ago  |  Logging in...             │  │   │
│  │  ├────────────────────────────────────────────────────┤  │   │
│  │  │ [○] Pending  [Bili] user3 "Another Vid"     --   │  │   │
│  │  │     Queued: waiting for available slot             │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │                                                          │   │
│  │  Completed Tasks                                         │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │ [✓] Success  [Douyin] user1 "Video A"    [Open]   │  │   │
│  │  │     Published at: 2026-05-08 14:30                 │  │   │
│  │  ├────────────────────────────────────────────────────┤  │   │
│  │  │ [✗] Failed   [XHS] user2 "Video B"   [Retry] [Log]│  │   │
│  │  │     Error: Cookie expired, re-login required       │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │                                                          │   │
│  │  [Load More...]                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Status Summary Cards

- Same style as Dashboard stat cards, 4 in a row
- Clickable: filters task list by that status
- Active filter: card has bright border, others dim

## Task List

### Running Task Row

```
┌──────────────────────────────────────────────────────────────┐
│  ● Running   [Douyin]  user1  "My Video Title"       45%    │
│                                                              │
│  ██████████████████░░░░░░░░░░░░░░░░░░░░░░░░░  2m 15s        │
│                                                              │
│  Status: Uploading video file...                             │
│  Started: 2026-05-08 14:28  |  Elapsed: 2m 15s              │
│                                              [Cancel]        │
└──────────────────────────────────────────────────────────────┘
```

- Left border: `3px solid var(--color-info)` (blue)
- Pulsing dot `●`: `animation: pulse 2s infinite`, blue color
- Progress bar: `el-progress`, `stroke-width: 4`, blue fill
- Status text: monospace font, real-time SSE updates
- "Cancel" button: ghost style, danger on hover

### Pending Task Row

```
┌──────────────────────────────────────────────────────────────┐
│  ○ Pending   [XHS]  user2  "Another Video Title"            │
│                                                              │
│  Queued: position #3  |  Waiting for available slot...       │
│  Created: 2026-05-08 14:30                                   │
│                                        [Cancel] [↑ Move Up]  │
└──────────────────────────────────────────────────────────────┘
```

- Left border: `3px solid var(--color-text-muted)` (gray)
- Static dot `○`
- "Move Up" button: only shown if not first in queue

### Success Task Row

```
┌──────────────────────────────────────────────────────────────┐
│  ✓ Success   [Douyin]  user1  "Video Title"                 │
│                                                              │
│  Published: 2026-05-08 14:30  |  Duration: 3m 22s           │
│  URL: https://douyin.com/video/xxxx                          │
│                                        [Open URL] [Details]  │
└──────────────────────────────────────────────────────────────┘
```

- Left border: `3px solid var(--color-cta)` (green)
- "Open URL" button: opens published content in browser
- URL text: truncated with "..." and copy-on-click

### Failed Task Row

```
┌──────────────────────────────────────────────────────────────┐
│  ✗ Failed    [Bili]  user3  "Video Title"     Retry 1/3     │
│                                                              │
│  Error: Element not found: [upload button]                   │
│  Last attempt: 2026-05-08 14:35  |  Next retry: in 30s      │
│                                        [Retry Now] [Cancel]  │
└──────────────────────────────────────────────────────────────┘
```

- Left border: `3px solid var(--color-error)` (red)
- Error message: monospace font, `var(--color-error)` text
- Retry count badge: `var(--color-warning)` background
- "Retry Now" button: ghost style with warning color

## Task Detail Drawer

Clicking "Details" or the task row opens a right-side drawer:

```
┌──────────────────────────────────────┐
│  Task Detail                    [X]  │
├──────────────────────────────────────┤
│                                      │
│  Task ID: task_20260508_001          │
│  Status: ● Running                   │
│  Platform: Douyin                    │
│  Account: user1                      │
│                                      │
│  Video: my_video.mp4                 │
│  Title: "My Video Title"             │
│  Description: "This is a great..."   │
│  Tags: #tag1 #tag2                   │
│                                      │
│  Progress: 45%                       │
│  ████████████░░░░░░░░░░░░░░          │
│                                      │
│  Timeline:                           │
│  ● 14:28:00  Task created            │
│  ● 14:28:02  Starting browser...     │
│  ● 14:28:15  Browser launched        │
│  ● 14:28:18  Navigating to upload    │
│  ● 14:28:25  Filling form fields...  │
│  ● 14:29:30  Uploading video file... │
│  ○ --        Publishing...           │  <- Pending step
│  ○ --        Done                    │
│                                      │
│  [Cancel Task]                       │
│                                      │
└──────────────────────────────────────┘
```

- Drawer width: `420px`, slides from right
- Timeline: vertical line with dots, completed steps green, current blue pulse, pending gray
- Each timeline entry has timestamp + description
- Real-time updates via SSE

## SSE Real-time Updates

- Connection: `EventSource('/api/v2/tasks/stream')`
- Event types:
  - `task_created`: New task appears in list
  - `task_started`: Task status → Running, progress bar appears
  - `task_progress`: Progress percentage update
  - `task_log`: New log line in timeline
  - `task_completed`: Task status → Success/Failed
  - `task_retrying`: Task status → Retrying

## Filters

- **Status filter:** `el-select` (All / Pending / Running / Success / Failed)
- **Platform filter:** `el-select` with platform options
- **Date range:** `el-date-picker type="daterange"`
- **Search:** Search by title or account name

## Empty State

- "No tasks yet"
- "Create your first publishing task from the Publish Center"
- [Go to Publish Center] button

## Interaction Details

- **Auto-scroll:** New running tasks auto-scroll into view
- **Sound notification:** Optional beep on task completion/failure (user setting)
- **Batch cancel:** Select multiple pending tasks → cancel all
- **Retry all failed:** One-click retry all failed tasks
