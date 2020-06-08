import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    username:"123",
    demoValue: 'demoValue'
  },
  getters: {
    getDemoValue: state => state.demoValue
  },
  mutations: {
    setLoginUsername(state, username) {
      state.username = username
    },
    setDemoValue(state,demoValue){
      state.demoValue = demoValue
    },
  },
  actions: {
    setLoginUsernameFun(context, username) {
      context.commit("setLoginUsername", username);
    },
  },
  modules: {
  },
});
