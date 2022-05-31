<template>
    <div class="dialog">
        <div class="dialog_inner">
            <el-button type="text" class="el-icon-close close-button" @click="close"></el-button>
            <el-row style="margin-top: 20px;">
                <input v-model="blog['title']" class="title" placeholder="请输入标题" />
            </el-row>
            <el-upload :action="uploadCoverUrl" :limit="1" :file-list="ImageList" :on-success="handleUploadSuccess">
                <div class="cover_div">
                    <img v-if="blog['cover']" :src="blog['cover']" class="cover">
                    <div v-else>
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    </div>
                </div>
            </el-upload>
            <div style="border: 1px solid #ccc;text-align: left;">
                <Toolbar style="border-bottom: 1px solid #ccc" :editor="editor" :defaultConfig="toolbarConfig"
                    :mode="mode" />
                <Editor style="height: 500px; overflow-y: hidden;" v-model="html" :defaultConfig="editorConfig"
                    :mode="mode" @onCreated="onCreated" />
            </div>
            <el-select v-model="blog['tags']" multiple filterable allow-create default-first-option
                placeholder="请选择文章标签" style="width: 100%;margin: 10px auto;">
                <el-option v-for="item in options" :key="item" :label="item" :value="item">
                </el-option>
            </el-select>

            <el-row style="margin: 10px auto;">
                <el-button @click="test">取消</el-button>
                <el-button type="primary" @click="submit">确认修改</el-button>
            </el-row>
        </div>
    </div>
</template>

<script>
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
// import { DomEditor } from '@wangeditor/editor'
import axios from 'axios'
import config from "@/config.json"
const server = config["server"]
export default {
    components: { Editor, Toolbar },
    name: "BlogEditor",
    props: ["BlogData"],
    data() {
        return {
            width: "80%",
            editor: null,
            html: '',
            toolbarConfig: {
                excludeKeys: [
                    'fullScreen',
                    'group-video', "todo", 'group-indent' // 排除菜单组，写菜单组 key 的值即可
                ]
            },
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
            username: "",
            identification: "",
            dialogVisible: true,
            uploadCoverUrl: server + "/file/uploadCover",
            blog: {
                cover: "",
                title: "",
            },
            ImageList: [],
            title: "",
            options: ["数据库", "前端", "后端", "python", "java", "c++", "html"]
        }
    },
    created() {
        this.username = sessionStorage.getItem("username")
        this.identification = sessionStorage.getItem("identification")
        this.dialogVisible = true;
        // this.onCreated()
        console.log(this.BlogData);
        this.blog["cover"] = this.BlogData["cover"]
        this.blog["title"] = this.BlogData["title"]
        this.blog["content_html"] = this.BlogData["content_html"]
        this.blog["blog_id"] = this.BlogData["blog_id"]
        this.blog["post_time"] = this.BlogData["post_time"]
    },
    methods: {
        onCreated(editor) {
            this.editor = Object.seal(editor) // 一定要用 Object.seal() ，否则会报错
        },
        close() {
            this.$store.state.blogEditorVisible = false;
        },
        handleUploadSuccess(response) {
            this.blog["cover"] = server + "/file/image/" + response["url"]
        },
        cancel() {
            this.$confirm("确定放弃当前编写的文章？").then(() => {
                this.$store.state.blogEditorVisible = false
            })
        },
        getTime() {
            let now = new Date()
            let year = now.getFullYear();
            let month = now.getMonth() + 1;
            let day = now.getDay();
            let houer = now.getHours();
            let minute = now.getMinutes();
            let second = now.getSeconds();
            let time = year + "-" + month + '-' + day + ' ' + houer + ":" + minute + ":" + second
            return time
        },
        submit() {
            this.username = sessionStorage.getItem("username")
            this.identification = sessionStorage.getItem("identification")
            let blog = this.blog;
            if (blog['title']) {
                this.fullscreenLoading = true;
                const loading = this.$loading({
                    lock: true,
                    text: '正在上传,请稍等...',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                });

                blog['owner_id'] = this.username
                blog['content_html'] = this.editor.getHtml()
                blog['content_text'] = this.editor.getText()
                blog['post_time'] = this.getTime()
                let formData = new FormData()
                formData.append("title", blog['title'])
                // formData.append("owner_name", blog['owner_name'])
                formData.append("content_text", blog['content_text'])
                formData.append("content_html", blog['content_html'])
                formData.append("post_time", blog['post_time'])
                formData.append("identification", blog['identification'])
                formData.append("cover", blog['cover'])
                formData.append("blog_id", blog["blog_id"])
                formData.append("tags", JSON.stringify(this.blog["tags"]))
                axios.post(server + "/blog/change", formData)
                    .then(() => {
                        this.$message({
                            message: "上传成功",
                            type: 'success'
                        })
                        this.$emit("submitSuccess", blog)
                        loading.close()
                        this.$emit("editSuccess", this.blog)
                        this.$store.state.blogEditorVisible = false;
                    }).catch(() => {
                        this.$message({
                            message: "上传失败",
                            type: 'error'
                        })
                        loading.close()
                        this.editor.destroy()
                    })
            }
            else {
                this.$alert("请输入标题！！！")
            }
        },
        test() {
            // let toolbar = DomEditor.getToolbar(this.editor)
            // console.log(toolbar.getConfig().toolbarKeys);
            console.log(this.blog['tags']);
        }
    },
    mounted() {
        this.onCreated()
        // 模拟 ajax 请求，异步渲染编辑器
        setTimeout(() => {
            this.html = this.BlogData["content_html"]
        }, 500)
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
        this.ImageList = []
    }
}
</script>
<style src="@wangeditor/editor/dist/css/style.css">
</style>
<style scoped>
.dialog {
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    background-color: #1e1e1e80;
    z-index: 1;
}

.cover_div {
    width: 59vw;
    min-width: 505px;
    min-height: 200px;
    border: 1px dashed #cccccc;
    margin: 10px auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.cover_div:hover {
    border: 1px dashed #409EFF;
}

.cover_div .el-icon-upload {
    font-size: 67px;
}

.cover_div .el-upload__text em {
    color: #409EFF;
}

.dialog_inner {
    width: 60vw;
    min-width: 520px;
    height: 100vh;
    margin: auto;
    background-color: #ffffff;
    padding: 10px;
    overflow: auto;
    position: relative;
}

.close-button {
    position: absolute;
    right: 0;
    top: 0;
}

.dialog_inner h1 {
    color: #23272e;
}

.cover {
    width: 100%;
    display: inline-block;
    object-fit: contain;
}

.title {
    outline: none;
    border: 1px solid #1e1e1e;
    font-size: 24px;
    font-weight: 600;
    width: 100%;
    margin: 10px auto;
    border-radius: 3px;
    height: 40px;
}

.title:focus {
    border: 1px solid #409EFF;
}
</style>