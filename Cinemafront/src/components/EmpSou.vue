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
  title="删除电影"
  style="text-align: center"
  :visible.sync="delDialogVisible"
  width="30%"
  :before-close="handleClose">
    <span>确定要删除周边“{{strip(last_soname)}}”吗</span><br><br><br>
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
      <el-form-item label="电影名称" prop="mno">
        <el-select v-model="souModel.mno" placeholder="请选择电影">
          <el-option v-for="(value) in movieList" :value="value.pk" :label="strip(value.fields.mname)"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="周边名称" prop="soname">
        <el-input v-model="souModel.soname"></el-input>
      </el-form-item>
      <el-form-item label="价格" prop="soprice">
        <el-input-number v-model="souModel.soprice" @change="handleChange" :min="10" :step="5"></el-input-number>
      </el-form-item>
      <el-form-item label="库存量" prop="sostore">
        <el-input-number v-model="souModel.sostore" @change="handleChange" :min="1" :step="1"></el-input-number>
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
      <el-menu-item index="3" >周边</el-menu-item>
      <el-menu-item index="4" @click="to_bill">流水</el-menu-item>
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
          <el-aside>
            <span style="font-size: 130%; float: left">目前上映影片数量：{{movieCount}}</span>
          </el-aside>
          <el-main></el-main>
          <el-aside mode="horizontal">
            <span style="font-size: 130%">您好，亲爱的{{emp_list.ename}}</span>
            <el-divider direction="vertical"></el-divider>
            <el-dropdown :hide-on-click="false">
                <el-button v-if="sort_type=='mname'"> <span>电影名称</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-button v-else-if="sort_type=='soname'"> <span>周边名称</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-button v-else-if="sort_type=='sostore'"> <span>库存量</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-button v-else-if="sort_type=='soprice'"> <span>价格</span>
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
                <el-dropdown-item @click.native="sort_type='mname'; showSou()">电影名称</el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='soname'; showSou()">周边名称</el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='sostore'; showSou()">库存量</el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='soprice'; showSou()">价格</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-aside>
        </el-conttainer>
      </el-header>

      <el-main>

        <el-table :data="souList">
          <el-table-column prop="name" label="电影名称">
          <template scope="scope"> {{ scope.row.fields.mname }} </template>
          </el-table-column>
          <el-table-column prop="address" label="周边名称">
          <template scope="scope"> {{ scope.row.fields.soname }} </template>
          </el-table-column>
          <el-table-column prop="address" label="价格">
          <template scope="scope"> {{ scope.row.fields.soprice}} </template>
          </el-table-column>
          <el-table-column prop="address" label="库存">
          <template scope="scope"> {{ scope.row.fields.sostore }} </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button size="mini" type="primary" @click.native="insert_sou">添加</el-button>
              <el-button size="mini" @click.native="update_sou(scope.row)">编辑</el-button>
              <el-button size="mini" type="danger" 
              @click.native="last_sono=scope.row.pk; last_soname=scope.row.fields.soname, delDialogVisible = true">
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
        souList: [],
        movieList: [],
        emp_list: [],
        new_sou: false,
        last_sono: 0,
        last_soname: '',
        souModel: { mno: 0, soname: '', soprice: 0, sostore:0 },
        sort_type: 'mname',
        reverse: false,
        logoutDialogVisible: false,
        souDialogVisible: false,
        delDialogVisible: false,
        souRules: {
          mno: [{ required: true, message: '请选择电影', trigger: 'blur' }],
          soname: [{ required: true, message: '请输入周边名称', trigger: 'blur' }],
          soprice: [{ required: true, message: '请输入价格', trigger: 'blur' }],
          sostore: [{ required: true, message: '请输入库存量', trigger: 'blur' }]
        }
      }
    },
    mounted: function() {
      this.init(),
      this.showemp(),
      this.getMovie(),
      this.showSou(),
      this.onInput()
      
    },
    watch: {
      reverse: 'showSou'
    },
    methods: {
      init() {
        if (sessionStorage.getItem("type") != 'emp') {
            sessionStorage.setItem("token", 'false')
            this.$router.push({ path: '/' })
        }
        this.id = this.$route.query.id
        console.log(this.id);
      },
      onInput(){
        this.$forceUpdate();
      },
      showemp(){
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
      getMovie(){
        console.log("get movie")
        this.$http.post('http://127.0.0.1:8000/api/show_movie',
          JSON.stringify({curFilm:true, curDate:new Date(), r:false, t:'online'}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
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
        if (this.movieList.length == 0) {
            this.$message.error('目前没有正在上映的电影')
            return;
        }
        this.new_sou = true;
        this.souModel = { mno: this.movieList[0].pk, soname: '', soprice: 100, sostore:1 };
        this.souDialogVisible = true;
      },
      update_sou(scope){
        this.new_sou = false;
        this.souModel = { id: scope.pk, mno: scope.fields.mno, soname: scope.fields.soname, 
          soprice: scope.fields.soprice, sostore: scope.fields.sostore};
        this.souDialogVisible = true;
      },
      delete_sou(){
        this.$http.post('http://127.0.0.1:8000/api/delete_sou',
          JSON.stringify({id: this.last_sono}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '删除周边成功!'});
                this.delDialogVisible = false;
                this.showSou();
              } else {
                if (res.error_num == 2)
                  this.$message.error('删除周边失败，该周边已被购买')
                else
                  this.$message.error('删除周边失败')
                console.log(res['msg'])
                this.delDialogVisible = false;
                this.showSou();
              }
          })
      },
      confirmSou(){
        if (this.new_sou) {
          this.$http.post('http://127.0.0.1:8000/api/add_sou',
            JSON.stringify(this.souModel), {emulateJSON: true})
            .then((response) => {
                var res = JSON.parse(response.bodyText)
                if (res.error_num == 0) {
                  this.$message({ type: 'success', message: '周边添加成功！'});
                  this.showSou();
                  this.souDialogVisible = false;
                } else {
                  this.$message.error('周边添加失败')
                  this.souDialogVisible = false;
                  console.log(res['msg'])
                  return;
                }
            })
        } else {
          this.$http.post('http://127.0.0.1:8000/api/update_sou',
            JSON.stringify(this.souModel), {emulateJSON: true})
            .then((response) => {
                var res = JSON.parse(response.bodyText)
                if (res.error_num == 0) {
                  this.$message({ type: 'success', message: '周边更新成功！'});
                  this.showSou();
                  this.souDialogVisible = false;
                } else if (res.error_num == 2) {
                  this.$message.error('周边更新失败，周边名称重复')
                  console.log(res['msg'])
                } else {
                  this.$message.error('周边更新失败')
                  this.souDialogVisible = false;
                  console.log(res['msg'])
                  return;
                }
            })
        }
      },
      strip(str) {
        return str.replace(/\s*/g,"")
      },
      to_scene() {
        this.$router.push({ path: '/empscene', query: {id: this.id} })
      },
      to_movie() {
        this.$router.push({ path: '/empmovie', query: {id: this.id} })
      },
      to_bill() {
        this.$router.push({ path: '/empbill', query: {id: this.id} })
      }
    }
  };
</script>
