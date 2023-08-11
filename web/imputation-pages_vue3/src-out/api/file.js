import request from '@/utils/request'

let baseURL = process.env.VUE_APP_BASE_API

let baseJobsUrl = process.env.VUE_APP_BASE_JOB_API
export default {
  //样本创建
  fileCreate(params) {
    return request.post(baseURL + `/cloudimpute/file/create`, params)
  },
  //样本检索
  fileSelect(params) {
    return request.post(baseURL + `/cloudimpute/file/select`, params)
  },
  //删除样本
  fileDelete(params) {
    return request.post(baseURL + `/cloudimpute/file/delete`, params)
  },
  //保存文件
  saveFilesInfo(params) {
    return request.get(baseJobsUrl + `/imputation/job/saveFilesInfo`, params)
  },
  //获取文件列表信息
  getFileList(params) {
    return request.get(baseJobsUrl + `/imputation/job/getFileList`, params)
  },
}
