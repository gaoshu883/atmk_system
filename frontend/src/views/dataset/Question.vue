<template>
  <div>Question</div>
</template>

<script>
  import { getMathContent } from '@/api/system'
  export default {
    name: 'Question',
    methods: {
      getData() {
        getMathContent()
          .then((res) => {
            console.log(res)
          })
          .catch((error) => {
            console.log('getMathContent error', error)
          })
      }
    },
    created() {
      this.getData()
    }
  }
</script>

<style scoped>
</style>
