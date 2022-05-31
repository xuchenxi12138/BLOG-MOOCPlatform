<template>
 <div>
     <el-result icon="error" title="错误提示" subTitle="找不到服务器">
      <template slot="extra">
        <!-- <el-button type="primary" size="medium">返回</el-button> -->
      </template>
    </el-result>
 </div>
</template>

<script>
export default {
  name:'NoConnection',
  data () {
    return {
    }
  },
  created(){
      
  },
  methods:{
  },
}

</script>
<style scoped>
</style>
