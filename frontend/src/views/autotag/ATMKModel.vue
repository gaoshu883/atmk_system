<template>
  <div>
    <a-card title="数据预处理">
      <a-form layout="inline">
        <a-form-item label="文本切分类型">
          <a-select v-model="textType" style="width: 100px">
            <a-select-option value="word"> word </a-select-option>
            <a-select-option value="char"> char </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="文本预训练向量版本">
          <a-select v-model="textVersion" style="width: 100px">
            <a-select-option value="atmk"> atmk </a-select-option>
            <a-select-option value="baidu"> baidu </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="公式预训练向量版本">
          <a-select v-model="formulaVersion" style="width: 100px">
            <a-select-option value="atmk"> atmk </a-select-option>
            <a-select-option value="wiki"> wiki </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="preprocess" :loading="loading">准备测试集、验证集、测试集</a-button>
          <p>
            数据集：<a-tag>{{ filenames.math_data }}</a-tag> 词表：<a-tag>{{ filenames.vocab_label }}</a-tag>
            词向量：<a-tag>{{ filenames.embeddings }}</a-tag>
          </p>
        </a-form-item>
      </a-form>
    </a-card>
    <br />
    <a-card title="模型训练">
      <a-button type="primary" style="width: 100px">操作</a-button>
    </a-card>
  </div>
</template>
<script>
  import { postDataPrecess } from '@/api/system'
  export default {
    name: 'ATMKModel',
    data() {
      return {
        loading: false,
        textType: 'word',
        textVersion: 'atmk',
        formulaVersion: 'atmk',
        filenames: {}
      }
    },
    methods: {
      preprocess() {
        this.loading = true
        postDataPrecess({
          text_type: this.textType,
          text_version: this.textVersion,
          formula_version: this.formulaVersion
        })
          .then((res) => {
            console.log(res)
            Object.assign(this.filenames, res.data)
            this.$message.success('操作成功！')
          })
          .catch((error) => {
            console.log('postDataPrecess ...', error)
          })
          .finally(() => {
            this.loading = false
          })
      }
    },
    created() {
      this.preprocess()
    }
  }
</script>
