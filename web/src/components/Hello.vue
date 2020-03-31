<template>
  <div id="hello">
    <el-row>
      <el-col :span="6">
        <div class="grid-content bg-purple-dark">
          <selector
            :valueFromParent.sync="language"
            :listFromParent.sync="languageList"
            selectorType="language"
          ></selector>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content bg-purple-dark">
          <selector
            :valueFromParent.sync="file"
            :listFromParent.sync="fileList"
            :newValueFromParent.sync="newFileName"
            selectorType="file"
          ></selector>
        </div>
      </el-col>
      <el-col :span="4">
        <el-button-group>
          <el-tooltip placement="bottom-end">
            <div slot="content">
              You can input *.h to create head file.
              <br />You can create *.file and read it in your program.
              <br />If you use java,plaese observe following rules:
              <br />1.There is a file named Main.java
              <br />2.There is a class named Main
            </div>
            <el-button type="primary" icon="el-icon-document-add" @click="addNewFile"></el-button>
          </el-tooltip>
          <el-tooltip placement="bottom-start">
            <div slot="content">The current file will be deleted</div>
            <el-button type="primary" icon="el-icon-delete" @click="DeleteFile"></el-button>
          </el-tooltip>
          <!--
          <el-button type="primary" icon="el-icon-document-add" @click="addNewFile"></el-button>
          <el-button type="primary" icon="el-icon-delete" @click="DeleteFile"></el-button>
          -->
        </el-button-group>
      </el-col>
      <el-col :span="4">
        <div class="grid-content bg-purple-dark">
          <el-button type="primary" @click="save">
            Save Code
            <i class="el-icon-folder el-icon--right"></i>
          </el-button>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="grid-content bg-purple-dark">
          <el-button type="primary" @click="compile">
            Compile&Run
            <i class="el-icon-upload el-icon--right"></i>
          </el-button>
          <el-tooltip placement="bottom-end">
            <div slot="content">Select and export exe to achieve interactive program.</div>
            <el-checkbox v-model="exportEXE"></el-checkbox>
          </el-tooltip>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="16">
        <div class="grid-content bg-purple">
          <!--
          <el-input
            type="textarea"
            :autosize="{minRows: 20}"
            placeholder="coding here"
            v-model="codeText"
            resize="none"
          ></el-input>
          -->
          <codeEditor
            :valueFromParent.sync="codeText"
            :languageFromParent.sync="language"
            :fileFromParent.sync="file"
          ></codeEditor>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="grid-content bg-purple-light">
          <el-row>
            <el-col :span="24">
              <div class="grid-input bg-purple-dark">
                <el-input
                  type="textarea"
                  :autosize="{minRows: 9}"
                  placeholder="stdout"
                  v-model="stdout"
                  resize="none"
                  :readonly="true"
                  v-loading="loading"
                ></el-input>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div class="grid-input bg-purple-dark">
                <el-input
                  type="textarea"
                  :autosize="{minRows: 9}"
                  placeholder="stdin"
                  v-model="stdin"
                  resize="none"
                ></el-input>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { Loading } from "element-ui";
//module.exports = {
export default {
  data() {
    return {
      visible: false,
      codeText:
        '#include<stdio.h>\nint main()\n{\n    char str[5];\n    scanf("%[^\\n]%*c",str);\n    printf("%s world\\n",str);\n    return 0;\n}',
      stdout: "",
      stdin: "Hello",
      language: "c",
      file: "main.c",
      newFileName: "main.c",
      fileIndex: 0,
      loading: false,
      exportEXE: false,
      languageList: [
        {
          value: "gcc 7.4.0",
          label: "c"
        },
        {
          value: "g++ 7.5.0",
          label: "cpp"
        },
        {
          value: "openjdk 11.0.6",
          label: "java"
        },
        {
          value: "python 3.6.9",
          label: "py"
        }
      ],
      fileList: [
        {
          value: "",
          label: "main.c"
        },
        {
          value: "",
          label: "example.h"
        },
        {
          value: "",
          label: "data.file"
        }
      ],
      codeList: [
        {
          file: "main.c",
          code:
            '#include<stdio.h>\n#include"example.h"\nint main()\n{\n    char str[5];\n    scanf("%[^\\n]%*c",str);\n    printf("%s\\n",str);\n    print();\n    return 0;\n}'
        },
        {
          file: "example.h",
          code:
            '#include<stdio.h>\nvoid print()\n{\n    FILE *fp = NULL;\n    char buff[255];\n    fp = fopen("data.file", "r");\n    fscanf(fp, "%s", buff);\n    printf("%s\\n", buff);\n    fclose(fp);\n}'
        },
        {
          file: "data.file",
          code: "world"
        }
      ]
    };
  },
  watch: {
    language(val) {
      console.log(val);
    },
    file(val) {
      for (var j = 0, len = this.codeList.length; j < len; j++) {
        if (this.codeList[j].file == val) {
          this.fileIndex = j;
          this.codeText = this.codeList[j].code;
          break;
        }
      }
    },
    codeText(val) {
      this.codeList[this.fileIndex].code = this.codeText;
    }
  },
  created() {
    var codeList = JSON.parse(localStorage.getItem("codeList"));
    if (codeList != null) {
      this.codeList = codeList;
      this.codeText = codeList[0].code;
      this.file = codeList[0].file;
    }
    var fileList = JSON.parse(localStorage.getItem("fileList"));
    if (fileList != null) {
      this.fileList = fileList;
    }
    if (fileList && codeList) {
      this.$message({
        message: "Code has been loaded",
        type: "success",
        showClose: true
      });
    }
  },
  methods: {
    compile() {
      if (this.loading) {
        this.$message({
          showClose: true,
          message: "The program is compiling!",
          type: "warning"
        });
        return;
      }
      if (
        (this.language == "java" || this.language == "py") &&
        this.exportEXE
      ) {
        this.exportEXE = false;
        this.$message({
          showClose: true,
          message: "Exporting exe is not supported in the current language",
          type: "warning"
        });
      }
      this.loading = true;
      var httpObject = new Object();
      for (var i = 0, len = this.codeList.length; i < len; i++) {
        var key = this.codeList[i].file;
        var value = this.codeList[i].code;
        httpObject[key] = value;
      }
      var fileArray = new Array();
      for (var i = 0, len = this.fileList.length; i < len; i++) {
        fileArray.push(this.fileList[i].label);
      }
      if (!this.exportEXE) {
        this.$http
          .post(
            "http://192.168.23.129:8080/polls/",
            Object.assign(
              {
                fileList: JSON.stringify(fileArray),
                stdin: this.stdin,
                language: this.language,
                exportEXE: false
              },
              httpObject
            ),
            { emulateJSON: true }
          )
          .then(function(res) {
            console.log(res);
            console.log(this.codeText);
            this.stdout = res.data.message;
            var result = res.data.result;
            switch (result) {
              case "success": {
                this.$message({
                  message: "Run success",
                  type: "success",
                  showClose: true
                });
                break;
              }
              case "Compile failed": {
                this.$message({
                  message: "Compile failed",
                  type: "error",
                  showClose: true
                });
                break;
              }
              case "Run timeout": {
                this.$message({
                  message: "Run timeout",
                  type: "error",
                  showClose: true
                });
                break;
              }
              case "outMemory": {
                this.$message({
                  message: "Out of memory",
                  type: "error",
                  showClose: true
                });
                break;
              }
            }
            this.loading = false;
          })
          .catch(function(err) {
            console.log(err);
            this.loading = false;
          });
      } else {
        this.$http
          .post(
            "http://192.168.23.129:8080/polls/",
            Object.assign(
              {
                fileList: JSON.stringify(fileArray),
                stdin: this.stdin,
                language: this.language,
                exportEXE: this.exportEXE
              },
              httpObject
            ),
            { emulateJSON: true, responseType: "blob" }
          )
          .then(function(res) {
            console.log(res);
            if (Object.prototype.toString.call(res.body) == "[object Blob]") {
              this.download(res);
              this.$message({
                message: "Compile success, please download the exe.",
                type: "success",
                showClose: true
              });
              this.stdout = "Compile success, please download the exe";
            } else {
              this.stdout = res.data.message;
              this.$message({
                message: "Compile failed",
                type: "error",
                showClose: true
              });
            }
            this.loading = false;
          })
          .catch(function(err) {
            console.log(err);
            this.loading = false;
          });
      }
    },
    save() {
      //localStorage.setItem("code", this.codeText);
      localStorage.setItem("codeList", JSON.stringify(this.codeList));
      localStorage.setItem("fileList", JSON.stringify(this.fileList));
      this.$message({
        message: "Code has been saved",
        type: "success",
        showClose: true
      });
    },
    addNewFile() {
      var repeat = false;
      var newFileName = this.newFileName;
      var language = this.language;
      if (
        (((language == "c" || language == "cpp") &&
          !newFileName.match(new RegExp(".h" + "$", "g")) &&
          !newFileName.match(new RegExp("." + language + "$", "g"))) ||
          (!(language == "c" || language == "cpp") &&
            !newFileName.match(new RegExp("." + language + "$", "g")))) &&
        !newFileName.match(new RegExp(".file" + "$", "g"))
      ) {
        newFileName += "." + language;
      }
      for (var j = 0, len = this.fileList.length; j < len; j++) {
        if (this.fileList[j].label == newFileName) {
          repeat = true;
          break;
        }
      }
      if (!repeat) {
        this.fileList.push({
          value: "",
          label: newFileName
        });
        this.file = newFileName;
        this.codeList.push({
          file: newFileName,
          code: ""
        });
        this.fileIndex = this.codeList.length;
        this.$message({
          message: "Add file " + newFileName,
          type: "success",
          showClose: true
        });
      } else {
        this.$message({
          showClose: true,
          message: newFileName + " is already exist!",
          type: "error"
        });
      }
    },
    DeleteFile() {
      if (this.fileList.length == 1) {
        this.$message({
          showClose: true,
          message: "Can not delete all file",
          type: "error"
        });
      } else {
        var file = this.file;
        for (var j = 0, len = this.fileList.length; j < len; j++) {
          if (this.fileList[j].label == file) {
            this.fileList.splice(j, 1);
            this.file = this.fileList[0].label;
            break;
          }
        }
        for (var j = 0, len = this.codeList.length; j < len; j++) {
          if (this.codeList[j].file == file) {
            this.codeList.splice(j, 1);
            break;
          }
        }
        this.fileIndex = 0;
        this.codeText = this.codeList[0].code;
        this.$message({
          showClose: true,
          message: "Delete " + file,
          type: "warning"
        });
      }
    },
    download(data) {
      if (!data) {
        return;
      }
      //let url = window.URL.createObjectURL(new Blob([data]));
      let url = window.URL.createObjectURL(data.body);
      let link = document.createElement("a");
      link.style.display = "none";
      link.href = url;
      link.setAttribute(
        "download",
        Math.random()
          .toString(36)
          .slice(-8) + ".exe"
      );

      document.body.appendChild(link);
      link.click();
    }
  }
};
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
}
.el-col {
  border-radius: 4px;
}
/*
.bg-purple {
  background: #d3dce6;
}*/
.grid-content {
  border-radius: 4px;
  min-height: 36px;
  /*box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);*/
}
.grid-input {
  border-radius: 4px;
  min-height: 36px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.row-bg {
  padding: 10px 0;
  /*background-color: #f9fafc;*/
}
</style>