<template>
  <div class="rounded border-2 border-dashed border-primary-hover position-relative mb-6">
    <uploader 
      ref="uploader"
      :options="options"
      :autoStart="false"
      :file-status-text="fileStatusText"
      @file-added="onFileAdded"
      @file-success="onFileSuccess"
      @file-error="onFileError"
      @file-progress="onFileProgress"
      @file-complete="onFileComplete"
      class="">
      <uploader-unsupport></uploader-unsupport>
      <uploader-drop class="d-flex justify-content-center px-5 py-5">
            <uploader-btn :attrs="attrs" id="upFlie"
              class="position-absolute w-full h-full top-0 start-0 cursor-pointer">
            </uploader-btn>
            <div class="text-center">
              <div class="text-2xl text-muted">
                <b-icon icon="upload"></b-icon>
              </div>
              <div class="d-flex text-sm mt-3">
                <p class="font-semibold">Upload a file</p>
              </div>
            </div>
      </uploader-drop>
      <uploader-list></uploader-list>
    </uploader>
  </div>
</template>

<script>
import SparkMD5 from 'spark-md5'
import { isEmpty, }  from "@/utils/validate"
import doCookie from "@/utils/cookie"
import  {fileInterface} from '@/api'
const FILE_UPLOAD_ID_KEY = 'file_upload_id'
// 分片大小，20MB
const CHUNK_SIZE = 20 * 1024 * 1024

  export default {
    name:"VueSimpleUploader",
    props: ['fileName','attr','descrition'],
    data () {
      return {
        options: {
          // 上传地址
          target: process.env.VUE_APP_BASE_JOB_API+'/imputation/job/upload',
          // 是否开启服务器分片校验。默认为 true
          testChunks: true,
          // 分片大小
          chunkSize: CHUNK_SIZE,
          //是否强制所有的块都是小于等于 chunkSize 的值。默认是 false
          forceChunkSize:true,
          // 并发上传数，默认为 3 
          simultaneousUploads: 3,
          //设置header
          headers: { 
              Authorization: doCookie.getCookie("imputation-cookie")
          },
          query:{
            fileId: null,
            fileNameInput:"",
            chunkIdentifier:""
          },
          //单文件上传
          singleFile: false,
          /**
           * 判断分片是否上传，秒传和断点续传基于此方法
           */
          checkChunkUploadedByResponse: (chunk, message) => {
            let messageObj = JSON.parse(message)
            let dataObj = messageObj.data
            if (dataObj.uploaded !== undefined) {
              return dataObj.uploaded
            }
            // 判断文件或分片是否已上传，已上传返回 true
            // 这里的 uploadedChunks 是后台返回
            return (dataObj.uploadedChunks || []).indexOf(chunk.offset + 1) >= 0
          }
        },
        attrs: {
          accept: this.attr
        },
        // 上传状态
        fileStatusTextObj:{
            success: 'success',
            error: 'error',
            uploading: 'uploading',
            paused: 'paused',
            waiting: 'waiting'
        },
        uploadIdInfo: null,
        uploadFileList: [],
        fileChunkList: [],
        desc:""
      }
    },
    
    watch: {
        'fileName': function (val) { //监听props中的属性
            this.options.query.fileNameInput = val;
        },
        'attr': function (val) { //监听props中的属性
            if(!isEmpty(val)){
              this.attrs.accept = val;
            }
        },
        'descrition':function(val){
          this.desc = val
        }
    },
    methods: {
      onFileAdded(file) {
        // 文件大小
        console.log('文件大小：' + file.size + 'B')
        // 1. todo 判断文件类型是否允许上传
        // 2. 计算文件 MD5 并请求后台判断是否已上传，是则取消上传
        console.log('校验MD5')

        var fileName1 = file.name;

        if(!isEmpty(this.fileName)){
            fileName1 = this.fileName + fileName1.substring(fileName1.indexOf("."),fileName1.length)
            file.name = fileName1
        }

        let totalChunksM = Math.ceil(file.size / CHUNK_SIZE)

        this.getFileMD5(file, md5 => {
          if (md5 != '') {
            // 修改文件唯一标识
            file.uniqueIdentifier = md5

            let subData = {
              fileSize : file.size,
              identifier: md5,
              fileName: file.name,
              localPath: file.relativePath,
              totalChunks: totalChunksM == 0 ? 1:totalChunksM,

              desc: this.desc ,
              OS : "linux",
            }
            fileInterface.fileCreate(subData).then((response) => {
              let code = response.code
              if(code === "0" || code === 0){
                this.options.query.fileId = response.data
                // 恢复上传
                file.resume()
              }
            })
            
          }
        })
      },
      onFileSuccess(rootFile, file, response, chunk) {
        console.log("上传成功")
        const resJaon = JSON.parse(response)
        console.log("chunk="+chunk)

        
        const data = resJaon.data
        console.log("data="+resJaon)

        if(!isEmpty(data)){
          const flag = data.flag
          if(flag){
            //触发总线绑定的fileChange函数
            this.$bus.$emit('fileChange',data)
          }
        }
        // if(!isEmpty(data)){
        //   const flag = data.flag
        //   if(flag){
            //触发总线绑定的fileChange函数
            // this.$bus.$emit('getFileList',1)
        //   }
        // }

      },
      onFileComplete(rootFile){
        console.log("onFileComplete"+rootFile)
        console.log("上传成功Complete")
      },
      onFileError(rootFile, file, message, chunk) {
        console.log('上传出错：' + message)
        console.log('上传出错chunk：' + chunk)
        //暂停上传
        file.pause()
        },
      onFileProgress(rootFile, file, chunk) {
        console.log(`当前进度：${Math.ceil(file._prevProgress * 100)}%`)
        console.log(`当前进度chunk：`+chunk)
      },
      getFileMD5(file, callback) {
        let spark = new SparkMD5.ArrayBuffer()
        let fileReader = new FileReader()
        let blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice
        let currentChunk = 0
        let chunks = Math.ceil(file.size / CHUNK_SIZE)
        let startTime = new Date().getTime()
        file.pause()
        loadNext()
        fileReader.onload = function(e) {
          spark.append(e.target.result)
          if (currentChunk < chunks) {
            currentChunk++
            loadNext()
          } else {
            let md5 = spark.end()
            console.log(`MD5计算完毕：${md5}，耗时：${new Date().getTime() - startTime} ms.`)
            callback(md5)
          }
        }
        fileReader.onerror = function() {
          this.$message.error('文件读取错误')
          file.cancel()
        }
        function loadNext() {
          const start = currentChunk * CHUNK_SIZE
          const end = ((start + CHUNK_SIZE) >= file.size) ? file.size : start + CHUNK_SIZE
          fileReader.readAsArrayBuffer(blobSlice.call(file.file, start, end))
        }
      },
      fileStatusText(status) {
        if (status === 'md5') {
          return '校验MD5'
        } else {
          return this.fileStatusTextObj[status]
        }
      },
      saveFileUploadId(data) {
        localStorage.setItem(FILE_UPLOAD_ID_KEY, data)
      },
      showMsgBoxTwo(msg) {
        this.box = ''
        this.$bvModal.msgBoxOk(msg, {
            size: 'sm',
            buttonSize: 'sm',
            okVariant: 'success',
            headerClass: 'p-2 border-bottom-0',
            footerClass: 'p-2 border-top-0',
            centered: true
        })
        .then(value => {
            this.box = value
        })
        .catch(err => {
            console.error(err)
        })
     }
    },
    //数据初始化
    mounted(){
      
      //为总线绑定函数
      // this.$bus.$on('addfile',this.addfile)
    }
  }
</script>

<style scoped>
  .uploader-drop {
      border: 1px dashed #fff !important;
      background-color: #fff !important;
  }
  .pagination{
    margin-top: 1rem;
  }
  .el-pagination.is-background .el-pager li:not(.disabled).active {
      background-color: #796CFF !important;
  }
  .border-dashed {
    border-style: dashed!important;
}

.rounded {
    border-radius: 0.375rem!important;
}
.mb-6 {
    margin-bottom: 1.5rem!important;
}
.border-2, .border-2-focus:focus, .border-2-hover:hover {
    border-width: 2px!important;
}
.position-relative {
    position: relative!important;
}
*, :after, :before {
    border: 0 solid #e7eaf0;
}
*, :after, :before {
    box-sizing: border-box;
}
.uploader-btn {
    display: inline-block;
    position: relative;
    padding: 4px 8px;
    font-size: 100%;
    line-height: 1.4;
    color: #666;
    border: 1px solid #666;
    cursor: pointer;
    border-radius: 2px;
    background: none;
    outline: none;
}

.uploader-btn {
    border: 0 solid #fff!important;
}
.h-full {
    height: 100%!important;
}
.w-full {
    width: 100%!important;
}
.start-0 {
    left: 0!important;
}
.top-0 {
    top: 0!important;
}
.position-absolute {
    position: absolute!important;
}
</style>