//校验姓名
export function checkName(name) {
    const regex = /^([\\u4e00-\\u9fa5]{1,20}|[a-zA-Z\\.\\s]{1,20})$/
    let flag = false
    if (!regex.test(name)) {
        flag = true
    }
    return flag
}

//校验邮箱
export function checkEmail(email) {
    const regex = /^(\w+([-.][A-Za-z0-9]+)*){3,18}@\w+([-.][A-Za-z0-9]+)*\.\w+([-.][A-Za-z0-9]+)*$/
    let flag = false
    if (regex.test(email)) {
        flag = true
    }
    return flag
}

//校验手机号
export function checkMobile(mobile) {
    const regex = /(\+|9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$/
    let flag = false
    if (!regex.test(mobile)) {
        flag = true
    }
    return flag
}

//校验密码
export function checkPassword(password) {
    //6~20位至少包含数字,大小写字母,字符
    // const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$#!%*?&])[A-Za-z\d$@$#!%*?&]{6,20}/
    //判断密码满足大写字母，小写字母，数字和特殊字符，其中任意三种组合，且长度在6到20之间
    // const regex = /^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\W_!@#$%^?&*`~()-+=]+$)(?![a-z0-9]+$)(?![a-z\W_!@#$%^?&*`~()-+=]+$)(?![0-9\W_!@#$%^?&*`~()-+=]+$)[a-zA-Z0-9\W_!@#$%^?&*`~()-+=]{6,20}$/
    const regex = /^[0-9a-zA-Z][0-9a-zA-Z_!@#$%^?&*`~()-+=]{5,20}/
    let flag = false
    if (regex.test(password)) {
        flag = true
    }
    return flag
}

// 校验字符串是否为空
export function isEmpty(str) {
    let flag = true
    if (!(str === undefined || str === "" || str === null)) {
        flag = false
    }
    return flag
}

// 校验系统类型
export function ckeckBrowerVersion() {
    let version = navigator.userAgent.toLowerCase();
    let mac = version.indexOf('mac');
    let os = version.indexOf('os');
    let linux = version.indexOf('linux');
    if (mac > 0 && os > 0) {
        // 苹果系统下执行的操作
        return "os"
    } else if (linux > 0) {
        return "linux"
    } else {
        // windows系统下执行的操作
        return "windows"
    }
}
