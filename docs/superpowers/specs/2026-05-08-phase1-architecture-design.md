# Phase 1 Design: Wrapper Architecture + Core Workflow Verification

**Date:** 2026-05-08
**Scope:** Phase 1 only — get upstream running, verify core publish workflow
**Upstream repo:** dreammis/social-auto-upload (via git submodule)
**Target platforms:** Linux (dev machine), Windows (end user)

---

## 1. Project Structure

```
social-auto-upload/
├── vendor/
│   └── upstream/              # git submodule → dreammis/social-auto-upload
├── backend/
│   ├── app.py                 # Flask entry, imports upstream routes + functions
│   ├── conf.py                # Config: BASE_DIR points to data/
│   ├── init_db.py             # Database initialization script
│   ├── ext_api/               # Skeleton for Phase 2
│   │   └── __init__.py
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html             # Entry HTML
│   ├── package.json           # Based on upstream, extended
│   ├── vite.config.js         # Dev proxy to Flask backend
│   ├── public/
│   └── src/
│       ├── main.js            # App entry
│       ├── App.vue            # Root component (sidebar + topbar shell)
│       ├── router/
│       │   └── index.js       # Routes: upstream pages + new page placeholders
│       ├── views/
│       │   ├── Dashboard.vue          # From upstream
│       │   ├── AccountManagement.vue  # From upstream
│       │   ├── MaterialManagement.vue # From upstream
│       │   ├── PublishCenter.vue      # From upstream
│       │   ├── TaskCenter.vue         # Placeholder (Phase 3)
│       │   ├── PublishHistory.vue     # Placeholder (Phase 3)
│       │   └── Settings.vue           # Placeholder (Phase 3)
│       ├── stores/
│       ├── api/
│       ├── styles/
│       │   └── design-system.scss     # Design system variables
│       └── assets/
├── data/                      # Runtime data (separated from code)
│   ├── db/                    # SQLite database
│   ├── videoFile/             # Uploaded video files
│   └── cookiesFile/           # Platform cookies
├── docs/
│   ├── requirement.md
│   └── superpowers/specs/
└── design-system/
```

Key decisions:
- **vendor/upstream/** is a git submodule, never manually modified
- **backend/** is our Flask app that imports upstream's uploader/myUtils
- **frontend/** is our Vue app, copied from upstream pages then progressively restyled
- **data/** holds all runtime data, separated from source code

---

## 2. Backend Architecture

### 2.1 Integration Strategy

Import the upstream Flask app directly. The upstream `sau_backend.py` imports `BASE_DIR` from `conf.py`, so our `backend/conf.py` controls the path configuration.

```python
# backend/conf.py
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent / "data"
```

```python
# backend/app.py
import sys
from pathlib import Path

# Add upstream to Python path
UPSTREAM_DIR = Path(__file__).parent.parent / "vendor" / "upstream"
sys.path.insert(0, str(UPSTREAM_DIR))

# Import upstream Flask app (which reads our conf.py)
from sau_backend import app

# Register extension blueprint (Phase 2)
# from ext_api import ext_api
# app.register_blueprint(ext_api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5409)
```

### 2.2 Database Initialization

Upstream uses `db/createTable.py` to create tables. Our `init_db.py` script runs this with the correct BASE_DIR:

```python
# backend/init_db.py
import sys
from pathlib import Path

UPSTREAM_DIR = Path(__file__).parent.parent / "vendor" / "upstream"
sys.path.insert(0, str(UPSTREAM_DIR))

from conf import BASE_DIR
from db.createTable import create_tables  # Run upstream table creation
```

The database file will be at `data/db/database.db`.

### 2.3 Dependencies

```
# backend/requirements.txt
# Upstream core dependencies
patchright==1.58.2
loguru==0.7.3
opencv-python>=4.13.0.92
qrcode==8.2
requests==2.32.3
Flask[async]==3.1.1
flask-cors==6.0.0
segno>=1.6.6
```

---

## 3. Frontend Architecture

### 3.1 Design System Application

Apply the dark theme from `design-system/social-auto-upload/MASTER.md`:
- Override Element Plus CSS variables for dark theme
- Apply Plus Jakarta Sans font
- Use the defined color palette, spacing, and typography tokens
- Implement the unified shell layout (collapsible sidebar + top bar)

### 3.2 Vite Dev Configuration

```js
// frontend/vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/login': 'http://localhost:5409',
      '/uploadSave': 'http://localhost:5409',
      '/getFiles': 'http://localhost:5409',
      '/getFile': 'http://localhost:5409',
      '/deleteFile': 'http://localhost:5409',
      '/getAccounts': 'http://localhost:5409',
      '/getValidAccounts': 'http://localhost:5409',
      '/deleteAccount': 'http://localhost:5409',
      '/postVideo': 'http://localhost:5409',
      '/postVideoBatch': 'http://localhost:5409',
      '/updateUserinfo': 'http://localhost:5409',
      '/uploadCookie': 'http://localhost:5409',
      '/downloadCookie': 'http://localhost:5409',
    }
  }
})
```

### 3.3 Phase 1 Frontend Tasks

1. Copy `sau_frontend/` from upstream to `frontend/`
2. Apply dark theme (override Element Plus CSS variables per design system)
3. Add unified shell layout (sidebar + top bar)
4. Extend router with new page placeholders (TaskCenter, PublishHistory, Settings)
5. Verify all upstream pages render correctly in dark theme

### 3.4 New Page Placeholders

New pages (TaskCenter, PublishHistory, Settings) get minimal placeholder components. They show the page title and "Coming in Phase 3" text. This establishes routing and navigation early.

---

## 4. Environment and Verification

### 4.1 Prerequisites

- Python 3.10 - 3.12 (upstream requirement)
- Node.js >= 18 (Vite 6 requirement)
- Git (submodule management)

### 4.2 Setup Steps

```bash
# 1. Init repo and add submodule
git init
git submodule add https://github.com/dreammis/social-auto-upload.git vendor/upstream

# 2. Python environment
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ../vendor/upstream
patchright install chromium

# 3. Initialize database
python init_db.py

# 4. Start backend
python app.py

# 5. Start frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### 4.3 Verification Checklist

| # | Test | Action | Expected |
|---|------|--------|----------|
| 1 | Backend starts | `python app.py` | localhost:5409 running without errors |
| 2 | Frontend starts | `npm run dev` | localhost:5173 shows dark theme UI |
| 3 | QR code login | Account Management → Add account → Select Douyin → Scan | Browser opens QR code, scan succeeds, account shows logged in |
| 4 | Video upload | Material Management → Drag upload video | File uploaded, appears in material list |
| 5 | Video publish | Publish Center → Select account/video → Publish | Patchright browser opens, completes upload flow |
| 6 | Multi-platform | Verify at least 2 platforms (Douyin + XiaoHongShu) | Both platforms publish successfully |

### 4.4 Phase 1 Deliverables

- [ ] Project directory structure created
- [ ] `conf.py` configured, BASE_DIR points to `data/`
- [ ] Flask backend starts, all upstream APIs accessible
- [ ] Vue frontend with dark theme and unified shell layout
- [ ] At least 2 platforms verified end-to-end
- [ ] Issue log documented (upstream bugs, missing features, improvements) for future phases

---

## 5. Key Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Upstream `conf.py` import path conflicts | Our `conf.py` in `backend/` takes precedence via `sys.path` ordering |
| Patchright browser binary (~200MB) | First-time download, cached locally |
| Platform selectors change upstream | Phase 1 verifies current state; sync via `git submodule update` |
| Dark theme breaks upstream components | Test each upstream page visually after theme application |
| Windows path issues | Use `pathlib.Path` everywhere, no hardcoded separators |
