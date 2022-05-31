<template>
    <div>
        <div class="header_menu">
            <div class="button-group">
                <el-button type="primary" size="small" @click="prepareAdd" class="el-icon-plus">添加
                </el-button>
                <el-button type="danger" size="small" class="el-icon-delete" @click="delItems">批量删除</el-button>
                <el-button size="small" class="el-icon-document" type="success" @click="tableDialogVisible = true">导入
                </el-button>
            </div>

            <div style="display:flex;">
                <el-select v-model="college" placehoder="请选择学院" filterable style="width: 100%;">
                    <el-option v-for="item in college_options" :key="item" :value="item"></el-option>
                </el-select>
                <el-input v-model="text" @keydown.native.enter="getList">
                    <el-button slot="append" @click="getList">搜索</el-button>
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
        <el-pagination layout="prev, pager, next,jumper" :total="teacher_total" :hide-on-single-page="false"
            :page-size="10" @current-change="handleCurrenChange"></el-pagination>
        <el-dialog :visible.sync="addDialogVisible" width="400px" title="添加" top="10px">
            <el-form label-width="40px" label-position="left" :model="form">
                <el-form-item label="工号">
                    <el-input v-model="form['username']"></el-input>
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
        <transition name="el-zoom-in-top">
            <div class="dialog" v-if="tableDialogVisible">
                <div class="dialog_inner">
                    <h1>按表格上传</h1>
                    <input type="file" @change="readTable" />
                    <el-table :data="upload_table" height="400px" border>
                        <el-table-column type="index" label="编号" width="55"></el-table-column>
                        <el-table-column prop="username" label="工号">
                            <template slot-scope="scope">
                                <input v-model="scope.row.username" class="upload-table-input" />
                                <el-link :type="scope.row.type">{{scope.row.message}}</el-link>
                            </template>
                        </el-table-column>
                        <el-table-column prop="name" label="姓名">
                            <template slot-scope="scope">
                                <input v-model="scope.row.name" class="upload-table-input" />
                                
                            </template>
                        </el-table-column>
                        <el-table-column prop="name" label="性别">
                            <template slot-scope="scope">
                                <el-select v-model="scope.row.gender">
                                  <el-option  label="男" value="男"></el-option>
                                  <el-option  label="女" value="女"></el-option>
                                </el-select>
                            </template>
                        </el-table-column>
                        <el-table-column prop="college" label="学院">
                            <template slot-scope="scope">
                                <input v-model="scope.row.college" class="upload-table-input" />
                            </template>
                        </el-table-column>
                        <el-table-column prop="email" label="邮箱">
                            <template slot-scope="scope">
                                <input v-model="scope.row.email" class="upload-table-input" />
                            </template>
                        </el-table-column>
                        <el-table-column prop="password" label="密码">
                            <template slot-scope="scope">
                                <form>
                                    <el-input v-model="scope.row.password" show-password></el-input>
                                </form>
                            </template>
                        </el-table-column>
                        <el-table-column label="操作" width="50px">
                            <template slot-scope="scope">
                                <el-button type="text" @click="deleteItem(scope.row)" class="el-icon-close"></el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div>
                        <el-button @click="tableDialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="submit" :diabled="upload_table.length == 0">提交
                        </el-button>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
import Password from "@/components/Password.vue"
import AHU from "@/js/college"
import config from "@/config.json"
import axios from "axios"
const server = config["server"]
import ReadTable from "@/js/ReadTable.js";
export default {
    name: "TeacherMangement",
    data() {
        return {
            tableData: [
            ],
            teacher_total: 0,
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
            tableDialogVisible: false,
            upload_table: [],
            college: "计算机科学与技术学院",
            text: "",
            uploadTableUrl: server + "/file/read_teacher_excel"
        };
    },
    created() {
        this.getList()
    },
    methods: {
        readTable(event) {
            ReadTable.readTeacherTable(event)
                .then(res => {
                    this.upload_table = res

                    this.tableDialogVisible = true;
                }).catch(res => {
                    this.$alert(res)
                });

        },
        submit() {
            let flag = true
            for (let item of this.upload_table) {
                if (!this.checkForm(item)) {
                    flag = false
                    break;
                }
            }
            if (flag) {
                let formdata = new FormData()
                let data = JSON.stringify(this.upload_table)
                formdata.append("data", data)
                let url = server + "/admin/upload_teacher_table"
                axios.post(url, formdata).then(
                    res => {
                        this.upload_table=res.data
                    }
                )
            }
        },
        search() {
            this.start = 0;
            this.end = 10; this.getList()
        },
        cancel() {
            this.getList()
            this.editDialogVisible = false
            this.addDialogVisible = false
            this.resetForm()
        },
        handleCurrenChange(page) {
            this.start = (page - 1) * 10;
            this.end = this.start + 20;

            this.getList()
        },
        changeSelection(selection) {
            this.selectedTable = []
            for (let item of selection) {
                this.selectedTable.push(item["username"])
            }
        },
        getList() {
            let url = server + "/admin/get_teacher_list?college=" + this.college + "&text=" + this.text + "&start=" + this.start + "&end=" + this.end
            axios.get(url).then(res => {
                this.teacher_total = res.data["total"]
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
                    let url = server + "/admin/edit_teacher"
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
                this.$message(`请输入${form['name']}的用户名`)
                flag = false
            } else
                if (!form["password"]) {
                    this.$message(`请输入${form['username']}${form['name']}的密码`)
                    flag = false
                } else
                    if (!form["name"]) {
                        this.$message(`请输入${form['username']}的姓名`)
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
                    let url = server + "/admin/create_teacher"
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
                let url = server + "/admin/delete_teacher"
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
                    let url = server + "/admin/delete_teacher"
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
        },
        uploadSuccess(res) {
            this.upload_table = res
        },
        deleteItem(row){
            let index=this.upload_table.indexOf(row)
            this.upload_table.splice(index,1)
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

.upload_file_button {
    width: 84px;
    height: 40px;
    background-color: #67c23a;
    margin: auto 10px;
    border-radius: 5px;
    position: relative;
    cursor: pointer;
}

.upload_file_button input {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    opacity: 0;
    cursor: pointer;
}

.button-group {
    display: flex;
    align-items: center;
    width: 250px;
    justify-content: space-between;
    /* grid-template-columns: 100px 100px 100px 100px; */
}

.dialog {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #00000080;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
}

.dialog_inner {
    background-color: #ffffff;
    width: 100%;
    max-width: 1000px;
    height: 550px;
    padding: 10px;
}

.upload-table-input {
    width: 100%;
    height: 100%;
    height: 40px;
    outline: none;
    border: 1px solid #ffffff00;
    background-color: #ffffff00;
    border-radius: 3px;
}

.upload-table-input:hover {
    background-color: #00000010;
}

.upload-table-input:focus {
    border: 1px solid #409EFF;
}
</style>
