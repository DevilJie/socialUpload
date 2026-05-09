<template>
  <div class="publish-center">
    <!-- ========== LEFT SIDEBAR ========== -->
    <aside class="account-sidebar">
      <div class="sidebar-header">
        <span class="sidebar-title">账号管理</span>
        <span class="sidebar-count">{{ totalCount }}</span>
      </div>

      <div class="group-list">
        <div
          v-for="group in accountGroups"
          :key="group.key"
          :class="['group-wrap', { 'is-selected': selectedPlatform === group.key }]"
        >
          <!-- Group header -->
          <div
            class="group-header cursor-pointer"
            @click="toggleGroup(group.key)"
          >
            <el-icon class="expand-icon" :style="{ color: selectedPlatform === group.key ? group.color : '' }">
              <component :is="expandedGroups.has(group.key) ? ArrowDown : ArrowRight" />
            </el-icon>
            <span class="platform-badge" :style="{ background: group.color }">{{ group.letter }}</span>
            <span class="group-name">{{ group.name }}</span>
            <span class="group-count">{{ group.accounts.length }}</span>
          </div>

          <!-- Expandable account list -->
          <transition name="slide">
            <div v-show="expandedGroups.has(group.key)" class="group-accounts">
              <div
                v-for="account in group.accounts"
                :key="account.id"
                :class="['account-item', 'cursor-pointer', { active: selectedAccountId === account.id }]"
                @click="selectAccount(account, group)"
              >
                <div :class="['account-avatar', { ring: selectedAccountId === account.id }]" :style="selectedAccountId === account.id ? { borderColor: group.color } : {}">
                  {{ account.name ? account.name.charAt(0) : '?' }}
                </div>
                <span class="account-name">{{ account.name }}</span>
                <span :class="['dot', account.status === '正常' ? 'on' : 'off']"></span>
              </div>
              <div v-if="group.accounts.length === 0" class="no-accounts">暂无账号</div>
            </div>
          </transition>
        </div>
      </div>

      <div class="sidebar-footer">
        <div class="add-btn cursor-pointer" @click="accountDialogVisible = true">+ 添加账号</div>
      </div>
    </aside>

    <!-- ========== RIGHT MAIN AREA ========== -->
    <main class="publish-main">
      <!-- Top bar -->
      <div class="main-header">
        <div class="header-left">
          <span class="page-title">发布视频</span>
          <span
            v-if="currentPlatformConfig"
            class="platform-tag"
            :style="{ background: currentPlatformConfig.bgColor, color: currentPlatformConfig.color }"
          >
            {{ currentPlatformConfig.name }} · 个性化设置
          </span>
        </div>
        <div class="header-right">
          <span class="text-btn cursor-pointer" @click="saveDraft">保存草稿</span>
          <el-button type="primary" class="publish-btn" @click="publishAll" :loading="publishing">
            一键发布
          </el-button>
        </div>
      </div>

      <!-- Scrollable content -->
      <div class="main-content">
        <!-- ===== PUBLIC CONFIG ===== -->
        <div class="config-section">
          <div class="section-bar">
            <div class="bar purple"></div>
            <span class="section-label">公共配置</span>
            <span class="hint">所有账号共享</span>
          </div>

          <!-- Video + Cover side by side -->
          <div class="media-row">
            <!-- Video upload card -->
            <div class="media-card">
              <div class="media-label">视频</div>
              <div v-if="commonConfig.fileList.length === 0" class="media-empty">
                <div class="empty-icon">
                  <el-icon :size="32"><Upload /></el-icon>
                </div>
                <div class="empty-text">无视频 - 请选择视频</div>
                <div class="empty-actions">
                  <el-button size="small" plain @click="triggerUploadVideo" class="cursor-pointer">本地选择</el-button>
                  <el-button size="small" plain @click="selectFromLibrary" class="cursor-pointer">素材库</el-button>
                </div>
              </div>
              <div v-else class="media-filled">
                <div v-for="(file, idx) in commonConfig.fileList" :key="idx" class="filled-item">
                  <div class="filled-info">
                    <el-link :href="file.url" target="_blank" type="primary" class="file-name">{{ file.name }}</el-link>
                    <span class="file-size">{{ formatSize(file.size) }}</span>
                  </div>
                  <el-button type="danger" size="small" text @click="commonConfig.fileList.splice(idx, 1)" class="cursor-pointer">删除</el-button>
                </div>
                <div class="filled-actions">
                  <el-button size="small" plain @click="triggerUploadVideo" class="cursor-pointer">继续添加</el-button>
                  <el-button size="small" plain @click="selectFromLibrary" class="cursor-pointer">素材库</el-button>
                </div>
              </div>
            </div>

            <!-- Cover upload card -->
            <div class="media-card">
              <div class="media-label">封面</div>
              <div v-if="!commonConfig.coverFile" class="media-empty">
                <div class="empty-icon">
                  <el-icon :size="32"><Picture /></el-icon>
                </div>
                <div class="empty-text">无封面 - 请选择封面</div>
                <div class="empty-actions">
                  <el-button size="small" plain @click="triggerUploadCover" class="cursor-pointer">本地上传</el-button>
                  <el-button size="small" plain @click="captureFromVideo" class="cursor-pointer">从视频截取</el-button>
                </div>
              </div>
              <div v-else class="media-filled">
                <div class="filled-item">
                  <div class="filled-info">
                    <span class="file-name">{{ commonConfig.coverFile.name }}</span>
                    <span class="file-size">{{ formatSize(commonConfig.coverFile.size) }}</span>
                  </div>
                  <el-button type="danger" size="small" text @click="commonConfig.coverFile = null" class="cursor-pointer">删除</el-button>
                </div>
                <div class="filled-actions">
                  <el-button size="small" plain @click="triggerUploadCover" class="cursor-pointer">更换封面</el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- Title -->
          <div class="form-field">
            <div class="field-head">
              <span>标题</span>
              <span class="field-counter">{{ commonConfig.title.length }}/20</span>
            </div>
            <el-input
              v-model="commonConfig.title"
              placeholder="请输入标题..."
              maxlength="20"
              show-word-limit
            />
          </div>

          <!-- Description -->
          <div class="form-field">
            <div class="field-head">
              <span>描述</span>
              <span class="field-counter">{{ commonConfig.description.length }}/1000</span>
            </div>
            <el-input
              v-model="commonConfig.description"
              type="textarea"
              :rows="4"
              placeholder="请输入描述..."
              maxlength="1000"
              show-word-limit
            />
          </div>

          <!-- Quick tag buttons -->
          <div class="quick-tags">
            <el-button size="small" plain @click="topicDialogVisible = true" class="cursor-pointer"># 添加话题</el-button>
            <el-button size="small" plain class="cursor-pointer">$ 参加活动</el-button>
            <el-button size="small" plain class="cursor-pointer">@ 添加好友</el-button>
          </div>
          <div v-if="commonConfig.topics.length" class="topics-row">
            <el-tag
              v-for="(t, i) in commonConfig.topics"
              :key="i"
              closable
              @close="commonConfig.topics.splice(i, 1)"
              size="small"
              class="cursor-pointer"
            >#{{ t }}</el-tag>
          </div>
        </div>

        <!-- Divider -->
        <div class="divider"></div>

        <!-- ===== PLATFORM-SPECIFIC SETTINGS ===== -->
        <div v-if="currentPlatformConfig" class="config-section">
          <div class="section-bar">
            <div class="bar" :style="{ background: currentPlatformConfig.color }"></div>
            <span class="section-label">{{ currentPlatformConfig.name }} 个性化设置</span>
            <span class="hint">仅对该分组账号生效</span>
          </div>

          <div class="settings-grid">
            <div
              v-for="field in currentPlatformConfig.settingsFields"
              :key="field.key"
              class="setting-card"
              :style="{
                borderColor: currentPlatformConfig.color + '26',
                background: currentPlatformConfig.color + '0a'
              }"
            >
              <div class="setting-label" :style="{ color: currentPlatformConfig.color }">{{ field.label }}</div>

              <!-- Input field -->
              <el-input
                v-if="field.type === 'input'"
                v-model="currentSettings[field.key]"
                :placeholder="field.placeholder"
                size="small"
              />

              <!-- Switch field -->
              <el-switch
                v-else-if="field.type === 'switch'"
                v-model="currentSettings[field.key]"
              />

              <!-- Radio field -->
              <div v-else-if="field.type === 'radio'" class="radio-row">
                <label
                  v-for="opt in field.options"
                  :key="String(opt.value)"
                  class="radio-item cursor-pointer"
                >
                  <input
                    type="radio"
                    :name="selectedPlatform + '-' + field.key"
                    :value="opt.value"
                    v-model="currentSettings[field.key]"
                    class="cursor-pointer"
                  />
                  <span
                    :class="['radio-text', { on: currentSettings[field.key] === opt.value }]"
                    :style="currentSettings[field.key] === opt.value ? { borderColor: currentPlatformConfig.color, color: currentPlatformConfig.color } : {}"
                  >{{ opt.label }}</span>
                </label>
              </div>

              <!-- Select field -->
              <el-select
                v-else-if="field.type === 'select'"
                v-model="currentSettings[field.key]"
                :placeholder="field.placeholder"
                size="small"
                clearable
                class="cursor-pointer"
              >
                <el-option label="暂无可选项" :value="''" disabled />
              </el-select>

              <!-- DateTime field -->
              <el-date-picker
                v-else-if="field.type === 'datetime'"
                v-model="currentSettings[field.key]"
                type="datetime"
                :placeholder="field.placeholder"
                size="small"
                class="cursor-pointer"
              />
            </div>
          </div>
        </div>

        <!-- No platform selected hint -->
        <div v-else class="no-platform-hint">
          <div class="hint-icon">
            <el-icon :size="48"><VideoCameraFilled /></el-icon>
          </div>
          <p>请在左侧选择一个平台分组</p>
          <p class="hint-sub">选择后可配置该平台的个性化发布设置</p>
        </div>
      </div>
    </main>

    <!-- ========== DIALOGS ========== -->

    <!-- Account Selection Dialog -->
    <el-dialog
      v-model="accountDialogVisible"
      title="选择账号"
      width="680px"
      :close-on-click-modal="false"
      class="account-select-dialog"
    >
      <div class="account-dialog-body">
        <div class="account-dialog-toolbar">
          <el-select
            v-model="accountFilterPlatform"
            placeholder="筛选平台"
            size="small"
            clearable
            class="cursor-pointer"
          >
            <el-option label="全部平台" :value="''" />
            <el-option
              v-for="p in platformList"
              :key="p.key"
              :label="p.name"
              :value="p.name"
            />
          </el-select>
          <el-input
            v-model="accountSearchQuery"
            placeholder="输入账号名称搜索..."
            size="small"
            clearable
            class="account-search-input"
          />
        </div>

        <div class="account-dialog-content">
          <!-- Left: platform list -->
          <div class="dialog-platform-list">
            <div
              :class="['dialog-platform-item', 'cursor-pointer', { active: !accountFilterPlatform }]"
              @click="accountFilterPlatform = ''"
            >全部平台</div>
            <div
              v-for="p in platformList"
              :key="p.key"
              :class="['dialog-platform-item', 'cursor-pointer', { active: accountFilterPlatform === p.name }]"
              @click="accountFilterPlatform = p.name"
            >
              <span class="dialog-platform-badge" :style="{ background: p.color }">{{ p.letter }}</span>
              {{ p.name }}
            </div>
          </div>

          <!-- Right: account checkboxes -->
          <div class="dialog-account-list">
            <el-checkbox-group v-model="tempSelectedAccounts">
              <div
                v-for="account in filteredAccounts"
                :key="account.id"
                :class="['dialog-account-item', { disabled: account.status !== '正常' }]"
              >
                <el-checkbox :label="account.id" class="cursor-pointer">
                  <div class="dialog-account-info">
                    <div class="dialog-account-avatar">{{ account.name ? account.name.charAt(0) : '?' }}</div>
                    <span class="dialog-account-name">{{ account.name }}</span>
                    <span class="dialog-account-platform">{{ account.platform }}</span>
                    <span :class="['dialog-account-status', account.status === '正常' ? 'ok' : 'err']">
                      {{ account.status === '正常' ? '正常' : '已失效' }}
                    </span>
                  </div>
                </el-checkbox>
              </div>
            </el-checkbox-group>
            <div v-if="filteredAccounts.length === 0" class="dialog-empty">暂无可选账号</div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <span class="selected-count">已选择 {{ tempSelectedAccounts.length }} 个账号</span>
          <div class="dialog-footer-btns">
            <el-button @click="accountDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmAccountSelection">确认添加</el-button>
          </div>
        </div>
      </template>
    </el-dialog>

    <!-- Topic Selection Dialog -->
    <el-dialog
      v-model="topicDialogVisible"
      title="添加话题"
      width="560px"
      class="topic-dialog"
    >
      <div class="topic-dialog-content">
        <div class="custom-topic-input">
          <el-input v-model="customTopic" placeholder="输入自定义话题" class="custom-input">
            <template #prepend>#</template>
          </el-input>
          <el-button type="primary" @click="addCustomTopic" class="cursor-pointer">添加</el-button>
        </div>

        <div class="recommended-topics">
          <h4>推荐话题</h4>
          <div class="topic-grid">
            <el-button
              v-for="topic in recommendedTopics"
              :key="topic"
              :type="commonConfig.topics.includes(topic) ? 'primary' : 'default'"
              @click="toggleRecommendedTopic(topic)"
              class="topic-btn cursor-pointer"
            >{{ topic }}</el-button>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer-right">
          <el-button @click="topicDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="topicDialogVisible = false">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Video Upload Dialog -->
    <el-dialog
      v-model="videoUploadDialogVisible"
      title="上传视频"
      width="600px"
      class="video-upload-dialog"
    >
      <el-upload
        class="video-upload"
        drag
        :auto-upload="true"
        :action="`${apiBaseUrl}/upload`"
        :on-success="handleVideoUploadSuccess"
        :on-error="handleUploadError"
        multiple
        accept="video/*"
        :headers="authHeaders"
      >
        <el-icon class="el-icon--upload" :size="48"><Upload /></el-icon>
        <div class="el-upload__text">
          将视频文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">支持MP4、AVI等视频格式，可上传多个文件</div>
        </template>
      </el-upload>

      <template #footer>
        <div class="dialog-footer-right">
          <el-button @click="videoUploadDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Cover Upload Dialog -->
    <el-dialog
      v-model="coverUploadDialogVisible"
      title="上传封面"
      width="500px"
      class="cover-upload-dialog"
    >
      <el-upload
        class="cover-upload"
        drag
        :auto-upload="true"
        :action="`${apiBaseUrl}/upload`"
        :on-success="handleCoverUploadSuccess"
        :on-error="handleUploadError"
        accept="image/*"
        :headers="authHeaders"
      >
        <el-icon class="el-icon--upload" :size="48"><Upload /></el-icon>
        <div class="el-upload__text">
          将封面图片拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">支持JPG、PNG等图片格式</div>
        </template>
      </el-upload>

      <template #footer>
        <div class="dialog-footer-right">
          <el-button @click="coverUploadDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Material Library Dialog -->
    <el-dialog
      v-model="materialLibraryVisible"
      title="选择素材"
      width="800px"
      class="material-library-dialog"
    >
      <div class="material-library-content">
        <el-checkbox-group v-model="selectedMaterials">
          <div class="material-list">
            <div
              v-for="material in materials"
              :key="material.id"
              class="material-item"
            >
              <el-checkbox :label="material.id" class="material-checkbox cursor-pointer">
                <div class="material-info">
                  <div class="material-name">{{ material.filename }}</div>
                  <div class="material-details">
                    <span class="mat-size">{{ material.filesize }}MB</span>
                    <span class="mat-time">{{ material.upload_time }}</span>
                  </div>
                </div>
              </el-checkbox>
            </div>
          </div>
        </el-checkbox-group>
        <div v-if="materials.length === 0" class="dialog-empty">素材库暂无素材</div>
      </div>

      <template #footer>
        <div class="dialog-footer-right">
          <el-button @click="materialLibraryVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmMaterialSelect">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Batch Publish Progress Dialog -->
    <el-dialog
      v-model="batchPublishDialogVisible"
      title="批量发布进度"
      width="500px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
      class="batch-progress-dialog"
    >
      <div class="publish-progress">
        <el-progress
          :percentage="publishProgress"
          :status="publishProgress === 100 ? 'success' : ''"
        />
        <div v-if="currentPublishingAccount" class="current-publishing">
          正在发布：{{ currentPublishingAccount }}
        </div>

        <div class="publish-results" v-if="publishResults.length > 0">
          <div
            v-for="(result, index) in publishResults"
            :key="index"
            :class="['result-item', result.status]"
          >
            <el-icon v-if="result.status === 'success'"><Check /></el-icon>
            <el-icon v-else-if="result.status === 'error'"><Close /></el-icon>
            <el-icon v-else><InfoFilled /></el-icon>
            <span class="result-label">{{ result.label }}</span>
            <span class="result-message">{{ result.message }}</span>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer-right">
          <el-button @click="cancelBatch" :disabled="publishProgress === 100">取消发布</el-button>
          <el-button type="primary" @click="batchPublishDialogVisible = false" v-if="publishProgress === 100">关闭</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Hidden file inputs -->
    <input
      ref="videoInputRef"
      type="file"
      accept="video/*"
      multiple
      style="display: none"
      @change="handleVideoFileChange"
    />
    <input
      ref="coverInputRef"
      type="file"
      accept="image/*"
      style="display: none"
      @change="handleCoverFileChange"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, nextTick } from 'vue'
import { Upload, ArrowDown, ArrowRight, Picture, VideoCameraFilled, Check, Close, InfoFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useAccountStore } from '@/stores/account'
import { useAppStore } from '@/stores/app'
import { materialApi } from '@/api/material'
import { http } from '@/utils/request'
import { platformList, getPlatformByKey, platformKeyToId } from '@/config/platforms'

// ========== Stores & Config ==========
const accountStore = useAccountStore()
const appStore = useAppStore()
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5409'
const authHeaders = computed(() => ({ 'Authorization': `Bearer ${localStorage.getItem('token') || ''}` }))

// ========== Left Sidebar State ==========
const expandedGroups = ref(new Set())
const selectedPlatform = ref(null)
const selectedAccountId = ref(null)

// Account groups computed from store
const accountGroups = computed(() => {
  return platformList.map(p => ({
    key: p.key,
    id: p.id,
    name: p.name,
    letter: p.letter,
    color: p.color,
    bgColor: p.bgColor,
    cssClass: p.cssClass,
    logo: p.logo,
    accounts: accountStore.accounts.filter(a => a.platform === p.name),
    settingsFields: p.settingsFields || [],
    defaultSettings: p.defaultSettings || {},
  }))
})

const totalCount = computed(() => accountStore.accounts.length)

const currentPlatformConfig = computed(() =>
  selectedPlatform.value ? getPlatformByKey(selectedPlatform.value) : null
)

// ========== Public Config (shared across all accounts) ==========
const commonConfig = reactive({
  fileList: [],
  coverFile: null,
  title: '',
  description: '',
  topics: [],
})

// ========== Per-platform Config ==========
const platformConfigs = reactive({
  douyin: { productTitle: '', productLink: '', aiContent: false, isOriginal: false, scheduleTime: '', visibility: 'public', allowDownload: true },
  xiaohongshu: { collection: '', groupChat: '', location: '', isOriginal: false, scheduleTime: '' },
  kuaishou: { productTitle: '', productLink: '', aiContent: false, isOriginal: false, scheduleTime: '' },
  bilibili: { zone: '', tags: '', topic: '', isOriginal: false, scheduleTime: '' },
  channels: { isDraft: false, location: '', isOriginal: false },
})

const currentSettings = computed(() =>
  selectedPlatform.value ? platformConfigs[selectedPlatform.value] || {} : {}
)

// ========== Init: expand first group with accounts ==========
const firstGroup = accountGroups.value.find(g => g.accounts.length > 0)
if (firstGroup) {
  expandedGroups.value.add(firstGroup.key)
  selectedPlatform.value = firstGroup.key
}

// ========== Dialog State ==========
const accountDialogVisible = ref(false)
const topicDialogVisible = ref(false)
const videoUploadDialogVisible = ref(false)
const coverUploadDialogVisible = ref(false)
const materialLibraryVisible = ref(false)
const batchPublishDialogVisible = ref(false)

// Account dialog state
const accountFilterPlatform = ref('')
const accountSearchQuery = ref('')
const tempSelectedAccounts = ref([])

// Topic dialog state
const customTopic = ref('')
const recommendedTopics = [
  '游戏', '电影', '音乐', '美食', '旅行', '文化',
  '科技', '生活', '娱乐', '体育', '教育', '艺术',
  '健康', '时尚', '美妆', '摄影', '宠物', '汽车',
]

// Material library state
const selectedMaterials = ref([])
const materials = computed(() => appStore.materials)

// Batch publish state
const publishing = ref(false)
const publishProgress = ref(0)
const publishResults = ref([])
const currentPublishingAccount = ref('')
const isCancelled = ref(false)

// File input refs
const videoInputRef = ref(null)
const coverInputRef = ref(null)

// ========== Sidebar Methods ==========

function toggleGroup(key) {
  if (expandedGroups.value.has(key)) {
    expandedGroups.value.delete(key)
  } else {
    expandedGroups.value.add(key)
  }
  selectedPlatform.value = key
  selectedAccountId.value = null
}

function selectAccount(account, group) {
  selectedAccountId.value = account.id
  selectedPlatform.value = group.key
  // Ensure the group is expanded
  expandedGroups.value.add(group.key)
}

// ========== Upload Methods ==========

function triggerUploadVideo() {
  videoUploadDialogVisible.value = true
}

function triggerUploadCover() {
  coverUploadDialogVisible.value = true
}

function captureFromVideo() {
  if (commonConfig.fileList.length === 0) {
    ElMessage.warning('请先上传视频')
    return
  }
  ElMessage.info('视频截取功能开发中')
}

function handleVideoUploadSuccess(response, file) {
  if (response.code === 200) {
    const filePath = response.data.path || response.data
    const filename = filePath.split('/').pop()
    commonConfig.fileList.push({
      name: file.name,
      url: materialApi.getMaterialPreviewUrl(filename),
      path: filePath,
      size: file.size,
      type: file.type,
    })
    ElMessage.success('视频上传成功')
  } else {
    ElMessage.error(response.msg || '上传失败')
  }
}

function handleCoverUploadSuccess(response, file) {
  if (response.code === 200) {
    const filePath = response.data.path || response.data
    const filename = filePath.split('/').pop()
    commonConfig.coverFile = {
      name: file.name,
      url: materialApi.getMaterialPreviewUrl(filename),
      path: filePath,
      size: file.size,
      type: file.type,
    }
    coverUploadDialogVisible.value = false
    ElMessage.success('封面上传成功')
  } else {
    ElMessage.error(response.msg || '上传失败')
  }
}

function handleUploadError() {
  ElMessage.error('文件上传失败')
}

function handleVideoFileChange(e) {
  // handled by el-upload dialog
}

function handleCoverFileChange(e) {
  // handled by el-upload dialog
}

// ========== Material Library ==========

async function selectFromLibrary() {
  if (materials.value.length === 0) {
    try {
      const response = await materialApi.getAllMaterials()
      if (response.code === 200) {
        appStore.setMaterials(response.data)
      } else {
        ElMessage.error('获取素材列表失败')
        return
      }
    } catch (error) {
      console.error('获取素材列表出错:', error)
      ElMessage.error('获取素材列表失败')
      return
    }
  }
  selectedMaterials.value = []
  materialLibraryVisible.value = true
}

function confirmMaterialSelect() {
  if (selectedMaterials.value.length === 0) {
    ElMessage.warning('请选择至少一个素材')
    return
  }
  selectedMaterials.value.forEach(materialId => {
    const material = materials.value.find(m => m.id === materialId)
    if (material) {
      const exists = commonConfig.fileList.some(f => f.path === material.file_path)
      if (!exists) {
        commonConfig.fileList.push({
          name: material.filename,
          url: materialApi.getMaterialPreviewUrl(material.file_path.split('/').pop()),
          path: material.file_path,
          size: material.filesize * 1024 * 1024,
          type: 'video/mp4',
        })
      }
    }
  })
  const count = selectedMaterials.value.length
  materialLibraryVisible.value = false
  selectedMaterials.value = []
  ElMessage.success(`已添加 ${count} 个素材`)
}

// ========== Topic Methods ==========

function addCustomTopic() {
  const topic = customTopic.value.trim()
  if (!topic) {
    ElMessage.warning('请输入话题内容')
    return
  }
  if (commonConfig.topics.includes(topic)) {
    ElMessage.warning('话题已存在')
    return
  }
  commonConfig.topics.push(topic)
  customTopic.value = ''
  ElMessage.success('话题添加成功')
}

function toggleRecommendedTopic(topic) {
  const idx = commonConfig.topics.indexOf(topic)
  if (idx > -1) {
    commonConfig.topics.splice(idx, 1)
  } else {
    commonConfig.topics.push(topic)
  }
}

// ========== Account Dialog Methods ==========

const filteredAccounts = computed(() => {
  let list = accountStore.accounts
  if (accountFilterPlatform.value) {
    list = list.filter(a => a.platform === accountFilterPlatform.value)
  }
  if (accountSearchQuery.value.trim()) {
    const query = accountSearchQuery.value.trim().toLowerCase()
    list = list.filter(a => a.name.toLowerCase().includes(query))
  }
  return list
})

function confirmAccountSelection() {
  // In the new design, this adds accounts to the sidebar groups
  // For now just close the dialog with a message
  accountDialogVisible.value = false
  ElMessage.success(`已选择 ${tempSelectedAccounts.value.length} 个账号`)
  tempSelectedAccounts.value = []
}

// ========== Publish Methods ==========

function saveDraft() {
  try {
    const draftData = {
      commonConfig: {
        title: commonConfig.title,
        description: commonConfig.description,
        topics: [...commonConfig.topics],
        fileList: commonConfig.fileList.map(f => ({ name: f.name, path: f.path, url: f.url, size: f.size, type: f.type })),
        coverFile: commonConfig.coverFile ? { name: commonConfig.coverFile.name, path: commonConfig.coverFile.path, url: commonConfig.coverFile.url, size: commonConfig.coverFile.size, type: commonConfig.coverFile.type } : null,
      },
      platformConfigs: JSON.parse(JSON.stringify(platformConfigs)),
      savedAt: new Date().toISOString(),
    }
    localStorage.setItem('publishDraft', JSON.stringify(draftData))
    ElMessage.success('草稿已保存')
  } catch (e) {
    ElMessage.error('草稿保存失败')
  }
}

async function publishAll() {
  // Validate
  if (commonConfig.fileList.length === 0) {
    ElMessage.error('请先上传视频文件')
    return
  }
  if (!commonConfig.title.trim()) {
    ElMessage.error('请输入标题')
    return
  }

  publishing.value = true
  publishProgress.value = 0
  publishResults.value = []
  isCancelled.value = false
  currentPublishingAccount.value = ''
  batchPublishDialogVisible.value = true

  // Collect all accounts across all groups
  const allTasks = []
  for (const group of accountGroups.value) {
    if (group.accounts.length === 0) continue
    const pSettings = platformConfigs[group.key] || {}
    for (const account of group.accounts) {
      allTasks.push({ account, group, platformSettings: { ...pSettings } })
    }
  }

  if (allTasks.length === 0) {
    ElMessage.warning('没有可发布的账号')
    publishing.value = false
    batchPublishDialogVisible.value = false
    return
  }

  for (let i = 0; i < allTasks.length; i++) {
    if (isCancelled.value) {
      publishResults.value.push({
        label: allTasks[i].account.name,
        status: 'cancelled',
        message: '已取消',
      })
      continue
    }

    const { account, group, platformSettings } = allTasks[i]
    currentPublishingAccount.value = account.name
    publishProgress.value = Math.floor((i / allTasks.length) * 100)

    try {
      const publishData = {
        type: group.id,
        title: commonConfig.title,
        tags: commonConfig.topics,
        fileList: commonConfig.fileList.map(f => f.path),
        accountList: [account.filePath],
        enableTimer: platformSettings.scheduleTime ? 1 : 0,
        videosPerDay: 1,
        dailyTimes: ['10:00'],
        startDays: 0,
        category: platformSettings.isOriginal ? 1 : 0,
        productLink: platformSettings.productLink || '',
        productTitle: platformSettings.productTitle || '',
        isDraft: platformSettings.isDraft || false,
      }

      await http.post('/postVideo', publishData)
      publishResults.value.push({
        label: account.name,
        status: 'success',
        message: '发布成功',
      })
    } catch (error) {
      publishResults.value.push({
        label: account.name,
        status: 'error',
        message: error.message || '发布失败',
      })
    }
  }

  publishProgress.value = 100
  currentPublishingAccount.value = ''
  publishing.value = false

  const successCount = publishResults.value.filter(r => r.status === 'success').length
  const failCount = publishResults.value.filter(r => r.status === 'error').length

  if (failCount > 0) {
    ElMessage.warning(`发布完成：${successCount}个成功，${failCount}个失败`)
  } else {
    ElMessage.success('全部发布成功')
    setTimeout(() => {
      batchPublishDialogVisible.value = false
    }, 1500)
  }
}

function cancelBatch() {
  isCancelled.value = true
  ElMessage.info('正在取消发布...')
}

// ========== Utility ==========

function formatSize(bytes) {
  if (!bytes) return '0B'
  if (bytes < 1024) return bytes + 'B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + 'KB'
  return (bytes / 1024 / 1024).toFixed(2) + 'MB'
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

// ========== Utility Classes ==========
.cursor-pointer {
  cursor: pointer;
}

// ========== Layout ==========
.publish-center {
  display: flex;
  height: 100%;
  gap: 0;
  overflow: hidden;
}

// ========== LEFT SIDEBAR ==========
.account-sidebar {
  width: 220px;
  flex-shrink: 0;
  background: $bg-base;
  border-right: 1px solid $border;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  .sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 16px 14px;
    border-bottom: 1px solid $border;

    .sidebar-title {
      font-size: 15px;
      font-weight: 600;
      color: $text-primary;
    }

    .sidebar-count {
      font-size: 12px;
      color: $text-muted;
      background: $bg-surface;
      padding: 2px 8px;
      border-radius: 10px;
    }
  }

  .group-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;

    &::-webkit-scrollbar {
      width: 4px;
    }
    &::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 2px;
    }
  }

  .group-wrap {
    margin: 2px 8px;
    border-radius: $radius-base;
    transition: $transition-base;

    &.is-selected {
      background: rgba(139, 92, 246, 0.06);
      border: 1px solid rgba(139, 92, 246, 0.12);
      margin: 2px 7px;
    }
  }

  .group-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px;
    border-radius: $radius-base;
    transition: $transition-base;
    user-select: none;

    &:hover {
      background: rgba(255, 255, 255, 0.03);
    }

    .expand-icon {
      font-size: 12px;
      color: $text-muted;
      transition: $transition-base;
    }

    .platform-badge {
      width: 22px;
      height: 22px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 11px;
      font-weight: 700;
      flex-shrink: 0;
    }

    .group-name {
      flex: 1;
      font-size: 13px;
      color: $text-secondary;
      font-weight: 500;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .group-count {
      font-size: 11px;
      color: $text-muted;
      background: rgba(255, 255, 255, 0.06);
      padding: 1px 6px;
      border-radius: 8px;
    }
  }

  .group-accounts {
    padding: 0 12px 8px 42px;

    .no-accounts {
      font-size: 12px;
      color: $text-muted;
      padding: 4px 0;
    }
  }

  // Slide transition
  .slide-enter-active,
  .slide-leave-active {
    transition: all 200ms ease;
    overflow: hidden;
  }
  .slide-enter-from,
  .slide-leave-to {
    opacity: 0;
    max-height: 0;
  }
  .slide-enter-to,
  .slide-leave-from {
    opacity: 1;
    max-height: 500px;
  }

  .account-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 8px;
    border-radius: 8px;
    transition: $transition-base;

    &:hover {
      background: rgba(255, 255, 255, 0.04);
    }

    &.active {
      background: rgba(139, 92, 246, 0.08);
    }

    .account-avatar {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      color: $text-secondary;
      font-weight: 600;
      flex-shrink: 0;
      border: 2px solid transparent;
      transition: $transition-base;

      &.ring {
        border-color: $brand-start;
      }
    }

    .account-name {
      flex: 1;
      font-size: 12px;
      color: $text-secondary;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      flex-shrink: 0;

      &.on {
        background: $success-color;
      }
      &.off {
        background: $danger-color;
      }
    }
  }

  .sidebar-footer {
    padding: 12px;
    border-top: 1px solid $border;

    .add-btn {
      border: 1px dashed $border;
      border-radius: $radius-base;
      padding: 8px;
      text-align: center;
      font-size: 13px;
      color: $text-muted;
      transition: $transition-base;

      &:hover {
        border-color: $border-active;
        color: $brand-start;
        background: rgba(139, 92, 246, 0.06);
      }
    }
  }
}

// ========== RIGHT MAIN ==========
.publish-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: $bg-elevated;
  overflow: hidden;

  .main-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    border-bottom: 1px solid $border;
    flex-shrink: 0;

    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;

      .page-title {
        font-size: 18px;
        font-weight: 700;
        color: $text-primary;
      }

      .platform-tag {
        font-size: 12px;
        font-weight: 500;
        padding: 4px 12px;
        border-radius: 20px;
      }
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 16px;

      .text-btn {
        font-size: 14px;
        color: $text-secondary;
        transition: $transition-base;

        &:hover {
          color: $brand-start;
        }
      }

      .publish-btn {
        background: $gradient-brand;
        border-color: transparent;
        color: #fff;
        font-weight: 600;
        padding: 8px 24px;

        &:hover,
        &:focus {
          opacity: 0.9;
          color: #fff;
        }
      }
    }
  }

  .main-content {
    flex: 1;
    overflow-y: auto;
    padding: 24px;

    &::-webkit-scrollbar {
      width: 6px;
    }
    &::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
    }
  }
}

// ========== Config Section ==========
.config-section {
  margin-bottom: 24px;
}

.section-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;

  .bar {
    width: 3px;
    height: 18px;
    border-radius: 2px;
    flex-shrink: 0;

    &.purple {
      background: $brand-start;
    }
  }

  .section-label {
    font-size: 15px;
    font-weight: 600;
    color: $text-primary;
  }

  .hint {
    font-size: 12px;
    color: $text-muted;
  }
}

// ========== Media Row (Video + Cover) ==========
.media-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.media-card {
  border: 1px dashed $border;
  border-radius: $radius-card;
  padding: 20px;
  min-height: 180px;
  display: flex;
  flex-direction: column;
  transition: $transition-base;

  &:hover {
    border-color: $border-active;
  }

  .media-label {
    font-size: 13px;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: 16px;
  }

  .media-empty {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;

    .empty-icon {
      color: $text-muted;
      opacity: 0.5;
    }

    .empty-text {
      font-size: 13px;
      color: $text-muted;
    }

    .empty-actions {
      display: flex;
      gap: 8px;
      margin-top: 8px;
    }
  }

  .media-filled {
    .filled-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid $border;
      border-radius: $radius-sm;
      margin-bottom: 8px;

      .filled-info {
        display: flex;
        align-items: center;
        gap: 8px;
        min-width: 0;
        flex: 1;

        .file-name {
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .file-size {
          font-size: 11px;
          color: $text-muted;
          flex-shrink: 0;
        }
      }
    }

    .filled-actions {
      display: flex;
      gap: 8px;
    }
  }
}

// ========== Form Fields ==========
.form-field {
  margin-bottom: 20px;

  .field-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 13px;
    font-weight: 500;
    color: $text-secondary;

    .field-counter {
      font-size: 12px;
      color: $text-muted;
    }
  }

  :deep(.el-input__wrapper),
  :deep(.el-textarea__inner) {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid $border;
    border-radius: $radius-base;
    box-shadow: none;
    color: $text-primary;
    transition: $transition-base;

    &:hover {
      border-color: $border-active;
    }

    &:focus,
    &.is-focus {
      border-color: $brand-start;
    }
  }

  :deep(.el-input__count) {
    color: $text-muted;
    background: transparent;
  }
}

// ========== Quick Tags ==========
.quick-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.topics-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;

  .el-tag {
    background: $gradient-brand-subtle;
    border-color: $border-active;
    color: $text-primary;
  }
}

// ========== Divider ==========
.divider {
  height: 1px;
  background: $border;
  margin: 8px 0 24px;
  background-image: repeating-linear-gradient(
    90deg,
    $border,
    $border 6px,
    transparent 6px,
    transparent 12px
  );
}

// ========== Settings Grid ==========
.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}

.setting-card {
  padding: 14px 16px;
  border: 1px solid;
  border-radius: $radius-card;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: $transition-base;

  &:hover {
    filter: brightness(1.1);
  }

  .setting-label {
    font-size: 13px;
    font-weight: 600;
  }

  :deep(.el-input__wrapper),
  :deep(.el-select .el-input__wrapper) {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid $border;
    border-radius: $radius-sm;
    box-shadow: none;
    transition: $transition-base;

    &:hover {
      border-color: $border-active;
    }
  }

  .radio-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .radio-item {
    display: flex;
    align-items: center;
    gap: 4px;

    input[type='radio'] {
      display: none;
    }

    .radio-text {
      padding: 4px 14px;
      border: 1px solid $border;
      border-radius: $radius-sm;
      font-size: 12px;
      color: $text-secondary;
      transition: $transition-base;

      &.on {
        border-color: $brand-start;
        color: $brand-start;
        background: rgba(139, 92, 246, 0.06);
      }
    }
  }
}

// ========== No Platform Hint ==========
.no-platform-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: $text-muted;
  text-align: center;

  .hint-icon {
    opacity: 0.3;
    margin-bottom: 16px;
  }

  p {
    font-size: 15px;
    margin: 4px 0;
  }

  .hint-sub {
    font-size: 13px;
    color: $text-muted;
  }
}

// ========== Account Dialog ==========
.account-select-dialog {
  .account-dialog-body {
    .account-dialog-toolbar {
      display: flex;
      gap: 12px;
      margin-bottom: 16px;

      .account-search-input {
        flex: 1;
      }
    }

    .account-dialog-content {
      display: flex;
      gap: 0;
      border: 1px solid $border;
      border-radius: $radius-base;
      overflow: hidden;
      min-height: 320px;
    }

    .dialog-platform-list {
      width: 140px;
      flex-shrink: 0;
      border-right: 1px solid $border;
      background: rgba(0, 0, 0, 0.2);
      overflow-y: auto;

      .dialog-platform-item {
        padding: 10px 12px;
        font-size: 13px;
        color: $text-secondary;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: $transition-base;

        &:hover {
          background: rgba(255, 255, 255, 0.03);
        }

        &.active {
          background: rgba(139, 92, 246, 0.08);
          color: $text-primary;
          font-weight: 500;
        }

        .dialog-platform-badge {
          width: 18px;
          height: 18px;
          border-radius: 4px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #fff;
          font-size: 9px;
          font-weight: 700;
          flex-shrink: 0;
        }
      }
    }

    .dialog-account-list {
      flex: 1;
      padding: 12px;
      overflow-y: auto;

      .dialog-account-item {
        padding: 8px 10px;
        border-radius: $radius-sm;
        transition: $transition-base;
        margin-bottom: 4px;

        &:hover {
          background: rgba(255, 255, 255, 0.03);
        }

        &.disabled {
          opacity: 0.5;
        }
      }

      .dialog-account-info {
        display: flex;
        align-items: center;
        gap: 8px;

        .dialog-account-avatar {
          width: 26px;
          height: 26px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.08);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 11px;
          color: $text-secondary;
          font-weight: 600;
          flex-shrink: 0;
        }

        .dialog-account-name {
          font-size: 13px;
          color: $text-primary;
          font-weight: 500;
        }

        .dialog-account-platform {
          font-size: 11px;
          color: $text-muted;
        }

        .dialog-account-status {
          font-size: 11px;
          margin-left: auto;

          &.ok {
            color: $success-color;
          }
          &.err {
            color: $danger-color;
          }
        }
      }
    }
  }

  .dialog-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .selected-count {
      font-size: 13px;
      color: $text-muted;
    }

    .dialog-footer-btns {
      display: flex;
      gap: 8px;
    }
  }
}

// ========== Topic Dialog ==========
.topic-dialog {
  .topic-dialog-content {
    .custom-topic-input {
      display: flex;
      gap: 12px;
      margin-bottom: 24px;

      .custom-input {
        flex: 1;
      }
    }

    .recommended-topics {
      h4 {
        margin: 0 0 16px 0;
        font-size: 15px;
        font-weight: 600;
        color: $text-primary;
      }

      .topic-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: 10px;

        .topic-btn {
          height: 36px;
          font-size: 14px;
          border-radius: $radius-base;
          min-width: 100px;
          padding: 0 12px;
          white-space: nowrap;
          text-align: center;
          display: flex;
          align-items: center;
          justify-content: center;
        }
      }
    }
  }
}

// ========== Upload Dialogs ==========
.video-upload-dialog,
.cover-upload-dialog {
  .video-upload,
  .cover-upload {
    width: 100%;

    :deep(.el-upload-dragger) {
      width: 100%;
      height: 180px;
      background: rgba(255, 255, 255, 0.02);
      border-color: $border;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: $transition-base;

      &:hover {
        border-color: $border-active;
      }

      .el-icon--upload {
        color: $text-muted;
        margin-bottom: 8px;
      }
    }

    .el-upload__text {
      color: $text-secondary;
      font-size: 14px;

      em {
        color: $brand-start;
      }
    }

    .el-upload__tip {
      color: $text-muted;
      font-size: 12px;
      margin-top: 8px;
    }
  }
}

// ========== Material Library Dialog ==========
.material-library-dialog {
  .material-library-content {
    .material-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-height: 400px;
      overflow-y: auto;

      .material-item {
        padding: 10px 14px;
        border: 1px solid $border;
        border-radius: $radius-base;
        transition: $transition-base;

        &:hover {
          border-color: $border-active;
        }

        .material-info {
          .material-name {
            font-size: 14px;
            color: $text-primary;
            font-weight: 500;
          }

          .material-details {
            display: flex;
            gap: 16px;
            margin-top: 4px;
            font-size: 12px;
            color: $text-muted;
          }
        }
      }
    }
  }
}

// ========== Batch Progress Dialog ==========
.batch-progress-dialog {
  .publish-progress {
    padding: 12px 0;

    .current-publishing {
      margin: 16px 0;
      text-align: center;
      color: $text-secondary;
      font-size: 14px;
    }

    .publish-results {
      margin-top: 20px;
      border-top: 1px solid $border;
      padding-top: 16px;
      max-height: 300px;
      overflow-y: auto;

      .result-item {
        display: flex;
        align-items: center;
        padding: 8px 0;
        color: $text-secondary;

        .el-icon {
          margin-right: 8px;
        }

        .result-label {
          margin-right: 10px;
          font-weight: 500;
          color: $text-primary;
        }

        .result-message {
          color: $text-muted;
          font-size: 13px;
        }

        &.success {
          .el-icon,
          .result-label {
            color: $success-color;
          }
        }

        &.error {
          .el-icon,
          .result-label {
            color: $danger-color;
          }
        }

        &.cancelled {
          color: $text-muted;

          .result-label {
            color: $text-muted;
          }
        }
      }
    }
  }
}

// ========== Shared Dialog Styles ==========
.dialog-footer-right {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.dialog-empty {
  text-align: center;
  padding: 40px 0;
  color: $text-muted;
  font-size: 14px;
}
</style>
