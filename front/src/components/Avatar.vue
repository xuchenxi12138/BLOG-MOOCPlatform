<template>
    <div>
        <div v-if="logged" style="display:flex;align-items:center;">

            <div class="avatar">
                <router-link :to="myspace">
                    <img :src="this.$store.state.avatar" alt="" />
                </router-link>
            </div>
            <el-dropdown @command="handleCommand">
                <span class="el-dropdown-link">
                    <i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                    <!-- <router-link to="/MyChat" style="text-decoration: none">
                        <el-dropdown-item>
                            <a>消息</a>
                        </el-dropdown-item>
                    </router-link>
                    <router-link :to="identification + '/PersonalInformation'" style="text-decoration: none">
                        <el-dropdown-item divided>修改信息</el-dropdown-item>
                    </router-link> -->
                    <el-dropdown-item divided v-if="identification=='student'" command="join">
                        <a >加入班级</a>
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                        <a  >注销</a>
                    </el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
        <el-button type="text" style="font-size:20px" @click="preLogin" v-else>登录</el-button>
        <el-dialog :visible.sync="loginDialogVisible" width="400px" title="登录">
            <div style="width: 100%;height: 60px;">
                <el-avatar :size="50" :src="avatarImage"></el-avatar>
            </div>
            <el-form label-width="80px" label-position="left">
                <el-form-item label="用户名">
                    <el-input v-model="username" @blur="getAvatar" @keydown.enter.native="onSubmit" @change="getAvatar">
                    </el-input>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input v-model="password" type="password" @keydown.enter.native="onSubmit"></el-input>
                </el-form-item>
                <el-radio-group v-model="identification_zh">
                    <el-radio-button label="学生"></el-radio-button>
                    <el-radio-button label="教师"></el-radio-button>
                    <el-radio-button label="管理员"></el-radio-button>
                </el-radio-group>
                <br>
                <br>
                <div>
                    <el-button type="primary" @click="onSubmit">登录</el-button>
                    <el-button @click="cancel">取消</el-button>
                </div>
            </el-form>
        </el-dialog>
        <el-dialog :visible.sync="dialogVisible2" width="400px" title="请输入班级码">
            <el-form label-position="left" lable-width="80px">
                <el-form-item label="班级号">
                    <el-input v-model="form['class_id']" @change="getClassById"></el-input>
                </el-form-item>
                <el-form-item label="班级名称">
                    <el-input v-model="form['class_name']" @change="getClassByName"></el-input>
                </el-form-item>
                <el-form-item label="学院">
                    <el-input v-model="form['college']" disabled></el-input>
                </el-form-item>
            </el-form>
            <br><br>
            <el-row type="flex" justify="space-between" style="width: 100%;">
                <el-col>
                    <el-button @click="dialogVisible2 = false">取消</el-button>
                </el-col>
                <el-col>
                    <el-button type="primary">确定</el-button>
                </el-col>
            </el-row>
        </el-dialog>
    </div>
</template>

<script>
import axios from "axios"
import config from "@/config.json"
export default {
    name: 'AvatarModule',
    data() {
        return {
            form: {
                class_id: "",
                class_name: "",
                college: ""
            },
            myspace: '',
            logged: "",
            dialogVisible: false,
            dialogVisible2: false,
            username: '',
            password: "",
            identification: "student",
            identification_zh: "学生",
            avatarImage: '',
            avatarSize: 50,
            avatarList: {
                "boy.svg": require("/src/assets/Avatars/boy.svg"),
                "cat.png": require("/src/assets/Avatars/cat.png"),
                "doctor.svg": require("/src/assets/Avatars/doctor.svg"),
                "dog.svg": require("/src/assets/Avatars/dog.svg"),
                "girl.svg": require("/src/assets/Avatars/girl.svg"),
                "github.svg": require("/src/assets/Avatars/github.svg"),
                "men.svg": require("/src/assets/Avatars/men.svg"),
                "women.svg": require("/src/assets/Avatars/women.svg"),
            },
            loginDialogVisible:false
        }
    },
    created() {
        this.username = sessionStorage.getItem("username")
        this.password = sessionStorage.getItem("password")
        this.identification = sessionStorage.getItem("identification")
        if (this.identification === "")
            this.identification = "student"
        this.$store.state.username = this.username
        this.$store.state.password = this.password
        this.$store.state.identification = this.identification
        this.setMySpace(this.identification)
        if (this.username) {
            this.logged = true
            this.getAvatar()
            this.$store.state.avtar = this.avatarImage;
        }
    },
    methods: {
        onSubmit() {
            if (this.username) {
                if (this.password) {
                    let url = config["server"] + "/login?username=" + this.username + "&password=" + this.password + "&identification=" + this.identification;
                    axios.get(url).then(res => {
                        if (res.data["result"] === "success") {
                            this.setMySpace(this.identification)
                            sessionStorage.setItem("username", this.username)
                            sessionStorage.setItem("password", this.password)
                            sessionStorage.setItem("identification", this.identification)
                            this.$store.state.username = this.username
                            this.$store.state.password = this.password
                            this.$store.state.identification = this.identification
                            this.getAvatar()
                            this.logged = true
                            this.loginDialogVisible = false
                            this.$router.push(this.myspace)
                        }
                        this.$message({
                            message: res.data["message"],
                            type: res.data["type"]
                        })
                    })
                }
                else {
                    this.$message({
                        message: "请输入密码",
                        type: "warning"
                    })
                }

            } else {
                this.$message({
                    message: "请输入账号",
                    type: "warning"
                })
            }
        },
        getAvatar() {
            let url = config["server"] + "/get_avatar?username=" + this.username + "&identification=" + this.identification
            if (this.username) {
                axios.get(url).then(res => {
                    console.log(res.data);
                    this.avatarImage = this.avatarList[res.data["avatar"]]
                    this.$store.state.avatar = this.avatarImage
                    this.$store.state.name = res.data["name"]
                    this.$store.state.signature = res.data["signature"]
                })
            }
        },
        logout() {
            this.username = ''
            this.password = ''
            this.identification = 'student'
            this.identification_zh = '学生'
            this.$store.state.username = ''
            this.$store.state.password = ''
            this.$store.state.identification = 'student'
            this.logged = false
            sessionStorage.setItem("username", "")
            sessionStorage.setItem("password", "")
            sessionStorage.setItem("identification", "student")
            this.$router.push("/")
        },
        setMySpace(key) {
            switch (key) {
                case "student":
                    this.myspace = "/Student";
                    break;
                case "teacher":
                    this.myspace = "/Teacher";
                    break;
                case "admin":
                    this.myspace = "/Admin";
                    break;
                default:
                    break;
            }
        },
        preLogin() {
            this.username = ""
            this.password = ""
            this.identification_zh = "学生"
            this.identification = "student"
            this.loginDialogVisible = true;
        },
        cancel() {
            this.loginDialogVisible = false;
        },
        getClassById(id) {
            axios.get(config["server"] + "/student/get_class_by_id?class_id=" + id)
                .then(res => {
                    if (res.data.message["type"] === "success") {
                        this.form = res.data["class_info"]
                    } else {
                        this.$message(res.data["message"])
                    }

                })
        },
        getClassByName(name) {
            axios.get(config["server"] + "/student/get_class_by_name?class_name=" + name)
                .then(res => {
                    if (res.data.message["type"] === "success") {
                        this.$notify({
                            title: '找到这些班级',
                            duration: 0,
                            type: 'success',
                            dangerouslyUseHTMLString: true,
                            message: res.data["class_info"]
                        });
                    } else {
                        this.$message(res.data["message"])
                    }
                })
        },
        handleCommand(command){
            switch (command) {
                case "join":
                    this.dialogVisible2=true;
                    break;
                case "logout":
                    this.logout();
                    break;
                default:
                    break;
            }
        }
    },
    mounted() {

    },
    watch: {
        identification_zh(val) {
            switch (val) {
                case "学生":
                    this.identification = "student";
                    break;
                case "教师":
                    this.identification = "teacher"
                    break;
                case "管理员":
                    this.identification = "admin"
                    break;
                default:
                    break;
            }
            console.log(this.identification);
            this.getAvatar()
        }
    }
}

</script>
<style scoped>
.avatar {
    width: 60px;
    /* height: 60px; */
    border-radius: 50%;

}

.avatar img {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background-color: #aaaaaa;
    transition: 0.1s;
}

.avatar img:hover {
    width: 55px;
    height: 55px;
    border-radius: 50%;
}
</style>
