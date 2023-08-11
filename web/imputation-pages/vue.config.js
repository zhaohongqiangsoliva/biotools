module.exports = {
  pages: {
    index: {
      //入口
      entry: 'src/main.js',
    },
  },
  lintOnSave: false, //关闭语法检查
  //开启代理服务器
  devServer: {
    proxy: {
      "/dev-api": {
        target: "http://192.168.77.45:9080",//"http://39.107.228.251:18081",
        // target: "http://119.78.66.78:80",
        changOrigin: true,
        pathRewrite: { '^/dev-api': '' },
      },
      "/prd-api": {
        // target: "http://119.78.66.78:80",
        target: "http://192.168.77.45:9080",//"http://39.107.228.251:18081",
        changOrigin: true,
        pathRewrite: { '^/prd-api': '' },
      },
      "/dev-job-api": {
        target: "http://192.168.77.45:9080",
        changOrigin: true,
        pathRewrite: { '^/dev-job-api': '' },
      },
      "/prd-job-api": {
        target: "http://192.168.77.45:9080",//"http://39.107.228.251:19080",
        changOrigin: true,
        pathRewrite: { '^/prd-job-api': '' },
      },
      "/prd-task-api": {
        target: "http://192.168.77.45:8000",//"http://39.107.228.251:19080",
        changOrigin: true,
        pathRewrite: { '^/prd-task-api': '' },
      },
      "/dev-task-api": {
        target: "http://192.168.77.45:8000",//"http://39.107.228.251:19080",
        changOrigin: true,
        pathRewrite: { '^/dev-task-api': '' },
      },
    }
  }
}


