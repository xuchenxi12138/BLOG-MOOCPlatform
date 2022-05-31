<template>
  <div class="lesson-view">
    <el-container>
      <el-header>
        <el-row type="flex" justify="space-between" align="middle" style="height: 100%;">
          <el-tag type="success">课程</el-tag>
          <el-col>
            <p>{{ LessonData["lesson_name"] }}</p>
          </el-col>
          <el-button class="el-icon-document" type="text" @click="dialogVisible = true">简介</el-button>
        </el-row>
      </el-header>
      <h2>{{ subchapter_title }}</h2>
      <el-container>
        <el-main style="padding:0;">

          <video style="width: 100%;" controls="controls" ref="video" :src="video_url">
          </video>
          <div class="footer">
            <el-button @click="downloadFile" class="el-icon-document" type="primary">下载课件</el-button>
            <el-button @click="downloadVideo" class="el-icon-video-camera-solid" type="primary">下载视频</el-button>
          </div>
        </el-main>
        <el-aside>
          <el-card>
            <el-collapse>
              <el-collapse-item v-for="item in ChapterList" :key="item['chapter_id']" :title="item['title']">
                <div v-for="subitem in item.children" :key="subitem['subchapter_id']" style="text-align: left;">
                  <router-link :to="subitem['subchapter_url']">
                    {{ subitem['title'] }}
                  </router-link>
                </div>
              </el-collapse-item>
            </el-collapse>
          </el-card>
        </el-aside>
      </el-container>
    </el-container>
    <transition name="el-zoom-in-top">
      <div class="dialog" v-if="dialogVisible">
        <div class="dialog_inner">
          <el-descriptions title="课程信息" border>
            <el-descriptions-item label="课程号">{{ LessonData["lesson_id"] }}</el-descriptions-item>
            <el-descriptions-item label="课程名称">{{ LessonData["lesson_name"] }}</el-descriptions-item>
            <el-descriptions-item label="授课教师">{{ LessonData["teacher_name"] }}</el-descriptions-item>
            <el-descriptions-item label="简介">
              <div v-html="LessonData['description']"></div>
            </el-descriptions-item>
          </el-descriptions>
          <el-button class="el-icon-close" type="primary" @click="dialogVisible = false">关闭</el-button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>

import config from "@/config.json"
import axios from "axios";
const server = config["server"]
export default {
  name: "LessonView",
  data() {
    return {
      LessonData: {},
      ChapterList: [],
      drawer: false,
      video_url: "",
      file_url: "",
      file_id: '',
      title: "",
      video_id: "",
      subchapter_id: "",
      subchapter_title: "",
      dialogVisible: false,
      description: ""
    };
  },
  created() {
    this.lesson_id = this.$route.query["lesson_id"];
    if(!this.lesson_id){this.$router.push("/errorPage")}
    this.subchapter_id = this.$route.query["subchapter_id"];
    if (!this.subchapter_id) {
      this.video_url = server + "/file/lesson/" + this.lesson_id;
      this.getVideoByLessonId();
    }
    else {
      this.video_url = server + "/file/subchapter/" + this.subchapter_id;
      this.getVideoByChapterId();
    }
  },
  beforeCcreated() {
  },
  methods: {
    handleClose(done) {
      done();
    },
    changeVideo(url) {
      this.$router.push(url);
    },
    getVideoByLessonId() {
      let url = server + "/home/get_lesson_info_by_leson_id?lesson_id=" + this.lesson_id;
      axios.get(url).then(res => {
        this.LessonData = res.data;
        console.log("by lessond id");
        let list = res.data["chapter_list"];
        for (let item of list) {
          item["chapter_url"] = "/Lesson?lesson_id=" + this.lesson_id + "&chapter_id=" + item["chapter_id"];
          for (let subitem of item.children) {
            subitem["subchapter_url"] = "/Lesson?lesson_id=" + this.lesson_id + "&subchapter_id=" + subitem["subchapter_id"];
          }
        }
        this.title = list[0]["children"][0]["title"];
        this.file_url = server + "/file/course_file/" + list[0]["children"][0]["file_id"];
        this.file_id = list[0]["children"][0]["file_id"];
        this.video_id = list[0]["children"][0]["video_id"];
        this.ChapterList = list;
      });
    },
    getVideoByChapterId() {
      let url = server + "/home/get_lesson_info_by_subchapter_id?lesson_id=" + this.lesson_id + "&subchapter_id=" + this.subchapter_id;
      axios.get(url).then(res => {
        this.LessonData = res.data;
        console.log("by subchapter id");
        let list = res.data["chapter_list"];
        for (let item of list) {
          item["chapter_url"] = "/Lesson?lesson_id=" + this.lesson_id + "&chapter_id=" + item["chapter_id"];
          for (let subitem of item.children) {
            subitem["subchapter_url"] = "/Lesson?lesson_id=" + this.lesson_id + "&subchapter_id=" + subitem["subchapter_id"];
          }
        }
        let subchapter_info = res.data["subchapter_info"];
        console.log(subchapter_info);
        this.file_url = server + "/file/course_file/" + subchapter_info["file_id"];
        this.file_id = subchapter_info["file_id"];
        this.video_id = subchapter_info["video_id"];
        this.subchapter_title = subchapter_info["title"];
        this.ChapterList = list;
      });
    },
    downloadFile() {
      if (this.file_id) {
        window.open(server + "/file/course_file/" + this.file_id)
      } else {
        this.$message("对不起，教师没有上传文件")
      }
    },
    downloadVideo() {
      console.log(this.video_id);
      console.log(this.video_url);
      if (this.video_id) {
        window.open(server + "/file/video/" + this.video_id)
      } else {
        this.$message("对不起，教师没有上传文件")
      }
    }
  },
  watch: {
    $route(value) {
      if (value.query["subchapter_id"]) {
        this.$refs.video.src = server + "/file/subchapter/" + value.query["subchapter_id"]
        this.getVideoByChapterId()
      }
      else {
        this.$refs.video.src = server + "/file/lesson/" + value.query["lesson_id"]
        this.getVideoByLessonId()
      }

    }
  }
}

</script>
<style scoped>
.lesson-view {
  width: 100%;
  max-width: 1000px;
  margin: 10px auto;
}

.el-header {
  background-color: #ffffff;
  box-shadow: 0 0 2px 1px #000000;
}

.el-collapse-item a {
  margin-left: 2em;
  text-align: left;
  text-decoration: none;
  color: #409EFF;
  line-height: 30px;
  width: 100%;
}

.el-collapse-item div {
  width: 100%;
  border-bottom: 1px solid #cccccc;
}

.footer {
  width: 100%;
  height: 50px;
  margin-top: 10px;
  display: flex;
  justify-content: flex-start;
}

.download-button {
  margin-left: 10px;
  width: 80px;
  height: 40px;
  background-color: #409EFF;
  text-decoration: none;
  text-align: center;
  line-height: 40px;
  color: #ffffff;
  border-radius: 5px;
}

.dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #00000080;
  z-index: 100;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.dialog_inner {
  width: 800px;
  min-height: 200px;
  margin: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
  padding: 20px;
  max-height: 100%;
  overflow: auto;
}
</style>
