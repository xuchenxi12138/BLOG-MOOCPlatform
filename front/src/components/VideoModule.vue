<template>
    <div class="lessonVideo">
        <h2>{{ subchapter_title }}</h2>
        <video style="width: 100%;" controls="controls">
          <source :src="this.video_url" type="video/mp4" style="width: 100%">
        </video>
        <div>
          <a :href="file_url">课件</a>
          <a :href="video_url">视频</a>
        </div>
    </div>
</template>

<script>
export default {
    name: 'VideoModule',
    data() {
        return {
            lesson_id:"",
            subchapter_title:"",
            video_url:"",
            file_url:"",
            chapter_id:this.$route.query["chapter_id"]
        }
    },
    created() {
        
    },
    methods: {
    },
    watch:{
        chapter_id(value){
            console.log(value);
        }
    }
}

</script>
<style scoped>
.lessonVideo {
    width: 100%;
    /*max-width: 900px;*/
    height: auto;
    background-color: #000000;
    /*margin: 5px;*/
}
</style>
