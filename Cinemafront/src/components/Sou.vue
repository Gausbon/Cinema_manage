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

  <el-dialog
  title="注 册"
  style="text-align: center"
  :visible.sync="regDialogVisible"
  width="30%"
  :before-close="handleClose">
    <el-form label-width="120px" :model="regModel" :rules="regRules" ref="regModel" >
      <el-row><el-col>
        <el-form-item label="用户名" prop="name" style = "float: left">
        <el-input v-model="regModel.name" @input="onInput()"></el-input>
      </el-col></el-row>
      <el-row><el-col>
        <el-form-item label="密码" prop="pass" style = "float: left">
        <el-input v-model="regModel.pass" type="password" @input="onInput()"></el-input>
      </el-col></el-row>
      <el-row><el-col>
        <el-form-item label="确认密码" prop="confirmpass" style = "float: left">
        <el-input v-model="regModel.confirmpass" type="password" @input="onInput()"></el-input>
      </el-col></el-row>
    </el-form>
    <el-button round @click="submitReg" type="primary">确 定 </el-button>
    <el-button round @click="regDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-header style = "background-color: #ffffff; text-align: right">
    <el-menu default-active="2" class="el-menu-demo" mode="horizontal" 
    @select="handleSelect" style = "float: left">
      <el-menu-item index="1"  @click="to_movie">电影</el-menu-item>
      <el-menu-item index="2">周边</el-menu-item>
    </el-menu>
    <el-button type="primary" round @click="login()">登 录</el-button>
    <el-button round  @click="reg()">注 册</el-button>
  </el-header>

  <el-container style="height: 600px">
    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <el-container>
          <el-aside>
            <span style="font-size: 130%; float: left">目前周边数量：{{souCount}}</span>
          </el-aside>
          <el-main></el-main>
          <el-aside width = "300px" mode="horizontal">
            <el-dropdown :hide-on-click="false">
                <el-button v-if="sort_type=='soname'"> <span>周边名称</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-button v-else-if="sort_type=='mname'"> <span>电影名称</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-button v-else-if="sort_type=='soprice'"> <span>售价</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>
                  <el-radio-group v-model="reverse">
                    <el-radio :label="false">正序</el-radio>
                    <el-radio :label="true">倒序</el-radio>
                  </el-radio-group>
                </el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='soname'; showSou()">周边名称</el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='mname'; showSou()">电影名称</el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='soprice'; showSou()">售价</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-aside>
        </el-conttainer>
      </el-header>

      <el-main>
        <el-table :data="souList">
          <el-table-column label="电影名称">
          <template scope="scope"> {{ scope.row.fields.mname }} </template>
          </el-table-column>
          <el-table-column label="周边名称">
          <template scope="scope"> {{ scope.row.fields.soname }} </template>
          </el-table-column>
          <el-table-column label="售价">
          <template scope="scope"> {{ scope.row.fields.soprice }} </template>
          </el-table-column>
          <el-table-column label="库存">
          <template scope="scope"> {{ scope.row.fields.sostore }} </template>
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
      var validatepass = (rule, value, callback) => {
          if (this.regModel.pass >= this.regModel.confirmpass) {
            callback(new Error('两次输入密码不一致'));
          } else {
            callback();
          }
      };
      return {
        souList: [],
        souCount: 0,
        sort_type: 'mname',
        loginDialogVisible: false,
        regDialogVisible: false,
        reverse: false,
        loginModel: { name: '', pass: '' },
        loginRules: {
          name: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
          pass: [{ required: true, message: '请输入密码', trigger: 'blur' }]
        },
        regModel: { name: '', pass: '', confirmpass: '', date:new Date() },
        regRules: {
          name: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
          pass: [{ required: true, message: '请输入密码', trigger: 'blur' }, { validator: validatepass, trigger: 'blur' }],
          confirmpass: [{ required: true, message: '请确认密码', trigger: 'blur' }, { validator: validatepass, trigger: 'blur' }],
        }
      }
    },
    mounted: function() {
      this.showSou(),
      this.onInput()
    },
    watch: {
      reverse: 'showSou'
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
      showSou(){
        console.log("show sou")
        this.$http.post('http://127.0.0.1:8000/api/show_sou',
          JSON.stringify({curSou:true, curDate : new Date(), r:this.reverse, t:this.sort_type}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.souList = res['list']
                this.souCount = this.souList.length
              } else {
                this.$message.error('查询周边失败')
                console.log(res['msg'])
              }
          })
      },
      login() {
        this.loginModel = { name: '', pass: '' };
        this.loginDialogVisible = true // 显示弹框
      },
      reg() {
        this.regModel = { name: '', pass: '', confirmpass: '', date: new Date() };
        this.regDialogVisible = true // 显示弹框
      },
      submitReg() {
        var name = this.regModel.name;
        this.$http.post('http://127.0.0.1:8000/api/reg',
          JSON.stringify(this.regModel), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '用户\"' + name + '\"注册成功!'});
                this.regDialogVisible = false;
              } else {
                if (res.error_num == 2)
                  this.$message.error('用户名有重复，请重新选取用户名！')
                else
                  this.$message.error('注册失败！请重试')
                console.log(res['msg'])
              }
          })
      },
      submitLogin() {
        this.$http.post('http://127.0.0.1:8000/api/login',
          JSON.stringify(this.loginModel), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                if (res.type == "vip") {
                  console.log('vip login, vip num = ' + res.id)
                  sessionStorage.setItem("token", 'true');
                  sessionStorage.setItem("type", 'vip');
                  this.$message({ type: 'success', message: '登录成功!'});
                  this.$router.push({ path: '/vipmovie', query: {id: res.id} })
                } else if (res.type == 'emp') {
                  console.log('employee login, employee num = ' + res.id)
                  sessionStorage.setItem("token", 'true');
                  sessionStorage.setItem("type", 'emp');
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
      },
      to_movie() {
        this.$router.push({path: '/'})
      }
    }
  };
</script>
