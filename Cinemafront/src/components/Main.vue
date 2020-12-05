<template>

<el-container style="margin-top: -50px; margin-bottom: -50px; border: 1px solid #eee">
  <el-dialog
  title="登 录"
  style="text-align: center"
  :visible.sync="loginDialogVisible"
  width="30%"
  :before-close="handleClose">
    <el-form label-width="120px" :model="loginModel" :rules="loginRules" ref="loginModel" >
      <el-row><el-col>
        <el-form-item label="用户名" prop="name" style = "float: left">
        <el-input v-model="loginModel.name" @input="onInput()"></el-input>
      </el-col></el-row>
      <el-row><el-col>
        <el-form-item label="密码" prop="pass" style = "float: left">
        <el-input v-model="loginModel.pass" type="password" @input="onInput()"></el-input>
      </el-col></el-row>
    </el-form>
    <el-button round @click="submitLogin" type="primary">确 定 </el-button>
    <el-button round @click="loginDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-header style = "background-color: #ffffff; text-align: right">
    <el-menu default-openeds="['1']" style = "float: left">
      <el-submenu index="1">
        <template slot="title">主页面</template>
      <el-submenu>
    </el-menu>
    <el-button type="primary" round @click="login()">登 录</el-button>
    <el-button round>注 册</el-button>
  </el-header>

  <el-container style="height: 600px">
    <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
      <el-menu :default-openeds="['1', '3']">
        <el-submenu index="1">
          <template slot="title"><i class="el-icon-message"></i>导航一</template>
          <el-menu-item-group>
            <template slot="title">分组一</template>
            <el-menu-item index="1-1">选项1</el-menu-item>
            <el-menu-item index="1-2">选项2</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="分组2">
            <el-menu-item index="1-3">选项3</el-menu-item>
          </el-menu-item-group>
          <el-submenu index="1-4">
            <template slot="title">选项4</template>
            <el-menu-item index="1-4-1">选项4-1</el-menu-item>
          </el-submenu>
        </el-submenu>
      </el-menu>
    </el-aside>



    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <el-container>
          <el-aside>
            <span style="font-size: 130%; float: left">目前上映影片数量：{{movieCount}}</span>
          </el-aside>
          <el-main></el-main>
          <el-aside width = "100px">
            <span>尚未登录</span>
          </el-aside>
        </el-conttainer>
      </el-header>

      <el-main>
        <el-table :data="movieList">
          <el-table-column prop="name" label="电影名称">
          <template scope="scope"> {{ scope.row.fields.mname }} </template>
          </el-table-column>
          <el-table-column prop="address" label="导演">
          <template scope="scope"> {{ scope.row.fields.director }} </template>
          </el-table-column>
          <el-table-column prop="address" label="主演">
          <template scope="scope"> {{ scope.row.fields.actor }} </template>
          </el-table-column>
          <el-table-column prop="address" label="类型">
          <template scope="scope"> {{ scope.row.fields.type }} </template>
          </el-table-column>
          <el-table-column prop="address" label="时长">
          <template scope="scope"> {{ scope.row.fields.time }} </template>
          </el-table-column>
          <el-table-column prop="address" label="上映时间">
          <template scope="scope"> {{showDate(scope.row.fields.online)}} </template>
          </el-table-column>
          <el-table-column prop="address" label="下映时间">
          <template scope="scope"> {{ showDate(scope.row.fields.offline) }} </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>
</el-container>
</template>

<style>
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }

  .el-aside {
    color: #333;
  }
</style>

<script>
  export default {
    data() {
      return {
        movieList: [],
        movieCount: 0,
        loginDialogVisible: false,
        loginModel: { name: '', pass: '' },
        loginRules: {
          name: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
          pass: [{ required: true, message: '请输入密码', trigger: 'blur' }]
        }
      }
    },
    mounted: function() {
      this.showMovies()
    },
    methods: {
      onInput(){
        this.$forceUpdate();
      },
      showDate(d){
        var date = new Date(d)
        var output = date.getFullYear()+"年"
        if (date.getMonth()+1 < 10)
          output = output + "0"
        output = output + (date.getMonth()+1)+"月"
        if (date.getDate() < 10)
          output = output + "0"
        return output+date.getDate()+"日";
      },
      showMovies(){
        this.$http.post('http://127.0.0.1:8000/api/show_movie',
          JSON.stringify({curFilm : true, curDate : new Date()}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              console.log(res)
              if (res.error_num == 0) {
                var curDate = new Date()
                this.movieList = res['list']
                console.log(typeof(this.movieList))
                this.movieCount = this.movieList.length
              } else {
                this.$message.error('查询电影失败')
                console.log(res['msg'])
              }
          })
      },
      login() {
        this.loginDialogVisible = true // 显示弹框
      },
      submitLogin() {
        this.$http.post('http://127.0.0.1:8000/api/login',
          JSON.stringify(this.loginModel), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              console.log(res)
              if (res.error_num == 0) {
                if (res.type == "vip") {
                  console.log('vip')
                  this.$router.push({ path: '/vip' })
                }
              } else {
                if (res.error_num == 2)
                  this.$message.error('用户名或密码错误！')
                else
                  this.$message.error('登录失败！请重试')
                console.log(res['msg'])
              }
          })
      }
    }
  };
</script>
