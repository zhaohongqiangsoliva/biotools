import * as Vuex from 'vuex'
import * as Vue from 'vue'
//引入模块的仓库
//需要暴露Vuex.Store类的实例(你需要暴露这个类的实例，如果你不对外暴露，外部是不能使用的)
export default Vuex.createStore({
  //模块：把小仓库进行合并变为大仓库
  modules: {},
})
