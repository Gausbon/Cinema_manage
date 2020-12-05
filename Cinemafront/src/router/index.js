import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import VipMain from '@/components/VipMain'

Vue.use(Router)

const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main,
      meta: {
        title: "电影院管理系统"
      },
      children: [

      ]
    },
    {
       path: '/vip',
       name: 'VipMain',
       component: VipMain,
       meta: {
         title: "电影院管理系统"
       },
     }
  ]
})
