<template>
  <div class="task-center-page">
    <div class="page-header">
      <h1>Task Center</h1>
      <p>Manage and monitor your publishing tasks</p>
    </div>
    <div class="empty-state">
      <el-icon class="empty-icon"><List /></el-icon>
      <h2>Coming Soon</h2>
      <p>Task management features are under development. Stay tuned for updates.</p>
    </div>
  </div>
</template>

<script setup>
import { List } from '@element-plus/icons-vue'
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.task-center-page {
  .page-header {
    margin-bottom: 24px;

    h1 {
      font-size: 24px;
      font-weight: 600;
      color: $text-primary;
      margin: 0 0 8px 0;
    }

    p {
      font-size: 14px;
      color: $text-secondary;
      margin: 0;
    }
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 20px;
    background-color: $bg-color-surface;
    border-radius: 8px;
    border: 1px solid $border-base;

    .empty-icon {
      font-size: 48px;
      color: $text-muted;
      margin-bottom: 16px;
    }

    h2 {
      font-size: 20px;
      font-weight: 500;
      color: $text-primary;
      margin: 0 0 8px 0;
    }

    p {
      font-size: 14px;
      color: $text-secondary;
      margin: 0;
    }
  }
}
</style>
