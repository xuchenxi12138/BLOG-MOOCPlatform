<template>
    <div>
        <el-table :data="tableData" stripe style="width: 100%;margin-top: 10px;" height="500">
            <el-table-column type="index" label="序号">
            </el-table-column>
            <el-table-column prop="student_id" label="学号">
            </el-table-column>
            <el-table-column prop="name" label="姓名">
            </el-table-column>
            <el-table-column prop="score" label="分数">
            </el-table-column>
            <el-table-column prop="comment" label="评语">
            </el-table-column>
            <el-table-column prop="post_time" label="上传时间">
            </el-table-column>
            <el-table-column label="操作" width="280">
                <template slot-scope="scope">
                    <el-button @click="download(scope.row['file_id'])" type="primary" size="small"
                        class="el-icon-document">下载
                    </el-button>
                    <el-button @click="preChange(scope.row)" type="danger" size="small" class="el-icon-delete">修改
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-row>
            <el-button @click="getLineChart" type="primary">生成折线图</el-button>
            <el-button @click="getPieChart" type="warning">生成饼图</el-button>
        </el-row>
        <el-dialog title="修改" :visible.sync="dialogVisible">
            <el-form label-width="80px" label-position="left">
                <el-form-item label="学号">
                    <el-input v-model="form['student_id']" disabled></el-input>
                </el-form-item>
                <el-form-item label="姓名">
                    <el-input v-model="form['name']" disabled></el-input>
                </el-form-item>
                <el-form-item label="作业标题">
                    <el-input v-model="form['title']" disabled></el-input>
                </el-form-item>
                <el-form-item label="分数">
                    <el-input v-model="form['score']"></el-input>
                </el-form-item>
                <el-form-item label="评语">
                    <el-input v-model="form['comment']"></el-input>
                </el-form-item>
            </el-form>
            <div>
                <el-button @click="cancel">取消</el-button>
                <el-button @click="submit" type="primary">确定</el-button>
            </div>
        </el-dialog>
        <transition name="el-zoom-in-top">
            <div class="dialog" v-show="dialogVisible2">
                <div class="dialog_inner">
                    <h1>{{chartType}}</h1>
                    <div id="chart"></div>
                    <el-button type="primary" @click="dialogVisible2=false" class="el-icon-close">关闭</el-button>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
import axios from 'axios'
import config from "@/config.json"
const server = config["server"]
import * as echarts from 'echarts/core';
// 引入柱状图图表，图表后缀都为 Chart
import { BarChart, LineChart, PieChart } from 'echarts/charts';
// 引入提示框，标题，直角坐标系，数据集，内置数据转换器组件，组件后缀都为 Component
import {
    TitleComponent,
    TooltipComponent,
    GridComponent,
    DatasetComponent,
    TransformComponent
} from 'echarts/components';
// 标签自动布局，全局过渡动画等特性
import { LabelLayout, UniversalTransition } from 'echarts/features';
// 引入 Canvas 渲染器，注意引入 CanvasRenderer 或者 SVGRenderer 是必须的一步
import { CanvasRenderer } from 'echarts/renderers';

// 注册必须的组件
echarts.use([
    TitleComponent,
    TooltipComponent,
    GridComponent,
    DatasetComponent,
    TransformComponent,
    BarChart,
    LabelLayout,
    UniversalTransition,
    CanvasRenderer,
    LineChart,
    PieChart
]);
export default {
    name: 'StudentDetail',
    data() {
        return {
            class_id: "",
            student_id: "",
            tableData: [],
            form: {},
            dialogVisible: false,
            chartType: "",
            dialogVisible2: false
        }
    },
    created() {
        this.class_id = this.$route.query["class_id"]
        this.student_id = this.$route.query["student_id"]
        this.$store.state.routerList = [{
            path: '/Teacher/ClassManagement',
            name: "班级列表"
        }, {
            path: "/Teacher/ClassMangement/StudentList?class_id" + this.class_id,
            name: "学生列表",
        }]


    },
    methods: {
        getStudentAssignments() {
            let url = server + "/teacher/get_student_assignments?class_id=" + this.class_id + "&student_id=" + this.student_id
            axios.get(url).then(res => {
                console.log(res.data);
                this.tableData = res.data;
            })
        },
        preChange(row) {
            this.form = row
            this.dialogVisible = true
        },
        download(id) {
            if (id!="null") {
                window.open(server + "/file/word/" + id)
            }else{
                this.$message("对不起，找不到文件")
            }
        },
        cancel() {
            this.dialogVisible = false
            this.form = {}
        },
        submit() {
            let url = server + "/teacher/check_assignment"
            let formdata = new FormData()
            formdata.append("assignment_id", this.form["assignment_id"])
            formdata.append("student_id", this.form["student_id"])
            formdata.append("score", this.form["score"])
            formdata.append("comment", this.form["comment"])
            axios.post(url, formdata).then(res => {
                this.$message(res.data)
                this.cancel()
            })
        },
        getLineChart() {
            this.chartType="折线图"
            this.dialogVisible2=true
            let data1 = []
            let data2 = []
            for (let item of this.tableData) {
                let arr = item["post_time"].split("-")
                data1.push(arr[1] + "-" + arr[2])
                data2.push(item["score"])
            }
            let option = {
                xAxis: {
                    type: 'category',
                    data: data1
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: data2,
                        type: 'line'
                    }
                ]
            };
            let myChart = echarts.init(document.getElementById('chart'));
            myChart.setOption(option)
        },
        getPieChart() {
            this.chartType="饼图"
            this.dialogVisible2=true
            let data = [
                { value: 0, name: "优秀" },
                { value: 0, name: "良好" },
                { value: 0, name: "一般" },
                { value: 0, name: "合格" },
                { value: 0, name: "不及格" },
            ]
            for (let item of this.tableData) {
                if (item["score"] >= 85) {
                    data[0]["value"] += 1
                } else {
                    if (item["score"] >=75) {
                        data[1]["value"] += 1
                    } else {
                        if (item["score"] >= 65) {
                            data[2]["value"] += 1
                        } else if(item["score"]>=60){
                            data[3]["value"]+=1
                        }else { data[4]["value"] += 1 }
                    }
                }
            }
            console.log(data);
            let option = {
                series: [
                    {
                        type: 'pie',
                        data: data
                    }
                ]
            };
            let myChart = echarts.init(document.getElementById('chart'));
            myChart.setOption(option)
        }
    },
    mounted() {
        this.getStudentAssignments()
    }
}

</script>
<style scoped>
.dialog{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #00000080;
    z-index: 100;
}
.dialog_inner{
    width: 800px;
    height: 100%;
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #ffffff;
}
#chart{
    width: 500px;
    height: 500px;
}
</style>
