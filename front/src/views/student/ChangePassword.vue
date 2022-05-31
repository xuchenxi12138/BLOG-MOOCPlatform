<template>
  <div class="change_password">
    <div style="width: 300px;margin:auto;padding: 20px;">
      <el-form label-position="left" label-width="80px" :model="form" :rules="rules">
        <el-form-item label="旧密码" prop="old_password">
          <el-input class="password" v-model="form['old_password']" type="password" @change="check"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input class="password" v-model="form['new_password']" type="password" @change="check"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input class="password" v-model="form['confirm_password']" type="password" @change="check"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submit" :disabled="!fitRule">确认修改</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import config from "@/config.json"
const server = config["server"]

export default {
  name: "ChangePassword",
  data() {
    let confirmNewPassword = (rule, value, callback) => {
      if (value !== this.form.new_password) {
        callback(new Error("前后密码不一致"))
      }
    };
    let checkNewPassword = (rule, value, callback) => {
      if (value.length < 8 || value.length > 18) {
        callback(new Error("密码必须在8到18位之间"))
      }
      if (value.search(/[a-z]|[A-Z]/) < 0 || value.search(/[0-9]/) < 0) {
        {
          callback(new Error("密码必须至少包含两种字符"))
        }
      }
      if (value === this.form.old_password) {
        callback(new Error("新密码不能与旧密码一致"))
      }

    }
    return {
      form: {
        old_password: '',
        new_password: '',
        confirm_password: ''
      },
      fitRule: false,
      rules: {
        old_password: [{ required: true, message: '旧密码不能为空' }],
        new_password: [{ required: true, message: '新密码不能为空' },
        { validator: checkNewPassword, trigger: 'blur' }
        ],
        confirm_password: [{ required: true, message: '请确认密码' },
        { validator: confirmNewPassword, trigger: 'blur' }
        ]
      },

    }
  },
  methods: {
    submit() {
      let username = sessionStorage.getItem("username")
      let formdata = new FormData()
      formdata.append("username", username)
      formdata.append("old_password", this.form["old_password"])
      formdata.append("new_password", this.form["new_password"])
      let url = server + "/student/change_password"
      axios.post(url, formdata).then(res => {
        this.$message(res.data)
        sessionStorage.setItem("password",this.form["new_password"])
      })
    },
    check(){
      this.fitRule=false
      if(this.form["old_password"]&&this.form["new_password"]&&this.form["confirm_password"]){
        if(this.form["new_password"].length>=8&&this.form["new_password"].length<=18){
          if(this.form['new_password'].search(/[a-z]|[A-Z]/)>=0&&this.form['new_password'].search(/[0-9]/)>=0)
          {
            if(this.form["new_password"]===this.form["confirm_password"]){
              this.fitRule=true;
            }
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.change_password {
  width: 1000px;
  background: #ffffff;
  /*padding: 1px;*/
  margin: auto;
  height: 100%;
}

.password {
  width: 250px;
}
</style>