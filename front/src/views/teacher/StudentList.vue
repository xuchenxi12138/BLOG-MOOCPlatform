<template>
    <div>
        <el-row type="flex" justify="space-between">
            <el-col>
                <el-page-header @back="goBack" :content="class_name">
                </el-page-header>
            </el-col>
            <el-button type="primary" @click="dialogVisible = true">添加</el-button>
        </el-row>
        <el-table :data="tableData" stripe style="width: 100%;margin-top: 10px;" height="500">
            <el-table-column type="index" label="序号">
            </el-table-column>
            <el-table-column prop="username" label="学号">
            </el-table-column>
            <el-table-column prop="name" label="姓名">
            </el-table-column>
            <el-table-column prop="gender" label="性别">
            </el-table-column>
            <el-table-column prop="college" label="学院">
            </el-table-column>
            <el-table-column label="操作" width="280">
                <template slot-scope="scope">
                    <el-button @click="detail(scope.row['username'])" type="primary" size="small" class="el-icon-document">更多
                    </el-button>
                    <el-button @click="del(scope.row)" type="danger" size="small" class="el-icon-delete">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog :visible.sync="dialogVisible" width="400px" title="添加">
            <el-form :model="form" label-width="80px" label-position="left">
                <el-form-item prop="username" label="学号">
                    <el-input v-model="form.username">
                        <template slot="append">
                            <i class="el-icon-refresh" @click="getStudent(form.username)">
                            </i>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="name" label="姓名">
                    <el-input v-model="form.name">
                        <template slot="append">
                            <i class="el-icon-refresh" @click="getStudentByName(form.name)">
                            </i>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="college" label="学院">
                    <el-input v-model="form.college" disabled></el-input>
                </el-form-item>
                <el-form-item prop="email" label="邮箱">
                    <el-input v-model="form.email" disabled></el-input>
                </el-form-item>
            </el-form>
            <el-row>
                <el-button>取消</el-button>
                <el-button type="primary" @click="submit(form)">提交</el-button>
            </el-row>
        </el-dialog>
    </div>
</template>

<script>
import axios from 'axios'
import config from "@/config.json"
const server = config["server"]

export default {
    name: 'StudentList',
    data() {
        return {
            ClassName: '',
            class_id: "",
            class_name: "",
            tableData: [],
            dialogVisible: false,
            form: {
                username: "",
                name: "",
                college: "",
                email: ""
            }
        }
    },
    created() {
         
        this.class_id = this.$route.query["class_id"]
        this.class_name = this.$route.query["class_name"]
        let url=server+"/teacher/get_students?class_id="+this.class_id
        axios.get(url).then(res=>{
            this.tableData=res.data["student_list"]
            this.class_name=res.data["class_name"]
        })
        this.$store.state.routerList=[{
            path:'/Teacher/ClassManagement',
            name:"班级列表"
        },{
            name:"学生列表"
        }]
    },
    methods: {
        goBack() {
            this.$router.push("/Teacher/ClassManagement")
        },
        getStudent(username) {
            let url = server + "/teacher/get_student_by_id?username=" + username
            axios.get(url).then(res => {
                if (res.data["type"] === "success") {
                    let data = res.data["data"]
                    this.form["name"] = data["name"]
                    this.form["college"] = data["college"]
                    this.form["email"] = data["email"]
                }
                else {
                    this.$message(res.data)
                    this.form["name"] = ""
                    this.form["college"] = ""
                    this.form["email"] = ""
                }

            })
        },
        getStudentByName(name) {
            let url = server + "/teacher/get_student_by_name?name=" + name
            axios.get(url).then(res => {
                if (res.data["type"] === "success") {
                    let data = res.data["data"]

                    for (let i = 0; i < data.length; i++) {
                        setTimeout(() => {
                            this.$notify({
                                title: data[i]["name"],
                                dangerouslyUseHTMLString: true,
                                message: `学号：<em style="color: #67C23A;">${data[i]['username']}</em><br>学院：${data[i]['college']}<br>邮箱：${data[i]['email']}<br>`,
                                duration: 0
                            })
                        }, 500 * i);
                    }
                }
                else {
                    this.$message(res.data)
                }

            })
        },
        submit(form) {
            if (form["username"]) {
                console.log(form);
                let url = server + "/teacher/add_student"
                let formdata = new FormData()
                formdata.append("class_id", this.class_id)
                formdata.append("username", form["username"])
                axios.post(url, formdata).then(res => {
                    if (res.data["type"] === "success") {
                        this.dialogVisible = false
                        this.tableData.push(form)
                        this.form = {
                            username: "",
                            name: "",
                            college: "",
                            email: ""
                        }
                    }
                    this.$message(res.data)
                })
            }
            else {
                this.$alert("请输入学生的学号！")
            }
        },
        del(row){
            let url=server+"/teacher/delete_student?class_id="+this.class_id+"&username="+row["username"]
            this.$confirm(`您确定要删除${row["username"]}${row["name"]}?`).then(()=>{
                axios.get(url).then(res=>{
                    if(res.data["type"]==="success"){
                        let index=this.tableData.indexOf(row)
                        this.tableData.splice(index,1)
                        this.$message(res.data)
                    }
                    this.$message(res.data)
                })
            })
        },
        detail(username){
            this.$router.push("/Teacher/ClassManagement/StudentList/StudentDetail?student_id="+username+"&class_id="+this.class_id)
        },
    },
}

</script>
<style scoped>
</style>
