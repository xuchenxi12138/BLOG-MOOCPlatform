<template>
  <form>
    <el-input v-model="pwd" disabled :type="type">
      <el-button class="el-icon-view" slot="append" @click="changeType"></el-button>
    </el-input>
  </form>

</template>

<script>
export default {
  name: "PasswordModule",
  props:['value','disable'],
  data(){
    return{
      type: 'password',
      pwd:""
    }
  },
  created(){
    this.pwd=this.value
    // this.pwd="123456"
  },
  methods: {
    changeType(){
      console.log(this.type);
      if(this.type==='password'){
        this.type='text'
      }
      else this.type='password'
    }
  }
}
</script>

<style scoped>
.eye{
  color: #7e7878;
}
.eye:hover{
  opacity: 0.5;
  cursor: pointer;
}
.password{
  border: none;
  width: 80%;
}
.password:disabled{
  background-color: #ffffff;
}
.password:focus{
  outline: none;
}
</style>