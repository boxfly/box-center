import Vue from 'vue';
import VueRouter from 'vue-router';
import Login from '../views/Login.vue';
import Store from '../views/Store.vue';
import StoreTwo from '../views/StoreTwo.vue';

import Pc from '../views/pcViews/parent.vue';
Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  linkActiveClass: 'active',
  routes:[
    {
      path: '/home',
      name: 'home', 
      component: () => import('../views/Home.vue'),
      redirect: '/home/user',
      children: [{ path: 'user',name: 'user',component: () => import( '../views/User.vue')}, 
                { path: 'contact',name: 'contact',component: () => import(  '../views/Contact.vue')}
              ]
    },
    { path: '/StoreTwo',name: 'Pc',component: Pc,},


    { path: '/',name: 'StoreTwo',component: StoreTwo,},
    { path: '/Store',name: 'Store',component: Store,},
    { path: '/login',name: 'login',component: Login,},
  ],
});

export default router;
