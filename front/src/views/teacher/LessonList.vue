<template>
 <div>
     <el-table :data="tableData" stripe style="width: 100%" height="500">
            <el-table-column type="index" label="序号">
            </el-table-column>
            <el-table-column prop="lesson_id" label="课程号">
            </el-table-column>
            <el-table-column prop="lesson_name" label="课程名">
            </el-table-column>
            <el-table-column prop="college" label="学院">
            </el-table-column>
            <el-table-column label="操作" width="280">
                <template slot-scope="scope">
                    <el-button @click="Edit(scope.row)" type="warning" size="small" class="el-icon-edit">修改课程</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination layout="prev, pager, next,jumper" :total="total" :hide-on-single-page="false" :page-size="20"
            @current-change="handleCurrenChange"></el-pagination>
 </div>
</template>

<script>
import axios from "axios"
import config from "@/config.json"
const server = config["server"]
export default {
  name:'LessonList',
  data () {
    return {
        tableData:[],
        username:"",
        total:0,
        start:0,
    }
  },
  created(){
      this.$store.state.routerList=[{
            name:"课程管理",
            path:"/Teacher/LessonManagement"
        },{
            name:"课程列表"
        }]
    this.username=this.$store.state.username
    this.getLessonList()
  },
  methods:{
      getLessonList(){
          let url=server+"/teacher/get_lesson_list?username="+this.username+"&start="+this.start
          axios.get(url).then(res=>{
              console.log(res.data);
              this.tableData=res.data["list"]
              this.total=res.data["total"]
          })
      },
      handleCurrenChange(page) {
            this.start = (page - 1) * 10;
            this.end = this.start + 10;
            // console.log(`当前页：${page}`);
            this.getLessonList()
        },
      Edit(row){
          console.log(row);
          let path="/Teacher/LessonManagement/EditLesson?lesson_id="+row["lesson_id"]
          this.$router.push(path)
      }
  },
}

</script>
<style scoped>
</style>
