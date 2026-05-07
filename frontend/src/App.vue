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
            background-color="#020617"
            text-color="#94A3B8"
            active-text-color="#22C55E"
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
              <!-- reserved -->
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

// 当前激活的菜单项
const activeMenu = computed(() => {
  return route.path
})

// 侧边栏折叠状态
const isCollapse = ref(false)

// 切换侧边栏折叠状态
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
  color: $text-primary;
  height: 100vh;
  overflow: hidden;
  transition: width $transition-normal;

  .sidebar {
    display: flex;
    flex-direction: column;
    height: 100%;

    .logo {
      height: 60px;
      padding: 0 16px;
      display: flex;
      align-items: center;
      background-color: $bg-color-overlay;
      overflow: hidden;

      .logo-img {
        width: 32px;
        height: 32px;
        margin-right: 12px;
      }

      h2 {
        color: $text-primary;
        font-size: 16px;
        font-weight: 600;
        white-space: nowrap;
        margin: 0;
      }
    }

    .sidebar-menu {
      border-right: none;
      flex: 1;

      .el-menu-item {
        display: flex;
        align-items: center;

        .el-icon {
          margin-right: 10px;
          font-size: 18px;
        }

        &.is-active {
          color: $primary-color;
          background-color: rgba($primary-color, 0.1);
        }

        &:hover {
          background-color: rgba($primary-color, 0.05);
        }
      }
    }
  }
}

.el-header {
  background-color: $bg-color-overlay;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
  padding: 0;
  height: 60px;

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    padding: 0 16px;

    .header-left {
      .toggle-sidebar {
        font-size: 20px;
        cursor: pointer;
        color: $text-secondary;

        &:hover {
          color: $primary-color;
        }
      }
    }

    .header-right {
      .user-dropdown {
        display: flex;
        align-items: center;
        cursor: pointer;

        .username {
          margin: 0 8px;
          color: $text-secondary;
        }

        .el-icon {
          font-size: 12px;
          color: $text-muted;
        }
      }
    }
  }
}

.el-main {
  background-color: $bg-color-page;
  padding: 20px;
  overflow-y: auto;
}
</style>
