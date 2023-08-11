import Vue from 'vue'
import {BootstrapVue, IconsPlugin, SpinnerPlugin} from 'bootstrap-vue'
import App from './App.vue'
//引入路由相关文件
import router from '@/router'
//引入仓库进行注册
import store from '@/store'


import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
//上传组件
import uploader from 'vue-simple-uploader'

import {Pagination} from 'element-ui'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'

// 设置Element语言
locale.use(lang)

Vue.use(uploader)

Vue.config.productionTip = false

Vue.use(BootstrapVue)

Vue.use(IconsPlugin)

Vue.use(SpinnerPlugin)

Vue.use(Pagination)

new Vue({
    render: h => h(App),
    //需要把router进行注册
    //可以让全部的组件（非路由|路由组件）都可以获取到$route|$router属性
    //$route(路由)：可以获取到路由信息（path、query、params）
    //$router:进行编程式导航路由跳转push||replace
    router,
    //在入口文件这里注册store,在每一个组件的身上都拥有一个$store这个属性
    store,
    beforeCreate() {
        //定义全局事件总线
        Vue.prototype.$bus = this
    },
}).$mount('#app')
