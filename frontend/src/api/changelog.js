import { http } from '@/utils/request'

export const changelogApi = {
  getChangelogList() {
    return http.get('/api/v2/changelog')
  },
}
