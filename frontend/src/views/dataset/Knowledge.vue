<template>
  <a-card>
    <a-tree show-line :tree-data="treeData" />
  </a-card>
</template>

<script>
  export default {
    name: 'Knowledge',
    data() {
      return {
        treeData: []
      }
    },
    methods: {
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
      this.$store.dispatch('getLabels')
    },
    watch: {
      '$store.getters.labels': {
        immediate: true,
        handler(list) {
          const temp = this.mapTreeData(list, '')
          this.treeData = temp
        }
      }
    }
  }
</script>

<style scoped></style>
