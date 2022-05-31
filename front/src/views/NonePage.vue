<template>
  <div class="none-page">
    <i class="el-icon-question" style="font-size: 100px;"></i>
    <a style="color: #F56C6C">{{errorPath}}</a>
    <p>这个页面不存在哦!</p>
    <p style="font-size: 20px;">This page does not exist!</p>
  </div>
</template>

<script>
export default {
  name: "NonePage",
  data(){
    return{
      errorPath:''
    }
  },
  created(){
    this.errorPath=""+this.$route.fullPath;
    // console.log(this.$route)
  }
}
</script>

<style scoped>
.none-page{
  height: 100vh;
  width: 100%;
  color: #F56C6C;
  font-size: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>