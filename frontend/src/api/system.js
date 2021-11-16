import request from '@/utils/request'

const systemApi = {
  Label: '/math_questions/label_list',
  Question: '/math_questions/content_list',
  ManualTag: '/math_questions/manual_tag'
}

export function getMathKnowledge() {
  return request({
    url: systemApi.Label,
    method: 'get'
  })
}

export function getMathContent(params) {
  return request({
    url: systemApi.Question,
    method: 'get',
    params: params
  })
}

export function tagQuestion(params) {
  return request({
    url: systemApi.ManualTag,
    method: 'post',
    data: params
  })
}
