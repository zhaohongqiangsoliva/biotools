//引入Vue
import Vue from "vue";
//引入路由插件
import VueRouter from "vue-router";


import login from "@/views/login";
import home from "@/views/home";
import register from "@/views/register";
import profile from "@/views/profile";
import upload from "@/views/upload";
import run from "@/views/run";

const originalPush = VueRouter.prototype.push

VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}


Vue.use(VueRouter);

export default new VueRouter({
    routes: [
        {
            path: "/",
            redirect: "/home"
        },
        {
            name: "home",
            path: "/home",
            component: home
        },
        {
            name: "login",
            path: "/login",
            component: login
        },
        {
            name: "register",
            path: "/register",
            component: register
        },
        {
            name: "profile",
            path: "/profile",
            component: profile
        },
        {
            name: "upload",
            path: "/upload",
            component: upload
        },
        {
            name: "run",
            path: "/run",
            component: run
        },
    ]
})