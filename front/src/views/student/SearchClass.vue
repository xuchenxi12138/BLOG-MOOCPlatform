<template>
    <div>
        <div v-if="tableData.length != 0">
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
                            <el-button @click="join(scope.row)" type="primary" size="mini"
                                class="el-icon-reading">加入
                            </el-button>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <el-empty v-else></el-empty>
    </div>
</template>

<script>
import axios from 'axios'
import config from "@/config.json"
export default {
    name: 'SearchClass',
    data() {
        return {
            text: "",
            tableData: []
        }
    },
    created() {
        this.text = this.$route.query["text"]
        axios.get(config["server"] + "/student/search_class?text=" + this.text)
            .then(res => {
                console.log(res.data);
                this.tableData = res.data
            })
    },
    methods: {
        join(row){
            let username=sessionStorage.getItem("username")
            axios.get(config["server"]+"/student/join_class?username="+username+"&class_id="+row["class_id"])
            .then(res=>{
                this.$message(res.data)
            })
        }
    },
    watch:{
        $route(val){
            this.text=val.query["text"]
            axios.get(config["server"] + "/student/search_class?text=" + this.text)
            .then(res => {
                console.log(res.data);
                this.tableData = res.data
            })
        }
    }
}

</script>
<style scoped>
</style>
