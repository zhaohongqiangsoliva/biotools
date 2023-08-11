<template>
  <div>
    <Header></Header>
    <!-- 路由组件出口的地方 -->
    <router-view></router-view>
    <!-- <Footer></Footer> -->
  </div>
</template>

<script>
import Header from './components/Header'
// import Footer from './components/Footer'

export default {
  name: 'App',
  components: {
    Header,
  },
}
</script>

<style>
.mt {
  margin-top: 8rem !important;
}
</style>
