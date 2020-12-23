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
  title="删除场次"
  style="text-align: center"
  :visible.sync="delDialogVisible"
  width="30%"
  :before-close="handleClose">
    <span>确定要删除该场次吗</span><br><br><br>
    <el-button round @click="delete_scene" type="primary">确 定 </el-button>
    <el-button round @click="delDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-dialog
  title="场次操作"
  style="text-align: center"
  :visible.sync="sceneDialogVisible"
  width="30%"
  :before-close="handleClose">
    <el-form label-width="80px" :model="sceneModel" :rules="sceneRules" ref="sceneModel" >
      <el-form-item label="影院" prop="cno">
        <el-select v-model="sceneModel.cno" placeholder="请选择影院">
          <el-option v-for="(value) in cinemaList" :value="value.cno" :label="strip(value.cname)"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="影厅" prop="hno">
        <el-select v-model="sceneModel.hno" placeholder="请选择影厅">
          <el-option v-for="(value) in hallList" :value="value.hno" :label="strip(value.hname)"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="电影" prop="mno">
        <el-select v-model="sceneModel.mno" placeholder="请选择电影">
          <el-option v-for="(value) in movieList" :value="value.fields.mno" :label="strip(value.fields.mname)"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="上映时间" prop="ontime">
        <el-date-picker
          v-model="sceneModel.ontime"
          type="datetime"
          placeholder="上映时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="价格" prop="price">
        <el-input-number v-model="sceneModel.price" @change="handleChange" :min="30" :max="300" :step="5"></el-input-number>
      </el-form-item>
    </el-form>
    <el-button round @click="confirmScene" type="primary">确 定 </el-button>
    <el-button round @click="sceneDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-header style = "background-color: #ffffff; text-align: right">
    <el-menu default-active="2" class="el-menu-demo" mode="horizontal" 
    @select="handleSelect" style = "float: left">
      <el-menu-item index="1" @click="to_movie">电影</el-menu-item>
      <el-menu-item index="2">场次</el-menu-item>
      <el-menu-item index="3" @click="to_sou">周边</el-menu-item>
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
          <el-table-column label="影院名称">
          <template scope="scope"> {{ scope.row.fields.cname }} </template>
          </el-table-column>
          <el-table-column label="位置">
          <template scope="scope"> {{ scope.row.fields.cloc }} </template>
          </el-table-column>
          <el-table-column label="影院规模">
          <template scope="scope"> {{ scope.row.fields.csize }} </template>
          </el-table-column>
          <el-table-column type="expand">
            <template slot-scope="scope">
              <el-table :data="scope.row.fields.scene">
                <template slot="empty"> 暂无场次，点此添加<br>
                  <el-button size="mini" type="primary" @click.native="insert_scene()">添加</el-button>
                </template>
                <el-table-column label="影厅">
                <template slot-scope="scope"> {{ scope.row.hname }} </template>
                </el-table-column>
                <el-table-column label="电影名称">
                <template slot-scope="scope"> {{ scope.row.mname }} </template>
                </el-table-column>
                <el-table-column label="上映时间">
                <template slot-scope="scope"> {{ showTime(scope.row.ontime) }} </template>
                </el-table-column>
                <el-table-column label="时长" min-width="50%">
                <template slot-scope="scope"> {{ scope.row.time }}分 </template>
                </el-table-column>
                <el-table-column label="票价" min-width="50%">
                <template slot-scope="scope"> {{ scope.row.price }} </template>
                </el-table-column>
                 <el-table-column label="操作" min-width="130%">
                    <template slot-scope="scope">
                      <el-button size="mini" type="primary" @click.native="insert_scene(scope.row.cno)">添加</el-button>
                      <el-button size="mini" @click.native="update_scene(scope.row)">编辑</el-button>
                      <el-button size="mini" type="danger" 
                      @click.native="sceneModel.last_pk=scope.row.sno; delDialogVisible = true">
                      删除</el-button>
                    </template>
                  </el-table-column>
              </el-table>
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
        sceneList: [],
        cinemaList: [],
        hallList: [],
        emp_list: [],
        movieList: [],
        reverse: false,
        delDialogVisible: false,
        sceneDialogVisible: false,
        logoutDialogVisible: false,
        new_scene: false,
        sceneModel: { last_pk: -1, cno: 0, hno: 0, mno: 0, ontime: '', offtime: '', price: ''},
        sceneRules: {
          cno: [{ required: true, message: '请选择影院', trigger: 'blur' }],
          hno: [{ required: true, message: '请选择影厅', trigger: 'blur' }],
          mno: [{ required: true, message: '请选择电影', trigger: 'blur' }],
          ontime: [{ required: true, message: '请选择上映时间', trigger: 'blur' }],
          price: [{ required: true, message: '请输入价格', trigger: 'blur' }]
        }
      }
    },
    mounted: function() {
      this.init(),
      this.showemp(),
      this.showScene(),
      this.getHall(),
      this.onInput()
    },
    watch: {
        'sceneModel.cno': {
          handler(newName, oldName) {
            this.getHallList();
          },
          immediate: true,
          deep: true
        }
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
      showScene(){
        console.log("show scene")
        this.$http.get('http://127.0.0.1:8000/api/show_scene')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              this.sceneList = res.list
            } else {
               this.$message.error('删除电影失败')
               console.log(res['msg'])
            }
          })
      },
      getHall(){
        console.log("get hall")
        this.$http.post('http://127.0.0.1:8000/api/show_hall_movie',
          JSON.stringify({curDate:new Date()}), {emulateJSON: true})
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              this.cinemaList = res.clist
              this.movieList = res.mlist
              this.getHallList()
            } else {
               this.$message.error('获取影院信息失败')
               console.log(res['msg'])
            }
          })
      },
      getHallList() {
        var i = 0, j = 0;
        var tmp_hno = 0;
        for (i = 0; i < this.cinemaList.length; i++) {
          if (this.cinemaList[i].cno == this.sceneModel.cno) {
            this.hallList = this.cinemaList[i].hall;
            if (this.hallList.length > 0)
              tmp_hno = this.hallList[0].hno;
            for (j = 0; j < this.hallList.length; j++) {
              if (this.hallList[j].hno == this.sceneModel.hno)
                return;
            }
            this.sceneModel.hno = tmp_hno;
            return;
          }
        }
      },
      logout() {
        this.logoutDialogVisible = true // 显示弹框
      },
      confirmLogout(){
        this.$message({ type: 'success', message: '注销成功!'});
        sessionStorage.setItem("token", 'false');
        this.$router.push("/");
      },
      insert_scene(cno_tmp){
        this.new_scene = true;
        var d = new Date();
        this.sceneModel = { 
          last_pk: 0, 
          cno: cno_tmp, 
          hno: 0, 
          mno: 0, 
          price: 70, 
          ontime:new Date(), 
          offtime:new Date() };
        this.getHallList();
        if (this.hallList.length > 0)
          this.sceneModel.mno = this.movieList[0].fields.mno;
        this.sceneDialogVisible = true;
      },
      update_scene(scope){
        this.new_scene = false;
        this.sceneModel = { 
          cno: scope.cno,
          last_pk: scope.sno,
          hno: scope.hno,
          mno: scope.mno, 
          price: scope.price, 
          ontime: scope.ontime, 
          offtime: scope.offtime };
        this.sceneDialogVisible = true;
      },
      confirmScene(){
        if (this.new_scene) {
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
      to_sou() {
        this.$router.push({ path: '/empsou', query: {id: this.id} })
      },
      to_bill() {
        this.$router.push({ path: '/empbill', query: {id: this.id} })
      }
    }
  };
</script>
