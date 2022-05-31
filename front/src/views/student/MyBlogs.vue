<template>
  <div class="MyBlogs">
    <div class="menu">
      <el-button class="el-icon-plus" type="primary" @click="prepareBlog">创建</el-button>
    </div>
    <div style="min-height: 400px;">
      <div v-for="(item) in blogTable" :key="item['blog_id']">
      <BlogEntrance :BlogData="item" @onDelete="onDelete">
      </BlogEntrance>
    </div>
    </div>
    <el-pagination layout="prev, pager, next,jumper" :total="blog_total" :hide-on-single-page="false"
      @current-change="handleCurrenChange"></el-pagination>
    <transition name="el-zoom-in-top">
      <BlogCreator v-if="this.$store.state.blogCreatorVisible" @submitSuccess="submitSuccess"></BlogCreator>
    </transition>

    <el-backtop target=".MyBlogs">Top</el-backtop>
  </div>
</template>

<script>
import BlogEntrance from "@/components/BlogEntrance.vue"

import BlogCreator from "@/components/BlogCreator.vue"
import config from "@/config.json"
import axios from "axios"
const server = config["server"]
export default {
  name: 'MyBlogs',
  data() {
    return {
      start: 0,
      blog_total: 0,
      blogTable:[],
      username:""
    }
  },
  created(){
    this.username=this.$store.state.username
    this.getBlogs()
  },
  components: {
    BlogEntrance,
    BlogCreator
  },
  methods: {
    prepareBlog() {
      this.$store.state.blogCreatorVisible = true;
    },
    getBlogs() {
      axios.get(server + "/student/get_blogs?username=" + this.username + "&start=0").then(res=>{
        this.blogTable=res.data["list"],
        this.blog_total=res.data["total"]
      })
    },
    submitSuccess() {
      this.start = 0
      this.blogTable = []
      this.start = 0;
      this.getBlogs()
    },
    handleCurrenChange(page) {
      this.start = (page - 1) * 10;
      this.end = this.start + 10;
      this.getBlogs()
    },
    onDelete(data){
      console.log(data);
      let index=this.blogTable.indexOf(data)
      this.blogTable.splice(index,1)
    },
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
  width: 100%;
  height: 70px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

/* 博客相关构造 */
</style>
