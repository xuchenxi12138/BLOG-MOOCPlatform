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
                    <div style="margin-top: 5px;">
                        <el-button @click="gotoLesson(scope.row)" type="primary" size="mini" class="el-icon-reading">课程
                    </el-button>
                    <el-badge :value="scope.row.messageNumber" :hidden="!scope.row.messageNumber" style="margin: 5px;">
                        <el-button @click="Assignment(scope.row)" size="mini" class="el-icon-files">作业
                        </el-button>
                    </el-badge>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import config from "@/config.json"
import axios from "axios"
const server = config["server"]
export default {
    name: 'ClassList',
    data() {
        return {
            username:"",
            tableData:[]
        }
    },
    created() {
        this.username=sessionStorage.getItem("username")
    },
    methods: {
        Chat(){
            
        },
        Assignment(row){
            let class_id=row["class_id"]
            this.$router.push("/Student/Assignment?class_id="+class_id)
        },
        gotoLesson(row){
            console.log(row);
            if(row["lesson_id"]){
                this.$router.push("/Lesson?lesson_id="+row["lesson_id"])
            }
            else{
                this.$message("抱歉任课教师没有选择课程")
            }
        }
    },
    mounted(){
        let url=server+"/student/get_class_list?username="+this.username
        axios.get(url).then(res=>{
            this.tableData=res.data
        })
    }
}

</script>
<style scoped>
</style>
