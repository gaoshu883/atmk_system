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
      <template slot="action">
        <a href="">test action</a>
      </template>
    </a-table>
  </a-card>
</template>

<script>
  import { getMathContent } from '@/api/system'
  export default {
    name: 'Question',
    data() {
      return {
        loading: false,
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
            dataIndex: 'label'
          },
          {
            title: '操作',
            dataIndex: 'action',
            scopedSlots: { customRender: 'action' }
          }
        ],
        data: [],
        pagination: {
          pageSize: 20,
          current: 1,
          total: 0
        }
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
      }
    },
    created() {
      this.getData()
    }
  }
</script>

<style scoped>
</style>
