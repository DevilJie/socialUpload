# Material Management Page Design

> **Route:** `/material-management`
> **Purpose:** Upload, preview, and manage video/image files for publishing

---

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Page Header                                                     │
│  "Material Library"                            [+ Upload Files]  │
│  "Manage your videos and images for publishing"                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Search Bar]            [Filter: Type ▼]  [Sort: Date ▼]       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │ ▶ Thumbnail │  │ ▶ Thumbnail │  │ ▶ Thumbnail │     │   │
│  │  │             │  │             │  │             │     │   │
│  │  │             │  │             │  │             │     │   │
│  │  ├─────────────┤  ├─────────────┤  ├─────────────┤     │   │
│  │  │ video1.mp4  │  │ video2.mov  │  │ video3.mp4  │     │   │
│  │  │ 128MB 3:24  │  │ 56MB  1:12  │  │ 200MB 5:00  │     │   │
│  │  │ [Select]    │  │ [Select]    │  │ [Select]    │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐                       │   │
│  │  │ ▶ Thumbnail │  │ ▶ Thumbnail │  ...                  │   │
│  │  └─────────────┘  └─────────────┘                       │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  [Pagination: < 1 2 3 ... 10 >]                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Upload Area (Modal or Top Panel)

When clicking "Upload Files":

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│         ┌──────────────────────────────────────┐             │
│         │                                      │             │
│         │     [Cloud Upload Icon - 48px]        │             │
│         │                                      │             │
│         │     Drag files here or click to       │             │
│         │     upload                            │             │
│         │                                      │             │
│         │     Supports: MP4, MOV, AVI, JPG,    │             │
│         │     PNG (Max 500MB per file)          │             │
│         │                                      │             │
│         └──────────────────────────────────────┘             │
│                                                              │
│  Upload Progress:                                            │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ video1.mp4  ████████████████░░░░  78%  12.3 MB/s      │  │
│  │ video2.mp4  ██████░░░░░░░░░░░░░░  35%  8.1 MB/s      │  │
│  │ image1.jpg  ████████████████████  100% Done            │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- Drop zone: `border: 2px dashed var(--color-border)`, `border-radius: var(--radius-lg)`
- On drag-over: border color → `var(--color-cta)`, bg → `rgba(34,197,94,0.05)`
- Progress bar: Element Plus `el-progress`, green fill on dark track
- Speed display: `font-family: var(--text-mono)`, `var(--text-small)`

## Material Grid

- Grid: `grid-template-columns: repeat(auto-fill, minmax(220px, 1fr))`
- `gap: 16px`

### Video Card

```
┌──────────────────────┐
│  ┌──────────────────┐│
│  │                  ││
│  │  [Play Button]   ││  <- Centered overlay on thumbnail
│  │       ▶          ││     opacity: 0, hover → 1
│  │                  ││
│  │     3:24         ││  <- Duration badge, bottom-right
│  └──────────────────┘│
│                      │
│  video_title.mp4     │  <- Truncated with tooltip
│  128 MB              │  <- text-small, text-muted
│  Uploaded: May 8     │  <- text-small, text-muted
│                      │
│  [Select]  [...More] │  <- Actions
└──────────────────────┘
```

- Thumbnail aspect ratio: 16:9 (`aspect-ratio: 16/9`)
- Play button overlay: `background: rgba(0,0,0,0.4)`, circle 40px
- Duration badge: `position: absolute; bottom: 8px; right: 8px`, pill shape
- Hover: thumbnail overlay darkens, play button appears
- "Select" button: primary style, navigates to PublishCenter with this material pre-selected
- "...More" dropdown: Preview, Rename, Download, Delete

### Image Card

- Same layout but without play button, show image directly
- Dimensions badge instead of duration: "1920x1080"

## Video Preview Modal

```
┌──────────────────────────────────────────────┐
│  Preview - video_title.mp4              [X]  │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │                                          ││
│  │          <video player>                  ││
│  │                                          ││
│  └──────────────────────────────────────────┘│
│                                              │
│  Title: video_title.mp4                      │
│  Size: 128 MB    Duration: 3:24              │
│  Uploaded: 2026-05-08 14:30                  │
│                                              │
│              [Use for Publishing]             │
│                                              │
└──────────────────────────────────────────────┘
```

- Modal width: `720px`
- Video player: native HTML5 `<video>` with controls
- "Use for Publishing" button: navigates to PublishCenter with pre-selected material

## Filters

- **Search:** `el-input` with search icon prefix, searches by filename
- **Type filter:** `el-select` dropdown (All / Video / Image)
- **Sort:** `el-select` dropdown (Date desc / Date asc / Size desc / Name A-Z)

## Pagination

- Element Plus `el-pagination` with dark theme
- Show: total count, page size selector (12/24/48), page numbers

## Empty State

- Icon: CloudUploadOutlined (64px, 30% opacity)
- Title: "No materials yet"
- Description: "Upload your first video or image to start publishing"
- CTA: [Upload Files] button

## Interaction Details

- **Multi-select:** Ctrl+Click to select multiple, then batch delete
- **Keyboard shortcut:** Delete key to delete selected
- **Upload resume:** Failed uploads show retry button
- **File size limit:** Show warning inline if file exceeds 500MB
