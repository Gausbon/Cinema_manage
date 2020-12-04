<template>
<el-container style="height: 90%; border: 1px solid #eee">
  <el-container>
  <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
    <el-menu :default-openeds="['1', '3']">
      <el-submenu index="1">
        <template slot="title"><i class="el-icon-message"></i>导航一</template>
        <el-menu-item-group>
          <template slot="title">分组一</template>
          <el-menu-item index="1-1">选项1</el-menu-item>
          <el-menu-item index="1-2">选项2</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="分组2">
          <el-menu-item index="1-3">选项3</el-menu-item>
        </el-menu-item-group>
        <el-submenu index="1-4">
          <template slot="title">选项4</template>
          <el-menu-item index="1-4-1">选项4-1</el-menu-item>
        </el-submenu>
      </el-submenu>
    </el-menu>
  </el-aside>



  <el-container>
    <el-header style="text-align: right; font-size: 12px">
    <span>目前上映影片数量：{{movie_count}}</span>
      <el-dropdown>
        <i class="el-icon-setting" style="margin-right: 15px"></i>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>查看</el-dropdown-item>
          <el-dropdown-item>新增</el-dropdown-item>
          <el-dropdown-item>删除</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <span>王小虎</span>
    </el-header>

    <el-main>
      <el-table :data="movieList">
        <el-table-column prop="name" label="电影名称">
        <template scope="scope"> {{ scope.row.fields.mname }} </template>
        </el-table-column>
        <el-table-column prop="address" label="导演">
        <template scope="scope"> {{ scope.row.fields.director }} </template>
        </el-table-column>
        <el-table-column prop="address" label="主演">
        <template scope="scope"> {{ scope.row.fields.actor }} </template>
        </el-table-column>
      </el-table>
    </el-main>

    <el-footer display="margin-top:10px">
        <el-input v-model="input2" @input="onInput()" placeholder="请输入书名" style="display:inline-table; width: 70%; float:left"></el-input>
        <el-button type="primary" @click="addBook()" style="float:left; margin: 2px;">新增</el-button>
    </el-footer>
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
        movieList: [],
        movie_count: 0
      }
    },
    mounted: function() {
      this.showMovies()
    },
    methods: {
      onInput(){
        this.$forceUpdate();
      },
      showMovies(){
        this.$http.get('http://127.0.0.1:8000/api/show_movie')
          .then((response) => {
              var res = JSON.parse(response.bodyText)
              console.log(res)
              if (res.error_num == 0) {
                this.movieList = res['list']
                this.movie_count = this.movieList.length
              } else {
                this.$message.error('查询电影失败')
                console.log(res['msg'])
              }
          })
      }
    }
  };
</script>
