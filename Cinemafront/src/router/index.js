import Vue from 'vue'
import Router from 'vue-router'
import Movie from '@/components/Movie'
import VipMovie from '@/components/VipMovie'
import VipScene from '@/components/VipScene'
import VipSou from '@/components/VipSou'
import VipMyTicket from '@/components/VipMyTicket'
import VipMySou from '@/components/VipMySou'
import EmpMovie from '@/components/EmpMovie'
import EmpScene from '@/components/EmpScene'
import EmpSou from '@/components/EmpSou'
import EmpBill from '@/components/EmpBill'

Vue.use(Router)

const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Movie',
      component: Movie,
      meta: {
        title: "柒伍捌电影院"
      }
    },
    {
       path: '/vipmovie',
       name: 'Vipmovie',
       component: VipMovie,
       meta: {
         title: "柒伍捌电影院",
         requireAuth: true
       },
     },
     {
       path: '/vipscene',
       name: 'VipScene',
       component: VipScene,
       meta: {
         title: "柒伍捌电影院",
         requireAuth: true
       },
     },
     {
       path: '/vipsou',
       name: 'VipSou',
       component: VipSou,
       meta: {
         title: "柒伍捌电影院",
         requireAuth: true
       },
     },
     {
       path: '/vipmyticket',
       name: 'VipMyTicket',
       component: VipMyTicket,
       meta: {
         title: "柒伍捌电影院",
         requireAuth: true
       },
     },
     {
       path: '/vipmysou',
       name: 'VipMySou',
       component: VipMySou,
       meta: {
         title: "柒伍捌电影院",
         requireAuth: true
       },
     },
     {
       path: '/empmovie',
       name: 'EmpMovie',
       component: EmpMovie,
       meta: {
         title: "柒伍捌电影院",
         requireAuth: true
       },
     },
     {
       path: '/empscene',
       name: 'EmpScene',
       component: EmpScene,
       meta: {
         title: "柒伍捌电影院",
         requireAuth: true
       },
     },
     {
       path: '/empsou',
       name: 'EmpSou',
       component: EmpSou,
       meta: {
         title: "柒伍捌电影院",
         requireAuth: true
       },
     },
     {
       path: '/empbill',
       name: 'EmpBill',
       component: EmpBill,
       meta: {
         title: "柒伍捌电影院",
         requireAuth: true
       },
     }
  ]
});

export default router

router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    if (sessionStorage.getItem("token") == 'true') {
      next()
    } else {
      next({
        path: '/'
      })
    }
  } else {
    next();
  }
});
