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
  title="充值操作"
  style="text-align: center"
  :visible.sync="creditDialogVisible"
  width="30%"
  :before-close="handleClose">
    <el-input-number v-model="credits" @change="handleChange" :min="100" :step="10"></el-input-number><br><br><br>
    <el-button style="margin-top:20px" round @click="confirmCredits" type="primary">确 定 </el-button>
    <el-button round @click="creditDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-dialog
  title="退票操作"
  style="text-align: center"
  :visible.sync="retDialogVisible"
  width="30%"
  :before-close="handleClose">
    <span>确定要退票吗</span><br><br><span style="font-color: #eb2a03">你只能得到半价赔偿，即{{this.retprice}}元</spam><br>
    <el-button style="margin-top:20px" round @click="confirmRet" type="primary">确 定 </el-button>
    <el-button round @click="retDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-header style = "background-color: #ffffff; text-align: right">
    <el-menu default-active="4" class="el-menu-demo" mode="horizontal" 
    @select="handleSelect" style = "float: left">
      <el-menu-item index="1" @click="to_movie">电影</el-menu-item>
      <el-menu-item index="2" @click="to_scene">场次</el-menu-item>
      <el-menu-item index="3" @click="to_sou">周边</el-menu-item>
      <el-menu-item index="4">我的</el-menu-item>
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
          <el-menu-item>
            <span slot="title">打折力度：{{vip_list.sale}}</span>
          </el-menu-item>
          <el-menu-item>
            <el-button type="warning" @click.native="creditDialogVisible = true">充值</el-button>
          </el-menu-item>
        </el-menu>
      </template>
    </el-aside>
    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <el-container>
          <el-main></el-main>
          <el-aside mode="horizontal">
            <span style="font-size: 130%">您好，亲爱的{{vip_list.vname}}</span>
            <el-divider direction="vertical"></el-divider>
          </el-aside>
        </el-conttainer>
      </el-header>

      <el-main>
        <el-container>
          <el-header style = "background-color: #ffffff; text-align: right">
            <el-menu default-active="1" class="el-menu-demo" mode="horizontal" 
            @select="handleSelect">
              <el-menu-item index="1">我的电影票</el-menu-item>
              <el-menu-item index="2" @click="to_mysou">我的周边</el-menu-item>
            </el-menu>
          </el-header>
          <el-main>
            <el-table :data="ticketList">
              <el-table-column label="影院">
              <template scope="scope"> {{ scope.row.fields.cname }} </template>
              </el-table-column>
              <el-table-column label="位置">
              <template scope="scope"> {{ scope.row.fields.cloc }} </template>
              </el-table-column>
              <el-table-column label="影厅">
              <template scope="scope"> {{ scope.row.fields.hname }} </template>
              </el-table-column>
              <el-table-column label="电影">
              <template scope="scope"> {{ scope.row.fields.mname }} </template>
              </el-table-column>
              <el-table-column label="座位号" min-width="50%">
              <template scope="scope"> {{ scope.row.fields.loc }} </template>
              </el-table-column>
              <el-table-column label="上映时间">
              <template scope="scope"> {{ showTime(scope.row.fields.ontime) }} </template>
              </el-table-column>
              <el-table-column label="价格" min-width="50%">
              <template scope="scope"> {{ scope.row.fields.price }} </template>
              </el-table-column>
                 <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button size="mini" type="danger" @click.native="ret_ticket(scope.row)">退票</el-button>
                  </template>
                </el-table-column>
            </el-table>    
          </el-aside>
        </el-container>
        
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

  .el-checkbox__input.is-checked .el-checkbox__inner {
    background-color: #B3C0D1;
    border-color: #B3C0D1;
  }
</style>

<script>
  export default {
    data() {
      return {
        id: 0,
        credits: 0,
        ticketList: [],
        vip_list: [],
        retprice: 0,
        retid: 0,
        logoutDialogVisible: false,
        creditDialogVisible: false,
        retDialogVisible: false
      }
    },
    mounted: function() {
      this.init(),
      this.showvip(),
      this.showTicket(),
      this.onInput()
    },
    watch: {
    },
    methods: {
      onInput(){
        this.$forceUpdate();
      },
      init() {
        if (sessionStorage.getItem("type") != 'vip') {
            sessionStorage.setItem("token", 'false')
            this.$router.push({ path: '/' })
        }
        this.id = this.$route.query.id;
        console.log(this.id);
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
      showTicket(){
        console.log("show scene")
        this.$http.post('http://127.0.0.1:8000/api/show_ticket',
          JSON.stringify({id: this.id}), {emulateJSON: true})
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              this.ticketList = res.list
            } else {
               this.$message.error('查询电影票失败')
               console.log(res['msg'])
            }
          })
      },
      confirmCredits() {
        var last_credits = this.credits;
          this.$http.post('http://127.0.0.1:8000/api/vip_credit',
          JSON.stringify({id: this.id, credits: this.credits}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '充值成功!充值了' + last_credits + '元'});
                this.creditDialogVisible = false;
                this.showvip();
              } else {
                this.$message.error('充值失败')
                this.creditDialogVisible = false;
                console.log(res['msg'])
              }
          })
      },
      confirmRet() {
        console.log('confirm ret');
          this.$http.post('http://127.0.0.1:8000/api/ret_ticket',
          JSON.stringify({id: this.id, retid: this.retid}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '退票成功!'});
                this.retDialogVisible = false;
                this.showvip();
                this.showTicket();
              } else {
                this.$message.error('退票失败')
                this.retDialogVisible = false;
                console.log(res['msg'])
              }
          })
      },
      ret_ticket(scope) {
        this.retid = scope.pk;
        this.retprice = scope.fields.price / 2;
        this.retDialogVisible = true;
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
      checkdup(x) {
        var i = 0;
        for (i = 0; i < this.checkList.length; i++) {
          if (this.checkList[i] == x)
            return true;
        }
        return false;
      },
      to_movie() {
        this.$router.push({ path: '/vipmovie', query: {id: this.id} })
      },
      to_scene() {
        this.$router.push({ path: '/vipscene', query: {id: this.id} })
      },
      to_mysou() {
        this.$router.push({ path: '/vipmysou', query: {id: this.id} })
      },
    }
  };
</script>
