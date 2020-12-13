import Vue from 'vue'
import Router from 'vue-router'
import Movie from '@/components/Movie'
import VipMovie from '@/components/VipMovie'
import EmpMovie from '@/components/EmpMovie'

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
      },
      children: [

      ]
    },
    {
       path: '/vip',
       name: 'VipMovie',
       component: VipMovie,
       meta: {
         title: "柒伍捌电影院",
         requireAuth: true
       },
     },
     {
       path: '/emp',
       name: 'EmpMovie',
       component: EmpMovie,
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
      console.log("authorize success")
      next()
    } else {
      console.log("return to main")
      next({
        path: '/'
      })
    }
  } else {
    next();
  }
});
