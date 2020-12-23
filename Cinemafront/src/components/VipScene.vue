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
  title="购票操作"
  style="text-align: center"
  :visible.sync="ticketDialogVisible"
  width="50%"
  :before-close="handleClose">
    <el-form label-position="top" v-model="ticketModel" ref="ticketModel">
      <el-form-item label="座位">
      <el-container> <el-main style="background-color: #B3C0D1;">
      <el-row v-for="index of (hallsize/10)">
      <el-checkbox-group v-model="ticketModel.ticketList">
        <el-checkbox-button size="mini" v-for="i of 10" :label="i+(index-1)*10" :disabled="checkdup(i+(index-1)*10)==true">
        {{get_checkbox_botton_word(i+(index-1)*10)}}</el-checkbox-button>
      </el-checkbox-group>
      </el-row>
      </el-main></el-container>
      <el-row style="margin-top:30px"><span>您已购票：{{ticketModel.ticketList.length}}张</span></el-row>
      
      <span>原单价：{{price}}元&nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span>会员单价：{{parseInt(price * vip_list.sale)}}元</span><br>
      <span>总价：{{ticketModel.price}}元</span>
    </el-form>
    <el-button round @click="confirmTicket" type="primary">确 定 </el-button>
    <el-button round @click="ticketDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-dialog
  title="充值操作"
  style="text-align: center"
  :visible.sync="creditDialogVisible"
  width="30%"
  :before-close="handleClose">
    <span>请输入要充值的金额</span><br><br>
    <el-input-number v-model="credits" @change="handleChange" :min="100" :step="10"></el-input-number><br><br><br>
    <el-button style="margin-top:20px" round @click="confirmCredits" type="primary">确 定 </el-button>
    <el-button round @click="creditDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-header style = "background-color: #ffffff; text-align: right">
    <el-menu default-active="2" class="el-menu-demo" mode="horizontal" 
    @select="handleSelect" style = "float: left">
      <el-menu-item index="1" @click="to_movie">电影</el-menu-item>
      <el-menu-item index="2">场次</el-menu-item>
      <el-menu-item index="3" @click="to_sou">周边</el-menu-item>
      <el-menu-item index="4" @click="to_myticket">我的</el-menu-item>
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
                 <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button size="mini" type="primary" @click.native="buy_ticket(scope.row)">购票</el-button>
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
        sceneList: [],
        vip_list: [],
        checkList: [],
        price: 0,
        discount: 0,
        ticketModel: { vno: 0, sno: 0, ticketList:[], price:0 },
        hallsize: 60,
        reverse: false,
        ticketDialogVisible: false,
        logoutDialogVisible: false,
        creditDialogVisible: false,
      }
    },
    mounted: function() {
      this.init(),
      this.showvip(),
      this.showScene(),
      this.onInput()
    },
    watch: {
      'ticketModel.ticketList': {
          handler(newName, oldName) {
            this.ticketModel.price = this.total_price();
          },
          immediate: true,
          deep: true
        }
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
      confirmCredits() {
        var last_credits = this.credits;
        console.log(this.id);
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
      logout() {
        this.logoutDialogVisible = true // 显示弹框
      },
      confirmLogout(){
        this.$message({ type: 'success', message: '注销成功!'});
        sessionStorage.setItem("token", 'false');
        this.$router.push("/");
      },
      buy_ticket(scope) {
        this.ticketModel.vno = this.id;
        this.ticketModel.ticketList = [];
        this.ticketModel.sno = scope.sno;
        this.price = scope.price;
        this.$http.post('http://127.0.0.1:8000/api/get_disabled',
          JSON.stringify({sno: scope.sno}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.checkList = res.d_list;
                this.hallsize = res.hv;
              } else {
                this.$message.error('查询场次失败')
                this.creditDialogVisible = false;
                console.log(res['msg'])
                return;
              }
          })
        this.ticketDialogVisible = true;
      },
      confirmTicket(){
        if (this.ticketModel.price > this.vip_list.vaccount) {
          this.$message.error('购买失败，您的余额不足！');
          return;
        } else if (this.ticketModel.ticketList.length == 0) {
          this.$message.error('请选择一个座位！');
          return;
        }
        this.$http.post('http://127.0.0.1:8000/api/add_ticket',
          JSON.stringify(this.ticketModel), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '购票成功！'});
                this.showvip();
                this.ticketDialogVisible = false;
              } else {
                this.$message.error('购票失败')
                this.ticketDialogVisible = false;
                console.log(res['msg'])
                return;
              }
          })
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
      to_sou() {
        this.$router.push({ path: '/vipsou', query: {id: this.id} })
      },
      to_myticket() {
        this.$router.push({ path: '/vipmyticket', query: {id: this.id} })
      },
      total_price() {
        return parseInt(this.ticketModel.ticketList.length * this.price * this.vip_list.sale);
      },
      get_checkbox_botton_word(b) {
        if (this.checkdup(b)==true)  return '禁';
        else if (b < 10) return '0' + b.toString();
        else return b;
      }
    }
  };
</script>
