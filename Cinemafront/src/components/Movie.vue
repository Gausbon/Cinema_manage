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
    <el-menu default-active="1" class="el-menu-demo" mode="horizontal" 
    @select="handleSelect" style = "float: left">
      <el-menu-item index="1">电影</el-menu-item>
      <el-menu-item index="2">周边</el-menu-item>
    </el-menu>
    <el-button type="primary" round @click="login()">登 录</el-button>
    <el-button round>注 册</el-button>
  </el-header>

  <el-container style="height: 600px">
    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <el-container>
          <el-aside>
            <span style="font-size: 130%; float: left">目前上映影片数量：{{movieCount}}</span>
          </el-aside>
          <el-main></el-main>
          <el-aside width = "300px" mode="horizontal">
            <el-dropdown :hide-on-click="false">
                <el-button v-if="sort_type=='online'"> <span>日期</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-button v-else-if="sort_type=='mname'"> <span>名称</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-button v-else-if="sort_type=='type'"> <span>类型</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>
                  <el-radio-group v-model="reverse" @click.native="showMovies()">
                    <el-radio :label="false">正序</el-radio>
                    <el-radio :label="true">倒序</el-radio>
                  </el-radio-group>
                </el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='online'; showMovies()">日期</el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='mname'; showMovies()">名称</el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='type'; showMovies()">类型</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
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
        sort_type: 'online',
        loginDialogVisible: false,
        reverse: false,
        loginModel: { name: '', pass: '' },
        loginRules: {
          name: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
          pass: [{ required: true, message: '请输入密码', trigger: 'blur' }]
        }
      }
    },
    mounted: function() {
      this.showMovies(),
      this.onInput()
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
        console.log("show movie")
        this.$http.post('http://127.0.0.1:8000/api/show_movie',
          JSON.stringify({curFilm:true, curDate : new Date(), r:this.reverse, t:this.sort_type}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                var curDate = new Date()
                this.movieList = res['list']
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
                  console.log('vip login, vip num = ' + res.id)
                  sessionStorage.setItem("token", 'true');
                  sessionStorage.setItem("type", 'vip');
                  this.$message({ type: 'success', message: '登录成功!'});
                  this.$router.push({ path: '/vip', query: {id: res.id} })
                } else if (res.type == 'movie') {
                  console.log('movie employee login, employee num = ' + res.id)
                  sessionStorage.setItem("token", 'true');
                  sessionStorage.setItem("type", 'movie');
                  this.$message({ type: 'success', message: '登录成功!'});
                  this.$router.push({ path: '/empmovie', query: {id: res.id} })
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
