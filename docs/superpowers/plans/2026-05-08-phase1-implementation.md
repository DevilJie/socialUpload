# Phase 1: Wrapper Architecture + Core Workflow Verification

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up a wrapper architecture around the upstream `dreammis/social-auto-upload` repo via git submodule, start both Flask backend and Vue frontend, and verify the core publish workflow end-to-end.

**Architecture:** Upstream repo is a git submodule at `vendor/upstream/`. Our `backend/` wraps the upstream Flask app by controlling `conf.py` (pointing data to `data/`). Our `frontend/` copies the upstream Vue app and applies dark theme + layout from the design system. No upstream files are modified.

**Tech Stack:** Python 3.10-3.12, Flask 3.1, Patchright 1.58, SQLite, Vue 3.5, Element Plus 2.9, Vite 6, Pinia 3, SCSS

---

## File Map

### New files to create:

| File | Responsibility |
|------|---------------|
| `backend/conf.py` | Path config — `BASE_DIR` points to `data/` |
| `backend/app.py` | Flask entry — imports upstream app with our conf |
| `backend/requirements.txt` | Python dependencies |
| `backend/init_db.py` | Database initialization script |
| `backend/ext_api/__init__.py` | Empty skeleton for Phase 2 |
| `data/db/.gitkeep` | Ensure db directory exists |
| `data/videoFile/.gitkeep` | Ensure videoFile directory exists |
| `data/cookiesFile/.gitkeep` | Ensure cookiesFile directory exists |
| `frontend/src/styles/variables.scss` | Dark theme variables (replaces upstream light theme) |
| `frontend/src/styles/design-system.scss` | Design system CSS custom properties |
| `frontend/src/views/TaskCenter.vue` | Placeholder page |
| `frontend/src/views/PublishHistory.vue` | Placeholder page |
| `frontend/src/views/Settings.vue` | Placeholder page |

### Files to copy from upstream and modify:

| File | Source | Modifications |
|------|--------|--------------|
| `frontend/package.json` | `vendor/upstream/sau_frontend/package.json` | Add `@` alias, same deps |
| `frontend/vite.config.js` | `vendor/upstream/sau_frontend/vite.config.js` | Full API proxy config |
| `frontend/index.html` | `vendor/upstream/sau_frontend/index.html` | Dark bg, font import |
| `frontend/src/main.js` | `vendor/upstream/sau_frontend/src/main.js` | Dark theme config |
| `frontend/src/App.vue` | `vendor/upstream/sau_frontend/src/App.vue` | Dark theme sidebar/topbar |
| `frontend/src/router/index.js` | `vendor/upstream/sau_frontend/src/router/index.js` | Add new routes |
| `frontend/src/views/Dashboard.vue` | `vendor/upstream/sau_frontend/src/views/Dashboard.vue` | Copy as-is |
| `frontend/src/views/AccountManagement.vue` | `vendor/upstream/sau_frontend/src/views/AccountManagement.vue` | Copy as-is |
| `frontend/src/views/MaterialManagement.vue` | `vendor/upstream/sau_frontend/src/views/MaterialManagement.vue` | Copy as-is |
| `frontend/src/views/PublishCenter.vue` | `vendor/upstream/sau_frontend/src/views/PublishCenter.vue` | Copy as-is |
| `frontend/src/api/*` | `vendor/upstream/sau_frontend/src/api/*` | Copy as-is |
| `frontend/src/stores/*` | `vendor/upstream/sau_frontend/src/stores/*` | Copy as-is |
| `frontend/src/utils/*` | `vendor/upstream/sau_frontend/src/utils/*` | Modify baseURL |
| `frontend/src/styles/reset.scss` | `vendor/upstream/sau_frontend/src/styles/reset.scss` | Copy as-is |
| `frontend/src/styles/index.scss` | `vendor/upstream/sau_frontend/src/styles/index.scss` | Use dark variables |
| `frontend/public/vite.svg` | `vendor/upstream/sau_frontend/public/vite.svg` | Copy as-is |

---

## Task 1: Environment Check and Git Init

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Check Python version**

Run: `python3 --version`
Expected: Python 3.10.x, 3.11.x, or 3.12.x

If not installed or wrong version, install with: `sudo apt install python3.12 python3.12-venv` (adjust version as needed).

- [ ] **Step 2: Check Node.js version**

Run: `node --version`
Expected: v18.x or higher

If not installed: `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt install -y nodejs`

- [ ] **Step 3: Check Git version**

Run: `git --version`
Expected: git version 2.x

- [ ] **Step 4: Initialize git repo**

Run: `git init`

- [ ] **Step 5: Create .gitignore**

Create `.gitignore`:

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
venv/
.venv/

# Node
node_modules/

# IDE
.vscode/
.idea/

# Runtime data
data/db/*.db
data/videoFile/*
data/cookiesFile/*
!data/**/.gitkeep

# Upstream (managed via submodule)
vendor/upstream/

# OS
.DS_Store
Thumbs.db

# Env
.env
*.env.local
```

- [ ] **Step 6: Initial commit**

```bash
git add .gitignore docs/ design-system/
git commit -m "chore: init project with docs and design system"
```

---

## Task 2: Add Upstream as Git Submodule

- [ ] **Step 1: Add the upstream repo as a submodule**

```bash
git submodule add https://github.com/dreammis/social-auto-upload.git vendor/upstream
```

Expected: Directory `vendor/upstream/` contains the upstream repo files.

- [ ] **Step 2: Verify submodule**

Run: `ls vendor/upstream/sau_backend.py vendor/upstream/sau_frontend/ vendor/upstream/uploader/`
Expected: All three paths exist.

- [ ] **Step 3: Commit**

```bash
git add .gitmodules vendor/
git commit -m "chore: add upstream social-auto-upload as git submodule"
```

---

## Task 3: Create Backend Skeleton

**Files:**
- Create: `backend/conf.py`
- Create: `backend/app.py`
- Create: `backend/requirements.txt`
- Create: `backend/init_db.py`
- Create: `backend/ext_api/__init__.py`

- [ ] **Step 1: Create `backend/conf.py`**

This file replaces the upstream's `conf.py`. The upstream `sau_backend.py` does `from conf import BASE_DIR`, so our conf.py must provide everything the upstream expects.

```python
from pathlib import Path

# Base directory for all runtime data
BASE_DIR = Path(__file__).parent.parent / "data"

# Upstream config fields (from conf.example.py)
XHS_SERVER = "http://127.0.0.1:11901"
LOCAL_CHROME_PATH = ""
LOCAL_CHROME_HEADLESS = True
DEBUG_MODE = True
```

- [ ] **Step 2: Create `backend/app.py`**

We insert the upstream path at position 1 (not 0) so our `backend/conf.py` is found before any upstream conf. The upstream has no `conf.py` (only `conf.example.py`), so there is no conflict.

```python
import sys
from pathlib import Path

# Add upstream to Python path at position 1
# Position 0 is automatically set to backend/ by Python
# This ensures our conf.py is found before any upstream conf
UPSTREAM_DIR = Path(__file__).parent.parent / "vendor" / "upstream"
sys.path.insert(1, str(UPSTREAM_DIR))

# Import upstream Flask app — it will pick up our conf.py
from sau_backend import app  # noqa: E402

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5409)
```

- [ ] **Step 3: Create `backend/requirements.txt`**

```
patchright==1.58.2
loguru==0.7.3
opencv-python>=4.13.0.92
qrcode==8.2
requests==2.32.3
Flask[async]==3.1.1
flask-cors==6.0.0
segno>=1.6.6
```

- [ ] **Step 4: Create `backend/init_db.py`**

The upstream `db/createTable.py` uses a hardcoded `./database.db` path. We cannot use it directly. Instead, we create our own init script that builds the same tables at the correct location.

```python
import sqlite3
from pathlib import Path
import sys

# Ensure our conf.py is importable
sys.path.insert(0, str(Path(__file__).parent))

from conf import BASE_DIR

DB_DIR = BASE_DIR / "db"
DB_PATH = DB_DIR / "database.db"


def init_database():
    DB_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Table: user_info (accounts)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type INTEGER NOT NULL,
        filePath TEXT NOT NULL,
        userName TEXT NOT NULL,
        status INTEGER DEFAULT 0
    )
    """)

    # Table: file_records (uploaded materials)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filesize REAL,
        upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        file_path TEXT
    )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")


if __name__ == "__main__":
    init_database()
```

- [ ] **Step 5: Create `backend/ext_api/__init__.py`**

```python
# Extension API blueprint skeleton — populated in Phase 2
```

- [ ] **Step 6: Commit**

```bash
git add backend/
git commit -m "feat: add backend wrapper skeleton with conf and init_db"
```

---

## Task 4: Create Data Directories and Initialize Database

**Files:**
- Create: `data/db/.gitkeep`
- Create: `data/videoFile/.gitkeep`
- Create: `data/cookiesFile/.gitkeep`

- [ ] **Step 1: Create data directories**

```bash
mkdir -p data/db data/videoFile data/cookiesFile
touch data/db/.gitkeep data/videoFile/.gitkeep data/cookiesFile/.gitkeep
```

- [ ] **Step 2: Create Python virtual environment**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

- [ ] **Step 3: Install Python dependencies**

```bash
pip install -r requirements.txt
```

- [ ] **Step 4: Install upstream as editable package**

```bash
pip install -e ../vendor/upstream
```

This makes the upstream packages (`uploader`, `utils`, `myUtils`) importable.

- [ ] **Step 5: Initialize the database**

```bash
python init_db.py
```

Expected output: `Database initialized at /home/czy/workspace/ai/social-auto-upload/data/db/database.db`

- [ ] **Step 6: Verify database was created**

Run: `ls -la ../data/db/database.db`
Expected: File exists with size > 0.

- [ ] **Step 7: Deactivate venv**

```bash
deactivate
cd ..
```

- [ ] **Step 8: Commit**

```bash
git add data/
git commit -m "chore: add data directories with gitkeep placeholders"
```

---

## Task 5: Install Patchright Browser

- [ ] **Step 1: Activate venv and install Patchright Chromium**

```bash
cd backend
source venv/bin/activate
patchright install chromium
```

Expected: Chromium browser binary downloaded (~200MB). This takes a few minutes.

- [ ] **Step 2: Verify Patchright is installed**

```bash
python -c "from patchright.sync_api import sync_playwright; print('Patchright OK')"
```

Expected: `Patchright OK`

- [ ] **Step 3: Deactivate venv**

```bash
deactivate
cd ..
```

---

## Task 6: Copy and Set Up Frontend

**Files:**
- Copy: all files from `vendor/upstream/sau_frontend/` to `frontend/`
- Modify: `frontend/vite.config.js`
- Modify: `frontend/src/utils/request.js`

- [ ] **Step 1: Copy upstream frontend**

```bash
cp -r vendor/upstream/sau_frontend/* frontend/
cp vendor/upstream/sau_frontend/.gitkeep frontend/ 2>/dev/null || true
```

Wait — the target directory doesn't exist yet:

```bash
mkdir -p frontend/public
cp -r vendor/upstream/sau_frontend/* frontend/
cp vendor/upstream/sau_frontend/public/* frontend/public/ 2>/dev/null || true
```

- [ ] **Step 2: Verify files were copied**

Run: `ls frontend/package.json frontend/src/main.js frontend/src/App.vue frontend/src/router/index.js`
Expected: All four files exist.

- [ ] **Step 3: Rewrite `frontend/vite.config.js`**

Replace the entire file with proxy config for all upstream API endpoints. The upstream frontend calls APIs directly (not under `/api/`), so we proxy each endpoint individually.

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {}
    }
  },
  server: {
    port: 5173,
    open: true,
    proxy: {
      '/login': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/upload': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/uploadSave': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/getFiles': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/getFile': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/deleteFile': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/getAccounts': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/getValidAccounts': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/deleteAccount': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/postVideo': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/postVideoBatch': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/updateUserinfo': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/uploadCookie': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
      '/downloadCookie': {
        target: 'http://localhost:5409',
        changeOrigin: true,
      },
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    chunkSizeWarningLimit: 1600,
    rollupOptions: {
      output: {
        manualChunks: {
          vue: ['vue', 'vue-router', 'pinia'],
          elementPlus: ['element-plus'],
          utils: ['axios']
        }
      }
    }
  }
})
```

- [ ] **Step 4: Modify `frontend/src/utils/request.js`**

The upstream sets `baseURL` to `http://localhost:5409`. Since we use Vite proxy, change to empty string so all requests go through the proxy:

In `frontend/src/utils/request.js`, change:
```js
baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5409',
```
to:
```js
baseURL: import.meta.env.VITE_API_BASE_URL || '',
```

- [ ] **Step 5: Install npm dependencies**

```bash
cd frontend
npm install
```

Expected: `node_modules/` created, no errors.

- [ ] **Step 6: Verify build works**

```bash
npm run build
```

Expected: `dist/` directory created without errors.

- [ ] **Step 7: Commit**

```bash
cd ..
git add frontend/
git commit -m "feat: copy upstream frontend with Vite proxy and request config"
```

---

## Task 7: Apply Dark Theme Design System

**Files:**
- Modify: `frontend/src/styles/variables.scss` (replace entirely)
- Create: `frontend/src/styles/design-system.scss`
- Modify: `frontend/src/styles/index.scss`
- Modify: `frontend/src/main.js`
- Modify: `frontend/index.html`

- [ ] **Step 1: Replace `frontend/src/styles/variables.scss`**

Replace the entire file with dark theme values from `design-system/social-auto-upload/MASTER.md`:

```scss
// Color palette — Dark theme
$primary-color: #22C55E;
$primary-color-hover: #16A34A;
$success-color: #22C55E;
$warning-color: #F59E0B;
$danger-color: #EF4444;
$info-color: #3B82F6;

// Text colors — Dark theme
$text-primary: #F8FAFC;
$text-regular: #CBD5E1;
$text-secondary: #94A3B8;
$text-placeholder: #64748B;

// Border colors — Dark theme
$border-base: #334155;
$border-light: #334155;
$border-lighter: #1E293B;
$border-extra-light: #1E293B;

// Background colors — Dark theme
$bg-color: #0F172A;
$bg-color-page: #020617;
$bg-color-overlay: #0F172A;
$bg-color-surface: #1E293B;

// Font sizes
$font-size-extra-large: 28px;
$font-size-large: 22px;
$font-size-medium: 16px;
$font-size-base: 14px;
$font-size-small: 12px;
$font-size-extra-small: 12px;
$font-size-mono: 13px;

// Spacing
$spacing-xs: 4px;
$spacing-sm: 8px;
$spacing-md: 16px;
$spacing-lg: 24px;
$spacing-xl: 32px;
$spacing-2xl: 48px;

// Border radius
$border-radius-sm: 6px;
$border-radius-base: 8px;
$border-radius-large: 12px;
$border-radius-round: 9999px;
$border-radius-circle: 50%;

// Shadows — Dark theme
$box-shadow-base: 0 1px 3px rgba(0, 0, 0, 0.3);
$box-shadow-dark: 0 4px 12px rgba(0, 0, 0, 0.4);
$box-shadow-light: 0 8px 24px rgba(0, 0, 0, 0.5);

// Transitions
$transition-fast: 150ms ease;
$transition-normal: 200ms ease;
$transition-slow: 300ms ease;

// Platform brand colors
$color-douyin: #FE2C55;
$color-bilibili: #00A1D6;
$color-xiaohongshu: #FF2442;
$color-kuaishou: #FF4906;
$color-wechat: #07C160;

// Z-index
$z-index-normal: 1;
$z-index-top: 1000;
$z-index-popper: 2000;
```

- [ ] **Step 2: Create `frontend/src/styles/design-system.scss`**

This file provides CSS custom properties for Element Plus dark theme override:

```scss
// Element Plus dark theme overrides
:root {
  // Element Plus CSS variable overrides for dark theme
  --el-bg-color: #020617;
  --el-bg-color-overlay: #0F172A;
  --el-bg-color-page: #020617;
  --el-text-color-primary: #F8FAFC;
  --el-text-color-regular: #CBD5E1;
  --el-text-color-secondary: #94A3B8;
  --el-text-color-placeholder: #64748B;
  --el-border-color: #334155;
  --el-border-color-light: #1E293B;
  --el-border-color-lighter: #1E293B;
  --el-border-color-extra-light: #1E293B;
  --el-fill-color: #1E293B;
  --el-fill-color-light: #1E293B;
  --el-fill-color-lighter: #0F172A;
  --el-fill-color-blank: #0F172A;
  --el-color-primary: #22C55E;
  --el-color-success: #22C55E;
  --el-color-warning: #F59E0B;
  --el-color-danger: #EF4444;
  --el-color-info: #3B82F6;

  // Card styles
  --el-card-bg-color: #0F172A;
  --el-card-border-color: #334155;

  // Input styles
  --el-input-bg-color: #1E293B;
  --el-input-border-color: #334155;
  --el-input-text-color: #F8FAFC;
  --el-input-placeholder-color: #64748B;

  // Table styles
  --el-table-bg-color: #0F172A;
  --el-table-tr-bg-color: #0F172A;
  --el-table-header-bg-color: #0F172A;
  --el-table-row-hover-bg-color: #1E293B;
  --el-table-border-color: #334155;
  --el-table-text-color: #F8FAFC;
  --el-table-header-text-color: #94A3B8;

  // Dialog / Overlay
  --el-dialog-bg-color: #0F172A;
  --el-overlay-color: rgba(0, 0, 0, 0.6);

  // Menu
  --el-menu-bg-color: #020617;
  --el-menu-text-color: #94A3B8;
  --el-menu-active-color: #22C55E;
  --el-menu-hover-bg-color: #1E293B;

  // Tag
  --el-tag-bg-color: rgba(34, 197, 94, 0.15);
  --el-tag-border-color: rgba(34, 197, 94, 0.3);

  // Design system custom properties
  --color-bg-base: #020617;
  --color-bg-elevated: #0F172A;
  --color-bg-surface: #1E293B;
  --color-border: #334155;
  --color-border-light: #1E293B;
  --color-text-primary: #F8FAFC;
  --color-text-secondary: #94A3B8;
  --color-text-muted: #64748B;
  --color-cta: #22C55E;
  --color-cta-hover: #16A34A;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;
  --color-douyin: #FE2C55;
  --color-bilibili: #00A1D6;
  --color-xiaohongshu: #FF2442;
  --color-kuaishou: #FF4906;
  --color-wechat: #07C160;
}
```

- [ ] **Step 3: Modify `frontend/src/styles/index.scss`**

Replace the entire file to use dark theme variables:

```scss
@use './reset.scss';
@use './variables.scss' as *;
@use './design-system.scss';

// Font import
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

body {
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  color: $text-primary;
  background-color: $bg-color-page;
  margin: 0;
}

#app {
  min-height: 100vh;
}

// Utility classes
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.flex { display: flex; }
.flex-center { display: flex; justify-content: center; align-items: center; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }
.flex-column { display: flex; flex-direction: column; }

.w-full { width: 100%; }
.h-full { height: 100%; }

// Spacing utilities
.m-0 { margin: 0; }
.mt-0 { margin-top: 0; }
.mb-0 { margin-bottom: 0; }
.m-1 { margin: $spacing-xs; }
.m-2 { margin: $spacing-sm; }
.m-3 { margin: $spacing-md; }
.m-4 { margin: $spacing-lg; }
.p-0 { padding: 0; }
.p-1 { padding: $spacing-xs; }
.p-2 { padding: $spacing-sm; }
.p-3 { padding: $spacing-md; }
.p-4 { padding: $spacing-lg; }

// Global card override for dark theme
.el-card {
  background-color: $bg-color-overlay !important;
  border-color: $border-base !important;
  color: $text-primary;
}

// Global button adjustments
.el-button--primary {
  --el-button-bg-color: #{$primary-color};
  --el-button-border-color: #{$primary-color};
  --el-button-hover-bg-color: #{$primary-color-hover};
  --el-button-hover-border-color: #{$primary-color-hover};
}

// Scrollbar styling for dark theme
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: $bg-color-page;
}

::-webkit-scrollbar-thumb {
  background: $border-base;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #475569;
}
```

- [ ] **Step 4: Modify `frontend/src/main.js`**

Add the dark theme config provider. Replace the entire file:

```js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './stores'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './styles/index.scss'

const app = createApp(App)

// Register Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(router)
app.use(pinia)
app.use(ElementPlus)
app.mount('#app')
```

The key addition is `import 'element-plus/theme-chalk/dark/css-vars.css'` which provides Element Plus's built-in dark theme foundation. Our `design-system.scss` overrides specific values on top.

- [ ] **Step 5: Modify `frontend/index.html`**

Add the dark class to the html element and font preconnect:

```html
<!doctype html>
<html lang="zh-CN" class="dark">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Social Auto Upload</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

- [ ] **Step 6: Verify frontend builds**

```bash
cd frontend
npm run build
```

Expected: Build succeeds without errors.

- [ ] **Step 7: Commit**

```bash
cd ..
git add frontend/
git commit -m "feat: apply dark theme design system to frontend"
```

---

## Task 8: Apply Dark Theme to App Shell (Sidebar + Topbar)

**Files:**
- Modify: `frontend/src/App.vue`

- [ ] **Step 1: Rewrite `frontend/src/App.vue`**

The upstream App.vue has a light-themed sidebar (background `#001529`) and header (`#fff`). Replace with dark theme values per the design system. Also update the sidebar menu items to include the new pages.

```vue
<template>
  <div id="app">
    <el-container>
      <el-aside :width="isCollapse ? '64px' : '200px'">
        <div class="sidebar">
          <div class="logo">
            <img v-show="isCollapse" src="/vite.svg" alt="Logo" class="logo-img">
            <h2 v-show="!isCollapse">Social Auto Upload</h2>
          </div>
          <el-menu
            :router="true"
            :default-active="activeMenu"
            :collapse="isCollapse"
            class="sidebar-menu"
          >
            <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>
              <span>Dashboard</span>
            </el-menu-item>
            <el-menu-item index="/account-management">
              <el-icon><User /></el-icon>
              <span>Account</span>
            </el-menu-item>
            <el-menu-item index="/material-management">
              <el-icon><Picture /></el-icon>
              <span>Material</span>
            </el-menu-item>
            <el-menu-item index="/publish-center">
              <el-icon><Upload /></el-icon>
              <span>Publish</span>
            </el-menu-item>
            <el-menu-item index="/task-center">
              <el-icon><List /></el-icon>
              <span>Tasks</span>
            </el-menu-item>
            <el-menu-item index="/publish-history">
              <el-icon><Clock /></el-icon>
              <span>History</span>
            </el-menu-item>
            <el-menu-item index="/settings">
              <el-icon><Setting /></el-icon>
              <span>Settings</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-aside>
      <el-container>
        <el-header>
          <div class="header-content">
            <div class="header-left">
              <el-icon class="toggle-sidebar" @click="toggleSidebar"><Fold /></el-icon>
            </div>
            <div class="header-right">
              <!-- Phase 2+: user info, notifications -->
            </div>
          </div>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeFilled, User, Picture, Upload,
  List, Clock, Setting, Fold
} from '@element-plus/icons-vue'

const route = useRoute()

const activeMenu = computed(() => {
  return route.path
})

const isCollapse = ref(false)

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

#app {
  min-height: 100vh;
}

.el-container {
  height: 100vh;
}

.el-aside {
  background-color: $bg-color-page;
  color: $text-secondary;
  height: 100vh;
  overflow: hidden;
  transition: width $transition-normal;
  border-right: 1px solid $border-lighter;

  .sidebar {
    display: flex;
    flex-direction: column;
    height: 100%;

    .logo {
      height: 56px;
      padding: 0 16px;
      display: flex;
      align-items: center;
      background-color: $bg-color-overlay;
      overflow: hidden;
      border-bottom: 1px solid $border-lighter;

      .logo-img {
        width: 32px;
        height: 32px;
        margin-right: 12px;
      }

      h2 {
        color: $text-primary;
        font-size: 14px;
        font-weight: 600;
        white-space: nowrap;
        margin: 0;
      }
    }

    .sidebar-menu {
      border-right: none;
      flex: 1;
      background-color: transparent;

      .el-menu-item {
        display: flex;
        align-items: center;
        color: $text-secondary;
        transition: all $transition-fast;

        .el-icon {
          margin-right: 10px;
          font-size: 18px;
        }

        &:hover {
          background-color: $bg-color-surface;
          color: $text-primary;
        }

        &.is-active {
          color: $primary-color;
          background-color: rgba($primary-color, 0.1);
        }
      }
    }
  }
}

.el-header {
  background-color: $bg-color-overlay;
  border-bottom: 1px solid $border-lighter;
  padding: 0;
  height: 56px;

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    padding: 0 24px;

    .header-left {
      .toggle-sidebar {
        font-size: 20px;
        cursor: pointer;
        color: $text-secondary;
        transition: color $transition-fast;

        &:hover {
          color: $text-primary;
        }
      }
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 16px;
    }
  }
}

.el-main {
  background-color: $bg-color-page;
  padding: 24px;
  overflow-y: auto;
}
</style>
```

- [ ] **Step 2: Verify frontend builds**

```bash
cd frontend
npm run build
```

Expected: Build succeeds. The `List`, `Clock`, `Setting` icons must be valid Element Plus icon names. If any fail, check `@element-plus/icons-vue` for correct icon names and adjust.

- [ ] **Step 3: Commit**

```bash
cd ..
git add frontend/src/App.vue
git commit -m "feat: dark theme sidebar and topbar layout with extended navigation"
```

---

## Task 9: Add Placeholder Pages and Extend Router

**Files:**
- Create: `frontend/src/views/TaskCenter.vue`
- Create: `frontend/src/views/PublishHistory.vue`
- Create: `frontend/src/views/Settings.vue`
- Modify: `frontend/src/router/index.js`

- [ ] **Step 1: Create `frontend/src/views/TaskCenter.vue`**

```vue
<template>
  <div class="placeholder-page">
    <div class="page-header">
      <h1>Task Center</h1>
      <p class="page-desc">Monitor and manage your publishing tasks</p>
    </div>
    <div class="empty-state">
      <el-icon :size="64" color="#64748B"><List /></el-icon>
      <h3>Coming Soon</h3>
      <p>Task queue management will be available in Phase 3.</p>
    </div>
  </div>
</template>

<script setup>
import { List } from '@element-plus/icons-vue'
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.placeholder-page {
  .page-header {
    margin-bottom: 24px;

    h1 {
      font-size: 28px;
      font-weight: 700;
      color: $text-primary;
      margin: 0 0 4px 0;
    }

    .page-desc {
      color: $text-secondary;
      font-size: 14px;
      margin: 0;
    }
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 24px;
    color: $text-muted;

    h3 {
      font-size: 16px;
      color: $text-secondary;
      margin: 16px 0 8px 0;
    }

    p {
      font-size: 14px;
      color: $text-muted;
      margin: 0;
    }
  }
}
</style>
```

- [ ] **Step 2: Create `frontend/src/views/PublishHistory.vue`**

```vue
<template>
  <div class="placeholder-page">
    <div class="page-header">
      <h1>Publish History</h1>
      <p class="page-desc">View your publishing history and reports</p>
    </div>
    <div class="empty-state">
      <el-icon :size="64" color="#64748B"><Clock /></el-icon>
      <h3>Coming Soon</h3>
      <p>Publish history tracking will be available in Phase 3.</p>
    </div>
  </div>
</template>

<script setup>
import { Clock } from '@element-plus/icons-vue'
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.placeholder-page {
  .page-header {
    margin-bottom: 24px;

    h1 {
      font-size: 28px;
      font-weight: 700;
      color: $text-primary;
      margin: 0 0 4px 0;
    }

    .page-desc {
      color: $text-secondary;
      font-size: 14px;
      margin: 0;
    }
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 24px;
    color: $text-muted;

    h3 {
      font-size: 16px;
      color: $text-secondary;
      margin: 16px 0 8px 0;
    }

    p {
      font-size: 14px;
      color: $text-muted;
      margin: 0;
    }
  }
}
</style>
```

- [ ] **Step 3: Create `frontend/src/views/Settings.vue`**

```vue
<template>
  <div class="placeholder-page">
    <div class="page-header">
      <h1>Settings</h1>
      <p class="page-desc">Configure your publishing preferences</p>
    </div>
    <div class="empty-state">
      <el-icon :size="64" color="#64748B"><Setting /></el-icon>
      <h3>Coming Soon</h3>
      <p>System settings will be available in Phase 3.</p>
    </div>
  </div>
</template>

<script setup>
import { Setting } from '@element-plus/icons-vue'
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.placeholder-page {
  .page-header {
    margin-bottom: 24px;

    h1 {
      font-size: 28px;
      font-weight: 700;
      color: $text-primary;
      margin: 0 0 4px 0;
    }

    .page-desc {
      color: $text-secondary;
      font-size: 14px;
      margin: 0;
    }
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 24px;
    color: $text-muted;

    h3 {
      font-size: 16px;
      color: $text-secondary;
      margin: 16px 0 8px 0;
    }

    p {
      font-size: 14px;
      color: $text-muted;
      margin: 0;
    }
  }
}
</style>
```

- [ ] **Step 4: Rewrite `frontend/src/router/index.js`**

Add the three new routes. Remove the `About` route (replaced by Settings):

```js
import { createRouter, createWebHashHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import AccountManagement from '../views/AccountManagement.vue'
import MaterialManagement from '../views/MaterialManagement.vue'
import PublishCenter from '../views/PublishCenter.vue'
import TaskCenter from '../views/TaskCenter.vue'
import PublishHistory from '../views/PublishHistory.vue'
import Settings from '../views/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/account-management',
    name: 'AccountManagement',
    component: AccountManagement
  },
  {
    path: '/material-management',
    name: 'MaterialManagement',
    component: MaterialManagement
  },
  {
    path: '/publish-center',
    name: 'PublishCenter',
    component: PublishCenter
  },
  {
    path: '/task-center',
    name: 'TaskCenter',
    component: TaskCenter
  },
  {
    path: '/publish-history',
    name: 'PublishHistory',
    component: PublishHistory
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
```

- [ ] **Step 5: Verify frontend builds**

```bash
cd frontend
npm run build
```

Expected: Build succeeds without errors.

- [ ] **Step 6: Commit**

```bash
cd ..
git add frontend/src/views/TaskCenter.vue frontend/src/views/PublishHistory.vue frontend/src/views/Settings.vue frontend/src/router/index.js
git commit -m "feat: add placeholder pages for TaskCenter, PublishHistory, Settings"
```

---

## Task 10: Backend Smoke Test

- [ ] **Step 1: Start the Flask backend**

```bash
cd backend
source venv/bin/activate
python app.py
```

Expected: Flask starts on `http://0.0.0.0:5409` without import errors. If there are import errors, check `sys.path` ordering and module availability.

- [ ] **Step 2: Test API endpoints (in another terminal)**

```bash
# Test that the server responds
curl -s http://localhost:5409/getFiles | python3 -m json.tool
```

Expected: `{"code": 200, "msg": "success", "data": []}`

- [ ] **Step 3: Test account endpoint**

```bash
curl -s http://localhost:5409/getAccounts | python3 -m json.tool
```

Expected: `{"code": 200, "msg": null, "data": []}`

- [ ] **Step 4: Verify data directory**

```bash
ls -la ../data/db/database.db
```

Expected: Database file exists.

- [ ] **Step 5: Stop the backend**

Press `Ctrl+C` in the backend terminal.

- [ ] **Step 6: Deactivate venv**

```bash
deactivate
cd ..
```

---

## Task 11: Frontend Smoke Test

- [ ] **Step 1: Start the frontend dev server**

```bash
cd frontend
npm run dev
```

Expected: Vite starts on `http://localhost:5173`. Browser opens automatically (if `open: true` in vite config).

- [ ] **Step 2: Verify dark theme visually**

Open browser to `http://localhost:5173`. Check:
- Background is dark (`#020617`)
- Sidebar is dark with green active state
- Text is light (`#F8FAFC`)
- Cards have dark background (`#0F172A`) with subtle borders
- All 7 navigation items visible in sidebar

- [ ] **Step 3: Verify all pages render**

Click through each sidebar item:
- Dashboard — should load (API calls will fail without backend, but page renders)
- Account — should load
- Material — should load
- Publish — should load
- Tasks — shows "Coming Soon" placeholder
- History — shows "Coming Soon" placeholder
- Settings — shows "Coming Soon" placeholder

- [ ] **Step 4: Stop the frontend**

Press `Ctrl+C` in the frontend terminal.

- [ ] **Step 5: Commit any fixes**

If any fixes were needed during testing, commit them:

```bash
git add frontend/
git commit -m "fix: adjustments from frontend smoke test"
```

---

## Task 12: Full Integration Test (Backend + Frontend Together)

- [ ] **Step 1: Start backend**

Terminal 1:
```bash
cd backend
source venv/bin/activate
python app.py
```

- [ ] **Step 2: Start frontend**

Terminal 2:
```bash
cd frontend
npm run dev
```

- [ ] **Step 3: Verify Dashboard loads with data**

Open `http://localhost:5173`. Dashboard should show stats (all zeros since no data yet) without API errors in browser console.

- [ ] **Step 4: Verify Account Management page renders**

Navigate to Account Management. The page should render the UI (empty table, add account button) without errors.

- [ ] **Step 5: Verify Material Management page renders**

Navigate to Material Management. Upload area should be visible.

- [ ] **Step 6: Record any issues found**

Create a file `docs/phase1-issues.md` documenting:
- Any upstream bugs discovered
- Missing features noticed
- UI/UX issues with the dark theme
- API response inconsistencies
- Browser console errors or warnings

Example format:
```markdown
# Phase 1 Issues Log

## Backend
- [issue description]

## Frontend
- [issue description]

## Dark Theme
- [issue description]
```

- [ ] **Step 7: Commit issues log**

```bash
git add docs/phase1-issues.md
git commit -m "docs: add Phase 1 issues log from integration testing"
```

---

## Spec Coverage Check

| Spec Section | Task | Status |
|---|---|---|
| 1. Project Structure | Tasks 1-4, 6-9 | All directories and files created |
| 2.1 Integration Strategy | Task 3 (app.py, conf.py) | sys.path.insert(1, ...) approach |
| 2.2 Database Init | Task 3 (init_db.py), Task 4 | Tables created in data/db/ |
| 2.3 Dependencies | Tasks 4, 5 | requirements.txt + pip install |
| 3.1 Dark Theme | Tasks 7, 8 | variables.scss + design-system.scss + App.vue |
| 3.2 Vite Config | Task 6 | Full proxy for all API endpoints |
| 3.3 Frontend Tasks | Tasks 6-9 | Copy, theme, layout, placeholders |
| 3.4 New Page Placeholders | Task 9 | Three placeholder Vue components |
| 4.1 Prerequisites | Task 1 | Python, Node, Git checked |
| 4.2 Setup Steps | Tasks 1-5 | Full setup procedure |
| 4.3 Verification | Tasks 10-12 | Backend + frontend + integration tests |
| 4.4 Deliverables | Tasks 1-12 | All deliverables covered |
