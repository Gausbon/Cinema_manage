<template>

<el-container style="margin-top: -50px; margin-bottom: -50px; border: 1px solid #eee">
  <el-dialog
  title="注 销"
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
    <span>请输入要充值的金额</span><br><br>
    <el-input-number v-model="credits" @change="handleChange" :min="100" :step="10"></el-input-number><br><br><br>
    <el-button style="margin-top:20px" round @click="confirmCredits" type="primary">确 定 </el-button>
    <el-button round @click="creditDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-dialog
  title="购买周边"
  style="text-align: center"
  :visible.sync="souDialogVisible"
  width="30%"
  :before-close="handleClose">
    <span>您要购买的周边名称：{{sou_scope.fields.soname}}</span><br><br>
    <span>剩余库存：{{sou_scope.fields.sostore - sounum}}件&nbsp;&nbsp;&nbsp;&nbsp;</span><br><br>
    <span>请输入要购买的周边数量</span><br><br>
    <el-input-number v-model="sounum" @change="handleChange" :min="1" :max="sou_scope.fields.sostore" :step="1"></el-input-number><br><br>
    <span>原单价：{{sou_scope.fields.soprice}}元&nbsp;&nbsp;&nbsp;&nbsp;</span>
    <span>会员单价：{{parseInt(sou_scope.fields.soprice * vip_list.sale)}}元</span><br><br>
    <span>总价：{{total_price()}}元</span><br>
    <el-button style="margin-top:20px" round @click="confirmSou" type="primary">确 定 </el-button>
    <el-button round @click="souDialogVisible = false">取 消</el-button>
  </el-dialog>

  <el-header style = "background-color: #ffffff; text-align: right">
    <el-menu default-active="3" class="el-menu-demo" mode="horizontal" 
    @select="handleSelect" style = "float: left">
      <el-menu-item index="1" @click="to_movie">电影</el-menu-item>
      <el-menu-item index="2" @click="to_scene">场次</el-menu-item>
      <el-menu-item index="3" >周边</el-menu-item>
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
          <el-aside>
            <span style="font-size: 130%; float: left">目前上映影片数量：{{movieCount}}</span>
          </el-aside>
          <el-main></el-main>
          <el-aside mode="horizontal">
            <span style="font-size: 130%">您好，亲爱的{{vip_list.vname}}</span><span></span>
            <el-divider direction="vertical"></el-divider>
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
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button size="mini" type="primary" @click.native="buy_sou(scope.row)">购买</el-button>
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
        credits: 0,
        sounum: 0,
        sou_scope: {fields: 0},
        souList: [],
        vip_list: [],
        souCount: 0,
        sort_type: 'mname',
        logoutDialogVisible: false,
        creditDialogVisible: false,
        souDialogVisible: false,
        reverse: false,
      }
    },
    mounted: function() {
      this.init(),
      this.showvip(),
      this.showSou(),
      this.onInput()
    },
    watch: {
      reverse: 'showSou'
    },
    methods: {
      init() {
        if (sessionStorage.getItem("type") != 'vip') {
            sessionStorage.setItem("token", 'false')
            this.$router.push({ path: '/' })
        }
        this.id = this.$route.query.id;
        console.log(this.id);
      },
      onInput(){
        this.$forceUpdate();
      },
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
      buy_sou(scope) {
        this.sou_scope = scope;
        this.souDialogVisible = true;
      },
      logout() {
        this.logoutDialogVisible = true // 显示弹框
      },
      confirmLogout() {
        this.$message({ type: 'success', message: '注销成功!'});
        sessionStorage.setItem("token", 'false');
        this.$router.push("/");
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
      confirmSou(){
        if (this.total_price() > this.vip_list.vaccount) {
          this.$message.error('购买失败，您的余额不足！');
          return;
        }
        this.$http.post('http://127.0.0.1:8000/api/buy_sou',
          JSON.stringify({vno: this.id, sono: this.sou_scope.pk, num: this.sounum }), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '购买周边成功！'});
                this.showvip();
                this.souDialogVisible = false;
              } else {
                this.$message.error('购买周边失败')
                this.souDialogVisible = false;
                console.log(res['msg'])
                return;
              }
          })
      },
      to_scene() {
        this.$router.push({ path: '/vipscene', query: {id: this.id} })
      },
      to_movie() {
        this.$router.push({ path: '/vipmovie', query: {id: this.id} })
      },
      to_myticket() {
        this.$router.push({ path: '/vipmyticket', query: {id: this.id} })
      },
      total_price() {
        return this.sounum * parseInt(this.sou_scope.fields.soprice * this.vip_list.sale);
      }
    }
  };
</script>
