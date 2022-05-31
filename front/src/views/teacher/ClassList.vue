<template>
    <div>
        <el-table :data="tableData" stripe style="width: 100%" height="500">
            <el-table-column type="index" label="序号">
            </el-table-column>
            <el-table-column prop="class_id" label="班级号">
            </el-table-column>
            <el-table-column prop="class_name" label="班级名">
            </el-table-column>
            <el-table-column prop="college" label="学院">
            </el-table-column>
            <el-table-column prop="lesson_id" label="课程id">
            </el-table-column>
            <el-table-column prop="lesson_name" label="课程名称">
            </el-table-column>
            <el-table-column label="操作" width="280">
                <template slot-scope="scope">
                    <el-button @click="Edit(scope.row)" type="text" size="small" class="el-icon-edit">编辑</el-button>
                    <!-- <el-button @click="Chat(scope.row)" type="text" size="small" class="el-icon-chat-line-round">班级群
                    </el-button> -->
                    <el-button @click="StudentList(scope.row)" type="text" size="small" class="el-icon-document">学生名单
                    </el-button>
                    <el-badge :value="scope.row.messageNumber" :hidden="!scope.row.messageNumber" is-dot>
                        <el-button @click="Assignment(scope.row)" type="text"  size="small" class="el-icon-files">作业
                    </el-button>
                    </el-badge>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog :visible.sync="dialogVisible" width="400px">
            <el-form :model="rowData" label-width="80px" label-position="left">
                <el-form-item prop="class_id" label="班级id">
                    <el-input v-model="rowData['class_id']" disabled></el-input>
                </el-form-item>
                <el-form-item prop="class_name" label="班级名称">
                    <el-input v-model="rowData['class_name']"></el-input>
                </el-form-item>
                <el-form-item prop="college" label="学院">
                    <el-input v-model="rowData['college']" disabled></el-input>
                </el-form-item>
                <el-form-item prop="lesson_id" label="课程id">
                    <el-input v-model="rowData['lesson_id']" @change="getLessonName"></el-input>
                </el-form-item>
                <el-form-item prop="lesson_name" label="课程名称">
                    <el-input v-model="rowData['lesson_name']" disabled></el-input>
                </el-form-item>
            </el-form>
            <el-row>
                <el-button>取消</el-button>
                <el-button type="primary" @click="confirm">确定</el-button>
            </el-row>
        </el-dialog>
        
    </div>
</template>

<script>
import axios from "axios"
import config from "@/config.json"
const server = config["server"]
export default {
    name: 'ClassList',
    data() {
        return {
            tableData: [],
            rowData: [],
            dialogVisible: false,
            AssignDialogVisible: false
        }
    },
    created() {
         this.$store.state.routerList=[{
            name:"班级列表"
        }]
        this.getClasses()
    },
    methods: {
        getClasses() {
            let url = server + "/teacher/get_classes?username=" + this.$store.state.username
            axios.get(url).then(res => {
                this.tableData = res.data
                console.log(this.tableData);
            })
        },
        Edit(value) {
            this.rowData = value
            this.dialogVisible = true;
        },
        getLessonName(id) {
            console.log(id);
            let url = server + "/teacher/get_lesson_name?lesson_id=" + id
            axios.get(url).then(res => {
                if (res.data["type"] === 'success') {
                    this.rowData["lesson_name"] = res.data["lesson_name"]
                } else {
                    this.$message(res.data)
                    this.rowData["lesson_name"] = ""
                }
            })
        },
        confirm() {
            let url = server + "/teacher/edit_class"
            let formdata = new FormData()
            formdata.append("class_id", this.rowData["class_id"])
            formdata.append("class_name", this.rowData["class_name"])
            formdata.append("lesson_id", this.rowData["lesson_id"])
            axios.post(url, formdata).then(res => {
                if (res.data["type"] === "success") {
                    this.dialogVisible = false
                    this.$message(res.data)
                    this.rowData = {}
                } else {
                    this.$message(res.data)
                }
            })
        },
        Chat(row) {
            console.log(row);
        },
        StudentList(row) {
            let path = "/Teacher/ClassManagement/StudentList?class_id=" + row["class_id"]
            this.$router.push(path)
        },
        Assignment(row) {
            let class_id=row.class_id
            this.$router.push("/Teacher/ClassManagement/Assignments?class_id="+class_id)
        }
    },
    
}

</script>
<style scoped>
.dialog {
    width: 100vw;
    height: 100vh;
    position: fixed;
    top: 0;
    width: 0;
    background-color: #00000080;
    z-index: 10000;
}

.dialog_inner {
    width: 80%;
    min-width: 520px;
    margin: auto;
}
</style>
