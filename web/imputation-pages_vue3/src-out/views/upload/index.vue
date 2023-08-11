<template>
  <!-- Content -->
  <div class="flex-lg-1 h-screen overflow-y-lg-auto" style="margin-top: 6rem">
    <!-- Main -->
    <main class="py-6 bg-surface-secondary">
      <div class="container">
        <!-- Title -->
        <h2 class="h2 ls-tight mb-4">
          Input Files (<b-link
            href="https://www.internationalgenome.org/wiki/Analysis/Variant%20Call%20Format/vcf-variant-call-format-version-41"
            >VCF</b-link
          >)
        </h2>

        <div class="card">
          <div class="card-body pb-0">
            <div class="row" style="margin: 0.5rem 0rem">
              <div class="des"><b>Name:</b></div>
              <div class="col-xl-3 col-sm-6 input-group-sm input-group-inline">
                <input
                  type="text"
                  class="form-control"
                  v-model.trim="fileName"
                  ref="fileName"
                  @blur="checkName"
                  style="border: 1px solid #ced4da"
                />
              </div>
            </div>
            <div class="row" style="margin: 0.5rem 0rem">
              <div class="des"><b>Description:</b></div>
              <div class="col-xl-3 col-sm-6 input-group-sm input-group-inline">
                <input
                  type="text"
                  class="form-control"
                  v-model.trim="descrition"
                  ref="descrition"
                  style="border: 1px solid #ced4da"
                />
              </div>
            </div>
            <div class="row" style="margin: 0.5rem 0rem">
              <div class="des"><b>chrom:</b></div>
              <div class="col-xl-3 col-sm-6 input-group-sm input-group-inline">
                <input
                  type="text"
                  class="form-control"
                  v-model.trim="chrom"
                  ref="fileName"
                  @blur="chrom"
                  style="border: 1px solid #ced4da"
                />
              </div>
            </div>

            <VueSimpleUploader
              :fileName="fileName"
              :descrition="descrition"
              attr="*"
            ></VueSimpleUploader>
          </div>
        </div>
        <div class="vstack gap-6 mt-3">
          <!-- Table -->
          <div class="card">
            <div class="card-header row">
              <div class="col-xl-9 col-sm-9"><h5 class="mb-0">JOBS</h5></div>
            </div>
            <div class="table-responsive">
              <table class="table table-hover table-nowrap">
                <thead class="table-light">
                  <tr>
                    <th scope="col-xl-1 col-sm-1">Name</th>
                    <th scope="col-xl-5 col-sm-5">Descrition</th>
                    <th scope="col-xl-2 col-sm-2">Upload Date</th>
                    <th scope="col-xl-1 col-sm-1">Status</th>
                    <th scope="col-xl-1 col-sm-1">operation</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="file in files.fileList" :key="file.fileId">
                    <td>
                      <div class="d-flex align-items-center">
                        {{ file.fileName }}
                      </div>
                    </td>
                    <td>
                      <div class="d-flex align-items-center">
                        {{ file.descrition }}
                      </div>
                    </td>
                    <td>
                      <div class="d-flex align-items-center">
                        {{ file.uploadTime }}
                      </div>
                    </td>
                    <td>
                      <div class="d-flex align-items-center">
                        {{ file.status }}
                        <!-- <el-tooltip class="item" effect="light" placement="right" >
                                <div slot="content">The file is valid for 30 days. <br/>Click Refresh to extend the current time by 30 days !</div>
                                <img :src="hintUrl" style="width: 1rem;">
                              </el-tooltip> -->
                      </div>
                    </td>
                    <td>
                      <!-- <a href="#" class="btn btn-sm btn-neutral operate" :class=" file.status==='refreshed'? 'refreshed':'' " @click.prevent="extensionFileValidTime(file.id,file.status)">Refresh</a>
                        <button
                          type="button"
                          class="
                            operate
                            btn btn-sm btn-square btn-neutral
                            text-danger-hover
                          "
                          @click="deleteFile(file.id,file.identifier)"
                        >
                          <i class="bi bi-trash"></i>
                        </button> -->
                      <b-button
                        variant="danger"
                        @click="deleteFile(file.fileId)"
                        style="
                          background-color: #f36 !important;
                          border-color: #f36 !important;
                        "
                        >submit</b-button
                      >
                    </td>
                  </tr>
                </tbody>
              </table>
              <div class="pagination">
                <el-pagination
                  @current-change="changePage"
                  @size-change="handleSizeChange"
                  :current-page="currentPage"
                  :background="true"
                  layout=" prev, pager, next"
                  :total="total"
                  :page-size="pageSize"
                >
                </el-pagination>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { $on, $off, $once, $emit } from '../../utils/gogocodeTransfer'
import { fileInterface } from '@/api'
import { isEmpty } from '@/utils/validate'

import VueSimpleUploader from '@/components/VueSimpleUploader'

export default {
  name: 'upload',
  components: {
    VueSimpleUploader,
  },
  data() {
    return {
      files: {
        fileList: [],
      },
      type: 'GWAS',
      descrition: '',
      fileName: '',
      hintUrl: './img/hint.png',
      total: 0,
      pageSize: 10,
      currentPage: 1,
    }
  },
  methods: {
    fileChange(data) {
      // let formData = new FormData();
      // formData.append('descrition',this.descrition)
      // formData.append('fileName',this.fileName)
      // formData.append('filePath',data.filePath)
      // formData.append('suffixName',data.suffixName)
      // formData.append('identifier',data.identifier)
      let subData = {
        descrition: this.descrition,
        fileName: this.fileName,
        filePath: data.filePath,
        suffixName: data.suffixName,
        identifier: data.identifier,
      }
      fileInterface.saveFilesInfo(subData).then((response) => {
        const resData = response
        const code = resData.code
        if (code === 0) {
          const innerData = resData.data
          const msg = innerData.msg
          if (innerData.code === 0) {
            this.fileName = ''
            this.descrition = ''
            //刷新table
            this.getFileList(this.currentPage, this.pageSize)
          } else {
            //提示框
            this.$MessageBox.alert(msg, 'Message', {
              confirmButtonText: 'OK',
              callback: () => {},
            })
          }
        } else {
          this.$MessageBox.alert(
            'System is busy, please try again later !',
            'Message',
            {
              confirmButtonText: 'OK',
              callback: () => {},
            }
          )
        }
      })
    },
    getFileList(currentPage) {
      this.currentPage = currentPage
      let subData = {
        pageNum: currentPage,
      }
      fileInterface.getFileList(subData).then((response) => {
        let code = response.code
        if (code === '0' || code === 0) {
          const resData = response.data
          if (resData.code == 0) {
            this.files.fileList = resData.resDTOList
            this.total = resData.total
          }
        }
      })
    },
    checkName() {
      //校验数据
      if (isEmpty(this.fileName)) {
        return
      }
      const fileList = this.files.fileList
      if (fileList.length > 0) {
        fileList.forEach((file) => {
          const fileName = file.fileName
          if (fileName === this.fileName) {
            this.$MessageBox.alert(
              'The file name already exists !',
              'Message',
              {
                confirmButtonText: 'OK',
                callback: () => {
                  this.fileName = ''
                  this.$refs.fileName.value = ''
                  this.$refs.fileName.innerHTML = ''
                },
              }
            )
          }
        })
      }
    },
    //删除文件
    deleteFile(id) {
      let subData = {
        fileId: id,
      }
      fileInterface.fileDelete(subData).then((response) => {
        if (response.code == 0) {
          // this.$message({
          //   message: "successful delete !",
          //   type: 'success',
          //   duration: 2 * 1000
          // })
          this.getFileList(this.currentPage)
        }
      })
    },
    //翻页
    changePage(val) {
      this.currentPage = val
      this.getFileList(this.currentPage)
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.getFileList(this.currentPage)
    },
  },
  //数据初始化
  mounted() {
    //为总线绑定函数
    $on(this.$bus, 'getFileList', this.getFileList)
    $on(this.$bus, 'fileChange', this.fileChange)
    this.getFileList(this.currentPage)
  },
  watch: {
    type: {
      deep: true,

      // 数据发生变化就会调用这个函数
      handler() {
        // this.getFileList(this.currentPage,this.pageSize);
        this.descrition = ''
        this.fileName = ''
      },

      // 立即处理 进入页面就触发
      immediate: true,
    },
  },
}
</script>

<style scoped>
.operate {
  margin-left: 0.5rem;
}
.wrong {
  color: #f36;
}
.des {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-clip: padding-box;
  background-color: #fff;
  color: #16192c;
  display: block;
  font-weight: 400;
  line-height: 1.3;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  width: 6rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  padding: 0.5rem 0rem;
}
.refreshed {
  background-color: #dcdfe6;
}
.pagination {
  margin-top: 1rem;
  margin-bottom: 1rem;
}
.el-pagination.is-background .el-pager li:not(.disabled).active {
  background-color: #796cff !important;
}
.gap-6 {
  gap: 1.5rem !important;
}
.vstack {
  flex: 1 1 auto;
  flex-direction: column;
}
.card {
  word-wrap: break-word !important;
  background-clip: border-box !important;
  background-color: #fff !important;
  border: 0 solid #eceef3 !important;
  border-radius: 0.75rem !important;
  box-shadow: 0 3px 3px -1px rgb(10 22 70 / 10%), 0 0 1px 0 rgb(10 22 70 / 6%) !important;
  display: flex !important;
  flex-direction: column !important;
  min-width: 0 !important;
  position: relative !important;
}
.card-header:first-child {
  border-radius: 0.75rem 0.75rem 0 0 !important;
}
.card-header {
  background-color: transparent !important;
  border-bottom: 0 solid #eceef3 !important;
  color: #16192c !important;
  margin-bottom: 0 !important;
  padding: 1.25rem 0rem !important;
}
.row {
  --x-gutter-y: 0 !important;
  display: flex !important;
  flex-wrap: wrap !important;
  margin-left: calc(var(--x-gutter-x) * -0.5) !important;
  margin-right: calc(var(--x-gutter-x) * -0.5) !important;
  margin-top: calc(var(--x-gutter-y) * -1) !important;
}
*,
:after,
:before {
  border: 0 solid #e7eaf0;
}
*,
:after,
:before {
  box-sizing: border-box;
}
.table > thead {
  vertical-align: bottom;
}
.table-light {
  --x-table-bg: #fff;
  --x-table-striped-bg: #f2f2f2;
  --x-table-striped-color: #000;
  --x-table-active-bg: #e6e6e6;
  --x-table-active-color: #000;
  --x-table-hover-bg: #fafafa;
  --x-table-hover-color: #000;
  border-color: #e6e6e6;
  color: #000;
}
.table.table-light th,
.table .table-light th {
  background-color: #f5f9fc;
  color: #525f7f;
}
.table thead th {
  border-bottom-width: 1px;
  font-size: 0.675rem;
  font-weight: 500;
  letter-spacing: 0.025em;
  padding-bottom: 1rem;
  padding-top: 1rem;
  text-transform: uppercase;
  vertical-align: middle;
  white-space: nowrap;
}
.table > :not(caption) > * > * {
  background-color: var(--x-table-bg);
  border-bottom-width: 1px;
  box-shadow: inset 0 0 0 9999px var(--x-table-accent-bg);
  padding: 1rem 1.5rem;
}
tbody,
td,
tfoot,
th,
thead,
tr {
  border: 0 solid;
  border-color: inherit;
}
td {
  vertical-align: middle !important;
}
th {
  font-weight: 500;
  text-align: inherit;
  text-align: -webkit-match-parent;
}
</style>
