<template>
    <div class="header">
        <router-link to="/">
            <img :src="homeImage" alt="首页" class="logo" />
        </router-link>
        <!-- <nav>
            <router-link to="/lessons">课程</router-link>
            <router-link to="/blogs">博客</router-link>
        </nav> -->
        <div>
            <el-input placeholder="请输入内容" v-model="search_text" @keydown.native.enter="search">
                <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
            </el-input>
        </div>
        <div>
            <Avatar ref="Avatar"></Avatar>
        </div>
    </div>
</template>

<script>
import Avatar from "@/components/Avatar"
export default {
    name: 'HeaderMenu',
    components: {
        Avatar
    },
    data() {
        return {
            homeImage: require("/src/assets/logo.png"),
            search_text: ''
        }
    },
    created() {
    },
    methods: {
        search() {
            if (this.search_text) {
                let url = "/Search/Blog?text=" + this.search_text+"&start=0"
                this.$router.push(url)
            }
        }

    },
}

</script>
<style scoped>
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 100%;

}

.logo {
    width: 50px;
    height: 50px;
    cursor: pointer;
}

nav a {
    font-weight: bold;
    color: #2c313c;
    text-decoration: none;
    font-size: 24px;
    margin: 0 10px;
}

nav a.router-link-exact-active {
    color: #42b983;
}
</style>
