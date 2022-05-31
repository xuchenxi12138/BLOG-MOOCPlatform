<template>
  <div>
    <div v-if="LessonList.length != 0" class="lesson_div">
      <div v-for="data in LessonList" :key="data['lesson_id']" class="entrance_div">
        <LessonEntranceVue :LessonData="data"></LessonEntranceVue>
      </div>
    </div>
    <el-empty v-else></el-empty>
    <el-pagination layout="prev, pager, next,jumper" :total="total" :hide-on-single-page="false" :page-size="10"
      @current-change="handleCurrenChange"></el-pagination>
  </div>
</template>

<script>
import LessonEntranceVue from '@/components/LessonEntrance.vue'
import axios from 'axios'
import config from "@/config.json"

export default {
  name: 'LessonView',
  data() {
    return {
      LessonList: [],
      text: "",
      start: 0,
      total: 0,
    }
  },
  components: { LessonEntranceVue },
  created() {
    this.start = this.$route.query["start"]
    this.text = this.$route.query["text"]
    this.getLessons()
  },
  methods: {
    handleCurrenChange(page) {
      this.start = (page - 1) * 10
      this.getLessons()
    },
    getLessons() {
      axios.get(config["server"] + "/search/lesson?text=" + this.text + "&start=" + this.start)
        .then(res => {
          console.log(res.data);
          this.LessonList = res.data["list"]
          this.total = res.data["total"]
        })
    }
  },
}

</script>
<style scoped>
.lesson_div {
  width: 100%;
  display: grid;
  grid-template-columns: 250px 250px 250px 250px;
  grid-template-rows: 250px;
}

.entrance_div {
  width: 230px;
  height: 230px;
  margin: 10px;
}
</style>
