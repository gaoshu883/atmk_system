<template>
  <a-card>
    <a-tree show-line :tree-data="treeData" />
  </a-card>
</template>

<script>
  import { getMathKnowledge } from '@/api/system'
  export default {
    name: 'Knowledge',
    data() {
      return {
        treeData: []
      }
    },
    methods: {
      getData() {
        getMathKnowledge()
          .then((res) => {
            const temp = this.mapTreeData(res.data, '')
            this.treeData = temp
          })
          .catch((error) => {
            console.log('getMathKnowledge error', error)
          })
      },
      mapTreeData(list, pid) {
        const children = []
        list
          .filter((item) => item.parent_uuid === pid)
          .forEach((item) => {
            const ret = {
              title: item.name,
              key: item.uuid
            }
            const subChild = this.mapTreeData(list, item.uuid)
            if (subChild.length > 0) ret.children = subChild
            children.push(ret)
          })
        return children
      }
    },
    created() {
      this.getData()
    }
  }
</script>

<style scoped></style>
