<template>
  <div class="entrance_basic_class" @click="gotoLesson">
    <img :src="this.img" alt="" class="cover">
    <div>
      <div>
        <div class="title">{{ LessonData["lesson_name"] }}</div>
        <div style="color: #909399;font-size: 14px;text-align: left;margin: auto 5px;width: 190px;">
          <span>{{ LessonData["teacher_name"] }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from "axios"
import config from "@/config.json"
export default {
  name: "LessonEntrance",
  props: ["LessonData"],
  data() {
    return {
      img: "",
      teacher: "xcx",
      university: "安徽大学",
      lesson_name: "课程",
      description: "",
      entranClass: "entrance_style1 entrance_basic_class"
    }
  },
  created() {
    this.img = config["server"] + "/file/image/" + this.LessonData["cover_id"]
    console.log(this.LessonData);
    // this.entranClass="entrance_style1 entrance_basic_class"
    // console.log(this.entranClass);
  },
  methods: {
    gotoLesson() {
      // let url="/Lesson?lesson_id="
      this.$router.push("/Lesson?lesson_id="+this.LessonData["lesson_id"])
    }
  },
  mounted() {
  
  }
}
</script>

<style scoped>

.entrance_basic_class {
  width: 100%;
  height: 100%;
  border-radius: 5px;
  box-shadow: 0 0 2px 1px #1e1e1e;
  border: 1px solid #cccccc;
  place-self: center;
}

.entrance_basic_class:hover {
  box-shadow: 0 0 2px 1px #66b1ff;
  cursor: pointer;
}
.cover {
  height: 50%;
  width: 100%;
  object-fit: cover;
}

</style>