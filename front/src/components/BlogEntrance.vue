<template>
  <div>
    <el-card class="BlogEntrance">
      <div class="card_header">
        <div>
          <el-avatar :src="avatar"></el-avatar>
          <div style="display:inline-block;margin: 0 10px;">
            <div class="name">{{ nickname }}</div>
            <div class="identi">{{ identification }}</div>
          </div>
        </div>
        <div>
          <el-dropdown @command="handleCommand">
            <i class="el-icon-menu"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item v-show="!isOwner" command="report">举报</el-dropdown-item>
              <el-dropdown-item v-show="isOwner" command="edit">编辑</el-dropdown-item>
              <el-dropdown-item v-show="isOwner" command="delete">删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>

      </div>
      <router-link :to="BlogPage">
        <el-row style="width: 100%" :gutter="20">
          <el-col :span="8">
            <img class="cover" alt="" :src="cover" />
          </el-col>
          <el-col :span="16">
            <div class="title">{{ title }}</div>
            <div class="text">{{ content_text }}</div>
          </el-col>
        </el-row>
      </router-link>
      <div class="card_footer">
        <div>{{ post_time }}</div>
        <div>
          <el-button @click="like" type="text" style="width: 40px;height: 40px;margin: 0 10px;">
            <img :src="likedImg" class="like_img" v-if="liked" />
            <img :src="likeImg" class="like_img" v-else />
            <div>{{ liked_number }}</div>
          </el-button>
        </div>
      </div>
    </el-card>
    <el-dialog :visible.sync="dialogVisible">
      <el-form label-position="left" label-width="80px">
        <el-form-item label="博客标题">{{ title }}</el-form-item>
        <el-form-item label="举报理由">
          <el-input type="textarea" v-model="reason"></el-input>
        </el-form-item>
      </el-form>
      <div>
        <el-button type="danger" @click="submit">提交</el-button>
        <el-button @click="dialogVisible = false">取消</el-button>
      </div>
    </el-dialog>
    <transition name="el-zoom-in-top">
      <BlogEditorVue v-if="this.$store.state.blogEditorVisible" :BlogData="BlogData" @editSuccess="editSuccess"></BlogEditorVue>
    </transition>
  </div>
</template>

<script>
import config from "@/config.json"
import BlogEditorVue from "./BlogEditor.vue"
const server = config["server"]
import axios from "axios"
export default {
  name: 'BlogEntrance',
  components: { BlogEditorVue },
  props: ["BlogData"],
  data() {
    return {
      isOwner: false,
      blog_id: '',
      nickname: "",
      identification: "teacher",
      post_time: "2021-1-1",
      title: "测试标题",
      content_text: "测试简介",
      likeImg: require('/src/assets/like.svg'),
      likedImg: require('/src/assets/liked.svg'),
      liked: false,
      liked_number: 0,
      BlogPage: '',
      blog_owner_id: '',
      cover: "",
      avatar: "",
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
      username: '',
      dialogVisible: false,
      reason: "",
    }
  },
  created() {
    console.log(this.BlogData);
    this.nickname = this.BlogData["nickname"]
    this.name = this.BlogData["name"]
    this.identification = this.BlogData["identification"]
    this.post_time = this.BlogData["post_time"]
    this.title = this.BlogData["title"]
    this.content_text = this.BlogData["content_text"]
    this.liked_number = this.BlogData["liked_number"]
    this.blog_id = this.BlogData["blog_id"]
    this.BlogPage = "/blog?blog_id=" + this.BlogData["blog_id"]
    this.liked = this.BlogData["liked"]
    this.username = sessionStorage.getItem("username")
    this.blog_owner_id = this.BlogData["blog_owner_id"]
    this.cover = this.BlogData["cover"]
    this.isOwner = this.username === this.blog_owner_id
    this.avatar = this.avatarList[this.BlogData["avatar"]]
  },
  methods: {
    like() {
      console.log("like....");
      let username = sessionStorage.getItem("username")
      if (username) {
        let url = server + "/blog/like?blog_id=" + this.blog_id + "&username=" + username;
        axios.get(url)
          .then(res => {
            this.liked = res.data["state"]
            this.liked_number = res.data["count"]
          })
      } else {
        this.$alert("请先登录！！！")
      }
    },
    handleCommand(command) {
      switch (command) {
        case "report":
          if (this.username) {
            this.dialogVisible = true
          } else {
            this.$alert("请先登录！")
          }
          break;
        case "edit":
          this.$store.state.blogEditorVisible = true;
          break;
        case "delete":
          this.delete(this.BlogData["blog_id"])
          break;
        default:
          break;
      }
    },
    delete(id) {
      let url = server + "/blog/delete?blog_id=" + id
      axios.get(url).then(res => {
        if (res.data["type"] === "success") {
          this.$emit("onDelete", this.BlogData);
        }
        this.$message(res.data)

      })
    },
    submit() {
      let form = new FormData()
      let identi = sessionStorage.get("identification")
      form.append("blog_id", this.blog_id)
      form.append("reporter_id", this.username)
      form.append("identification", identi)
      axios.post(server + "/blog/report", form).then(() => {
        this.$message("待管理员审核后续")
        this.dialogVisible = false;
      })
    },
    editSuccess(blog){
      console.log(blog);
      this.title=blog['title']
      this.content_text=blog['content_text']
      this.post_time=blog['post_time']
      this.cover=blog["cover"]
    }
  },
}

</script>
<style scoped>
.BlogEntrance {
  margin: 10px auto;
  width: 80%;
  min-height: 200px;
}

.card_header {
  padding: 0;
  display: flex;
  justify-content: space-between;
}

.name {
  font-size: 20px;
  font-weight: 600;
  color: #282c34;
  text-align: left;
}

.identi {
  font-size: 16px;
  /* font-weight: 500; */
  color: #909399;
  text-align: left;
}

.cover {
  width: 100%;
  height: 150px;
  object-fit: contain;
}

.title {
  width: 100%;
  text-align: left;
  height: 40px;
  font-size: 20px;
  font-weight: 600;
  color: #282c34;
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 8;
  max-height: 110px;
  text-overflow: ellipsis;
}

.text {
  width: 100%;
  text-align: left;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 5;
  overflow: hidden;

}

.card_footer {
  display: flex;
  justify-content: space-between;
  margin: 5px auto;
  align-items: center;
}

.like_img {
  width: 20px;
  transition: 0.1s;
}

.like_img:hover {

  animation-name: change_statu;
  animation-duration: 0.3s;
  animation-iteration-count: 2;
  color: #fb7299;
}

@keyframes change_statu {
  0% {
    transform: rotate(15deg);
  }

  20% {
    transform: rotate(30deg);
  }

  40% {
    transform: rotate(45deg);
  }

  60% {
    transform: rotate(30deg);
  }

  80% {
    transform: rotate(15deg);
  }

  100% {
    transform: rotate(0deg);
  }
}
</style>
