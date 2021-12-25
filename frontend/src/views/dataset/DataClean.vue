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
          <li>数学表达式用特殊模式替换，提供模式与数学表达式的映射</li>
          <li>清洗掉标记数少于 <a-input-number v-model="tagNum" :min="0" /> 的知识点</li>
          <li>清洗掉字符数少于 <a-input-number v-model="charNum" :min="0" /> 的题目</li>
        </ul>
      </a-alert>
      <br />
      <p>
        <a-button type="primary" style="width: 100px" @click="cleanData" :loading="pending">清洗</a-button>
      </p>
      <p>
        <a-tag color="green">{{ fileName }}</a-tag>
        <span>
          清洗于：<strong>{{ updatedAt }}</strong>
        </span>
        <span>（清洗时间~5min）</span>
      </p>
      <br />
      <a-card title="示例" size="small" :loading="loading">
        <p>题目：{{ demoData.text }}</p>
        <p>
          知识点：<a-tag v-for="item in demoData.labels" :key="item">{{ getLabelName(item) }} </a-tag>
        </p>
        <a-table :pagination="false" bordered :dataSource="demoData.formulas" :columns="columns">
          <template slot="action" slot-scope="text, record">
            <a href="javascript:;" @click="onClick(record)">解析</a>
          </template>
        </a-table>
      </a-card>
    </a-card>
  </div>
</template>
<script>
  /*  eslint-disable camelcase  */
  import { getCleanResult, postCleanData, parseFormula } from '@/api/system'
  import { labelMixin } from '@/store/dataset-mixin'
  import moment from 'moment'
  export default {
    name: 'DataClean',
    data() {
      return {
        pending: false,
        loading: false,
        updatedAt: 'null',
        fileName: '暂无文件',
        tagNum: 5,
        charNum: 5,
        demoData: {
          text: '',
          formulas: [],
          labels: []
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
            title: '渲染',
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
          },
          {
            title: '操作',
            dataIndex: 'action',
            width: 150,
            scopedSlots: { customRender: 'action' }
          }
        ]
      }
    },
    mixins: [labelMixin],
    methods: {
      getData() {
        this.loading = true
        getCleanResult()
          .then((res) => {
            const data = res.data
            if (data.file_name) this.parseData(data)
          })
          .catch((error) => {
            console.log(error, 'getCleanResult...')
          })
          .finally(() => {
            this.loading = false
          })
      },
      cleanData() {
        this.pending = true
        postCleanData({
          tag_min: this.tagNum,
          char_min: this.charNum
        })
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
        const { text, formulas, label_list } = data.demo_data || {}
        const temp = Object.entries(formulas).map(([key, value]) => ({ key, value }))
        Object.assign(this, {
          fileName: data.file_name,
          demoData: { text, formulas: temp, labels: label_list },
          updatedAt: moment(data.updated_at * 1000).format('YYYY-MM-DD HH:mm:ss')
        })
      },
      onClick(record) {
        parseFormula({
          cond: [
            {
              key: record.key,
              content: record.value
            }
          ]
        })
          .then((res) => {
            this.$info({
              content: JSON.stringify(res.data)
            })
          })
          .catch((error) => {
            console.log('parseFormula', error)
          })
      }
    },
    created() {
      this.getData()
    }
  }
</script>
