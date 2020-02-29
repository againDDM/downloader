import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Tasks from '@/components/Tasks';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Tasks',
      component: Tasks,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
  mode: 'history',
});
