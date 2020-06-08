<template>
  <div class="my-child">
    <h5>我是子组件，我可以通过属性props来接收父组件传过来的年龄值是:{{deliverParentAge}}，这是一个数字类型</h5>
    <h5>现在我要告诉父组件，我的年龄是{{childAge}},这样他就可以知道，我们<button @click="DiffAge">相差</button>多少岁</h5>
    <h5>并且，我要告诉他，他今年生日已经过了，所以他的年龄应该<button @click="AddAge">加1</button></h5>
    下面我要通过this.$emit方法提交一个事件addParentAge，告诉我的父组件，他的实际年龄
    <hr> 关于钱
    <button @click="add">加10</button>  
    <h3>笔记</h3>
    <br> 传值可以使用 :  冒号传,props接收
    <br> 设置值可以使用 emit 事件 @childEmitFunction="parentHandle" 提交事件
    <br>
  </div>
</template>

<script>
export default {
  data() {
    return {
      childAge: 22,
      cmoney:0,
    };
  },
  props: {
    deliverParentAge: Number,
    money: Number,
  },
  computed: {
    parentActualAge() {
      return this.deliverParentAge + 1;
    }
  },
  mounted(){
     console.log("child ",this.$props)  
     this.cmoney = this.$props.money
  },
  methods: {
    AddAge() {
      this.$emit("addParentAge", this.parentActualAge);
    },
    DiffAge() {
      this.$emit("differAge", this.childAge);
    },
    add: function () {
              this.cmoney += 10;
              this.$emit('input', this.cmoney); // 这里emit 的是 input事件哦~
            //  事件名不存在任何自动化的大小写转换,而是触发的事件名需要完全匹配监听这个事件所用的名称，所以这里仍旧是'update-data'
     },
  }
};
</script>
 