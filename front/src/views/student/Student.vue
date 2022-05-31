<template>
  <div class="student-page">
    <el-container>
      <el-header height="190px">
        <img class="header-back" :src="header_back" />
        <div class="header-info">
          <div style="margin: 0 20px;display: flex;justify-content: flex-start;">
            <el-avatar :size="60" :src="this.$store.state.avatar"></el-avatar>
            <div style="margin-left:20px;">
              <div>
                <span class="name">{{ nickname }}</span>
                <el-tag type="success" effect="dark" style="margin:0 20px;">学生</el-tag>
              </div>
              <div>
                <!-- <div class="signature">{{signature}}</div> -->
                <!-- <el-input v-model="signature" @change="changeSignature" size="small" ></el-input> -->
                <input v-model="signature" @change="changeSignature" class="signature" />
              </div>
            </div>
          </div>
        </div>
      </el-header>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" active-text-color="#409eff" router>
        <el-menu-item index="/Student">班级列表</el-menu-item>
        <el-menu-item index="/Student/MyBlogs">博客</el-menu-item>
        <el-menu-item index="/Student/MyInfo">我的信息</el-menu-item>
        <el-menu-item>
          <el-input v-model="text" @keydown.enter.native="search">
            <template slot="append">
              <el-button class="el-icon-search" @click="search"></el-button>
            </template>
          </el-input>
        </el-menu-item>
      </el-menu>
      <div class="main">
        <router-view />
        <div>{{new Date().toLocaleDateString()}}</div>
      </div>
    </el-container>
  </div>
</template>

<script>
import config from "@/config.json"
import axios from "axios"
const server = config["server"]
export default {
  name: 'StudentView',
  data() {
    return {
      header_back: require("/src/assets/background.jpg"),
      username: "",
      name: "",
      activeIndex: "/Student",
      signature: "",
      text:'',
      nickname:""
    }
  },
  created() {
    if (this.$store.state.identification=="student") {
      console.log("已经登录");
      this.activeIndex=this.$route.path
      this.username=this.$store.state.username
    } else {
      this.$router.push("/")
    }
    axios.get(server+"/student/get_info?username="+this.username).then(res=>{
      this.name=res.data["name"]
      this.signature=res.data["signature"]
      this.nickname=res.data["nickname"]
    })
  },
  methods: {
    changeSignature() {
      let url = server + "/student/change_signature"
      let formdata = new FormData()
      formdata.append("username", this.username)
      formdata.append("signature", this.signature)
      axios.post(url, formdata).then(res => {
        console.log(res);
      })
    },
    search(){
      this.$router.push("/Student/SearchClass?text="+this.text)
    }
  },
  mounted() {
    this.name=this.$store.state.name
    this.avatar=this.$store.state.avatar
    this.signature=this.$store.state.signature
  }
}

</script>
<style scoped>
.student-page {
  width: 90%;
  min-width: 800px;
  margin: auto;
}

.el-header {
  background-color: #23272e;
  padding: 0;
  position: relative;
}

.header-back {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.el-main {
  overflow: hidden;
}

.header-info {
  position: absolute;
  bottom: 0;
  height: 70px;
  background-image: linear-gradient(#00000000, #000000);
  width: 100%;
  color: #ffffff;
  text-align: left;
}

.name {
  font-size: 18px;
  font-weight: 700;
}


.signature {
  width: 400px;
  color: #ffffff;
  height: 20px;
  border-radius: 3px;
  font-size: 12px;
  outline: none;
  border: none;
  background-color: #ffffff00;
  border: 1px solid #ffffff00;
  transition: 0.1s;
}

.signature:hover {
  background-color: #ffffff70;
  border: 1px solid #ffffff;
}

.signature:focus {
  background-color: #ffffff;
  color: #000000;
}

.header-menu {
  width: 100%;
  height: 50px;
  display: flex;
  justify-content: flex-start;
  background-color: #ffffff;
  box-shadow: 0 2px 4px 0 rgb(0 0 0 / 8%);
}

.main {
  width: 100%;
  margin-top: 10px;
  background-color: #ffffff;
  min-height: 500px;
}
</style>
