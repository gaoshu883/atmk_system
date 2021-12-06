<template>
  <div>
    <a-card title="数据清洗">
      <a-alert message="清洗的内容" type="info">
        <ul slot="description">
          <li>所有的空字符，包括空格、换行(\n)、制表符(\t)等</li>
          <li>题号、选项序号：1、(1)、A、</li>
          <li>用于显示答案位置的括号（）</li>
          <li>一些标签：table、input、img、.exam-foot</li>
          <li>没有标签的题目</li>
          <li>重复的题目</li>
        </ul>
      </a-alert>
      <br />
      <a-alert message="数学表达式用特殊模式替换，提供模式与数学表达式的映射" />
      <br />
      <p>
        <a-tag color="green">{{ fileName }}</a-tag>
        <span>
          清洗于：<strong>{{ updatedAt }}</strong>
        </span>
        <span>（清洗时间~5min）</span>
      </p>
      <p>
        <a-button type="primary" style="width: 100px" @click="cleanData" :loading="pending">清洗</a-button>
      </p>
      <br />
      <a-card title="示例" size="small">
        <p>{{ demoData.text }}</p>
        <a-table :pagination="false" bordered :dataSource="demoData.formulas" :columns="columns" />
      </a-card>
    </a-card>
  </div>
</template>
<script>
  import { getCleanResult, postCleanData } from '@/api/system'
  import moment from 'moment'
  export default {
    name: 'DataClean',
    data() {
      return {
        pending: false,
        updatedAt: 'null',
        fileName: '暂无文件',
        demoData: {
          text: '',
          formulas: []
        },
        columns: [
          {
            title: '模式',
            dataIndex: 'key',
            key: 'key',
            width: 200
          },
          {
            title: '公式',
            dataIndex: 'value',
            key: 'value'
          },
          {
            title: '解析',
            dataIndex: 'value',
            key: 'formula',
            width: '20%',
            customRender: (text) => (
              <div
                {...{
                  domProps: {
                    innerHTML: text
                  }
                }}
              ></div>
            )
          }
        ]
      }
    },
    methods: {
      getData() {
        getCleanResult()
          .then((res) => {
            const data = res.data
            if (data.file_name) this.parseData(data)
          })
          .catch((error) => {
            console.log(error, 'getCleanResult...')
          })
      },
      cleanData() {
        this.pending = true
        postCleanData()
          .then((res) => {
            this.parseData(res.data)
          })
          .catch((error) => {
            console.log('postCleanData ...', error)
          })
          .finally(() => {
            this.pending = false
          })
      },
      parseData(data) {
        const { text, formulas } = data.demo_data || {}
        const temp = Object.entries(formulas).map(([key, value]) => ({ key, value }))
        Object.assign(this, {
          fileName: data.file_name,
          demoData: { text, formulas: temp },
          updatedAt: moment(data.updated_at * 1000).format('YYYY-MM-DD HH:mm:ss')
        })
      }
    },
    created() {
      this.getData()
    }
  }
</script>
