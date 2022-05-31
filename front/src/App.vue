<template>
  <div id="app">
    <el-container>
      <el-header>
        <Header></Header>
      </el-header>
      <el-main style="padding: 0;">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>
<script>
import Header from "@/components/Header"
import config from "@/config.json"
import axios from "axios"
export default {
  name: 'app',
  components: {
    Header
  },
  data() {
    return {
      // server:config["server"]
    }
  },
  created() {
    axios.get(config["server"]).then(res=>{
          console.log(res.data);
      }).catch(()=>{
          // this.$router.push("/NoConnection")
      })
    document.title="数据库原理示范教学平台"
  },
  methods: {
  },
}
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background:linear-gradient(#fafafa,#f4f4f4,#efefef);
  min-height: 100vh;
}



.el-header {
  box-shadow: 0 2px 4px 0 #00000050;
  background-color: #ffffff;
}

.el-footer {
  box-shadow: 0 -2px 4px 0 rgb(0 0 0 / 8%);
  background-color: #282c34;
  color: #ffffff;
}
.el-footer a{
  width: 100%;
  text-align: left;
  
}
.el-main {
  height: 600px;
  overflow: auto;
  position: relative;
}
</style>
