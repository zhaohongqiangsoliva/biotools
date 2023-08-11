import request from "@/utils/request";
let baseURL = process.env.VUE_APP_BASE_TASK_API
export default {
    //提交
    submit(params) {
        return request.post(baseURL+`/imputation/job/jobs/submit`, params);
    },
    //查询
    query(params) {
        return request.get(baseURL+`/imputation/job/jobs/query`, params);
    },
}