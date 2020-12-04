<template>
  <div>
    <el-button type="primary" round @click="handleShowCreate">增加书籍</el-button>
    <el-input v-model="search" placeholder="请输入内容" style="width: 200px"  @keyup.enter.native="handleSearch"/>
    <el-button type="primary" round @click="handleSearch">搜索</el-button>
    <el-table :data="booksData" height="250" border style="width: 600px; margin: 40px auto;"  v-loading="loading">
      <el-table-column
        prop="book_name"
        label="书名"
        align="center"
        width="200">
      </el-table-column>
      <el-table-column
        prop="book_price"
        label="价格"
        align="center"
        width="200">
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="handleUpdate(scope.$index, scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="修改书籍" :visible.sync="dialogUpdateVisible">
      <el-form :model="updateData">
        <el-form-item label="书籍名称">
          <el-input auto-complete="off" v-model="updateData.name"></el-input>
        </el-form-item>
        <el-form-item label="书籍价格">
          <el-input-number v-model="updateData.price" :precision="2" :step="0.01" :max="9999"></el-input-number>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleCancel('dialogUpdateVisible')">Cancel</el-button>
        <el-button type="primary" @click="handleConfirm('dialogUpdateVisible')">Submit</el-button>
      </div>
    </el-dialog>
    <el-dialog title="增加书籍" :visible.sync="dialogCreateVisible">
      <el-form :model="createData">
        <el-form-item label="书籍名称">
          <el-input auto-complete="off" v-model="createData.name"></el-input>
        </el-form-item>
        <el-form-item label="书籍价格">
          <el-input-number v-model="createData.price" :precision="2" :step="0.01" :max="9999"></el-input-number>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleCancel('dialogCreateVisible')">Cancel</el-button>
        <el-button type="primary" @click="handleCreate('dialogCreateVisible')">Submit</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
