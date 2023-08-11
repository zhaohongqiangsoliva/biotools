import request from "@/utils/request";
let baseURL = process.env.VUE_APP_BASE_JOB_API
export default {
    //提交
    submit(params) {
        return request.post(baseURL+`/imputation/job/submit`, params);
    },
    //查询
    query(params) {
        return request.get(baseURL+`/imputation/job/query`, params);
    },
}