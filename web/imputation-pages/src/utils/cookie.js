export default {
    setCookie: (name, value, days) => {
        var d = new Date;
        d.setTime(d.getTime() + 24 * 60 * 60 * 1000 * days);
        window.document.cookie = name + "=" + value + ";path=/;expires=" + d.toGMTString();
    },
    getCookie: name => {
        var v = window.document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
        return v ? v[2] : null;
    },
    delCookie: name => {
        var d = new Date;
        d.setTime(d.getTime() + 24 * 60 * 60 * 1000 * (-1));//将时间设置为过去时，立即删除cookie
        window.document.cookie = name + "=" + "" + ";path=/;expires=" + d.toGMTString();
    }

}