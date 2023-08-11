import requests from "@/utils/request";

let baseURL = process.env.VUE_APP_BASE_JOB_API
export default {
    //注册
    auth(params){return requests.get(baseURL+`/imputation/job/auth`,params);},
    //登录
    reqLogin(params){return requests.get(baseURL+`/imputation/job/login`,params);},
    //初始化用户数据
    getUserInfo(params){return requests.get(baseURL+`/imputation/job/getUserInfo`,params);},
    //修改用户数据
    updatedUser(params){return requests.get(baseURL+`/imputation/job/updatedUser`,params);},
    //删除用户数据
    deleteUser(params){return requests.get(baseURL+`/imputation/job/deleteUser`,params);},
}