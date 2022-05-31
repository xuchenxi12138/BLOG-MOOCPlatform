import XLSX from "xlsx/dist/xlsx.full.min.js"
let ReadTable = {
    readTable(event) {
        let _this=this
        let table=new Promise(function(resolve,reject){
            if (_this.checkFile(event)) {
                let file = event.target.files[0];
                _this.getSheet(file).then(sheet => {
                    let sheet_json = _this.readSheet(sheet)
                    let sheet_json_en = _this.translateTeacherSheet(sheet_json)
                    resolve(sheet_json_en)
                })
            }
            else{
                reject("文件格式不正确")
            }
        })
        return table
    },
    //读一个sheet
    getSheet(file) {
        let reader = new FileReader();
        reader.readAsBinaryString(file);
        let promise = new Promise(function (resolve, reject) {
            reader.onload = function (e) {
                let data = e.target.result;
                let workbook = XLSX.read(data, { type: 'binary' });
                let sheet = workbook.Sheets[workbook.SheetNames[0]]
                if (sheet['!ref'] === undefined) {
                    reject("该表格为空，请上传有效表格！")
                } else {
                    //表格有效，返回sheet
                    resolve(sheet)
                }
            }
        })
        return promise
    },
    readSheet(table) {
        let ref = table['!ref'];
        let table_size = ref.split(":")[1];
        let arr = table_size.split("");
        let width = ''
        let height = ''
        for (let item of arr) {
            if (item >= 'A' && item <= "Z") {
                width = width + item;
            } else {
                if (item >= "0" && item <= "9") {
                    height = height + item;
                }
            }
        }
        let top_arr = {}
        let pattern = /^[A-Z]*1$/
        for (let item in table) {
            if (pattern.exec(item))
                top_arr[item] = table[item].v
        }
        let data = []
        for (let i = 2; i <= Number(height); i++) {
            let t = {}
            for (let item in top_arr) {
                let name = item.split('1')[0] + i;
                t[top_arr[item]] = table[name].v
            }
            data.push(t)
        }
        return data;
    },
    //把我读到的每一个item的中文名称键名换成英文
    translateTable(item) {
        let obj = {};
        if (item['工号'] != undefined || item['工号'] != '')
            obj['username'] = item['工号']
        else if (item['学号'] != undefined || item['学号'] != "")
            obj['username'] = item['学号']
        obj['class_id'] = item['班级码']
        obj['lesson_id'] = item['课程码']
        obj['name'] = item['姓名']
        obj['gender'] = item['性别']
        obj['college'] = item['学院']
        obj['email'] = item['邮箱']
        obj['major'] = item['专业']
        obj['password'] = item['密码']
        obj['teacher_name'] = item['授课教师']
        obj['teacher_id'] = item['教师工号']
        obj['class_name'] = item['班级名称']
        obj['lesson_name'] = item['课程名称']
        return obj
    },
    readTeacherTable(event) {
        let _this=this
        let table=new Promise(function(resolve,reject){
            if (_this.checkFile(event)) {
                let file = event.target.files[0];
                _this.getSheet(file).then(sheet => {
                    let sheet_json = _this.readSheet(sheet)
                    let sheet_json_en = _this.translateTeacherSheet(sheet_json)
                    resolve(sheet_json_en)
                })
            }
            else{
                reject("文件格式不正确")
            }
        })
        return table
    },
    translateTeacherSheet(sheet) {
        let sheet_en = []
        for (let row of sheet) {
            let row_en = {}
            row_en["username"] = row["工号"]
            row_en['name'] = row['姓名']
            row_en['gender'] = row['性别']
            // switch (row_en["gender"]) {
            //     case "男":
            //         row_en["gender"]="male";
            //         break;
            //     case "女":
            //         row_en["gender"]="female";
            //         break;
            //     default:
            //         break;
            // }
            row_en['college'] = row['学院']
            row_en['email'] = row['邮箱']
            row_en['password'] = row['密码']
            sheet_en.push(row_en)
        }
        return sheet_en
    },
    readStudentTable(event) {
        let _this=this
        let table=new Promise(function(resolve,reject){
            if (_this.checkFile(event)) {
                let file = event.target.files[0];
                _this.getSheet(file).then(sheet => {
                    let sheet_json = _this.readSheet(sheet)
                    let sheet_json_en = _this.translateStudentSheet(sheet_json)
                    resolve(sheet_json_en)
                })
            }
            else{
                reject("文件格式不正确")
            }
        })
        return table
    },
    translateStudentSheet(sheet) {
        let sheet_en = []
        for (let row of sheet) {
            let row_en = {}
            row_en["username"] = row["学号"]
            row_en['name'] = row['姓名']
            row_en['gender'] = row['性别']
            // switch (row_en["gender"]) {
            //     case "男":
            //         row_en["gender"]="male";
            //         break;
            //     case "女":
            //         row_en["gender"]="female";
            //         break;
            //     default:
            //         break;
            // }
            row_en['college'] = row['学院']
            row_en['email'] = row['邮箱']
            row_en['major'] = row['专业']
            row_en['password'] = row['密码']
            sheet_en.push(row_en)
        }
        return sheet_en
    },
    readClassTable(event) {
        let _this=this
        let table=new Promise(function(resolve,reject){
            if (_this.checkFile(event)) {
                let file = event.target.files[0];
                _this.getSheet(file).then(sheet => {
                    let sheet_json = _this.readSheet(sheet)
                    let sheet_json_en = _this.translateClassSheet(sheet_json)
                    resolve(sheet_json_en)
                })
            }
            else{
                reject("文件格式不正确")
            }
        })
        return table
    },
    translateClassSheet(sheet) {
        let sheet_en = []
        for (let row of sheet) {
            let row_en = {}
            row_en["class_id"] = row["班级码"]
            row_en['class_name'] = row['班级名']
            row_en['teacher_name'] = row['授课教师']
            row_en['teacher_id'] = row['教师工号']
            row_en['college'] = row['学院']
            sheet_en.push(row_en)
        }
        return sheet_en
    },
    readLessonTable(event) {
        let _this=this
        let table=new Promise(function(resolve,reject){
            if (_this.checkFile(event)) {
                let file = event.target.files[0];
                _this.getSheet(file).then(sheet => {
                    let sheet_json = _this.readSheet(sheet)
                    let sheet_json_en = _this.translateLessonSheet(sheet_json)
                    resolve(sheet_json_en)
                })
            }
            else{
                reject("文件格式不正确")
            }
        })
        return table
    },
    translateLessonSheet(sheet) {
        let sheet_en = []
        for (let row of sheet) {
            let row_en = {}
            row_en["lesson_id"] = row["课程码"]
            row_en['lesson_name'] = row['课程名']
            row_en['teacher_name'] = row['授课教师']
            row_en['teacher_id'] = row['教师工号']
            row_en['college'] = row['学院']
            sheet_en.push(row_en)
        }
        return sheet_en
    },
    checkFile(event) {
        let file = event.target.files[0];
        let fileType = file.name.split(".")[1];
        if (fileType !== "xlsx" && fileType !== "xls") {
            alert('请上传xlsx或xls格式的文件');
            event.target.value = '';
            return false
        }
        else return true
    },
    checkTable(table) {
        for (let item of table) {
            console.log(item)
        }
    },
    test(file){
        let reader = new FileReader();
        reader.readAsBinaryString(file);
        reader.onload = function (e) {
            let data = e.target.result;
            let workbook = XLSX.read(data, { type: 'binary' });
            let sheet = workbook.Sheets[workbook.SheetNames[0]]
            console.log(sheet);
            
        }
    }
}
export default ReadTable;