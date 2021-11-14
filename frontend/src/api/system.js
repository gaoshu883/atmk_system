import request from '@/utils/request'

const systemApi = {
  Label: '/math_questions/label_list',
  Question: '/math_questions/content_list'
}

export function getMathKnowledge() {
  return request({
    url: systemApi.Label,
    method: 'get'
  })
}

export function getMathContent() {
  return request({
    url: systemApi.Question,
    method: 'get'
  })
}
