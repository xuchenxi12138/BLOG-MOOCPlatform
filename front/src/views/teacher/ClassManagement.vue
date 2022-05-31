<template>
    <div>
        <el-breadcrumb separator="/">
            <el-breadcrumb-item v-for="(item,index) in this.$store.state.routerList" :key="index" :to="item['path']">
            {{item["name"]}}
            </el-breadcrumb-item>
        </el-breadcrumb>
        <div style="margin-top: 10px;">
            <router-view/>
        </div>
    </div>
</template>

<script>

export default {
    name: 'ClassManagement',
    data() {
        return {
        }
    },
    created() {
        this.$store.state.routerList=[{
            path:'/Teacher/ClassManagement',
            name:"班级列表"
        }]
    },
    methods: {
    },
}

</script>
<style scoped>
</style>
