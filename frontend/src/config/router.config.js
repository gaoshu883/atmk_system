// eslint-disable-next-line
import { UserLayout, BasicLayout } from '@/layouts'

const RouteView = {
  name: 'RouteView',
  render: h => h('router-view')
}

export const asyncRouterMap = [
  {
    path: '/',
    name: 'index',
    component: BasicLayout,
    meta: { title: '首页' },
    redirect: '/dataset/question',
    children: [
      {
        path: '/dataset',
        name: 'dataset',
        redirect: '/dataset/question',
        component: RouteView,
        meta: { title: '数据集', keepAlive: true, icon: 'database' },
        children: [
          {
            path: '/dataset/question',
            name: 'Question',
            component: () => import('@/views/dataset/Question'),
            meta: { title: '题目管理', keepAlive: false }
          },
          {
            path: '/dataset/knowledge',
            name: 'Knowledge',
            component: () => import('@/views/dataset/Knowledge'),
            meta: { title: '知识点管理', keepAlive: false }
          }
        ]
      },
      {
        path: '/dataclean',
        name: 'DataClean',
        component: () => import('@/views/dataset/DataClean'),
        meta: { title: '数据清洗', icon: 'scissor', keepAlive: false }
      },
      {
        path: '/preprocess',
        name: 'Preprocess',
        component: () => import('@/views/dataset/Preprocess'),
        meta: { title: '数据预处理', icon: 'highlight', keepAlive: true }
      },
      {
        path: '/atmkmodel',
        name: 'ATMKModel',
        component: () => import('@/views/autotag/ATMKModel'),
        meta: { title: '模型训练', icon: 'deployment-unit', keepAlive: true }
      },
      {
        path: '/analysis',
        name: 'Analysis',
        component: () => import('@/views/autotag/Analysis'),
        meta: { title: '结果分析', icon: 'monitor', keepAlive: true }
      }
    ]
  },
  {
    path: '*',
    redirect: '/404',
    hidden: true
  }
]

/**
 * 基础路由
 * @type { *[] }
 */
export const constantRouterMap = [
  {
    path: '/user',
    component: UserLayout,
    redirect: '/user/login',
    hidden: true,
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Login')
      },
      {
        path: 'register',
        name: 'register',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Register')
      },
      {
        path: 'register-result',
        name: 'registerResult',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/RegisterResult')
      },
      {
        path: 'recover',
        name: 'recover',
        component: undefined
      }
    ]
  },

  {
    path: '/404',
    component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404')
  }
]
