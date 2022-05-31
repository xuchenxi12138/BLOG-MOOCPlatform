<template>
  <div class="MyBlogs" v-infinite-scroll="getMore">
    <div v-for="(item) in blogTable" :key="item['blog_id']">
      <BlogEntrance :BlogData="item" @onDelete="onDelete">
      </BlogEntrance>
    </div>
    <p style="text-align:center" v-if="loading">加载中...<i class="el-icon-loading"></i></p>
    <p style="text-align:center" v-else>没有更多了...</p>
    <div class="menu">
      <el-button class="el-icon-plus" type="primary" @click="prepareBlog">创建</el-button>
    </div>
    <transition name="el-zoom-in-top">
      <BlogCreator v-if="this.$store.state.blogVisible" @submitSuccess="submitSuccess"></BlogCreator>
    </transition>

    <el-backtop target=".MyBlogs">Top</el-backtop>
  </div>
</template>

<script>
import BlogEntrance from "@/components/BlogEntrance.vue"
// import axios from "axios"
import config from "@/config.json"
import BlogCreator from "@/components/BlogCreator.vue"
import axios from "axios"
const server = config["server"]
export default {
  name: 'MyBlogs',
  components: {
    BlogEntrance,
    BlogCreator
  },
  data() {
    return {
      blog: {
        cover: ''
      },
      finished: false,
      loading: true,
      blogTable: [],
      username: '',
      start: 0,
      dialogVisible: false,
      editor: null,
      uploadCoverUrl: server + "/file/uploadOneImage"
    }
  },
  created() {
    this.username = sessionStorage.getItem("username")
    this.start = 0
    this.getBlogs()
  },
  methods: {
    prepareBlog() {
      this.$store.state.blogCreatorVisible = true;
    },
    getBlogs() {
      let url = server + "/teacher/get_blogs?username=" + this.username + "&start=" + this.start
      axios.get(url).then(res => {
        // this.blogTable = res.data
        if (res.data["message"] === "nomore") {
          // this.$message("已经全部加载完了...")
          this.finished = true
          this.loading=false
        } else {
          let arr = res.data
          for (let item of arr) {
            this.blogTable.push(item)
          }
          this.loading = false
        }
      })
    },
    getMore() {
      if (!this.finished) {
        this.loading = true
        this.start += 5
        this.getBlogs()
      }
      else{
        this.loading=false
      }
    },
    onDelete(data){
      console.log(data);
      let index=this.blogTable.indexOf(data)
      this.blogTable.splice(index,1)
    },
    submitSuccess(){
    this.start=0
    this.blogTable=[]
    this.getBlogs()
    }
  }

}

</script>
<style scoped>
.MyBlogs {
  width: 100%;
  height: 100%;
  overflow: auto;
  position: relative;
}

.menu {
  position: fixed;
  top: 100px;
  right: 50px;
}

/* 博客相关构造 */
</style>
