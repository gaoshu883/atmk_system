<template>
  <a-card title="数据预处理">
    <p>{{ demoData.text }}</p>
    <a-input-search style="width: 200px" placeholder="查询并下载字向量" @search="getCharVector" />
    <a-divider />
    <a-table :pagination="false" bordered :dataSource="demoData.formulas" :columns="columns">
      <template slot="action" slot-scope="name, record">
        <a href="javascript:;" @click="getFormulaVector(record)">下载</a>
      </template>
    </a-table>
  </a-card>
</template>
<script>
  import { getCleanResult, getVectorByType } from '@/api/system'
  import { downloadFile } from '@/utils/util'
  export default {
    name: 'Preprocess',
    data() {
      return {
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
            title: '向量',
            dataIndex: 'action',
            width: 80,
            scopedSlots: { customRender: 'action' }
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
      parseData(data) {
        const { text, formulas } = data.demo_data || {}
        const temp = Object.entries(formulas).map(([key, value]) => ({ key, value }))
        this.demoData = { text, formulas: temp }
      },
      getFormulaVector(record) {
        getVectorByType({
          ...record,
          type: 'formula'
        })
          .then((res) => {
            downloadFile(JSON.stringify(res.data), `${record.key}.json`)
          })
          .catch((error) => {
            console.log('getFormulaVector ...', error)
          })
      },
      getCharVector(value) {
        getVectorByType({
          type: 'char',
          value: value
        })
          .then((res) => {
            downloadFile(JSON.stringify(res.data), `${value}.json`)
          })
          .catch((error) => {
            console.log('getCharVector ...', error)
          })
      }
    },
    created() {
      this.getData()
    }
  }
</script>
