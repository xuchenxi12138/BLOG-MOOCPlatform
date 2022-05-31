<template>
  <div style="margin: 5px">
    <h3 style="text-align: left;">首页推荐列表</h3>
    <div>
      <form>
        <table style>
          <tr style="background-color: #545c64;color: #ffffff;" class="table_line">
            <th>序号</th>
            <th>封面</th>
            <th>标题</th>
            <th>类型</th>
            <th>作者</th>
            <th>链接</th>
            <th>操作</th>
          </tr>
          <tr v-for="(item, index) in recommend_list" :key="index" class="table_line">
            <td>{{ index }}</td>
            <td>
              <div class="cover_div">
                <img :src="item['cover_url']" alt class="cover" />
                <div class="cover_menu">
                  <div class="upload_image_button">
                    <input type="file" name="file" :id="item['id']" @change="uploadCover" />
                    <el-button type="text" class="el-icon-edit-outline"></el-button>
                  </div>

                  <el-button type="text" class="el-icon-zoom-in" style="width: 50%;"
                    @click="showCover(item['cover_url'])"></el-button>
                </div>
              </div>
            </td>
            <td>{{ item['title'] }}</td>
            <td>{{ item['type'] }}</td>
            <td>{{ item['author'] }}</td>
            <td>
              <a :href="item['url']" class="link">{{ item['url'] }}</a>
            </td>
            <td>
              <el-button class="el-icon-edit" type="text" @click="openSetDialog(item)"></el-button>
              <!-- <el-button class="el-icon-delete" type="text"></el-button> -->
            </td>
          </tr>
        </table>
      </form>
    </div>
    <el-dialog top="50px" title="展示封面" :visible.sync="dialogVisible" width="90%">
      <div style="position: relative;height: 400px;display: flex;justify-content:center">
        <el-empty></el-empty>
        <img :src="dialog_img" alt class="large_cover" />
      </div>
    </el-dialog>
    <el-dialog top="50px" title="编辑" :visible.sync="editDialogVisible">
      <el-form label-width="80px" label-position="left">
        <el-form-item label="编号">
          <el-input v-model="form['id']" disabled></el-input>
        </el-form-item>
        <el-form-item label="标题">
          <el-input v-model="form['title']"></el-input>
        </el-form-item>

        <el-form-item label="类型">
          <el-input v-model="form['type']"></el-input>
        </el-form-item>
        <el-form-item label="作者">
          <el-input v-model="form['author']"></el-input>
        </el-form-item>
        <el-form-item label="作者地址">
          <el-input v-model="form['author_url']"></el-input>
        </el-form-item>
        <el-form-item label="链接">
          <el-input v-model="form['url']"></el-input>
        </el-form-item>
      </el-form>
      <div>
        <el-button type="primary" @click="onSubmit">确定</el-button>
        <el-button>取消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
// import config from "@/config.json"
// const server=config["server"]
export default {
  name: "HomeManagement",
  data() {
    return {
      editDialogVisible: false,
      dialogVisible: false,
      dialog_img: '',
      recommend_list: [],
      form: {
        id: '',
        title: '',
        type: '',
        author: '',
        author_url: '',
        url: '',
      },
      upload_cover_url: [
        "http://localhost:5000/admin/set_recommend_work_cover/recommend_option_1",
        "http://localhost:5000/admin/set_recommend_work_cover/recommend_option_2",
        "http://localhost:5000/admin/set_recommend_work_cover/recommend_option_3",
        "http://localhost:5000/admin/set_recommend_work_cover/recommend_option_4",
      ]
    }
  },
  created() {
    axios.get(
      'http://localhost:5000/admin/get_recommend_list'
    ).then(res => {
      this.recommend_list = res.data;
      this.recommend_list.forEach(element => {
        element['cover_url'] = "http://localhost:5000/file/image/" + element['cover_url'];
      })
      // console.log(res);
    })
  },
  methods: {
    onSubmit() {
      var params = new URLSearchParams();
      params.append('title', this.form['title']);
      params.append('id', this.form['id']);
      params.append('type', this.form['type']);
      params.append('author', this.form['author']);
      params.append('author_url', this.form['author_url']);
      params.append('url', this.form['url']);
      // console.log(params);
      axios.post(
        "http://localhost:5000/admin/set_recommend_work", params
      ).then(res => {
        if (res.data["result"] === "OK") {
          this.$message({
            message: '上传成功',
            type: 'success'
          });
        } else if (res.data["result"] === "ERROR") {
          this.$message.error("上传失败，数据库访问失败！")
        }
        this.editDialogVisible = false;
      })
    },
    openSetDialog(item) {
      this.editDialogVisible = true;
      this.form = item
    },
    uploadCover(event) {
      // console.log(event);
      let image = event.target.files[0]
      // let params = new URLSearchParams();
      let params = new FormData()
      params.append("file", image)
      params.append("id", event.target.id)
      let url = 'http://localhost:5000/admin/set_recommend_work_cover'
      axios.post(url, params).then(res => {
        this.recommend_list.forEach(element => {
          if (element['id'] === event.target.id) {
            element['cover_url'] = res.data["url"]
          }
        });
      })
    },
    showCover(value) {
      this.dialog_img = value;
      this.dialogVisible = true;
    }
  },
  mounted() {

  }

}
</script>

<style scoped>
.table_line {
  width: 1100px;
  display: grid;
  grid-template-columns: 50px 200px 200px 100px 150px 300px 100px;
  min-height: 40px;
  text-align: center;
  line-height: 40px;
}

.table_line th {
  border-right: 1px solid #aaaaaa;
}

.table_line td {
  border-right: 1px solid #aaaaaa;
  min-height: 100px;
  border-bottom: 1px solid #aaaaaa;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cover_div {
  position: relative;
  width: 200px;
  height: 100px;
  overflow: hidden;
}

.cover {
  /* width: 100%; */
  height: 100%;
  border: none;
}

.cover_menu {
  width: 100%;
  height: 100%;
  position: absolute;
  background-color: #1e1e1e50;
  display: flex;
  align-items: center;
  top: 0;
  opacity: 0;
}

.cover_menu:hover {
  opacity: 1;
  transition: opacity 1s;
}

.large_cover {
  /* width: 800px; */
  height: 400px;
  position: absolute;
  top: 0;
  object-fit: contain;
  max-width: 100%;
}

.upload_image_button {
  width: 50%;
  /* height: 100%; */
  position: relative;
}

.upload_image_button input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
}

.link {
  max-width: 100%;
  word-break: break-all;
}
</style>