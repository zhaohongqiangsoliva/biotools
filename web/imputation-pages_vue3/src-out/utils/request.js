import axios from 'axios'
// import { MessageBox  } from 'element-ui'
// import store from '@/store'

import doCookie from '@/utils/cookie'
// import router from '@/router'

axios.defaults.timeout = 50000
axios.defaults.baseURL = ''
axios.defaults.headers.post['Content-Type'] = 'application/json charset=UTF-8'
// axios.defaults.withCredentials=false
//请求拦截器：携带的token字段
axios.interceptors.request.use(
  (config) => {
    // do something before request is sent

    if (doCookie.getCookie('imputation-cookie')) {
      // 添加登录成功的token
      config.headers['Authorization'] = doCookie.getCookie('imputation-cookie')
    }
    return config
  },
  (error) => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

//响应拦截器
axios.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
   */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  (response) => {
    const res = response
    console.log(res)
    const status = res.status
    if (status === '200' || status === 200) {
      return res.data
    } else {
      //todo
    }
  },
  (error) => {
    console.log('err=' + error) // for debug
    //删除cookie
    doCookie.delCookie('imputation-cookie')
    doCookie.delCookie('imputation-username')
    // MessageBox.alert('The login status is invalid, please log in again', 'prompt', {
    //   confirmButtonText: 'ok',
    //   callback: action => {
    //     console.log("action="+action)
    //     //删除cookie
    //     doCookie.delCookie("imputation-cookie")
    //     doCookie.delCookie("imputation-username")
    //     router.push({
    //         name:'login'
    //     });
    //   }
    // });

    // Message({
    //   message: error.message,
    //   type: 'error',
    //   duration: 5 * 1000
    // })
    return Promise.reject(error)
  }
)

export default {
  get(url, params = {}) {
    return axios.get(url, {
      params: params,
    })
  },
  post(url, data = {}) {
    return axios.post(url, null, {
      params: data,
    })
    // return axios.post(url, data)
  },
}
