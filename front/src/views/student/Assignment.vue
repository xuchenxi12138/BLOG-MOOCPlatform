<template>
    <div>
        <el-table :data="tableData" highlight-current-row stripe style="width: 100%" height="500px">
            <el-table-column type="index" width="50">
            </el-table-column>
            <el-table-column property="title" label="名称">
            </el-table-column>
            <el-table-column property="description" label="简介">
                <template slot-scope="scope">
                    <el-popover placement="top-start" title="简介" width="400" trigger="hover"
                        :content="scope.row.description">
                        <el-button slot="reference" class="el-icon-zoom-in" type="text"></el-button>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column property="deadline" label="截止日期">
            </el-table-column>
            <el-table-column property="score" label="分数">
            </el-table-column>
            <el-table-column property="finished" label="状态">
            </el-table-column>
            <el-table-column property="" label="操作" width="200">
                <template slot-scope="scope">
                    <el-button size="mini" type="primary" style="margin-top:5px;" @click="check(scope.row)">查看
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog :visible.sync="dialogVisible" title="查看" :before-close="handleClose" width="500px" top="10px">
            <el-form label-width="80px" label-position="left">
                <el-form-item label="标题">
                    <a>{{ form["title"] }}</a>
                </el-form-item>
                <el-form-item label="介绍">
                    <div>{{ form["description"] }}</div>
                </el-form-item>
                <el-form-item label="下载文件">
                    <a :href="form['q_file_url']">{{ form["q_file_id"] }}</a>
                </el-form-item>
                <el-form-item label="评语">
                    <div>{{ form["comment"] }}</div>
                </el-form-item>
                <el-form-item label="选择文件" >
                    <el-upload  :disabled="form['overdue']" :action="uploadFileServer" :on-success="uploadSuccess" :file-list="fileList" :limit="1">
                        <el-button type="primary" size="mini"  :disabled="form['overdue']">选择文件</el-button>
                    </el-upload>
                </el-form-item>
                <el-button @click="cancel">取消</el-button>
                <el-button type="primary" @click="submit"  :disabled="form['overdue']">提交</el-button>
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
            tableData: [],
            class_id: '',
            username: this.$store.state.username,
            uploadFileServer: server + "/file/upload_word",
            form: {},
            dialogVisible: false,
            fileList: [],
        }
    },
    created() {
        this.class_id = this.$route.query["class_id"]
        let url = server + "/student/get_all_assignments?username=" + this.username + "&class_id=" + this.class_id
        axios.get(url).then(res => {
            let data = res.data
            for (let item of data) {
                let now = new Date()
                let deadline = new Date(item["deadline"])
                item["finished"] = item["finished"] == true ? "已上传" : "待完成"
                item["overdue"] = now > deadline ? true : false
                item["score"] = item["score"] == 0 ? "未打分" : item["score"]
                item["q_file_url"] = server + "/file/word/" + item["q_file_id"]
                item["file_url"] = server + "/file/word/" + item["file_id"]
            }
            this.tableData = data
            console.log(this.tableData);
        })
    },
    methods: {
        submit() {
            if (this.fileList.length === 0) {
                this.$alert("请选择文件")
            } else {
                let url = server + "/student/hand_on_assignment"
                let formdata = new FormData()
                formdata.append("assignment_id", this.form["assignment_id"])
                formdata.append("file_id", this.form["file_id"])
                formdata.append("username", this.username)
                axios.post(url, formdata).then(res => {
                    this.$message(res.data)
                    this.dialogVisible = false;
                    let index=this.tableData.indexOf(this.form)
                    this.tableData[index]["file_id"]=this.form["file_id"]
                    this.fileList = []
                    this.form = {}
                })
            }
        },
        check(row) {
            console.log(row);
            this.form = row
            this.fileList = [{ name: row["file_id"] }]
            this.dialogVisible = true
        },
        cancel() {
            this.dialogVisible = false;
            this.form = {

            }
        },
        uploadSuccess(res) {
            this.form["file_id"] = res["url"]
            // this.fileList = [{
            //     name: res["url"]
            // }]
        },
        handleClose(){
            this.dialogVisible=false;
            this.form={}
            this.fileList=[]
        }
    },
}

</script>
<style scoped>
</style>
