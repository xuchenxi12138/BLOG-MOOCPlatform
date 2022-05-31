<template>
 <div class="login">
     <img :src="background" class="background_image">
     <div class="main">
       <h1>数据库示范教学平台教学</h1>
     </div>
 </div>
</template>

<script>
export default {
  name:'LogIn',
  data () {
    return {
        background:require("@/assets/database.webp")
    }
  },
  created(){
  },
  methods:{
  },
}

</script>
<style scoped>
.login{
    width: 100%;
    height: 100vh;

}
.background_image{
    position: fixed;
    top:0;
    left: 0;
    width: 100%;
    height: 100%;
}
.main{
    position: fixed;
    top:0;
    left: 0;
    width: 100%;
    height: 100%;
    color: #fff;
    z-index: 1;
    background-color: #00000080;
}
</style>
