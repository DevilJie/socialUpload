# Account Management Page Design

> **Route:** `/account-management`
> **Purpose:** Manage platform accounts, bind/unbind, view status

---

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Page Header                                                     │
│  "Account Management"                              [+ Add Account]│
│  "Manage your platform accounts and login status"                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Platform Tabs]                                                 │
│  [All] [Douyin] [Bilibili] [XHS] [Kuaishou] [WeChat Video]      │
│                                                                  │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │
│  │  ┌──────────────┐│ │  ┌──────────────┐│ │                  │ │
│  │  │  [Avatar]    ││ │  │  [Avatar]    ││ │   [+ Bind New]  │ │
│  │  │  Username    ││ │  │  Username    ││ │                  │ │
│  │  └──────────────┘│ │  └──────────────┘│ │   Click to scan │ │
│  │                  │ │                  │ │   QR code and    │ │
│  │  Platform: Douyin│ │  Platform: XHS   │ │   bind account   │ │
│  │  Status: [Active]│ │  Status: [Active]│ │                  │ │
│  │  Bound: 3 days   │ │  Bound: 2 weeks  │ │                  │ │
│  │                  │ │                  │ │                  │ │
│  │  [Validate] [Del]│ │  [Validate] [Del]│ │                  │ │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘ │
│                                                                  │
│  ┌──────────────────┐ ┌──────────────────┐                      │
│  │  (more cards...) │ │                  │                      │
│  └──────────────────┘ └──────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Platform Tabs

- Element Plus `el-tabs` with platform name + count badge
- Tab style: `border-card` with dark overrides
- "All" tab shows all accounts, sorted by platform group
- Each platform tab has a small platform-brand-colored indicator dot

## Account Card (Bound Account)

```
┌────────────────────────────────────┐
│  ┌────────┐                        │
│  │ Avatar │  Username              │
│  │  48x48 │  @handle (text-muted)  │
│  └────────┘                        │
│                                    │
│  [Douyin Logo] Douyin              │  <- Platform icon + name
│  ┌────────┐                        │
│  │ Active │                        │  <- Status badge
│  └────────┘                        │
│  Last validated: 2 hours ago       │  <- text-small text-muted
│  Bound since: 2026-04-15           │  <- text-small text-muted
│                                    │
│  [Check Status]    [Unbind]        │  <- Actions row
└────────────────────────────────────┘
```

- Card: `width: 280px`, min-height `200px`
- Grid: `grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`
- `gap: 16px`
- Avatar: `border-radius: var(--radius-full)`, 48x48px, fallback to first letter
- Platform badge: small colored dot + platform name
- Status badge color follows global status badge spec

## Account Card (Unbound / Add New)

```
┌────────────────────────────────────┐
│                                    │
│         [+ Add Account]            │  <- Dashed border card
│                                    │
│     Click to scan QR code          │  <- text-muted
│     and bind your account          │
│                                    │
└────────────────────────────────────┘
```

- `border: 2px dashed var(--color-border)`
- `background: transparent`
- On hover: border color changes to `var(--color-cta)`, cursor: pointer
- Center content vertically

## QR Code Login Modal

```
┌────────────────────────────────────┐
│  Bind Account - Douyin        [X]  │
├────────────────────────────────────┤
│                                    │
│      ┌──────────────────┐          │
│      │                  │          │
│      │   [QR Code]      │          │
│      │   200x200        │          │
│      │                  │          │
│      └──────────────────┘          │
│                                    │
│  Open Douyin APP to scan           │
│  Account name: [________]          │  <- Required before scanning
│                                    │
│  Status: Waiting for scan...       │  <- SSE status updates
│  ● Scanning... (animated dot)      │
│                                    │
│  [Cancel]                          │
└────────────────────────────────────┘
```

- Modal width: `400px`
- QR code loading: skeleton spinner, then image
- SSE status updates (3 states):
  1. "Waiting for scan..." (animated pulse dot, info color)
  2. "Scanned, confirming..." (warning color)
  3. "Login successful!" (success color, checkmark animation)
- On success: close modal after 1.5s, refresh account list
- On failure: show error, offer retry

## Account Actions

- **Check Status:** Validates cookie, shows inline loading spinner, then updates badge
- **Unbind:** Confirmation dialog, then removes cookie + DB record
- **Cookie Export:** (hidden in "... more" dropdown) Downloads cookie JSON

## Empty State

- "No accounts bound yet"
- "Add your first platform account to start publishing"
- [Add Account] CTA button

## Interaction Details

- **Drag to reorder:** Accounts can be reordered within a platform (optional)
- **Bulk validate:** Button in header to validate all accounts at once
- **Status polling:** Bound accounts show last-validated timestamp, auto-revalidate every 30 min
