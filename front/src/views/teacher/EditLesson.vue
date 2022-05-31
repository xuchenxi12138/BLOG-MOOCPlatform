<template>
    <div>
        <el-row type="flex" justify="start">
            <el-input class="title" :show-word-limit="true" maxlength="20" v-model="lesson_name">
                <template slot="prepend">课程名</template>
            </el-input>
        </el-row>
        <el-row type="flex" justify="space-between" style="width:700px;margin-top: 20px;">
            <span>章节列表</span>
            <el-button class="el-icon-plus" type="success" size="small" @click="addChapter">章节</el-button>
        </el-row>
        <div style="display: flex;justify-content:space-between;width:100%;">
            <div class="chapter_div">
                <div class="chapter" v-for="(chapter, index) in ChapterData" :key="index">
                    <div class="chapter_header">
                        <div class="chapter_index">{{ chapter['chapter_index'] }}</div>
                        <div class="chapter_title">{{ chapter['title'] }}</div>
                        <el-button size="mini" type="primary" @click="preEditChapter(chapter)">编辑</el-button>
                        <el-button size="mini" type="danger">删除</el-button>
                        <el-button type="text" class="" @click="fold(chapter)">展开
                            <i class="el-collapse-item__arrow el-icon-arrow-right" v-if="chapter['open']"></i>
                            <i class="el-collapse-item__arrow el-icon-arrow-right is-active" v-else></i>
                        </el-button>
                    </div>
                    <el-collapse-transition>
                        <div v-if="chapter['open']">
                            <el-row type="flex" justify="end">
                                <el-button class="el-icon-plus" size="mini" type="success"
                                    @click="addSubChapter(chapter['chapter_id'])">小节</el-button>
                            </el-row>
                            <div class="subchapter" v-for="(subchapter, subindex) in chapter.children" :key="subindex">
                                <span style="width: 150px;">{{ subchapter.subchapter_index }}</span>
                                <span style="width: 300px;">{{ subchapter.title }}</span>
                                <el-button type="primary" size="mini" @click="preEditSubChapter(subchapter)">编辑
                                </el-button>
                                <el-button type="danger" size="mini">删除</el-button>
                            </div>
                            <el-collapse-transition>
                                <div v-if="subChapterFormVisible">
                                    <el-form :inline="true" :model="form" class="demo-form-inline">
                                        <el-form-item label="索引" prop="subchapter_index" :rules="[
                                        { required: true, message: '索引不能为空' },
                                        { type: 'number', message: '索引必须是数字' }]">
                                            <el-input v-model.number="form['subchapter_index']" style="width: 50px;">

                                            </el-input>
                                        </el-form-item>
                                        <el-form-item label="标题">
                                            <el-input v-model="form['title']" style="width: 200px;">
                                            </el-input>
                                        </el-form-item>
                                        <el-button type="primary" class="el-icon-check" @click="confirmAddSubChapter">确定
                                        </el-button>
                                        <el-button class="el-icon-close" @click="subChapterFormVisible = false">取消
                                        </el-button>
                                    </el-form>
                                </div>
                            </el-collapse-transition>
                            <br />
                        </div>
                    </el-collapse-transition>
                </div>
                <el-collapse-transition>
                    <div v-if="chapterFormVisible">
                        <el-form :inline="true" :model="form" class="demo-form-inline">
                            <el-form-item label="索引" prop="chapter_index" :rules="[
                            { required: true, message: '索引不能为空' },
                            { type: 'number', message: '索引必须是数字' }]">
                                <el-input v-model.number="form['chapter_index']" style="width: 50px;">

                                </el-input>
                            </el-form-item>
                            <el-form-item label="标题">
                                <el-input v-model="form['title']" style="width: 200px;">
                                </el-input>
                            </el-form-item>
                            <el-button type="primary" class="el-icon-check" @click="confirmAddChapter">确定
                            </el-button>
                            <el-button class="el-icon-close" @click="chapterFormVisible = false">取消</el-button>
                        </el-form>
                    </div>
                </el-collapse-transition>
            </div>
            <el-upload class="upload-demo" drag :action="uploadCover"
                accept="image/jpg,image/jpeg,image/png" :on-success="uploadCoverSuccess" :file-list="coverList">
                <img v-if="coverImage" :src="coverImage" class="cover">
                        <div v-else>
                            <i class="el-icon-upload"></i>
                            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                        </div>
                <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
        </div>
        <p>简介</p>
        <div style="border: 1px solid #ccc;text-align: left;">
            <Toolbar style="border-bottom: 1px solid #ccc" :editor="editor" :defaultConfig="toolbarConfig"
                :mode="mode" />
            <Editor style="height: 500px; overflow-y: hidden;" v-model="html" :defaultConfig="editorConfig" :mode="mode"
                @onCreated="onCreated" />
        </div>
        <el-dialog :visible.sync="dialogVisible" title="编辑" :before-close="handleClose">
            <el-form label-width="80px" label-position="left" :model="form">
                <el-form-item label="索引" prop="chapter_index" :rules="[
                    { required: true, message: '索引不能为空' },
                    { type: 'number', message: '索引必须是数字' }
                ]">
                    <el-input v-model.number="form['chapter_index']"></el-input>
                </el-form-item>
                <el-form-item label="标题">
                    <el-input v-model="form['title']"></el-input>
                </el-form-item>
            </el-form>
            <el-row>
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button @click="confirmChangeChapter" type="primary">提交</el-button>
            </el-row>
        </el-dialog>
        <el-dialog :visible.sync="dialogVisible2" title="编辑" :before-close="handleClose">
            <el-form label-width="80px" label-position="left" :model="form">
                <el-form-item label="索引" prop="subchapter_index" :rules="[
                    { required: true, message: '索引不能为空' },
                    { type: 'number', message: '索引必须是数字' }
                ]">
                    <el-input v-model.number="form['subchapter_index']"></el-input>
                </el-form-item>
                <el-form-item label="标题">
                    <el-input v-model="form['title']"></el-input>
                </el-form-item>
                <el-form-item label="视频">
                    <el-upload :action="uploadVideo" accept="video/mp4" :limit="1" :on-success="uploadVideoSuccess"
                        :file-list="videoList">
                        <el-button>上传视频</el-button>
                    </el-upload>
                </el-form-item>
                <el-form-item label="课件">
                    <el-upload :action="uploadFile" :limit="1" :on-success="uploadFileSuccess" :file-list="fileList">
                        <el-button>上传课件</el-button>
                    </el-upload>
                </el-form-item>
            </el-form>
            <el-row>
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button @click="confirmChangeSubchapter" type="primary">提交</el-button>
            </el-row>
        </el-dialog>
        <el-button type="primary" class="el-icon-check submit" @click="submit">提交</el-button>
    </div>
</template>

<script>
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
// import axios from 'axios'
import config from "@/config.json"
import axios from 'axios'
const server = config["server"]

export default {
    name: 'EditLesson',
    data() {
        return {
            uploadVideo: server + "/file/upload_video",
            uploadFile: server + "/file/upload_course_file",
            uploadCover:server + "/file/uploadOneImage",
            lesson_name: '',
            description: '',
            lesson_id: '',
            editor: null,
            html: '<p>hello</p>',
            toolbarConfig: {},
            editorConfig: {
                placeholder: '请输入内容...',
                MENU_CONF: {
                    uploadImage: {
                        fieldName: "file",
                        server: server + "/file/uploadTextImage"
                    }
                }
            },
            mode: 'default', // or 'simple'
            ChapterData: [],
            form: {},
            chapterFormVisible: false,
            subChapterFormVisible: false,
            dialogVisible: false,
            dialogVisible2: false,
            videoList: [],
            fileList: [],
            coverImage:"",
            coverList:[]
            
        }
    },
    components: { Editor, Toolbar },
    created() {
        this.lesson_id = this.$route.query["lesson_id"]
        this.$store.state.routerList = [{
            name: "课程管理",
            path: '/Teacher/LessonManagement'
        }, {
            name: "课程列表",
            path: '/Teacher/LessonManagement'
        }, {
            name: "编辑课程",
        }]
        this.getLessonInfo()
       
    },
    mounted() {
        this.onCreated()
        // 模拟 ajax 请求，异步渲染编辑器
        const that = this
        window.onresize = () => {
            return (() => {
                if (document.body.clientWidth > 700) {
                    that.width = "80%"
                }
                else that.width = "520px"
            })()
        }

    },
    beforeDestroy() {
        const editor = this.editor
        // if (editor == null) return
        editor.destroy() // 组件销毁时，及时销毁编辑器
        this.cover = ""
        this.title = ""
        this.ImageList = []
    },
    methods: {
        onCreated(editor) {
            this.editor = Object.seal(editor) // 一定要用 Object.seal() ，否则会报错
        },
        getLessonInfo() {
            let url = server + "/teacher/get_lesson_info?lesson_id=" + this.lesson_id
            axios.get(url).then(res => {
                // console.log(res);
                this.lesson_name = res.data["lesson_name"]
                this.description = res.data["description"]
                this.html = this.description
                if(res.data["cover_id"])
                this.coverImage=server+"/file/image/"+res.data["cover_id"]
                else this.coverImage=""
                let data = res.data['chapter_list']
                for (let item of data) {
                    item["open"] = false
                }
                this.ChapterData = data
                // this.getChapterList()
            })
        },
        getChapterList() {
            let url = server + "/teacher/get_chapter_list?lesson_id=" + this.lesson_id
            axios.get(url).then(res => {
                let data = res.data
                for (let item of data) {
                    item["open"] = false
                }
                this.ChapterData = data
            })
        },
        fold(chapter) {
            chapter['open'] = !chapter['open']
            this.chapterFormVisible = false
            this.subChapterFormVisible = false
        },
        addChapter() {
            this.form = {
                lesson_id: this.lesson_id,
                chapter_index: "",
                title: ""
            }
            this.chapterFormVisible = true
            this.subChapterFormVisible = false
        },
        addSubChapter(id) {
            this.form = {
                chapter_id: id,
                subchapter_index: "",
                title: "",
                lesson_id: this.lesson_id
            }
            this.subChapterFormVisible = true
            this.chapterFormVisible = false
        },
        confirmAddChapter() {

            if (this.form['chapter_index']) {
                let url = server + "/teacher/add_chapter"
                let formdata = new FormData()
                formdata.append("lesson_id", this.form["lesson_id"])
                formdata.append("chapter_index", this.form["chapter_index"])
                formdata.append("title", this.form["title"])
                axios.post(url, formdata).then(res => {
                    this.$message(res.data)
                    this.chapterFormVisible = false
                    this.getChapterList()
                })
            } else {
                this.$message("请输入索引")
            }
        },
        confirmAddSubChapter() {

            if (this.form["subchapter_index"]) {
                let url = server + "/teacher/add_subchapter"
                let formdata = new FormData()
                formdata.append("chapter_id", this.form["chapter_id"])
                formdata.append("subchapter_index", this.form["subchapter_index"])
                formdata.append("title", this.form["title"])
                axios.post(url, formdata).then(res => {
                    this.$message(res.data)
                    this.subChapterFormVisible = false
                    this.getChapterList()
                })
            }

            else {
                this.$message("请输入索引")
            }
        },
        preEditSubChapter(subchapter) {
            this.dialogVisible2 = true
            this.form = subchapter
            console.log(this.form);
            if (subchapter['video_id'])
                this.videoList = [{ name: subchapter['title'] }]
            else this.videoList = []
            if (subchapter['file_id'])
                this.fileList = [{ name: subchapter['title'] }]
            else this.fileList = []
            // this.form["file_url"]=server+"/file/video/"+subchapter['file_id']
        },
        preEditChapter(chapter) {

            this.dialogVisible = true
            this.form = chapter
            console.log(this.form);
            if (chapter['video_id'])
                this.videoList = [{ name: chapter['title'] }]
            else this.videoList = []
            if (chapter['file_id'])
                this.fileList = [{ name: chapter['title'] }]
            else this.fileList = []
        },
        handleClose() {
            this.form = {}
            this.dialogVisible = false
            this.dialogVisible2 = false
            this.getChapterList()
        },
        uploadVideoSuccess(res) {
            this.form['video_id'] = res["id"]
        },
        uploadFileSuccess(res) {
            this.form['file_id'] = res["id"]
        },
        confirmChangeChapter() {

            if (this.form['chapter_index']) {
                let url = server + "/teacher/change_chapter"
                let formdata = new FormData()
                formdata.append("chapter_id", this.form["chapter_id"])
                formdata.append("chapter_index", this.form["chapter_index"])
                formdata.append("title", this.form["title"])
                formdata.append("file_id", this.form["file_id"])
                formdata.append("video_id", this.form["video_id"])
                axios.post(url, formdata).then(res => {
                    this.$message(res.data)
                    this.dialogVisible = false
                })
            } else {
                this.$message("请输入索引")
            }
        },
        confirmChangeSubchapter() {
            console.log(this.form);
            if (this.form['subchapter_index']) {
                let url = server + "/teacher/change_subchapter"
                let formdata = new FormData()
                formdata.append("subchapter_id", this.form["subchapter_id"])
                formdata.append("subchapter_index", this.form["subchapter_index"])
                formdata.append("title", this.form["title"])
                formdata.append("file_id", this.form["file_id"])
                formdata.append("video_id", this.form["video_id"])
                axios.post(url, formdata).then(res => {
                    this.$message(res.data)
                    this.dialogVisible2 = false
                })
            } else {
                this.$message("请输入索引")
            }
        },
        submit() {
            let des_html = this.editor.getHtml()
            if (this.lesson_name) {
                let url = server + "/teacher/edit_lesson"
                let formdata = new FormData()
                formdata.append("lesson_id", this.lesson_id)
                formdata.append('lesson_name', this.lesson_name)
                formdata.append("description", des_html)
                axios.post(url, formdata).then(res => {
                    this.$message(res.data)
                })
            } else {
                this.$message("请输入标题")
            }


        },
        uploadCoverSuccess(res,file){
            console.log(file);
            this.coverList=[file]
            let cover=res["url"]
            console.log(cover);
            let formdata=new FormData()
            formdata.append("lesson_id",this.lesson_id)
            formdata.append("cover_id",cover)
            axios.post(server+"/teacher/change_lesson_cover",formdata).then(res=>{
                this.coverImage=server+"/file/image/"+cover
                this.$message(res.data)
            })
        }
    },

}

</script>
<style src="@wangeditor/editor/dist/css/style.css">
</style>
<style scoped>
.cover {
    /* width: 1000px; */
    height: 178px;
    display: inline-block;
    object-fit: contain;
}
.title {
    width: 500px;
}

.chapter_div {
    background-color: #f4f4f4;
    border: 1px solid #cccccc;
    width: 700px;
}

.chapter {
    width: 700px;
    border-radius: 3px;
    transition: all 0.1s;
}

.chapter_header {
    width: 100%;
    height: 50px;
    background-color: #ffffff;
    cursor: pointer;
    border-bottom: 1px solid #cccccc;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

/* .chapter_header span{
    color: #ffffff;
}
.chapter_header:hover span{
    color: #409eff;
} */
.subchapter {
    background-color: #f4f4f4;
    height: 50px;
    margin: auto;
    width: 90%;
    border-bottom: 1px solid #cccccc;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

p {
    text-align: left;
}

.chapter_index {

    width: 80px;
    border-radius: 3px;
    height: 42px;
    transition: 0.1s;
    text-align: left;
    line-height: 40px;
}

.chapter_title {

    width: 300px;
    border-radius: 3px;
    height: 42px;
    transition: 0.1s;
    text-align: left;
    line-height: 40px;
}

.submit {
    position: fixed;
    right: 100px;
    top: 100px;
}
</style>
