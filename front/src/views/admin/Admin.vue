<template>
 <div>
    <el-container>
      <el-aside width="200px" style="background-color: #545c64;">
        <div class="menu">
          <router-link to="/admin">
            <span>首页设置</span>
          </router-link>
          <router-link to="/admin/TeacherManagement">
            <span>教师管理</span>
          </router-link>

          <router-link to="/admin/StudentManagement">
            <span>学生管理</span>
          </router-link>
          <router-link to="/admin/ClassManagement">
            <span>班级管理</span>
          </router-link>
          <router-link to="/admin/LessonManagement">
            <span>课程管理</span>
          </router-link>
        <router-link to="/admin/AdminManagement" v-if="identification=='super_admin'">
          <span>管理员</span>
        </router-link>
      </div>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
 </div>
</template>

<script>
export default {
  name:'AminView',
  data () {
    return {
      identification:""
    }
  },
  created(){
    console.log(this.$store.state.identification);
    if (this.$store.state.identification=="admin") {
      this.identification=this.$store.state.identification
      console.log("已经登录");
    } else {
      this.$router.push("/")
    }
  },
  methods:{
  },
}

</script>
<style scoped>
.menu {
  display: flex;
  flex-direction: column;
  background-color: #545c64;
  width: 100%;
  height: 100%;
}
.menu a{
  line-height:60px;
  color: #ffffff;
  text-decoration: none;
  font-size: 18px;
  font-weight: 600;
  transition: background-color .5s;
}
.menu a:hover{
  cursor: pointer;
  background-color: #434a50;

}
.menu  a.router-link-exact-active{
   color: #42b983;
 }
</style>
