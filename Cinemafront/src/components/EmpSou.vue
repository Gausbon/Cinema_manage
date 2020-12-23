<template>

<el-container style="margin-top: -50px; margin-bottom: -50px; border: 1px solid #eee">
  <el-dialog
  title="注销用户"
  style="text-align: center"
  :visible.sync="logoutDialogVisible"
  width="30%"
  :before-close="handleClose">
    <span>确定要注销吗</span><br><br><br>
    <el-button round @click="confirmLogout" type="primary">确 定 </el-button>
    <el-button round @click="logoutDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-dialog
  title="删除周边"
  style="text-align: center"
  :visible.sync="delDialogVisible"
  width="30%"
  :before-close="handleClose">
    <span>确定要删除该周边吗</span><br><br><br>
    <el-button round @click="delete_sou" type="primary">确 定 </el-button>
    <el-button round @click="delDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-dialog
  title="周边操作"
  style="text-align: center"
  :visible.sync="souDialogVisible"
  width="30%"
  :before-close="handleClose">
    <el-form label-width="80px" :model="souModel" :rules="souRules" ref="souModel" >
      <el-form-item label="电影" prop="mno">
        <el-select v-model="souModel.mno" placeholder="请选择电影">
          <el-option v-for="(value) in movieList" :value="value.mno" :label="strip(value.mname)"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="周边名称" prop="soname">
        <el-input v-model="souModel.soname"></el-input>
      </el-form-item>
      <el-form-item label="库存量" prop="sostore">
        <el-input-number v-model="souModel.sosotre" @change="handleChange" :min="1" :step="1"></el-input-number>
      </el-form-item>
    </el-form>
    <el-button round @click="confirmSou" type="primary">确 定 </el-button>
    <el-button round @click="souDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-header style = "background-color: #ffffff; text-align: right">
    <el-menu default-active="3" class="el-menu-demo" mode="horizontal" 
    @select="handleSelect" style = "float: left">
      <el-menu-item index="1" @click="to_movie">电影</el-menu-item>
      <el-menu-item index="2" @click="to_scene">场次</el-menu-item>
      <el-menu-item index="3">场次</el-menu-item>
    </el-menu>
    <el-button round @click="logout">注 销</el-button>
  </el-header>

  <el-container style="height: 600px"> 
    <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
      <template slot-scope="props">
        <el-menu class="el-menu-vertical-demo">
          <el-menu-item>
            <span slot="title">员工姓名：{{emp_list.ename}}</span>
          </el-menu-item>
          <el-menu-item>
            <span slot="title">员工性别：{{emp_list.esex}}</span>
          </el-menu-item>
          <el-menu-item>
            <span slot="title">员工薪资：{{emp_list.ewage}}</span>
          </el-menu-item>
          <el-menu-item>
            <span slot="title">员工部门：{{emp_list.epart}}</span>
          </el-menu-item>
        </el-menu>
      </template>
    </el-aside>
    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <el-container>
          <el-main></el-main>
          <el-aside mode="horizontal">
            <span style="font-size: 130%">您好，亲爱的{{emp_list.ename}}</span>
            <el-divider direction="vertical"></el-divider>
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
                  <el-radio-group v-model="reverse">
                    <el-radio :label="false">正序</el-radio>
                    <el-radio :label="true">倒序</el-radio>
                  </el-radio-group>
                </el-dropdown-item>
                <el-dropdown-item>日期</el-dropdown-item>
                <el-dropdown-item>名称</el-dropdown-item>
                <el-dropdown-item>类型</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-aside>
        </el-conttainer>
      </el-header>

      <el-main>

        <el-table :data="sceneList">
          <el-table-column label="电影名称">
          <template scope="scope"> {{ scope.row.fields.mname }} </template>
          </el-table-column>
          <el-table-column label="周边名称">
          <template scope="scope"> {{ scope.row.fields.soname }} </template>
          </el-table-column>
          <el-table-column label="周边价格">
          <template scope="scope"> {{ scope.row.fields.soprice }}元 </template>
          </el-table-column>
          <el-table-column label="周边库存">
          <template scope="scope"> {{ scope.row.fields.sostore }}件 </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button size="mini" type="primary" @click.native="insert_sou">添加</el-button>
              <el-button size="mini" @click.native="update_sou(scope.row)">编辑</el-button>
              <el-button size="mini" type="danger" 
              @click.native="movieModel.last_name=scope.row.fields.mname; delDialogVisible = true">
              删除</el-button>
            </template>
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
        id: 0,
        emp_list: [],
        movieList: [],
        reverse: false,
        delDialogVisible: false,
        souDialogVisible: false,
        logoutDialogVisible: false,
        new_sou: false,
        sort_type: 'mname',
        reverse: false,
        souModel: { soname:'', sostore:0, mno:0 },
        souRules: {
          soname: [{ required: true, message: '请选择影院', trigger: 'blur' }],
          sostore: [{ required: true, message: '请输入库存', trigger: 'blur' }],
          mno: [{ required: true, message: '请选择电影', trigger: 'blur' }]
        }
      }
    },
    mounted: function() {
      this.init(),
      this.showemp(),
      this.showMovie(),
      this.showSou(),
      this.onInput()
    },
    watch: {
    },
    methods: {
      onInput(){
        this.$forceUpdate();
      },
      showTime(d){
        var date = new Date(d) 
        var output = date.getFullYear()+"年"
        if (date.getMonth()+1 < 10)
          output = output + "0"
        output = output + (date.getMonth()+1)+"月"
        if (date.getDate() < 10)
          output = output + "0"
        output = output+date.getDate()+"日"
        if (date.getHours()<10)
          output = output + "0"
        output = output+date.getHours()+":"
        if (date.getMinutes()<10)
          output = output + "0"
        return output+date.getMinutes();
      },
      showemp(){
        this.id = this.$route.query.id
        console.log("show emp")
        this.$http.post('http://127.0.0.1:8000/api/show_employee',
          JSON.stringify({id: this.id}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.emp_list = res['list']
              } else {
                this.$message.error('查询员工信息失败')
                console.log(res['msg'])
                this.$router.push("/");
              }
          })
      },
      showMovie() {
        console.log("show movie")
        this.$http.post('http://127.0.0.1:8000/api/show_movie',
          JSON.stringify({curFilm:true, curDate:new Date(), r:this.reverse, t:this.sort_type}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                var curDate = new Date()
                this.movieList = res['list']
              } else {
                this.$message.error('查询电影失败')
                console.log(res['msg'])
              }
          })
      },
      showSou(){
        console.log("show sou")
        this.$http.post('http://127.0.0.1:8000/api/show_sou',
          JSON.stringify({curSou:false, r:this.reverse, t:this.sort_type}), {emulateJSON: true})
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
      logout() {
        this.logoutDialogVisible = true // 显示弹框
      },
      confirmLogout(){
        this.$message({ type: 'success', message: '注销成功!'});
        sessionStorage.setItem("token", 'false');
        this.$router.push("/");
      },
      insert_sou(){
        this.new_sou = true;
        this.sceneModel = { 
          mno: this.movieList[0].pk,
          soname:'', sostore:0
        };
        this.souDialogVisible = true;
      },
      update_sou(scope){
        var i = 0, get = 0;
        for (i = 0; i < this.movieList.length; i++) {
            if (this.movieList[i].pk == scope.mno) {
              get = 1;
              return;
            }
        }
        if (get == 0) {
            this.$message.error('不能修改已经下架或暂未上架电影的周边');
            return;
        }
        this.new_sou = false;
        this.souModel = { 
          mno: scope.mno,
          soname:scope_soname, sostore:scope.sostore };
        this.souDialogVisible = true;
      },
      confirmSou(){
        if (this.new_sou) {
          this.$http.post('http://127.0.0.1:8000/api/insert_scene',
          JSON.stringify(this.sceneModel), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '添加场次成功!'});
                this.sceneDialogVisible = false;
                this.showScene();
              } else {
                this.$message.error('添加场次失败')
                console.log(res['msg'])
              }
          })
        } else {
          console.log("update scene")
          this.$http.post('http://127.0.0.1:8000/api/update_scene',
          JSON.stringify(this.sceneModel), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '修改场次成功!'});
                this.sceneDialogVisible = false;
                this.showScene();
              } else {
                this.$message.error('修改场次失败，未知错误')
                console.log(res['msg'])
              }
          })
        }
      },
      delete_scene(){
        this.$http.post('http://127.0.0.1:8000/api/delete_scene',
          JSON.stringify(this.sceneModel), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '删除场次成功!'});
                this.delDialogVisible = false;
                this.showScene();
              } else {
                this.$message.error('删除场次失败')
                console.log(res['msg'])
                this.delDialogVisible = false;
                this.showScene();
              }
          })
      },
      strip(str) {
        return str.replace(/\s*/g,"")
      },
      to_movie() {
        this.$router.push({ path: '/empmovie', query: {id: this.id} })
      },
      to_scene() {
        this.$router.push({ path: '/empscene', query: {id: this.id} })
      }
    }
  };
</script>
