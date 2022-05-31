<template>
    <div>
        <el-row type="flex" justify="space-between">
            <el-col>
                <el-page-header @back="goBack">
                </el-page-header>
            </el-col>
        </el-row>
        <el-table :data="tableData" highlight-current-row stripe style="width: 100%" height="500px">
            <el-table-column type="index" width="50">
            </el-table-column>
            <el-table-column property="student_id" label="学号">
            </el-table-column>
            <el-table-column property="name" label="姓名">
            </el-table-column>
            <el-table-column property="title" label="作业题目">
            </el-table-column>
            <el-table-column property="score" label="分数">
            </el-table-column>
            <el-table-column property="post_time" label="发布日期">
            </el-table-column>
            <el-table-column property="hand_on_time" label="提交日期">
            </el-table-column>
            <el-table-column property="" label="操作" width="200">
                <template slot-scope="scope">
                    <a :href="scope.row.file_url" v-if="scope.row.file_url"><i class="el-icon-download" ></i>下载文件</a>
                    <el-button size="mini" type="warning" class="el-icon-edit" @click="preCheck(scope.row)">打分
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog title="打分" :before-close="handleClose" :visible.sync="dialogVisible" top="10px">
            <el-form :model="form" label-position="left" label-width="80px">
                <el-form-item label="学号" prop="student_id">
                    <el-input v-model="form['student_id']" disabled></el-input>
                </el-form-item>
                <el-form-item label="姓名" prop="name">
                    <el-input v-model="form['name']" disabled></el-input>
                </el-form-item>
                <el-form-item label="作业标题" prop="title">
                    <el-input v-model="form['title']" disabled></el-input>
                </el-form-item>
                <el-form-item label="分数" prop="score">
                    <el-input v-model="form['score']"></el-input>
                </el-form-item>
                <el-form-item label="评语" prop="comment">
                    <el-input v-model="form['comment']" type="textarea"
                    :autosize="{ minRows: 7}"></el-input>
                </el-form-item>
            </el-form>
            <el-row>
                <el-button @click="dialogVisible=false">稍后</el-button>
                <el-button type="primary" @click="check">提交</el-button>
            </el-row>
        </el-dialog>
    </div>
</template>

<script>
import config from "@/config.json"
import axios from "axios"
const server = config["server"]
export default {
    name: 'AssignmentDone',
    data() {
        return {
            class_id: "",
            tableData: [],
            form: {},
            dialogVisible: false
        }
    },
    created() {
        this.class_id = this.$route.query["class_id"]
        this.$store.state.routerList = [{
            path: '/Teacher/ClassManagement',
            name: "班级列表"
        }, {
            path: '/Teacher/ClassManagement/Assignments?class_id=' + this.class_id,
            name: "作业记录",
        }, {
            name: "新提交的作业",
        }]
    },
    methods: {
        goBack() {
            this.$router.push("/Teacher/ClassManagement/Assignments?class_id=" + this.class_id)
        },
        preCheck(row) {
            this.form = row
            this.dialogVisible = true;
        },
        check() {
            let url =server+"/teacher/check_assignment"
            let formdata=new FormData()
            formdata.append("assignment_id",this.form["assignment_id"])
            formdata.append("score",this.form["score"])
            formdata.append("comment",this.form["comment"])
            formdata.append("student_id",this.form["student_id"])
            axios.post(url,formdata).then(res=>{
                this.dialogVisible=false
                this.$message(res.data)
            })
        },
        handleClose() {
            this.form = {}
            this.dialogVisible=false
        }
    },
    mounted(){
        let url=server+"/teacher/get_new_hand_on?class_id="+this.class_id
        axios.get(url).then(res=>{
            let data=res.data
            for (let item of data){
                if(item["file_id"]){
                    item["file_url"]=server+"/file/word/"+item["file_id"]
                }else{
                    item["file_url"]=""
                }
            }
            this.tableData=data
        })
    }
}

</script>
<style scoped>
</style>
