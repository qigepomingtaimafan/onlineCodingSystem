<template>
  <el-select
    ref="selector"
    v-model="value"
    placeholder="请选择"
    filterable
    :filter-method="updateNewValue"
  >
    <el-option v-for="item in valueList" :key="item.value" :label="item.label" :value="item.label">
      <span style="float: left">{{ item.label }}</span>
      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
    </el-option>
  </el-select>
</template>

<script>
export default {
  data() {
    return {
      valueList: this.listFromParent,
      value: this.valueFromParent
    };
  },
  props: {
    valueFromParent: String,
    listFromParent: Array,
    selectorType: String,
    newVauleFromParent: String
  },
  watch: {
    valueFromParent(val) {
      this.value = val;
    },
    listFromParent(val) {
      this.valueList = val;
    },
    value(val) {
      this.$emit("update:valueFromParent", val);
    },
    valueList(val) {
      this.$emit("update:listFromParent", val);
    }
  },
  mounted() {
  },
  methods: {
    updateNewValue(val) {
      if (this.selectorType == "file") {
        this.$emit("update:newValueFromParent", val);
      }
    }
  }
};
</script>