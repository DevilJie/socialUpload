# Publish Center Page Design

> **Route:** `/publish-center`
> **Purpose:** Create and publish content to multiple platforms simultaneously

---

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Page Header                                                     │
│  "Publish Center"                                                │
│  "Create and schedule content for multiple platforms"            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────┐ ┌────────────────────────┐  │
│  │  Step 1: Select Material       │ │  Preview               │  │
│  │                                │ │                        │  │
│  │  ┌──────────────────────────┐  │ │  ┌──────────────────┐  │  │
│  │  │  [Selected video thumb]  │  │ │  │                  │  │  │
│  │  │  my_video.mp4  [Change]  │  │ │  │  Video Thumbnail │  │  │
│  │  └──────────────────────────┘  │ │  │  16:9 preview    │  │  │
│  │                                │ │  │                  │  │  │
│  │  or [Select from Library]      │ │  └──────────────────┘  │  │
│  │                                │ │                        │  │
│  ├────────────────────────────────┤ │  Title preview here    │  │
│  │  Step 2: Content Details       │ │  @account1 @account2   │  │
│  │                                │ │                        │  │
│  │  Title:                        │ │  Platform preview:     │  │
│  │  [________________________]    │ │  [Douyin] [XHS] [Bili] │  │
│  │                                │ │                        │  │
│  │  Description:                  │ └────────────────────────┘  │
│  │  [________________________]    │                              │
│  │  [________________________]    │                              │
│  │                                │                              │
│  │  Tags:                         │                              │
│  │  [#tag1] [#tag2] [+ Add tag]   │                              │
│  │                                │                              │
│  ├────────────────────────────────┤                              │
│  │  Step 3: Select Platforms      │                              │
│  │                                │                              │
│  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐  │                              │
│  │  │☑   │ │☑   │ │☐   │ │☑   │  │                              │
│  │  │Dou │ │XHS │ │Bili│ │KS  │  │                              │
│  │  │yin │ │    │ │    │ │    │  │                              │
│  │  │    │ │    │ │    │ │    │  │                              │
│  │  │v1  │ │v1  │ │    │ │v1  │  │                              │
│  │  └────┘ └────┘ └────┘ └────┘  │                              │
│  │                                │                              │
│  ├────────────────────────────────┤                              │
│  │  Step 4: Platform Config       │                              │
│  │                                │                              │
│  │  [Douyin]                      │                              │
│  │    Account: [user1 ▼]          │                              │
│  │    Product link: [________]    │                              │
│  │    Location: [________]        │                              │
│  │                                │                              │
│  │  [XHS]                         │                              │
│  │    Account: [user2 ▼]          │                              │
│  │    Is original: [✓]            │                              │
│  │                                │                              │
│  ├────────────────────────────────┤                              │
│  │  Step 5: Schedule              │                              │
│  │                                │                              │
│  │  (●) Publish now               │                              │
│  │  ( ) Schedule for later        │                              │
│  │      Date: [2026-05-08]        │                              │
│  │      Time: [18:00]             │                              │
│  │                                │                              │
│  ├────────────────────────────────┤                              │
│  │                                │                              │
│  │  [Save Draft]    [Publish Now] │                              │
│  │                                │                              │
│  └────────────────────────────────┘                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Two-Column Layout

- **Left column (60%):** Form steps, scrollable
- **Right column (40%):** Sticky preview panel, `position: sticky; top: 80px`

## Step 1: Select Material

- If material pre-selected (from MaterialManagement): show thumbnail + filename + "Change" button
- If not selected: show "Select from Library" button → opens material picker modal
- Material picker modal: grid of materials with search, same as MaterialManagement but in modal form

## Step 2: Content Details

### Title Input
- `el-input` with character counter (max varies by platform, show "X/Y" indicator)
- Title is shared across platforms by default
- "Customize per platform" toggle to unlock per-platform titles

### Description Textarea
- `el-input type="textarea"` with `:rows="4"`
- Character counter
- Support @mention for accounts
- Support hashtag input with autocomplete

### Tags Section
- `el-tag` chips with close button
- Input with autocomplete from recent tags
- Max tag count indicator per platform

## Step 3: Platform Selection

### Platform Card (Selected)

```
┌────────────────────┐
│  ☑                  │  <- Checkbox, checked
│  [Douyin Logo]      │  <- Platform icon (Simple Icons SVG)
│  Douyin             │  <- Platform name
│                     │
│  3 accounts         │  <- text-small, text-muted
│  ● user1 (active)   │  <- Selected account
└────────────────────┘
```

- Background: `var(--color-bg-elevated)` + left border `3px solid var(--color-douyin)`
- Checkbox: green when checked
- Grid: `grid-template-columns: repeat(auto-fill, minmax(160px, 1fr))`

### Platform Card (Unselected)

- Same layout but `opacity: 0.5`, no colored border
- Hover: `opacity: 0.8`, border appears
- Cursor: pointer

### Platform-specific warnings

- If no account bound for a platform: show "No account bound" in red, disable selection
- If Cookie expired: show "Cookie expired" warning badge

## Step 4: Platform Configuration

- Accordion/collapsible panels, one per selected platform
- Only shown for selected platforms
- Each platform has its own config fields:

| Platform | Fields |
|----------|--------|
| Douyin | Account selector, Product link (optional), Location (optional) |
| Bilibili | Account selector, Tag selector, Topic selector |
| XiaoHongShu | Account selector, Is original checkbox, Location |
| Kuaishou | Account selector, Product link |
| WeChat Video | Account selector, Draft mode toggle |

- Account selector: `el-select` with account avatar + name, only shows bound accounts for that platform
- All fields use dark-themed inputs per global spec

## Step 5: Schedule

- Radio group: "Publish now" / "Schedule"
- Date picker + time picker when schedule selected
- Element Plus `el-date-picker` and `el-time-picker` with dark theme
- Show timezone info: "Will publish at 2026-05-08 18:00 (local time)"

## Preview Panel (Right Column)

- Sticky positioned, scrolls with page but stays visible
- Shows live preview of how the post will look

```
┌────────────────────────────┐
│  Preview                   │
│                            │
│  ┌──────────────────────┐  │
│  │                      │  │
│  │  Video Thumbnail     │  │
│  │  16:9 aspect ratio   │  │
│  │                      │  │
│  └──────────────────────┘  │
│                            │
│  Title preview here        │  <- Live bound to title input
│  Description preview...    │  <- Live bound to description
│  #tag1 #tag2              │  <- Tags
│                            │
│  Platforms:                │
│  [Douyin] [XHS] [Kuaishou]│  <- Colored tags
│                            │
│  Accounts:                 │
│  user1 (Douyin)            │
│  user2 (XHS)               │
│  user3 (Kuaishou)          │
│                            │
│  Schedule: Now             │  <- or scheduled time
│                            │
└────────────────────────────┘
```

- Preview updates in real-time as form fields change
- Video thumbnail: click to play preview
- Platform tags: use platform brand colors

## Action Buttons

- **Save Draft:** `btn-ghost` style, saves to DB without publishing
- **Publish Now:** `btn-cta` style (green), creates tasks in queue
  - On click: confirmation dialog "Publish to 3 platforms with 3 accounts?"
  - Loading state: button shows spinner, disabled
  - On success: toast notification + navigate to TaskCenter
  - On error: inline error message near the problematic field

## Validation Rules

- Title: required, max length per platform (warn if exceeding)
- Material: required
- At least 1 platform selected
- Each selected platform must have a valid account
- Schedule time must be in the future (if scheduled)
- Show validation errors inline, not alert dialogs

## Empty State

- "Select a video or image to start creating"
- Quick-action: [Go to Material Library] button
