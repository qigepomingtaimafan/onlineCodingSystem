<template>
  <div>
    <codemirror :value="value" :options="editorOption" ref="myEditor" @change="change"></codemirror>
  </div>
</template>

<script>
import { codemirror } from "vue-codemirror-lite";
//require('codemirror/mode/cmake/cmake');
require("codemirror/mode/clike/clike");
require("codemirror/mode/python/python");
require("codemirror/theme/idea.css");
export default {
  data() {
    return {
      value: this.valueFromParent,
      language: this.languageFromParent,
      editorOption: {
        mode: "text/x-c++src", //text/x-c++src,text/x-csrc,text/x-java
        lineNumbers: "true",
        smartIndent: "true",
        matchBrackets: "true",
        styleActiveLine: "true",
        lineWrapping: true,
        extraKeys: { "Ctrl-Space": "autocomplete" },
        direction: "ltr"
        //theme: 'idea'
      }
    };
  },
  props: {
    valueFromParent: String,
    languageFromParent: String,
    fileFromParent: String
  },
  watch: {
    fileFromParent(val) {
      if (this.editor) this.editor.setValue(this.valueFromParent);
    },
    valueFromParent(val) {
      //if (this.editor) this.editor.setValue(val);
      this.value = val;
    },
    languageFromParent(val) {
      this.language = val;
      if (this.editor)
        switch (val) {
          case "c":
            this.editor.setOption("mode", "text/x-csrc");
            break;
          case "cpp":
            this.editor.setOption("mode", "text/x-java");
            break;
          case "cpp":
            this.editor.setOption("mode", "text/x-c++src");
            break;
          case "py":
            this.editor.setOption("mode", "python");
            break;
        }
    },
    value(val) {
      this.$emit("update:valueFromParent", val);
      //this.editor.refresh();
    }
  },
  computed: {
    editor() {
      // get current editor object
      return this.$refs.myEditor.editor;
    }
  },
  mounted() {
    // use editor object...
    this.editor.focus();
    console.log("this is current editor object", this.editor);
    this.editor.setSize("100%", "100%");
  },
  methods: {
    change(val) {
      this.$emit("update:valueFromParent", val);
    }
  }
};
</script>

<style>
.CodeMirror {
  /*border: 1px solid #eee;*/
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: auto;
}

.CodeMirror-scroll {
  height: auto;
  overflow-y: hidden;
  overflow-x: auto;
}
</style>