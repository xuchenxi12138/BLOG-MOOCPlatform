<template>
    <div class="personal-info">
        <div style="display: flex;justify-content: space-between;padding: 5px;">
            <div class="title">基本信息</div>
            <router-link to="/teacher/ChangePassword" class="link">修改密码</router-link>
        </div>

        <div class="content">
            <el-form label-width="70px" label-position="left" :model="form" style="width: 900px;">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="工号">
                            <el-input v-model="form['username']" disabled></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="姓名">
                            <el-input v-model="form['name']" disabled></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">

                    <el-col :span="12">
                        <el-form-item label="昵称">
                            <el-input v-model="form['nickname']" :disabled="disable_change"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="性别">
                            <el-select v-model="form['gender']" value="男" :disabled="disable_change">
                                <el-option label="男" value="男"></el-option>
                                <el-option label="女" value="女"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>

                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="手机">
                            <el-input v-model="form['phone_number']" :disabled="disable_change"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="邮箱">
                            <el-input v-model="form['email']" :disabled="disable_change"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">

                    <el-col :span="12">
                        <el-form-item label="学院">
                            <el-select v-model="form['college']" :disabled="disable_change">
                                <el-option v-for="item in college_options" :key="item" :label="item"
                                    :value="item"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="研究方向">
                            <el-input v-model="form['major']" :disabled="disable_change"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="8">
                        <el-form-item label="当前学历">
                            <el-select v-model="form['degree']" placeholder="请选择" :disabled="disable_change">
                                <el-option label="本科" value="bachelor"></el-option>
                                <el-option label="硕士" value="master"></el-option>
                                <el-option label="博士" value="doctor"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="入职年月">
                            <el-date-picker v-model="form['entrance_date']" type="date" placeholder="选择日期"
                                value-format="yyyy-MM-dd" :disabled="disable_change">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="生日">
                            <el-date-picker v-model="form['birthday']" type="date" placeholder="选择日期"
                                value-format="yyyy-MM-dd" :disabled="disable_change">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>

        </div>
        <el-dropdown trigger="click" @command="changeAvatar" :disabled="disable_change">
            <el-button type="text" :disabled="disable_change">
                选择头像<i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item v-for="img in avatar_list" :key="img" :command="img">
                    <img :src="require('/src/assets/Avatars/' + img)" style="height: 20px;">
                </el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
        <img class="avatar" :src="avatar" />
        <div class="footer">
            <el-button type="primary" @click="prepare" v-if="disable_change">修改</el-button>
            <el-button type="" @click="cancel" v-else>取消</el-button>
            <el-button type="danger" v-if="!disable_change" @click="submit(form)">提交</el-button>
            <el-button type="info" v-else disabled>提交</el-button>
        </div>
    </div>
</template>

<script>
import axios from "axios"
import config from "@/config.json"
const server = config["server"]
import AHU from "@/js/college"
export default {
    name: "MyInfo",
    data() {
        return {
            college_options: AHU["college_options"],
            avatar: '',
            date:'',
            form: {
                username: '',
                name: '',
                college: '',
                nickname: '',
                phone_number: '',
                email: '',
                birthday: '',
                major: '',
                degree: '',
                entrance_date: '',
                avatar: ''
            },
            disable_change: true,
            avatar_list: [
                "boy.svg", "cat.png", "doctor.svg", "dog.svg", "girl.svg", "github.svg", "men.svg", "women.svg"
            ],
            avatarList: {
                "boy.svg": require("/src/assets/Avatars/boy.svg"),
                "cat.png": require("/src/assets/Avatars/cat.png"),
                "doctor.svg": require("/src/assets/Avatars/doctor.svg"),
                "dog.svg": require("/src/assets/Avatars/dog.svg"),
                "girl.svg": require("/src/assets/Avatars/girl.svg"),
                "github.svg": require("/src/assets/Avatars/github.svg"),
                "men.svg": require("/src/assets/Avatars/men.svg"),
                "women.svg": require("/src/assets/Avatars/women.svg"),
            }
        }
    },
    created() {
        this.username = sessionStorage.getItem("username")
        console.log(this.username);
        axios.get("http://localhost:5000/teacher/get_my_info?username=" + this.username)
            .then(res => {
                this.form = res.data;
                this.avatar = this.avatarList[res.data["avatar"]]
                this.$store.state.avatar=this.avatarList[res.data["avatar"]]
                console.log(res.data);
            })

    },
    methods: {
        changeAvatar(val) {
            this.form["avatar"] = val
            this.avatar = this.avatarList[val]
        },
        prepare() {
            this.disable_change = false;
        },
        cancel() {
            this.$confirm("确定放弃修改？").then(() => {
                let username = sessionStorage.getItem("username")
                this.disable_change = true;
                axios.get(server+"/teacher/get_my_info?username=" + username)
                    .then(res => {
                        this.avatar=this.$store.state.avatar
                        this.form = res.data;
                        console.log(res);
                    })
            })
        },
        submit(form) {
            console.log(form);
            this.$confirm("确定提交当前修改?").then(() => {
                let formData = new FormData()
                formData.append("username", form["username"])
                formData.append("name", form["name"])
                formData.append("college", form["college"])
                formData.append("nickname", form["nickname"])
                formData.append("phone_number", form["phone_number"])
                formData.append("email", form["email"])
                formData.append("degree", form["degree"])
                formData.append("entrance_date", form["entrance_date"])
                formData.append("birthday", form["birthday"])
                formData.append("major", form["major"])
                formData.append("gender", form["gender"])
                formData.append("avatar", form["avatar"])
                // console.log(formData);
                axios.post("http://localhost:5000/teacher/edit_my_info", formData)
                    .then(res => {
                        console.log(res);
                        this.$store.state.avatar=this.avatar
                        this.$message({
                            message: res.data["message"],
                            type: res.data["type"]
                        })
                    })
                this.disable_change = true;
            })
        }
    }
}
</script>

<style scoped>
.personal-info {
    width: 1000px;
    margin: auto;
    padding: 1px;
    text-align: left;
}

.title {
    font-size: 20px;
    color: #1e1e1e;
    font-weight: 700;
}

.info-div {
    display: flex;
    align-items: center;
    margin: 5px;
}

.info-div a {
    width: 75px;
    font-size: 18px;
    font-weight: bold;
}

.content {
    margin: 10px;
    display: grid;
    grid-template-columns: 50% 50%;
}

.link {
    text-decoration: none;
    color: #42b983;
}

.footer {
    display: flex;
    justify-content: center;
    /*margin: 20px;*/
    position: absolute;
    bottom: 20px;
    width: 1000px;
}

.avatar {
    width: 50px;
    height: 50px;
    /* border-radius: 50%;
  background-color: #545c64; */
}
</style>