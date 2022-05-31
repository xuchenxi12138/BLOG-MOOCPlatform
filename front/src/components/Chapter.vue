<template>
    <div>
        <div @click="open = !open" class="chapter_header">
            <a>{{ tableData.chapter_index }}</a>
            <el-input v-model="tableData.title"></el-input>
        </div>
        <transition>
            <div v-if="open">
                <div v-for="(item, index) in tableData.children" :key="index"></div>
            </div>
        </transition>
    </div>
</template>

<script>
export default {
    name: 'ChapterModule',
    props: ["ChapterData"],
    components: {},
    data() {
        return {
            tableData: [],
            open: false,
            lesson_id:""
        }
    },
    created() {
        this.tableData = this.ChapterData
        this.lesson_id=this.$router.query["lesson_id"]
    },
    methods: {
    },
}

</script>
<style scoped>
.chapter_header {
    width: 100%;
    height: 50px;
    background-color: #ffffff;
    cursor: pointer;
    border-bottom: 1px solid #cccccc;
    display: flex;
    align-items: center;
}
</style>
