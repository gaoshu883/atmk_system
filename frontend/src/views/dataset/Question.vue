<template>
  <a-card>
    <a-table
      :loading="loading"
      rowKey="id"
      :columns="columns"
      :data-source="data"
      :pagination="pagination"
      @change="onTableChange"
    >
      <template slot="action" slot-scope="name, record">
        <a href="javascript:;" @click="openTag(record)">知识点标记</a>
      </template>
    </a-table>

    <a-modal width="80%" title="知识点标记" v-model="visible" @ok="handleSubmit" :confirmLoading="pending">
      <p><img :src="question.label_img" alt="知识点图片" /></p>
      <a-select
        mode="multiple"
        style="width: 100%"
        placeholder="请选择知识点"
        :filter-option="false"
        v-model="question.labels"
        @search="searchLabels"
        :not-found-content="fetching ? undefined : null"
      >
        <a-spin v-if="fetching" slot="notFoundContent" size="small" />
        <a-select-option v-for="item in filterLabels" :key="item.uuid" :value="item.id">
          {{ item.name }}
        </a-select-option>
      </a-select>
    </a-modal>
  </a-card>
</template>

<script>
  import { getMathContent, tagQuestion } from '@/api/system'
  import debounce from 'lodash.debounce'
  import cloneDeep from 'lodash.clonedeep'
  export default {
    name: 'Question',
    data() {
      this.searchLabels = debounce(this.searchLabels, 800)
      return {
        visible: false,
        loading: false,
        pending: false,
        fetching: false,
        searchKey: '',
        columns: [
          {
            title: '序号',
            dataIndex: 'id',
            width: '10%'
          },
          {
            title: '题目',
            dataIndex: 'text',
            width: '50%',
            customRender: (text) => (
              <div
                {...{
                  domProps: {
                    innerHTML: unescape(text)
                  }
                }}
              ></div>
            )
          },
          {
            title: '知识点',
            dataIndex: 'labels',
            customRender: (list) => {
              return (
                <div>
                  {list.map((item) => (
                    <a-tag>{this.getLabelName(item)}</a-tag>
                  ))}
                </div>
              )
            }
          },
          {
            title: '操作',
            dataIndex: 'action',
            width: 150,
            scopedSlots: { customRender: 'action' }
          }
        ],
        data: [],
        question: {
          label_img: '',
          labels: []
        },
        pagination: {
          pageSize: 20,
          current: 1,
          total: 0
        }
      }
    },
    computed: {
      filterLabels() {
        const { labels } = this.$store.getters
        const { searchKey, question } = this
        let data = []
        if (searchKey === '') {
          data = labels.filter((item) => question.labels.includes(item.id))
        } else {
          data = labels.filter((item) => item.name.includes(this.searchKey))
        }
        return data
      }
    },
    methods: {
      getData() {
        this.loading = true
        const { current, pageSize } = this.pagination
        getMathContent({
          page: current,
          size: pageSize
        })
          .then((res) => {
            this.data = res.data.data
            this.pagination.total = res.data.count
          })
          .catch((error) => {
            console.log('getMathContent error', error)
          })
          .finally(() => {
            this.loading = false
          })
      },
      onTableChange(pagination) {
        this.pagination = pagination
        this.getData()
      },
      openTag(record) {
        this.visible = true
        this.searchKey = ''
        this.question = cloneDeep(record)
      },
      // 确认知识点标注
      handleSubmit() {
        this.pending = true
        const { id, labels } = this.question
        tagQuestion({ id, labels })
          .then((res) => {
            this.pending = false
            this.visible = false
            const item = this.data.find((item) => item.id === id)
            if (item) {
              item.labels = labels
            }
          })
          .catch((error) => {
            this.pending = false
            console.log('tagQuestion ...', error)
          })
      },
      searchLabels(value) {
        this.searchKey = value
      },
      getLabelName(id) {
        const { labels } = this.$store.getters
        const item = labels.find((item) => item.id === id)
        if (item) {
          return item.name
        } else {
          return id
        }
      }
    },
    created() {
      this.getData()
      this.$store.dispatch('getLabels')
    }
  }
</script>

<style scoped>
</style>
