<template>
  <div>
    <div class="header_menu">
      <div>
        <el-button type="primary" size="small" @click="prepareAdd" class="el-icon-plus">添加
        </el-button>
        <el-button type="danger" size="small" class="el-icon-delete" @click="delItems">批量删除</el-button>
        <el-button size="small" class="el-icon-document" type="success" @click="tableDialogVisible = true">导入
                </el-button>
      </div>
      <div>
        <el-input>
          <el-button slot="append">搜索</el-button>
        </el-input>
      </div>

    </div>
    <el-table :data="tableData" height="480" border style="width:100%" @selection-change="changeSelection">
      <el-table-column type="selection" width="55">
      </el-table-column>
      <el-table-column prop="class_id" label="班级号">
      </el-table-column>
      <el-table-column prop="class_name" label="班级名称">
      </el-table-column>
      <el-table-column prop="college" label="学院">
      </el-table-column>
      <el-table-column prop="teacher_id" label="教师id">
      </el-table-column>
      <el-table-column prop="teacher_name" label="教师姓名">
      </el-table-column>
      <el-table-column prop="lesson_id" label="课程id">
      </el-table-column>
      <el-table-column prop="lesson_name" label="课程名称">
      </el-table-column>
      <el-table-column  label="操作" width="180">
        <template slot-scope="scope">
          <el-button size="small" @click="prepareEdit(scope.row)" class="el-icon-edit">编辑</el-button>
          <el-button size="small" type="danger" @click="delCurrentItem(scope.row)" class="el-icon-delete">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination layout="prev, pager, next,jumper" :total="class_total" :hide-on-single-page="false" :page-size="20"
      @current-change="handleCurrenChange"></el-pagination>
    <el-dialog :visible.sync="addDialogVisible" width="400px" title="添加" top="10px"
    >
      <el-form label-width="80px" label-position="left" :model="form">
        <el-form-item label="班级号">
          <el-input v-model="form['class_id']"></el-input>
        </el-form-item>
        <el-form-item label="班级名称">
          <el-input v-model="form['class_name']"></el-input>
        </el-form-item>
        <el-form-item label="学院">
          <el-select v-model="form['college']" filterable style="width: 100%;">
            <el-option v-for="college in college_options" :key="college" :value="college"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="教师工号">
          <el-input v-model="form['teacher_id']" @change="getTeacherName"></el-input>
        </el-form-item>
        <el-form-item label="教师名称">
          <el-input v-model="form['teacher_name']" disabled></el-input>
        </el-form-item>
        <el-form-item label="课程id">
          <el-input v-model="form['lesson_id']" @change="getLessonName"></el-input>
        </el-form-item>
        <el-form-item label="课程名称">
          <el-input v-model="form['lesson_name']" disabled></el-input>
        </el-form-item>
      </el-form>
      <el-button @click="cancel">取 消</el-button>
      <el-button type="primary" @click="confirmAddItem(form)">确认</el-button>
    </el-dialog>
    <el-dialog :visible.sync="editDialogVisible" width="400px" title="编辑" top="10px">
      <el-form label-width="80px" label-position="left" :model="form" v-if="fresh">
        <el-form-item label="班级号">
          <el-input v-model="form['class_id']" disabled></el-input>
        </el-form-item>
        <el-form-item label="班级名称">
          <el-input v-model="form['class_name']"></el-input>
        </el-form-item>
        <el-form-item label="学院">
          <el-select v-model="form['college']" filterable style="width: 100%;">
            <el-option v-for="college in college_options" :key="college" :value="college"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="教师工号">
          <el-input v-model="form['teacher_id']" @change="getTeacherName"></el-input>
        </el-form-item>
        <el-form-item label="教师名称">
          <el-input v-model="form['teacher_name']" disabled></el-input>
        </el-form-item>
        <el-form-item label="课程id">
          <el-input v-model="form['lesson_id']" @change="getLessonName"></el-input>
        </el-form-item>
        <el-form-item label="课程名称">
          <span>{{form['lesson_name']}}</span>
        </el-form-item>
      </el-form>
      <el-button @click="cancel">取 消</el-button>
      <el-button type="primary" @click="confirmEditItem(form)">确认</el-button>
    </el-dialog>
  </div>
</template>

<script>
import AHU from "@/js/college"
import config from "@/config.json"
import axios from "axios"
const server = config["server"]
export default {
  name: "ClassMangement",
  data() {
    return {
      tableData: [
      ],
      class_total: 0,
      selectedTable: [],
      addDialogVisible: false,
      editDialogVisible: false,
      form: {
        class_id: "",
        class_name: "",
        college: "计算机科学与技术学院",
        teacher_id:"",
        lesson_id:"",
        teacher_name:'',
        lesson_name:'',
      },
      college_options: AHU["college_options"],
      start: 0,
      end: 20,
      teacher_not_exist:true,
      fresh:true
    }
  },
  created() {
    this.getList()
  },
  methods: {
    handleCurrenChange(page) {
      this.start = (page - 1) * 10;
      this.end = this.start + 20;
      // console.log(`当前页：${page}`);
      this.getList()
    },
    changeSelection(selection) {
      this.selectedTable = []
      for (let item of selection) {
        this.selectedTable.push(item["class_id"])
      }
    },
    getList() {
      let url = server + "/admin/get_class_list?start=" + this.start + "&end=" + this.end
      axios.get(url).then(res => {
        this.class_total = res.data["total"]
        this.tableData = res.data["list"]
      })
    },
    prepareAdd() {
      this.resetForm()
      this.addDialogVisible = true
    },
    prepareEdit(item) {
      this.resetForm()
      this.form = item
      this.form["lesson_name"]=""
      this.editDialogVisible = true
    },
    cancel(){
      this.getList()
      this.editDialogVisible=false
      this.addDialogVisible=false
      this.resetForm()
      this.teacher_not_exist=true
    },
    confirmEditItem(form) {
      if (this.checkForm(form)) {
        this.$confirm("是否确认信息无误？").then(() => {
          let url = server + "/admin/edit_class"
          let formData = this.getFormData(form)
          axios.post(url, formData).then(res => {
            this.$message(res.data)
            this.getList()
            this.editDialogVisible = false
          })
        })
          .catch(() => {
            console.log("取消");
          })
      }
    },
    checkForm(form) {
      let flag = true
      if (!form["class_id"]) {
        this.$alert("请输入班级号")
        flag = false
      }
      if (!form["class_name"]) {
        this.$alert("请输入班级名称")
        flag = false
      }
      if (!form["teacher_id"]) {
        this.$alert("请输入教师工号")
        flag = false
      }
      return flag
    },
    resetForm() {
      this.form = {
        class_id: "",
        class_name: "",
        college: "计算机科学与技术学院",
        teacher_id:"",
        lesson_id:"",
        teacher_name:'',
        lesson_name:'',
      }
    },
    getFormData(form) {
      let formData = new FormData()
      formData.append("class_id", form['class_id'])
      formData.append("class_name", form['class_name'])
      formData.append("teacher_id", form['teacher_id'])
      formData.append("college", form['college'])
      formData.append("lesson_id", form['lesson_id'])
      return formData
    },
    confirmAddItem(form) {
      if (this.checkForm(form)) {
        this.$confirm("是否确认信息无误？").then(() => {
          let url = server + "/admin/create_class"
          let formData = this.getFormData(form)
          axios.post(url, formData).then(res => {
            this.$message(res.data)
            this.tableData.push(form)
            this.resetForm()
            this.addDialogVisible = false
          })
        })
          .catch(() => {
            console.log("取消");
          })
      }
    },
    delCurrentItem(form) {
      this.$confirm(`确认要删除${form["class_id"]}`).then(() => {
        let url = server + "/admin/delete_class"
        let formData = new FormData()
        formData.append("class_id", form["class_id"])
        axios.post(url, formData).then(res => {
          this.$message(res.data)
          this.getList()
        })
      })
    },
    delItems() {
      let loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      let l = this.selectedTable.length;
      for (let i = 0; i < l; i++) {
        setTimeout(() => {
          let url = server + "/admin/delete_class"
          let formData = new FormData()
          formData.append("class_id", this.selectedTable[i])
          axios.post(url, formData).then(res => {
            this.$message(res.data)
            if (i === l - 1) {
              loading.close()
              this.selectedTable = []
              this.getList()
            }
          })
        }, 500 * i)
      }
    },
    getTeacherName(id){
      let url=server+"/admin/get_teacher_name?id="+id
      axios.get(url).then(res=>{
        if(res.data["type"]==='success'){
          console.log(res.data);
          this.form['teacher_name']=res.data['name']
          this.teacher_not_exist=false
        }else{
          this.teacher_not_exist=true
          this.form["teacher_id"]=''
          this.$message(res.data)
        }
      })
    },
    getLessonName(id){
      let url=server+"/admin/get_lesson_name?id="+id
      console.log(this.form);
      axios.get(url).then(res=>{
        if(res.data["type"]==='success'){
          this.form['lesson_name']=res.data['lesson_name']
          this.fresh=false
          this.fresh=true
          
        }else{
          this.$message(res.data)
          setTimeout(() => {
            this.form["lesson_id"]=''
          }, 1000);
        }
      })
    },
  },
  components: {}
}

</script>
<style scoped>
.el-table {
  margin-top: 10px;
}

.header_menu {
  display: flex;
  justify-content: space-between;
  min-width: 450px;
}
</style>
