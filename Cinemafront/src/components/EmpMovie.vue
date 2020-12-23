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
    <span>确定要删除电影{{movieModel.last_name}}吗</span><br><br><br>
    <el-button round @click="delete_movie" type="primary">确 定 </el-button>
    <el-button round @click="delDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-dialog
  title="电影操作"
  style="text-align: center"
  :visible.sync="movieDialogVisible"
  width="30%"
  :before-close="handleClose">
    <el-form label-width="80px" :model="movieModel" :rules="movieRules" ref="movieModel" >
      <el-form-item label="电影名称" prop="mname">
        <el-input v-model="movieModel.mname"></el-input>
      </el-form-item>
      <el-form-item label="导演" prop="director">
        <el-input v-model="movieModel.director"></el-input>
      </el-form-item>
      <el-form-item label="主演" prop="actor">
        <el-input v-model="movieModel.actor"></el-input>
      </el-form-item>
      <el-form-item label="电影时长" prop="time">
        <el-input-number v-model="movieModel.time" @change="handleChange" :min="60" :max="300" :step="5"></el-input-number>
      </el-form-item>
      <el-form-item label="电影类型" prop="type">
        <el-select v-model="movieModel.type" placeholder="请选择活动区域">
          <el-option label="恐怖片" value="恐怖片"></el-option>
          <el-option label="喜剧片" value="喜剧片"></el-option>
          <el-option label="动作片" value="动作片"></el-option>
          <el-option label="科幻片" value="科幻片"></el-option>
          <el-option label="言情片" value="言情片"></el-option>
          <el-option label="警匪片" value="警匪片"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="上映时间" prop="online">
        <el-date-picker
          v-model="movieModel.online"
          type="date"
          placeholder="上映时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="下映时间"  prop="offline">
        <el-date-picker
          v-model="movieModel.offline"
          type="date"
          placeholder="下映时间">
        </el-date-picker>
      </el-form-item>
    </el-form>
    <el-button round @click="confirmMovie" type="primary">确 定 </el-button>
    <el-button round @click="movieDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-header style = "background-color: #ffffff; text-align: right">
    <el-menu default-active="1" class="el-menu-demo" mode="horizontal" 
    @select="handleSelect" style = "float: left">
      <el-menu-item index="1">电影</el-menu-item>
      <el-menu-item index="2" @click="to_scene">场次</el-menu-item>
      <el-menu-item index="3" @click="to_sou">周边</el-menu-item>
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
          <el-table-column prop="address" label="类型">
          <template scope="scope"> {{ scope.row.fields.type }} </template>
          </el-table-column>
          <el-table-column prop="address" label="上映时间">
          <template scope="scope"> {{showDate(scope.row.fields.online)}} </template>
          </el-table-column>
          <el-table-column prop="address" label="下映时间">
          <template scope="scope"> {{ showDate(scope.row.fields.offline) }} </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button size="mini" type="primary" @click.native="insert_movie">添加</el-button>
              <el-button size="mini" @click.native="update_movie(scope.row.fields)">编辑</el-button>
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
      var validateline = (rule, value, callback) => {
          if (this.movieModel.online >= this.movieModel.offline) {
            callback(new Error('下映时间需晚于上映时间'));
          } else {
            callback();
          }
      };
      return {
        id: 0,
        movieList: [],
        emp_list: [],
        movieCount: 0,
        new_movie: false,
        last_name: '',
        movieModel: { last_name: '', mname: '', director: '', actor: '', time: 120, type: '', online:'', offline:'' },
        sort_type: 'online',
        logoutDialogVisible: false,
        movieDialogVisible: false,
        reverse: false,
        delDialogVisible: false,
        movieRules: {
          mname: [{ required: true, message: '请输入电影名称', trigger: 'blur' }],
          director: [{ required: true, message: '请输入导演', trigger: 'blur' }],
          actor: [{ required: true, message: '请输入主演', trigger: 'blur' }],
          director: [{ required: true, message: '请输入导演', trigger: 'blur' }],
          time: [{ required: true, message: '请输入时长', trigger: 'blur' }],
          type: [{ required: true, message: '请选择类型', trigger: 'blur' }],
          online: [{ required: true, message: '请选择上映时间', trigger: 'blur' }, { validator: validateline, trigger: 'blur' }],
          offline: [{ required: true, message: '请选择下映时间', trigger: 'blur' }, { validator: validateline, trigger: 'blur' }]
        }
      }
    },
    mounted: function() {
      this.showemp(),
      this.showMovies(),
      this.onInput()
      
    },
    watch: {
      reverse: 'showMovies'
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
      showemp(){
        if (sessionStorage.getItem("type") != 'movie') {
          sessionStorage.setItem("token", 'false')
          this.$router.push({ path: '/' })
        }
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
      showMovies(){
        console.log("show movie")
        this.$http.post('http://127.0.0.1:8000/api/show_movie',
          JSON.stringify({curFilm:false, r:this.reverse, t:this.sort_type}), {emulateJSON: true})
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
      logout() {
        this.logoutDialogVisible = true // 显示弹框
      },
      confirmLogout(){
        this.$message({ type: 'success', message: '注销成功!'});
        sessionStorage.setItem("token", 'false');
        this.$router.push("/");
      },
      insert_movie(){
        this.new_movie = true;
        var d = new Date();
        this.movieModel = { 
          last_name: 'last_movie', 
          mname: '', 
          director: '', 
          actor: '', 
          time: 120, 
          type: '', 
          online:new Date(), 
          offline:new Date(d.setTime(d.getTime()+24*60*60*1000)) };
        this.movieDialogVisible = true;
      },
      update_movie(scope){
        this.new_movie = false;
        console.log(scope.mno)
        this.movieModel = { 
          last_name: scope.mname,
          mname: scope.mname.replace(/\s*/g,""), 
          director: scope.director.replace(/\s*/g,""), 
          actor: scope.actor.replace(/\s*/g,""), 
          time: scope.time,  
          type: scope.type, 
          online: scope.online,
          offline: scope.offline };
        this.movieDialogVisible = true;
      },
      confirmMovie(){
        if (this.new_movie) {
          this.$http.post('http://127.0.0.1:8000/api/insert_movie',
          JSON.stringify(this.movieModel), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '添加电影成功!'});
                this.movieDialogVisible = false;
                this.showMovies();
              } else if (res.error_num == 2) {
                this.$message.error('添加电影失败，影片名称重复')
                console.log(res['msg'])
              } else {
                this.$message.error('添加电影失败')
                console.log(res['msg'])
              }
          })
        } else {
          console.log("update movie")
          this.$http.post('http://127.0.0.1:8000/api/update_movie',
          JSON.stringify(this.movieModel), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '修改电影成功!'});
                this.movieDialogVisible = false;
                this.showMovies();
              } else if (res.error_num == 2) {
                this.$message.error('修改电影失败，影片名称重复')
                console.log(res['msg'])
              } else {
                this.$message.error('修改电影失败，未知错误')
                console.log(res['msg'])
              }
          })
        }
      },
      delete_movie(){
        this.$http.post('http://127.0.0.1:8000/api/delete_movie',
          JSON.stringify(this.movieModel), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '删除电影成功!'});
                this.delDialogVisible = false;
                this.showMovies();
              } else {
                if (res.error_num == 2)
                  this.$message.error('删除电影失败，存在包含该电影的场次')
                else
                  this.$message.error('删除电影失败')
                console.log(res['msg'])
                this.delDialogVisible = false;
                this.showMovies();
              }
          })
      },
      to_scene() {
        this.$router.push({ path: '/empscene', query: {id: this.id} })
      },
      to_sou() {
        this.$router.push({ path: '/empsou', query: {id: this.id} })
      }
    }
  };
</script>
