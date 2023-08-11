import * as Vue from 'vue'
import { BootstrapVue, IconsPlugin, SpinnerPlugin } from 'bootstrap-vue'
import App from './App.vue'
//引入路由相关文件
import router from '@/router'
//引入仓库进行注册
import store from '@/store'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
//上传组件
import uploader from 'vue-simple-uploader'

import { Pagination } from 'element-ui'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'

// 设置Element语言
locale.use(lang)

window.$vueApp.use(uploader)

window.$vueApp.use(BootstrapVue)

window.$vueApp.use(IconsPlugin)

window.$vueApp.use(SpinnerPlugin)

window.$vueApp.use(Pagination)

window.$vueApp = Vue.createApp(App)
window.$vueApp.mount('#app')
window.$vueApp.config.globalProperties.routerAppend = (path, pathToAppend) => {
  return path + (path.endsWith('/') ? '' : '/') + pathToAppend
}
window.$vueApp.use(store)
window.$vueApp.use(router)
