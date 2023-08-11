<template>
  <b-container class="bv-example-row">
    <b-navbar
      class="fixed-top"
      style="background: rgb(79, 93, 115) !important"
      toggleable="lg"
      type="dark"
      variant="dark"
    >
      <div class="container d-flex justify-content-between">
        <b-navbar-brand href="#">Imputation</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav align="center">
            <b-nav-item to="/home">Home</b-nav-item>
            <b-nav-item to="/upload" v-show="isLogin">Upload</b-nav-item>
            <b-nav-item to="/run" v-show="isLogin">Run</b-nav-item>
            <b-nav-item to="#" v-show="isLogin">Jobs</b-nav-item>
            <b-nav-item to="#">Help</b-nav-item>
            <b-nav-item to="#">Contact</b-nav-item>
          </b-navbar-nav>

          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto" v-show="!isLogin">
            <b-nav-item to="/register">Sign up</b-nav-item>
            <b-nav-item to="/login">Login</b-nav-item>
          </b-navbar-nav>
          <div class="ml-auto" v-show="isLogin">
            <b-dropdown id="dropdown-1" text="Dropdown Button" class="m-md-2">
              <template #button-content>
                <b-icon icon="person-fill"></b-icon> {{ userName }}
              </template>
              <b-dropdown-item to="/profile">Profile</b-dropdown-item>
              <b-dropdown-item @click="logout">Logout</b-dropdown-item>
            </b-dropdown>
          </div>
        </b-collapse>
      </div>
    </b-navbar>
  </b-container>
</template>

<script>
import { $on, $off, $once, $emit } from '../../utils/gogocodeTransfer'
import { user } from '@/api'
import { isEmpty } from '@/utils/validate'
import doCookie from '@/utils/cookie'
export default {
  name: 'Header',
  data() {
    return {
      isLogin: false,
      userName: '',
    }
  },
  methods: {
    setLoginVal(flag, userName) {
      this.isLogin = flag
      this.userName = userName
    },
    logout() {
      user.logout('').then((response) => {
        let code = response.code
        if (code === '0' || code === 0) {
          //删除cookie
          //将时间设置为过去时，立即删除cookie
          doCookie.setCookie('imputation-cookie', '', -1)
          doCookie.setCookie('imputation-username', '', -1)

          if (this.$router.path !== '/home') {
            this.setLoginVal(false, '')
            //跳转home页
            this.$router.push({
              name: 'home',
            })
          } else {
            this.setLoginVal(false, '')
            //刷新
            this.$router.go(0)
          }
        }
      })
    },
  },
  mounted() {
    let loginToken = doCookie.getCookie('imputation-cookie')
    let username = doCookie.getCookie('imputation-username')
    if (!isEmpty(loginToken) && !isEmpty(username)) {
      this.setLoginVal(true, username)
    } else {
      this.setLoginVal(false, '')
    }
    //为总线绑定函数
    $on(this.$bus, 'setLoginVal', this.setLoginVal)
  },
  beforeUnmount() {
    //销毁总线绑定的函数
    $off(this.$bus, 'setLoginVal')
  },
}
</script>

<style>
.bg-dark {
  background-color: #4f5d73 !important;
}
.btn-secondary {
  color: #fff;
  background-color: #4f5d73 !important;
  border-color: #4f5d73 !important;
}
</style>
