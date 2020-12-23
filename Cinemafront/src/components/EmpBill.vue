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
    <el-menu default-active="4" class="el-menu-demo" mode="horizontal" 
    @select="handleSelect" style = "float: left">
      <el-menu-item index="1" @click="to_movie">电影</el-menu-item>
      <el-menu-item index="2" @click="to_scene">场次</el-menu-item>
      <el-menu-item index="3" @click="to_sou">周边</el-menu-item>
      <el-menu-item index="4" >流水</el-menu-item>
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
          </el-aside>
        </el-conttainer>
      </el-header>

      <el-main>
        <div id="echarts_box" style="width: 600px;height:400px;"></div>
        <el-table :data="billList">
          <el-table-column prop="name" label="人员类型">
          <template scope="scope"> {{ scope.row.fields.type }} </template>
          </el-table-column>
          <el-table-column prop="address" label="人员id">
          <template scope="scope"> {{ scope.row.fields.num }} </template>
          </el-table-column>
          <el-table-column prop="address" label="流水">
          <template scope="scope"> {{ scope.row.fields.value }}元 </template>
          </el-table-column>
          <el-table-column prop="address" label="事项">
          <template scope="scope"> {{ scope.row.fields.reason }} </template>
          </el-table-column>
          <el-table-column prop="address" label="时间">
          <template scope="scope"> {{ showDate(scope.row.fields.date, false) }} </template>
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
  import echarts from 'echarts';
  export default {
    data() {
      return {
        id: 0,
        emp_list: [],
        billList: [],
        logoutDialogVisible: false,
        option: {
            title: { text: '流水图表' },
            tooltip: {},
            legend: { data:['入账','出账'] },
            xAxis: { data: [],     
            axisLabel: {  
              interval:0,  
              rotate:40  
            }},
            yAxis: {},
            series: [{
                name: '入账',
                type: 'bar',
                data: []
            },
            {
                name: '出账',
                type: 'bar',
                data: []
            }]
        }
      }
    },
    mounted: function() {
      this.init(),
      this.showemp(),
      this.showBill(),
      this.showAllBill()
    },
    created() {},
    watch: {
    },
    methods: {
      init() {
        if (sessionStorage.getItem("type") != 'emp') {
            sessionStorage.setItem("token", 'false')
            this.$router.push({ path: '/' })
        }
        this.id = this.$route.query.id
        console.log(this.id);
        var curd = new Date();
        var curdtmp = new Date();
        var i = 7;
        for (i = 7; i >= 0; i--) {
          var d = new Date(curdtmp.setTime(curd.getTime()-i*24*60*60*1000))
          this.option.xAxis.data.push(this.showDate(d,true));
        }
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
      showBill(){
        var d = new Date();
        console.log("show bill")
        this.$http.post('http://127.0.0.1:8000/api/show_bill',
          JSON.stringify({minDate: new Date(d.setTime(d.getTime()-7*24*60*60*1000)) }), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                this.billList = res['list']
              } else {
                this.$message.error('查询流水失败')
                console.log(res['msg'])
              }
          })
      },
      showAllBill(){
        var d = new Date();
        console.log("all bill")
        this.$http.post('http://127.0.0.1:8000/api/show_allbill',
          JSON.stringify({minDate: this.toDate(new Date(d.setTime(d.getTime()-7*24*60*60*1000)))}), {emulateJSON: true})
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.error_num == 0) {
                console.log("all_bill" + this.option.series[1].data);
                this.option.series[0].data = res['inbill'];
                this.option.series[1].data = res['outbill'];
                console.log("all_bill" + this.option.series[1].data);
                var myChart = echarts.init(document.getElementById('echarts_box'))
		            myChart.setOption(this.option)
              } else {
                this.$message.error('查询流水失败')
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
      showDate(d,b){
        var date = new Date(d);
        var output;
        if (b)
          output = "";
        else output = date.getFullYear()+"年"

        if (date.getMonth()+1 < 10)
          output = output + "0"
        output = output + (date.getMonth()+1)+"月"
        if (date.getDate() < 10)
          output = output + "0"
        return output+date.getDate()+"日";
      },
      toDate(d){
        var date = new Date(d);
        var output = date.getFullYear() + "-"

        if (date.getMonth()+1 < 10)
          output = output + "0"
        output = output + (date.getMonth()+1)+"-"
        if (date.getDate() < 10)
          output = output + "0"
        return output+date.getDate();
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
      to_sou() {
        this.$router.push({ path: '/empsou', query: {id: this.id} })
      }
    }
  };
</script>
