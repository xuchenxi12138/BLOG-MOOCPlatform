<template>
  <div class="home">
    <!-- <div class="carousel">
      <el-carousel trigger="click" height="500" style="border-radius: 5px;">
        <el-carousel-item v-for="(item, index) in carousel" :key="index">
          <a class="img__container" :href="item['url']">
            <img :src="item['cover_url']" alt="" style="width: 100%;height: 100%;object-fit: contain;">
          </a>
        </el-carousel-item>
      </el-carousel>
    </div>
    <div class="main">
      <div :class="lesson_div">
        <div v-for="item in lesson_list" :key="item.lesson_id" :class="entrance_style">
          <LessonEntrance :LessonData="item"></LessonEntrance>
        </div>
      </div>
    </div> -->
    <img :src="background" class="background" />
    <div style="z-index: 1;">
      <h1>数据库原理示范教学平台</h1>
      <div class="search_div">
        <input v-model="text" @keydown.enter="search" />
        <el-button type="success" @click="search">搜索</el-button>
      </div>
    </div>

    <br><br>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios"
import config from "@/config.json"
// import LessonEntrance from "@/components/LessonEntrance.vue"
export default {
  name: 'HomeView',
  data() {
    return {
      carousel: [1, 2, 3, 4],
      lesson_list: [],
      lesson_div: "lesson_div_1",
      entrance_style: "entrance_style_1",
      text: "",
      logo: require("/src/assets/logo.png"),
      background: require("/src/assets/background3.png")
    }
  },
  components: {
    // LessonEntrance
  },
  created() {
    axios.get(config["server"] + "/home/get_start").then(res => {
      console.log(res.data);
      let data = res.data['recommend_list']
      for (let item of data) {
        if (item["cover_url"]) {
          item["cover_url"] = config["server"] + "/file/image/" + item["cover_url"]
        }
      }
      this.carousel = data
      this.lesson_list = res.data["lesson_list"]
    })
  },
  methods: {
    search() {
      if (this.text) {
        let url = "/Search/Blog?text=" + this.text + "&start=0"
        this.$router.push(url)
        // location.reload()
      }
    }
  },
  mounted() {
    window.onresize = () => {
      return (() => {
        if (document.body.clientWidth > 1000) {
          this.lesson_div = "lesson_div_1"
          this.entrance_style = "entrance_style_1"
        }
        else if (document.body.clientWidth > 800 && document.body.clientWidth < 1000) {
          this.lesson_div = "lesson_div_2"
          this.entrance_style = "entrance_style_2"
        }
        else if (document.body.clientWidth > 600 && document.body.clientWidth < 800) {
          this.lesson_div = "lesson_div_3"
          this.entrance_style = "entrance_style_3"
        }
        else if (document.body.clientWidth < 600) {
          this.lesson_div = "lesson_div_4"
          this.entrance_style = "entrance_style_4"
        }
      })()
    }
  }
}
</script>
<style scoped>
.home {
  width: 100%;
  max-width: 1000px;
  margin: auto;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.carousel {
  width: 100%;
  /*padding: 40%;*/
  max-width: 1000px;
  box-shadow: 0 0 5px 1px #000000;
  border-radius: 5px;
  background-color: #ffffff;
}

.main {
  padding-top: 10px;
  width: 100%;
  /* min-height: 120vh; */
  margin: 10px auto auto auto;
  box-shadow: 0 0 5px 1px #000000;
  border-radius: 5px;
  background-color: #ffffff;
}

.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}

.lesson_div_1 {
  width: 100%;
  display: grid;
  grid-template-columns: 250px 250px 250px 250px;
  grid-template-rows: 250px;
}

.entrance_style_1 {
  width: 230px;
  height: 230px;
  margin: 10px;
}

.lesson_div_2 {
  width: 100%;
  display: grid;
  grid-template-columns: 25vw 25vw 25vw 25vw;
  grid-template-rows: 25vw;
}

.entrance_style_2 {
  width: 23vw;
  height: 23vw;
  margin: 1vw;
}

.lesson_div_3 {
  width: 100%;
  display: grid;
  grid-template-columns: 33vw 33vw 33vw;
  grid-template-rows: 33vw;
}

.entrance_style_3 {
  width: 30vw;
  height: 30vw;
  margin: 1.5vw;
}

.lesson_div_4 {
  width: 100%;
  display: grid;
  grid-template-columns: 50vw 50vw;
  grid-template-rows: 50vw;
}

.entrance_style_4 {
  width: 48vw;
  height: 48vw;
  margin: 1vw;
}

.search_div input {
  width: 300px;
  height: 50px;
  border: 1px solid #cccccc;
  border-radius: 5px;
  outline: none;
}

.search_div input:focus {
  border: 1px solid #1e1e1e;
}

.search_div .el-button {
  height: 50px;
  /* width: 60px;
  background-color: #409EFF;
  color: #ffffff;
  outline: none;
  border: none; */
}

.background {
  width: 100%;
  height: 100%;
  position: absolute;
  object-fit: cover;
}
</style>