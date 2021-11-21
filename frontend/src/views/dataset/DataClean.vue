<template>
  <div>
    <a-card title="数据清洗">
      <a-alert message="清洗的内容" type="info">
        <ul slot="description">
          <li>所有的空字符，包括空格、换行(\n)、制表符(\t)等</li>
          <li>题号、选项序号：1、(1)、A、</li>
          <li>用于显示答案位置的括号（）</li>
          <li>一些标签：table、input、img、.exam-foot</li>
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
        <span>（清洗时间~1.6min）</span>
      </p>
      <p>
        <a-button type="primary" style="width: 100px" @click="cleanData" :loading="pending">清洗</a-button>
      </p>
      <br />
      <a-card title="示例" size="small">
        <p>题目：{{ demoData.text }}</p>
        <a-table :pagination="false" bordered :dataSource="demoData.formulas" :columns="columns" />
      </a-card>
    </a-card>
    <br />
    <a-card title="数据分析">
      <a-descriptions bordered>
        <a-descriptions-item label="题目数量">{{ result.q_count }}</a-descriptions-item>
        <a-descriptions-item label="标签数量"> {{}} </a-descriptions-item>
        <a-descriptions-item label="平均标签数量">{{}}</a-descriptions-item>
        <a-descriptions-item label="标签排序">
          <a-table :pagination="false" bordered :dataSource="result.list" :columns="labelColumns" />
          <!-- TODO 柱状图 -->
        </a-descriptions-item>
      </a-descriptions>
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
        ],
        result: {
          list: []
        },
        labelColumns: [
          {
            title: '标签序号',
            dataIndex: 'id'
          },
          {
            title: '标签',
            dataIndex: 'name'
          },
          {
            title: '标记次数',
            dataIndex: 'num'
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
          result: data.analysis,
          updatedAt: moment(data.updated_at * 1000).format('YYYY-MM-DD HH:mm:ss')
        })
      }
    },
    created() {
      this.getData()
    }
  }
</script>
