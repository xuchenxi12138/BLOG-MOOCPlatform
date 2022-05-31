<template>
  <div class="page">
    <div class="blog">
      <div class="blog-user-info">
        <div style="display:flex;height: 50px;">
          <el-avatar :src="avatar"></el-avatar>
          <div style="line-height: 20px;margin: auto 10px;">
            <div class="blog-user-info-name">{{ blog_owner_name }}</div>
            <div class="blog-user-info-identification">{{ identification }}</div>
          </div>
        </div>
      </div>
      <div class="blog_main">
        <div class="header">
          <div style="width: 90%;margin: auto;text-align: left">
            <p class="title">{{ title }}</p>
            <div>
              <el-tag type="success" style="margin: auto 5px;" v-for="tag in tags" :key="tag">{{tag}}</el-tag>
            </div>
            <div class="blog-info">
              <span>
                <!-- {{tag}} -->
              </span>
              <span>
                {{ post_time }}
              </span>
              <span>
                {{ liked_number }}喜欢
              </span>
              <!-- <el-dropdown :command="operate" v-if="username == blog_owner_id">
                <el-button type="text">
                  操作<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="edit">编辑</el-dropdown-item>
                  <el-dropdown-item command="delete">删除</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown> -->
            </div>
          </div>

        </div>
        <div class="main">
          <div class="cover_div">
            <el-empty v-if="!cover" description="没有设置封面哦"></el-empty>
            <img :src="cover" v-else />
          </div>
          <h1>正文</h1>
          <div class="blog_content">
            <div v-html="content_html"></div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BlogView",
  data() {
    return {
      avatar: '',
      title: '',
      tag: '',
      readNumber: 1000,
      liked_number: 500,
      commentNumber: 100,
      blog_id: '',
      post_time: '',
      blog_owner_name: '',
      blog_owner_id: '',
      identification: '',
      content_html: '',
      cover: '',
      avatarList: {
        "boy.svg": require("/src/assets/Avatars/boy.svg"),
        "cat.png": require("/src/assets/Avatars/cat.png"),
        "doctor.svg": require("/src/assets/Avatars/doctor.svg"),
        "dog.svg": require("/src/assets/Avatars/dog.svg"),
        "girl.svg": require("/src/assets/Avatars/girl.svg"),
        "github.svg": require("/src/assets/Avatars/github.svg"),
        "men.svg": require("/src/assets/Avatars/men.svg"),
        "women.svg": require("/src/assets/Avatars/women.svg"),
      },
      coverImageStyle: false,
      username: "",
      tags:[]
    }
  },
  created() {
    this.blog_id = this.$route.query['blog_id']
    this.username = sessionStorage.getItem("username")
    let url = "http://localhost:5000/blog/get?blog_id=" + this.blog_id + "&username=" + this.username;
    axios.get(url).then(
      res => {
        this.title = res.data["title"]
        this.post_time = res.data["post_time"]
        this.blog_owner_name = res.data["blog_owner_name"]
        this.identification = res.data["identification"]
        this.avatar = this.avatarList[res.data["avatar"]]
        this.content_html = res.data["content_html"]
        this.liked_number = res.data["liked_number"]
        this.cover = res.data["cover"]
        this.blog_owner_id = res.data["blog_owner_id"]
        this.tags=JSON.parse(res.data["tags"])
      }
    )
  },
  mounted() {

  },
  methods: {
    operate(choice) {
      switch (choice) {
        case "edit":

          break;
        case "delete":

          break;
        default:
          break;
      }
    }
  }
}
</script>

<style scoped>
.page {
  height: 100%;
  width: 100%;
  overflow: auto;
}

.blog {
  width: 1000px;
  margin: auto;
  display: flex;
}

.header {
  width: 100%;
  background-color: #ffffff;
  padding-top: 1px;
  border-radius: 5px;
}

.blog-info {
  font-size: 14px;
  color: #99a9bf;
  
}

.blog-info span {
  margin: auto 10px;
}

.title {
  font-weight: 700;
  font-size: 24px;
  color: #2F2C4E;
}

.blog-user-info {
  margin: 10px auto;
  width: 300px;
  background-color: #ffffff;
  padding: 10px;
  margin-right:10px ;
  border-radius: 3px;
  box-shadow: 0 0 2px 1px #aaaaaa;
  /*align-content: space-between;*/
}

.blog-user-info-name {
  color: #409EFF;
  font-size: 18px;
  font-weight: 700;
}

.blog-user-info-identification {
  color: #909399;
  font-size: 14px;
}
.blog_main{
  border-radius: 5px;
  box-shadow: 0 0 5px 1px #aaaaaa;
  margin: 10px auto;
  width: 100%;
}
.main {
  width: 100%;
  border-top: 1px solid #cccccc;
  background-color: #ffffff;
  padding-top: 1px;
}

.blog_content {
  padding: 10px;
  text-align: left;
  word-break: break-all;
}

.cover_div {
  width: 90%;
  /* height: 250px; */
  overflow: hidden;
  margin: 10px auto;
  box-shadow: 0 0 5px 1px #00000080;
}

.higherCover {
  width: 100%;
  margin: 5px;
  border-radius: 10px;
  transition: 0.1s;
}

.higherCover:hover {
  width: 105%;
  cursor: pointer;
}

.widerCover {
  height: 100%;
  margin: 5px;
  border-radius: 10px;
  transition: 0.1s;
}

.widerCover:hover {
  height: 105%;
  cursor: pointer;
}
.cover_div img{
  width: 100%;
  display: block;
}
.cover_div img:hover {
  box-shadow: 0 0 10px 0px #1e1e1e50;
}
</style>