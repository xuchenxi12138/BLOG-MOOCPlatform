<template>
  <div>
    <el-row type="flex" justify="space-between">
      <el-col>
        <el-page-header @back="goBack" :content="class_name">
        </el-page-header>
      </el-col>
      <el-button type="primary" @click="dialogVisible = true">添加</el-button>
      <el-badge :value="messageNumber" :hidden="!messageNumber" class="item">
        <el-button @click="goCheckAssignment">新的提交</el-button>
      </el-badge>
    </el-row>
    <el-table ref="singleTable" :data="tableData" highlight-current-row stripe style="width: 100%" height="500px">
      <el-table-column type="index" width="50">
      </el-table-column>
      <el-table-column property="post_time" label="发布日期">
      </el-table-column>
      <el-table-column property="title" label="名称">
      </el-table-column>
      <el-table-column property="description" label="简介">
        <template slot-scope="scope">
          <el-popover placement="top-start" title="简介" width="400" trigger="hover" :content="scope.row.description">
            <el-button slot="reference" class="el-icon-zoom-in" type="text"></el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column property="deadline" label="截止日期">
      </el-table-column>
      <el-table-column property="" label="操作" width="200">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" class="el-icon-edit" @click="edit(scope.row)">修改</el-button>
          <el-button size="mini" type="danger" class="el-icon-edit" @click="del(scope.row)">取消</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="dialogVisible" title="添加" width="500px" :before-close="cancel">
      <el-form :model="rowForm" label-width="120px" label-position="left">
        <el-form-item label="标题(必填)">
          <el-input v-model="rowForm['title']"></el-input>
        </el-form-item>
        <el-form-item label="简介(选填)">
          <el-input type="textarea" v-model="rowForm['description']"></el-input>
        </el-form-item>
        <el-form-item label="文件(必选)">
          <el-upload ref="upload" :action="fileServer" :on-remove="handleRemove" :limit="1" class="upload-demo"
            :file-list="fileList"
            accept="application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            :on-success="uploadSuccess">
            <el-button slot="trigger" size="small" type="primary">选择文件</el-button>
            <i slot="tip" style="margin-left: 5px;">如需更换,请先移除<em>已有</em>的文件</i>
          </el-upload>
        </el-form-item>
        <el-form-item label="截止日期(选填)">
          <el-date-picker v-model="rowForm['deadline']" type="date" value-format="yyyy-MM-dd" placeholder="默认七天后"
            style="width:100%;">
          </el-date-picker>
        </el-form-item>
        <el-row>
          <el-button @click="cancel">取消</el-button>
          <el-button type="primary" @click="submit">提交</el-button>
        </el-row>
      </el-form>
    </el-dialog>
    <el-dialog :visible.sync="editDialogVisible" title="修改内容" width="500px" :before-close="cancel">
      <el-form :model="rowForm" label-width="120px" label-position="left">
        <el-form-item label="标题(必填)">
          <el-input v-model="rowForm['title']"></el-input>
        </el-form-item>
        <el-form-item label="简介(选填)">
          <el-input type="textarea" v-model="rowForm['description']"></el-input>
        </el-form-item>
        <el-form-item label="文件">
          <el-upload ref="upload" :action="fileServer" :on-remove="handleRemove" :limit="1" class="upload-demo"
            :file-list="fileList"
            accept="application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            :on-success="uploadSuccess">
            <el-button slot="trigger" size="small" type="primary">选择文件</el-button>
            <i slot="tip" style="margin-left: 5px;">如需更换,请先移除<em>已有</em>的文件</i>
          </el-upload>
        </el-form-item>
        <el-form-item label="截止日期(选填)">
          <el-date-picker v-model="rowForm['deadline']" type="date" value-format="yyyy-MM-dd" placeholder="默认七天后"
            style="width:100%;">
          </el-date-picker>
        </el-form-item>
        <el-row>
          <el-button @click="cancel">取消</el-button>
          <el-button type="primary" @click="confirmEdit">提交</el-button>
        </el-row>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import config from "@/config.json"
import axios from "axios"
const server = config["server"]
export default {
  name: 'AssignmentView',
  data() {
    return {
      class_id: '',
      dialogVisible: false,
      editDialogVisible: false,
      tableData: [],
      rowForm: {
        title: "",
        description: "",
        deadline: "",
        file_id: ""
      },
      fileServer: server + "/file/upload_word",
      fileList: [],
      fileName: "",
      class_name: "",
      messageNumber: 0
    }
  },
  created() {
    this.class_id = this.$route.query["class_id"]
    this.$store.state.routerList = [{
      path: '/Teacher/ClassManagement',
      name: "班级列表"
    }, {
      name: "作业记录"
    }]
    this.getAssignments()
  },
  methods: {
    goBack() {
      this.$router.push("/Teacher/ClassManagement")
    },
    edit(value) {
      this.rowForm = value
      if (value["file_id"])
        this.fileList = [{ name: value["file_id"] }]
      else this.fileList = []
      this.editDialogVisible = true;
    },
    handleRemove(file, fileList) {
      console.log(file);
      console.log(fileList);
    },
    cancel() {
      this.rowForm = {
        title: "",
        description: "",
        deadline: "",
        file_id: ""
      }
      this.fileList = []
      this.dialogVisible = false
      this.editDialogVisible = false
    },
    uploadSuccess(response) {
      this.rowForm["file_id"] = response["url"]
      this.fileList=[{
        name: response["url"]
      }]
      return response["url"]
    },
    getDeadline() {
      let date = new Date().getTime();
      let deadline = new Date(date + 7 * 24 * 60 * 60 * 1000)
      let year = deadline.getFullYear();
      let month = deadline.getMonth() + 1
      let day = deadline.getDate()
      let time = year + "-" + month + "-" + day
      return time
    },
    submit() {
      if (this.rowForm["title"]) {
        if (this.fileList.length==0) {
          this.$message({
            message: "必须上传文件",
            type: "warning"
          })
        }
        else {
          let url = server + "/teacher/create_assignment"
          let formdata = new FormData()
          formdata.append("title", this.rowForm["title"])
          if (this.rowForm["deadline"]) {
            formdata.append("deadline", this.rowForm["deadline"])
          }
          else {
            formdata.append("deadline", this.getDeadline())
          }
          formdata.append("description", this.rowForm["description"])
          formdata.append("file_id", this.rowForm["file_id"])
          formdata.append("class_id", this.class_id)
          let teacher_id = sessionStorage.getItem("username")
          formdata.append("teacher_id", teacher_id)
          axios.post(url, formdata).then(res => {
            if (res.data["type"] === "success") {
              this.fileList = []
              console.log(res.data);
              this.getAssignments()
              this.cancel()
            }
            this.$message(res.data)
          })
        }
      }
      else {
        this.$message({
          message: "请输入标题",
          type: "warning"
        })
      }
    },
    test(v) {
      console.log(v);
    },
    getAssignments() {
      let url = server + "/teacher/get_assignments?class_id=" + this.class_id
      axios.get(url).then(res => {
        this.tableData = res.data
      })
    },
    del(row) {
      this.$confirm("您确定要取消该作业？").then(() => {
        let url = server + "/teacher/delete_assignment"
        let formdata = new FormData()
        formdata.append("id", row.id)
        axios.post(url, formdata).then(res => {
          console.log(res.data);
          this.getAssignments()
        })
      })
    },
    confirmEdit() {
      if (this.rowForm["title"]) {
        let url = server + "/teacher/edit_assignment"
        let formdata = new FormData()
        formdata.append("title", this.rowForm["title"])
        if (this.rowForm["deadline"]) {
          formdata.append("deadline", this.rowForm["deadline"])
        }
        else {
          formdata.append("deadline", this.getDeadline())
        }
        formdata.append("description", this.rowForm["description"])
        formdata.append("file_id", this.rowForm["file_id"])
        formdata.append('id', this.rowForm["id"])
        axios.post(url, formdata).then(res => {
          if (res.data["type"] === "success") {
            this.fileList = []
            this.cancel()
          }
          this.$message(res.data)
        })
      }
      else {
        this.$message({
          message: "请输入标题",
          type: "warning"
        })
      }
    },
    goCheckAssignment() {
      this.$router.push("/Teacher/ClassManagement/AssignmentDone?class_id=" + this.class_id)
    }
  },
  mounted() {
    axios.get(server + "/teacher/count_assignment?class_id=" + this.class_id)
      .then(res => {
        this.messageNumber = res.data["number"]
        console.log(this.messageNumber);
      })
  }
}

</script>
<style scoped>
.upload-demo {
  text-align: left;
}

em {
  color: #409EFF;
  margin: auto 5px;
}

.item {
  margin-left: 10px;
}
</style>
