import request from '@/utils/request'

const systemApi = {
  Label: '/math_questions/label_list',
  Question: '/math_questions/content_list',
  ManualTag: '/math_questions/manual_tag',
  CleanResult: '/math_questions/cleaned_result',
  CleanQuestion: '/math_questions/clean_data',
  ReadVector: '/math_questions/read_vector'
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
    method: 'post',
    data: params
  })
}

export function tagQuestion(params) {
  return request({
    url: systemApi.ManualTag,
    method: 'post',
    data: params
  })
}

export function getCleanResult(params) {
  return request({
    url: systemApi.CleanResult,
    method: 'get',
    params: params
  })
}

export function postCleanData(params) {
  return request({
    url: systemApi.CleanQuestion,
    method: 'post',
    data: params,
    timeout: 0
  })
}

export function getVectorByType(params) {
  return request({
    url: systemApi.ReadVector,
    method: 'post',
    data: params,
    timeout: 0
  })
}
