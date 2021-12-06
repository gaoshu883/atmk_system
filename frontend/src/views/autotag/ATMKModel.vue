<template>
  <div>
    <a-card title="数据平衡">
      <a-alert message="目标" type="info">
        <ul slot="description">
          <li>把题目分布较少的标签去掉</li>
          <li>把太短文本的题目清洗掉</li>
        </ul>
      </a-alert>
      <br />
      <a-button type="primary" style="width: 100px">操作</a-button>
    </a-card>
  </div>
</template>
<script>
  export default {
    name: 'ATMKModel'
  }
</script>
