
<template>
  <div class="flex-lg-1 h-screen overflow-y-lg-auto " style="margin-top: 6rem">

    <!-- Main -->
    <main class="py-6 bg-surface-secondary">
      <div class="container">
        <h2 class="h2 ls-tight mb-4">JOBLIST (<b-link
            href="https://www.internationalgenome.org/wiki/Analysis/Variant%20Call%20Format/vcf-variant-call-format-version-41">VCF</b-link>)
        </h2>



        <ul class="list-group">
          <li v-for="task in tasks" :key="task.id" class="list-group-item">
            <b-badge v-if="task.jobStatus == 'Succeeded'" variant="success">Task Name:{{ task.fileName }} </b-badge>
            <b-badge v-else variant="Info">Task Name:{{ task.fileName }} </b-badge>
            <b-badge v-if="task.jobStatus == 'Succeeded'" variant="success">Task UUID {{ task.jobID }}</b-badge>
            <b-badge v-else variant="Info">Task UUID {{ task.jobID }}</b-badge>
            <b-progress :max="max">
              <b-progress-bar v-if="task.jobStatus == 'Succeeded'" :value="getProgress(task.jobStatus)" variant="success">
                {{ getProgress(task.jobStatus) }}%
              </b-progress-bar>
              <b-progress-bar v-else-if="task.jobStatus == 'Failed'" :value="getProgress(task.jobStatus)" variant="danger">
                  {{ getProgress(task.jobStatus) }}%
                </b-progress-bar>
              <b-progress-bar v-else :value="getProgress(task.jobStatus)" animated variant="primary">
                {{ getProgress(task.jobStatus) }}%
              </b-progress-bar>
            </b-progress>
            <div class="clearfix">
                <b-spinner v-if="task.jobStatus !== 'Succeeded' && task.jobStatus !== 'Failed' && task.jobStatus !== 'Abort'" label="Running" class="float-right"></b-spinner>
                <b-p v-else label="Succeeded" class="float-right"></b-p>
            </div>
          </li>
        </ul>










        <!-- <div class="progress">
                      <div class="progress-bar" role="progressbar" aria-valuenow="2" aria-valuemin="0" aria-valuemax="100" style="min-width: 10em; width: 2%;">
                        2%
                      </div>
                    </div> -->

        <!--              下载页面-->
        <div class="row">
          <p>{{ wgetCommand }}</p>
          <div class="col-md-12 offset-md-0 mt-5">
            <b-card title="Imputation Results">
              <b-table :items="tasks" :fields="tableFields" striped hover>
                <template #cell(fileName)="row">
                  {{ row.item.fileName }}
                </template>
                <template #cell(downloadButton)="row">
                  <b-button v-if="row.item.jobStatus === 'Succeeded'" @click="copyToClipboard(row.index)"
                    variant="primary">
                    task Copy wget command
                  </b-button>
                  <b-button v-else variant="secondary" disabled>
                    {{ row.item.jobStatus }}
                  </b-button>

                </template>
              </b-table>
              <div v-if="showCopyMessage">
                Copied to clipboard!
              </div>
            </b-card>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { jobs } from "@/api"
import doCookie from "@/utils/cookie"
import axios from 'axios'

export default {



  data() {
    return {
      tasks: [],
      copiedIndex: null,
      showCopyMessage: false,



      imputationResults: [],
      //   // Replace this with your actual imputation results data

      //   // Add more objects representing each imputation result file
      // ],
      tableFields: [
        { key: 'fileName', label: 'File Name' },
        { key: 'fileName', label: 'File Name' },
        { key: 'jobID', label: 'job ID' },
        { key: 'jobStatus', label: 'job Status' },
        { key: 'local', label: 'Localation' },
        { key: 'downloadButton', label: 'Download' },



      ],
      uploadUrls: [],

    }
  },







  methods: {
    downloadResult(resultItem) {
      // Implement your download logic here based on the selected result item
      // For demonstration purposes, let's just show an alert with the selected file name.
      alert(`Downloading ${resultItem.fileName}...`);
    },

    query() {

      let subData = {
        // userID: doCookie.getCookie("id"),
        userName: doCookie.getCookie("imputation-username"),

      }
      jobs.query(subData).then((response) => {
        let code = response.code

        if (code === "200" || code === 200) {
          this.test = response.data.Tasks[0].uploadUrl

          // if (resData.)
          this.Jobslists = response.data.total;
          this.imputationResults = response.data.Tasks;
          const task = response.data.Tasks[0];
          this.tasks = response.data.Tasks

          // Parse the uploadUrl string as an array
          this.uploadUrls = JSON.parse(task.uploadUrl)

        }
      })

    },
    parseUploadUrls(uploadUrlStr) {
      try {
        const uploadUrls = JSON.parse({ uploadUrlStr });
        return console.log(uploadUrls)
          ;
      } catch (error) {
        console.error("Error parsing uploadUrls:", error);
        return []; // 返回空数组或者其它默认值，如果解析失败
      }
    },
    copyToClipboard(index) {

      const task = this.tasks[index];
      const wgetCommand = `wget -c ${task.uploadUrl}`;
      const el = document.createElement('textarea');
      el.value = wgetCommand;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);

      this.copiedIndex = index;
      this.showCopyMessage = true;

      setTimeout(() => {
        this.showCopyMessage = false;
      }, 2000);
    },
    getProgress(jobStatus) {
      return jobStatus === "Succeeded" ? 100 : 60;
    },
    getStatus(jobStatus) {
      return jobStatus === "Succeeded" ? "Succeeded" : "Running";
    },



  },
  mounted() {
    //为总线绑定函数
    this.$bus.$on('query', this.query)

    this.query();
    this.autoUpdateInterval = setInterval(() => {
    this.query();
    }, 50000);



  },
  beforeDestroy() {
    // 在组件销毁前，清除定时器，避免内存泄漏
    clearInterval(this.autoRefreshInterval);
  },

}
</script>