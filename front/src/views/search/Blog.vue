<template>
  <div>
    <div v-if="BlogList.length != 0">
      <BlogEntrance v-for="data in BlogList" :key="data['blog_id']" :BlogData="data"></BlogEntrance>
    </div>
    <el-empty v-else></el-empty>
    <el-pagination layout="prev, pager, next,jumper" :total="total" :hide-on-single-page="false" :page-size="10"
      @current-change="handleCurrenChange"></el-pagination>
  </div>
</template>

<script>
import BlogEntrance from '@/components/BlogEntrance.vue'
import axios from 'axios'
import config from "@/config.json"
export default {
  name: 'BlogView',
  data() {
    return {
      BlogList: [],
      total: 0
    }
  },
  components: {
    BlogEntrance
  },
  created() {
    this.start = this.$route.query["start"]
    this.text = this.$route.query["text"]
    this.getBlogs()
  },
  methods: {
    handleCurrenChange(page) {
      this.start = (page - 1) * 10
      this.getBlogs()
    },
    getBlogs() {
      axios.get(config["server"] + "/search/blog?text=" + this.text + "&start=" + this.start)
        .then(res => {
          console.log(res.data);
          this.BlogList = res.data["list"]
          this.total = res.data["total"]
        })
    }
  },
}

</script>
<style scoped>
</style>
