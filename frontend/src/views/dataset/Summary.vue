<template>
  <div>
    <a-card title="数据分析">
      <a-button type="primary" style="width: 100px" @click="handleClick" :loading="loading">开始分析</a-button>
      <br />
      <br />
      <a-descriptions bordered layout="vertical" :column="4">
        <a-descriptions-item label="题目数量" :span="4">{{ question.count }}</a-descriptions-item>
        <a-descriptions-item label="题目平均字数"> {{ question.avg_char }} </a-descriptions-item>
        <a-descriptions-item label="题目平均词数"> {{ question.avg_word }} </a-descriptions-item>
        <a-descriptions-item label="题目平均公式数"> {{ question.avg_formula }} </a-descriptions-item>
        <a-descriptions-item label="题目平均知识点数"> {{ question.avg_label }} </a-descriptions-item>
        <a-descriptions-item label="标签数量" :span="2"> {{ label.count }} </a-descriptions-item>
        <a-descriptions-item label="标签平均标记数" :span="2"> {{ label.avg_tag }} </a-descriptions-item>
        <a-descriptions-item label="标签排序" :span="4">
          <a-table rowKey="id" bordered :dataSource="labelTags" :columns="labelColumns" />
          <!-- TODO 柱状图 -->
        </a-descriptions-item>
      </a-descriptions>
    </a-card>
  </div>
</template>
<script>
  import { getDataSummary } from '@/api/system'
  import { labelMixin } from '@/store/dataset-mixin'
  export default {
    name: 'Summary',
    data() {
      return {
        loading: false,
        question: {},
        label: {},
        labelTags: []
      }
    },
    computed: {
      labelColumns() {
        const columns = [
          {
            title: '序号',
            dataIndex: 'id'
          },
          {
            title: '知识点',
            key: 'name',
            customRender: (text, record) => this.getLabelName(record.id)
          },
          {
            title: '标记次数',
            dataIndex: 'num'
          }
        ]

        return columns
      }
    },
    mixins: [labelMixin],
    methods: {
      handleClick() {
        this.loading = true
        getDataSummary()
          .then((res) => {
            const data = res.data
            const { question, label } = data
            this.question = question
            this.label = label
            this.formatTags(data.label_tags)
          })
          .catch((error) => {
            console.log('getDataSummary', error)
          })
          .finally(() => {
            this.loading = false
          })
      },
      formatTags(tagRet) {
        const temp = Object.entries(tagRet)
          .map((item) => ({ id: Number(item[0]), num: item[1] }))
          .sort((a, b) => b.num - a.num)

        this.labelTags = temp
      }
    }
  }
</script>
