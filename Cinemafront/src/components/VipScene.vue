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

  <el-header style = "background-color: #ffffff; text-align: right">
    <el-menu default-active="2" class="el-menu-demo" mode="horizontal" 
    @select="handleSelect" style = "float: left">
      <el-menu-item index="1" @click="to_movie">电影</el-menu-item>
      <el-menu-item index="2">场次</el-menu-item>
    </el-menu>
    <el-button round @click="logout">注 销</el-button>
  </el-header>

  <el-container style="height: 600px"> 
    <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
      <template slot-scope="props">
        <el-menu class="el-menu-vertical-demo">
          <el-menu-item>
            <span slot="title">用户等级：{{vip_list.vlevel}}</span>
          </el-menu-item>
          <el-menu-item>
            <span slot="title">用户余额：{{vip_list.vaccount}}</span>
          </el-menu-item>
        </el-menu>
      </template>
    </el-aside>
    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <el-container>
          <el-main></el-main>
          <el-aside mode="horizontal">
            <span style="font-size: 130%">您好，亲爱的{{vip_list.ename}}</span>
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
                <template slot="empty"> 暂无场次<br>
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
        vip_list: [],
        movieList: [],
        reverse: false,
        logoutDialogVisible: false
      }
    },
    mounted: function() {
      this.showvip(),
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
      showvip(){
        if (sessionStorage.getItem("type") != 'vip') {
          sessionStorage.setItem("token", 'false')
          this.$router.push({ path: '/' })
        }
        this.id = this.$route.query.id
        console.log("show vip")
        this.$http.post('http://127.0.0.1:8000/api/show_vip',
          JSON.stringify({id: this.id}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.vip_list = res['list']
              } else {
                this.$message.error('查询vip信息失败')
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
      strip(str) {
        return str.replace(/\s*/g,"")
      },
      to_movie() {
        this.$router.push({ path: '/vipmovie', query: {id: this.id} })
      }
    }
  };
</script>
