<template>
  <div>
    <div class="header_menu">
      <div>
        <el-button type="primary" size="small" @click="prepareAdd" class="el-icon-plus">添加
        </el-button>
        <el-button type="danger" size="small" class="el-icon-delete" @click="delItems">批量删除</el-button>
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
      <el-table-column prop="username" label="账号" width="160">
      </el-table-column>
      <el-table-column prop="name" label="姓名" width="160">
      </el-table-column>
      <el-table-column prop="college" label="学院" width="180">
      </el-table-column>
      <el-table-column prop="email" label="邮箱" width="180">
      </el-table-column>
      <el-table-column prop="password" label="密码" width="200">
        <template slot-scope="scope">
          <Password :value="scope.row.password"></Password>
        </template>
      </el-table-column>
      <el-table-column prop="" label="操作" width="170">
        <template slot-scope="scope">
          <el-button size="small" @click="prepareEdit(scope.row)" class="el-icon-edit">编辑</el-button>
          <el-button size="small" type="danger" @click="delCurrentItem(scope.row)" class="el-icon-delete">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination layout="prev, pager, next,jumper" :total="admin_total" :hide-on-single-page="false" :page-size="20"
      @current-change="handleCurrenChange"></el-pagination>
    <el-dialog :visible.sync="addDialogVisible" width="400px" title="添加" top="10px">
      <el-form label-width="80px" label-position="left" :model="form" :rules="rules">
        <el-form-item label="工号" prop="username">
          <el-input v-model="form['username']"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form['name']"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="form['gender']" value="男" style="width: 100%;">
            <el-option label="男" value="male"></el-option>
            <el-option label="女" value="female"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="学院">
          <el-select v-model="form['college']" filterable style="width: 100%;">
            <el-option v-for="college in college_options" :key="college" :value="college"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form['email']"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form['password']" type="password" show-password></el-input>
        </el-form-item>
      </el-form>
      <el-button @click="cancel(form)">取 消</el-button>
      <el-button type="primary" @click="confirmAddItem(form)">确认</el-button>
    </el-dialog>
    <el-dialog :visible.sync="editDialogVisible" width="400px" title="添加" top="10px">
      <el-form label-width="40px" label-position="left" :model="form">
        <el-form-item label="工号">
          <el-input v-model="form['username']" disabled></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form['name']"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="form['gender']" value="男" style="width: 100%;">
            <el-option label="男" value="male"></el-option>
            <el-option label="女" value="female"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="学院">
          <el-select v-model="form['college']" filterable style="width: 100%;">
            <el-option v-for="college in college_options" :key="college" :value="college"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form['email']"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form['password']" type="password" show-password></el-input>
        </el-form-item>
      </el-form>
      <el-button @click="cancel(form)">取 消</el-button>
      <el-button type="primary" @click="confirmEditItem(form)">确认</el-button>
    </el-dialog>
  </div>
</template>

<script>
import Password from "@/components/Password.vue"
import AHU from "@/js/college"
import config from "@/config.json"
import axios from "axios"
const server = config["server"]
export default {
  name: "AdminMangement",
  data() {
    return {
      tableData: [
      ],
      admin_total: 0,
      selectedTable: [],
      addDialogVisible: false,
      editDialogVisible: false,
      form: {
        username: "",
        name: "",
        gender: "男",
        college: "计算机科学与技术学院",
        password: "",
        email: ""
      },
      college_options: AHU["college_options"],
      start: 0,
      end: 20,
      rules: {
        username: [
          { required: true, message: '新账号不能为空' },
          { min: 8, max: 18, message: '账号长度必须在8到18个字符之间', trigger: 'blur' },
          { pattern: /^([a-z]*[A-Z]*[0-9]*)*$/, message: '账号必须是字母和数字组成', trigger: 'blur' },
        ],
        name: [
          { required: true, message: '姓名不能为空' }
        ],
        password: [
          { required: true, message: '新密码不能为空' },
        ]
      }
    };
  },
  created() {
    this.getList()
  },
  methods: {
    cancel() {
      this.getList()
      this.editDialogVisible = false
      this.addDialogVisible = false
      this.resetForm()
    },
    handleCurrenChange(page) {
      this.start = (page - 1) * 10;
      this.end = this.start + 20;
      // console.log(`当前页：${page}`);
      this.getList()
    },
    changeSelection(selection) {
      this.selectedTable = []
      for (let item of selection) {
        this.selectedTable.push(item["username"])
      }
    },
    getList() {
      let url = server + "/admin/get_admin_list?start=" + this.start + "&end=" + this.end
      axios.get(url).then(res => {
        this.admin_total = res.data["total"]
        this.tableData = res.data["list"]
      })
    },
    prepareAdd() {
      this.resetForm()
      this.addDialogVisible = true
    },
    prepareEdit(item) {
      this.form = item
      this.editDialogVisible = true
    },
    confirmEditItem(form) {
      if (this.checkForm(form)) {
        this.$confirm("是否确认信息无误？").then(() => {
          let url = server + "/admin/edit_admin"
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
      if (!form["username"]) {
        this.$alert("请输入用户名")
        flag = false
      }
      if (!form["password"]) {
        this.$alert("请输入密码")
        flag = false
      }
      if (!form["name"]) {
        this.$alert("请输入姓名")
        flag = false
      }
      return flag
    },
    resetForm() {
      this.form = {
        username: "",
        name: "",
        gender: "男",
        college: "计算机科学与技术学院",
        password: "",
        email: ""
      }
    },
    getFormData(form) {
      let formData = new FormData()
      formData.append("username", form['username'])
      formData.append("name", form['name'])
      formData.append("gender", form['gender'])
      formData.append("college", form['college'])
      formData.append("email", form['email'])
      formData.append("password", form['password'])
      return formData
    },
    confirmAddItem(form) {
      if (this.checkForm(form)) {
        this.$confirm("是否确认信息无误？").then(() => {
          let url = server + "/admin/create_admin"
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
      this.$confirm(`确认要删除${form["username"]}`).then(() => {
        let url = server + "/admin/delete_admin"
        let formData = new FormData()
        formData.append("username", form["username"])
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
          let url = server + "/admin/delete_admin"
          let formData = new FormData()
          formData.append("username", this.selectedTable[i])
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
    }
  },
  components: { Password }
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
