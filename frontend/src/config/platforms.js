/**
 * 统一平台配置 — 所有平台相关数据的唯一真实来源
 *
 * 使用方式：
 *   import { PLATFORMS, platformList, platformIdToName } from '@/config/platforms'
 */

// Logo 文件使用 Vite 的静态资源导入
import logoDouyin from '@/assets/logos/logo-douyin.svg'
import logoKuaishou from '@/assets/logos/logo-kuaishou.svg'
import logoXiaohongshu from '@/assets/logos/logo-xiaohongshu.svg'
import logoChannels from '@/assets/logos/logo-channels.svg'
import logoBilibili from '@/assets/logos/logo-bilibili.svg'

export const PLATFORMS = {
  XIAOHONGSHU: {
    id: 1,
    key: 'xiaohongshu',
    name: '小红书',
    shortName: 'XHS',
    letter: 'X',
    logo: logoXiaohongshu,
    color: '#8b5cf6',
    bgColor: 'rgba(139, 92, 246, 0.15)',
    cssClass: 'xiaohongshu',
    creatorUrl: 'https://creator.xiaohongshu.com/',
    settingsFields: [
      { key: 'collection', label: '合集', type: 'select', placeholder: '请选择合集' },
      { key: 'groupChat', label: '群聊', type: 'select', placeholder: '请选择群聊' },
      { key: 'location', label: '位置', type: 'select', placeholder: '选择位置' },
      { key: 'isOriginal', label: '原创声明', type: 'radio', options: [{ label: '原创', value: true }, { label: '非原创', value: false }] },
      { key: 'scheduleTime', label: '定时发布', type: 'datetime', placeholder: '选择时间' },
    ],
    defaultSettings: { collection: '', groupChat: '', location: '', isOriginal: false, scheduleTime: '' },
  },
  CHANNELS: {
    id: 2,
    key: 'channels',
    name: '视频号',
    shortName: 'SPH',
    letter: 'V',
    logo: logoChannels,
    color: '#3b82f6',
    bgColor: 'rgba(59, 130, 246, 0.15)',
    cssClass: 'channels',
    creatorUrl: 'https://channels.weixin.qq.com/',
    settingsFields: [
      { key: 'isDraft', label: '草稿模式', type: 'switch', description: '仅保存草稿（用手机发布）' },
      { key: 'location', label: '位置', type: 'select', placeholder: '选择位置' },
      { key: 'isOriginal', label: '原创声明', type: 'radio', options: [{ label: '原创', value: true }, { label: '非原创', value: false }] },
    ],
    defaultSettings: { isDraft: false, location: '', isOriginal: false },
  },
  DOUYIN: {
    id: 3,
    key: 'douyin',
    name: '抖音',
    shortName: 'DY',
    letter: 'D',
    logo: logoDouyin,
    color: '#f43f5e',
    bgColor: 'rgba(244, 63, 94, 0.15)',
    cssClass: 'douyin',
    creatorUrl: 'https://creator.douyin.com/',
    settingsFields: [
      { key: 'productTitle', label: '商品名称', type: 'input', placeholder: '请输入商品名称' },
      { key: 'productLink', label: '商品链接', type: 'input', placeholder: '请输入商品链接' },
      { key: 'aiContent', label: '包含AI生成内容', type: 'switch' },
      { key: 'isOriginal', label: '原创声明', type: 'radio', options: [{ label: '原创', value: true }, { label: '非原创', value: false }] },
      { key: 'scheduleTime', label: '定时发布', type: 'datetime', placeholder: '选择时间' },
      { key: 'visibility', label: '谁可以看', type: 'radio', options: [{ label: '公开', value: 'public' }, { label: '私密', value: 'private' }] },
      { key: 'allowDownload', label: '允许下载', type: 'switch' },
    ],
    defaultSettings: { productTitle: '', productLink: '', aiContent: false, isOriginal: false, scheduleTime: '', visibility: 'public', allowDownload: true },
  },
  KUAISHOU: {
    id: 4,
    key: 'kuaishou',
    name: '快手',
    shortName: 'KS',
    letter: 'K',
    logo: logoKuaishou,
    color: '#f59e0b',
    bgColor: 'rgba(245, 158, 11, 0.15)',
    cssClass: 'kuaishou',
    creatorUrl: 'https://k.kuaishou.com/',
    settingsFields: [
      { key: 'productTitle', label: '商品名称', type: 'input', placeholder: '请输入商品名称' },
      { key: 'productLink', label: '商品链接', type: 'input', placeholder: '请输入商品链接' },
      { key: 'aiContent', label: '包含AI生成内容', type: 'switch' },
      { key: 'isOriginal', label: '原创声明', type: 'radio', options: [{ label: '原创', value: true }, { label: '非原创', value: false }] },
      { key: 'scheduleTime', label: '定时发布', type: 'datetime', placeholder: '选择时间' },
    ],
    defaultSettings: { productTitle: '', productLink: '', aiContent: false, isOriginal: false, scheduleTime: '' },
  },
  BILIBILI: {
    id: 5,
    key: 'bilibili',
    name: 'B站',
    shortName: 'BL',
    letter: 'B',
    logo: logoBilibili,
    color: '#00a1d6',
    bgColor: 'rgba(0, 161, 214, 0.15)',
    cssClass: 'bilibili',
    creatorUrl: 'https://member.bilibili.com/',
    settingsFields: [
      { key: 'zone', label: '分区', type: 'select', placeholder: '选择投稿分区' },
      { key: 'tags', label: '标签', type: 'input', placeholder: '自定义标签，逗号分隔' },
      { key: 'topic', label: '话题', type: 'select', placeholder: '选择话题' },
      { key: 'isOriginal', label: '原创声明', type: 'radio', options: [{ label: '原创', value: true }, { label: '非原创', value: false }] },
      { key: 'scheduleTime', label: '定时发布', type: 'datetime', placeholder: '选择时间' },
    ],
    defaultSettings: { zone: '', tags: '', topic: '', isOriginal: false, scheduleTime: '' },
  },
}

// 派生数据
export const platformList = Object.values(PLATFORMS)

export const platformIdToName = Object.fromEntries(
  platformList.map(p => [p.id, p.name])
)

export const platformNameToId = Object.fromEntries(
  platformList.map(p => [p.name, p.id])
)

export const platformCssMap = Object.fromEntries(
  platformList.map(p => [p.name, p.cssClass])
)

/**
 * 根据平台ID获取平台配置
 */
export function getPlatformById(id) {
  return platformList.find(p => p.id === id) || null
}

/**
 * 根据平台名称获取平台配置
 */
export function getPlatformByName(name) {
  return platformList.find(p => p.name === name) || null
}

/**
 * 根据 key 获取平台配置
 */
export function getPlatformByKey(key) {
  return platformList.find(p => p.key === key) || null
}

/**
 * 根据 key 获取平台 ID
 */
export const platformKeyToId = Object.fromEntries(
  platformList.map(p => [p.key, p.id])
)
