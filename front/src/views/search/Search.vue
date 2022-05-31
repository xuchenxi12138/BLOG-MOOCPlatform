<template>
  <div class="search">
    <nav>
      <router-link :to="blog_url">博客</router-link>
      <router-link :to="lesson_url">课程</router-link>
    </nav>
    <div class="main">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchView',
  data() {
    return {
      text: "",
      activeIndex: "/Search/Blog",
      lesson_url: "",
      blog_url: "",
      start: 0
    }
  },
  created() {
    this.activeIndex = this.$route.fullPath
    this.text = this.$route.query["text"]
    this.start = this.$route.query["start"]
    if(!this.start)
    this.start=0
    this.blog_url = "/Search/Blog?text=" + this.text + "&start=" + this.start
    this.lesson_url = "/Search/Lesson?text=" + this.text + "&start=" + this.start
  },
  methods: {
  },
  watch: {
    $route() {
      location.reload()
    }
  }
}

</script>
<style scoped>
.search {
  width: 1000px;
  margin: 10px auto;
}

.main {
  width: 100%;
  min-height: 50vh;
  margin: 10px auto;
  background-color: #ffffff;
  border: 1px solid #cccccc;
}
nav{
  width: 100%;
  height: 50px;
  background-color: #ffffff;
  display: flex;
  justify-content: flex-start;
}
nav a {
  font-size: 24px;
  font-weight: bold;
  color: #2c313c;
  text-decoration: none;
  width: 100px;
  height: 50px;
  line-height: 50px;
  
}

nav a.router-link-exact-active {
  color: #42b983;
  border-bottom: 2px solid #42b983;
}
</style>
