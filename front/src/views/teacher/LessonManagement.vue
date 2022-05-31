<template>
    <div>
        <el-breadcrumb separator="/">
            <el-breadcrumb-item v-for="(item, index) in this.$store.state.routerList" :key="index" :to="item['path']">
                {{ item["name"] }}
            </el-breadcrumb-item>
        </el-breadcrumb>
        <div style="margin-top: 10px;">
            <router-view/>
        </div>
    </div>
</template>

<script>
export default {
    name: 'LessonManagement',
    data() {
        return {
        }
    },
    created() {
    },
    methods: {
    },
}

</script>
<style scoped>
</style>
