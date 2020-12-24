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
  title="退款操作"
  style="text-align: center"
  :visible.sync="retDialogVisible"
  width="30%"
  :before-close="handleClose">
    <span>确定要退款吗</span><br><br>
    <span>退款商品：{{sou_scope.fields.soname}}</span><br><br><span style="font-color: #eb2a03">你只能得到半价赔偿，即{{this.retprice}}元</spam><br>
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
            <el-dropdown :hide-on-click="false">
                <el-button v-if="sort_type=='soname'"> <span>周边名称</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-button v-else-if="sort_type=='mname'"> <span>电影名称</span>
                  <i class="el-icon-sort-up" v-if="reverse==false"></i>
                  <i class="el-icon-sort-down" v-if="reverse==true"></i>
                </el-button>
                <el-button v-else-if="sort_type=='price'"> <span>价格</span>
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
                <el-dropdown-item @click.native="sort_type='soname'; showSousingle()">周边名称</el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='mname'; showSousingle()">电影名称</el-dropdown-item>
                <el-dropdown-item @click.native="sort_type='price'; showSousingle()">价格</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-aside>
        </el-conttainer>
      </el-header>

      <el-main>
        <el-container>
          <el-header style = "background-color: #ffffff; text-align: right">
            <el-menu default-active="2" class="el-menu-demo" mode="horizontal" 
            @select="handleSelect">
              <el-menu-item index="1" @click="to_myticket">我的电影票</el-menu-item>
              <el-menu-item index="2">我的周边</el-menu-item>
            </el-menu>
          </el-header>
          <el-main>
            <el-table :data="sousingleList">
              <el-table-column label="电影名称">
              <template scope="scope"> {{ scope.row.fields.mname }} </template>
              </el-table-column>
              <el-table-column label="周边名称">
              <template scope="scope"> {{ scope.row.fields.soname }} </template>
              </el-table-column>
              <el-table-column label="价格">
              <template scope="scope"> {{ scope.row.fields.price }} </template>
              </el-table-column>
                 <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button size="mini" type="danger" @click.native="ret_sou(scope.row)">退款</el-button>
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
        retprice: 0,
        sousingleList: [],
        vip_list: [],
        sou_scope: {fields: []},
        logoutDialogVisible: false,
        creditDialogVisible: false,
        retDialogVisible: false,
        sort_type: 'mname',
        reverse: false,
      }
    },
    mounted: function() {
      this.init(),
      this.showvip(),
      this.showSousingle(),
      this.onInput()
    },
    watch: {
      reverse: 'showSousingle'
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
      showSousingle(){
        console.log("show sou single")
        this.$http.post('http://127.0.0.1:8000/api/show_sousingle',
          JSON.stringify({id: this.id, r:this.reverse, t:this.sort_type}), {emulateJSON: true})
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              this.sousingleList = res.list
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
          this.$http.post('http://127.0.0.1:8000/api/ret_sou',
          JSON.stringify({id: this.id, retid: this.sou_scope.pk}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.$message({ type: 'success', message: '退款成功!'});
                this.retDialogVisible = false;
                this.showvip();
                this.showSousingle();
              } else {
                this.$message.error('退款失败')
                this.retDialogVisible = false;
                console.log(res['msg'])
              }
          })
      },
      ret_sou(scope) {
        this.sou_scope = scope;
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
      to_myticket() {
        this.$router.push({ path: '/vipmyticket', query: {id: this.id} })
      },
      to_sou() {
        this.$router.push({ path: '/vipsou', query: {id: this.id} })
      },
      to_scene() {
        this.$router.push({ path: '/vipscene', query: {id: this.id} })
      },
    }
  };
</script>
