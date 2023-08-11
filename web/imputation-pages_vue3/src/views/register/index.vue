<template>

  <b-container  class="bv-example-row page mt p-5 " style="">
    <h2>Sign up</h2>
    <br>

    <!-- <div class="alert alert-success" id="success-message" style="display: none;">
        <b>Well done!</b> An email including the activation code has been sent to your address.
        <br>
    </div> -->
        <b-row class="my-1">
            <b-col md="4" lg="3">
                <div class="form-group">
                    <label for="username" class="control-label">Username:</label>
                    <input id="username" name="username" type="text" class="form-control" autocomplete="off" v-model="form.username" @blur="checkUserName">
                    <div class="invalid" v-show="invalidUsername.type">{{invalidUsername.msg}}</div>
                </div>
            </b-col>
        </b-row>
        <b-row class="my-1">
            <b-col  md="4" lg="3">
                <div class="form-group">
                    <label for="first-name" class="control-label">First Name:</label>
                    <input id="first-name" name="first-name" type="text" class="form-control" autocomplete="off" v-model="form.firstName" @blur="checkFirstName">
                    <div class="invalid" v-show="invalidFirstName.type">{{invalidFirstName.msg}}</div>
                </div>
            </b-col>
            <b-col  md="4" lg="3">
                <div class="form-group">
                    <label for="last-name" class="control-label">Last Name:</label>
                    <input id="last-name" name="last-name" type="text" class="form-control" autocomplete="off" v-model="form.lastName" @blur="checkLastName">
                    <div class="invalid" v-show="invalidLastName.type">{{invalidLastName.msg}}</div>
                </div>
            </b-col>
        </b-row>
        
        <b-row class="my-1">
            <b-col  md="4" lg="3">
                <div class="form-group">
                    <label for="mail" class="control-label">E-Mail:</label>
                    <input id="mail" name="mail" type="text" class="form-control" autocomplete="off" v-model="form.email" @blur="checkmail">
                    <div class="invalid" v-show="invalidEmail.type">{{invalidEmail.msg}}</div>
                </div>
            </b-col>
        </b-row>
        <b-row class="my-1">
            <b-col  md="4" lg="3">
                <div class="form-group">
                    <label for="job-title" class="control-label">Job Title:</label>
                    <input id="job-title" name="job-title" type="text" class="form-control" autocomplete="off" v-model="form.jobTitle" @blur="checkJobTitle">
                    <div class="invalid" v-show="invalidJobTitle.type">{{invalidJobTitle.msg}}</div>
                </div>
            </b-col>
        </b-row>
        <b-row class="my-1">
            <b-col  md="4" lg="3">
                <div class="form-group">
                    <label for="organisation" class="control-label">Organisation:</label>
                    <input id="organisation" name="organisation" type="text" class="form-control" autocomplete="off"  v-model="form.organisation" @blur="checkOrganisation">
                    <div class="invalid" v-show="invalidOrganisation.type">{{invalidOrganisation.msg}}</div>
                </div>
            </b-col>
        </b-row>

        <b-row class="my-1">
            <b-col  md="4" lg="3">
                <div class="form-group">
                    <label for="country" class="control-label">Country:</label>
                    <input id="country" name="country" type="text" class="form-control" autocomplete="off"  v-model="form.country" @blur="checkCountry">
                    <div class="invalid" v-show="invalidCountry.type">{{invalidCountry.msg}}</div>
                </div>
            </b-col>
            <b-col  md="4" lg="3">
                <div class="form-group">
                    <label for="city" class="control-label">City:</label>
                    <input id="city" name="city" type="text" class="form-control" autocomplete="off"  v-model="form.city" @blur="checkCity">
                    <div class="invalid" v-show="invalidCity.type">{{invalidCity.msg}}</div>
                </div>
            </b-col>
        </b-row>
        <b-row class="my-1">
            <b-col  md="4" lg="3">
                <div class="form-group">
                    <label for="new-password" class="control-label">Password:</label>
                    <div class="outer">
                        <input id="new-password" name="new-password" :type="passwordType" class="inner form-control" style="width: 90%;"  autocomplete="off"  v-model="form.password" @blur="checkPw">
                        <img class="eyes" :src="eyesImage" @click="clickEyes"/>
                    </div>
                    <div class="invalid" v-show="invalidPassword.type">{{invalidPassword.msg}}</div>
                </div>
            </b-col>
        </b-row>
        <b-row class="my-1">
            <b-col  md="4" lg="3">
                <div class="form-group">
                    <label for="confirm-new-password" class="control-label">Confirm password:</label>
                    <div class="outer">
                        <input id="confirm-new-password" name="confirm-new-password" :type="passwordType" class="inner form-control" style="width: 90%;"  autocomplete="off"  v-model="form.confirm" @blur="confirmPw">
                        <img class="eyes" :src="eyesImage" @click="clickEyes"/>
                    </div>
                    <div class="invalid" v-show="invalidConfirm.type">{{invalidConfirm.msg}}</div>
                </div>
            </b-col>
        </b-row>

        <div class="form-group">
            <button id="save" class="btn btn-primary" @click="onReset">Register</button>
        </div>
    </b-container >
</template>

<script>
import  {user} from '@/api'
import { MessageBox  } from 'element-ui'
import { checkEmail,checkPassword,isEmpty }  from "@/utils/validate"
export default {
    name:'register',
    data() {
      return {
        form: {
            username:'',
            password:'',
            confirm:'',
            email: '',
            firstName: '',
            lastName: '',
            jobTitle: '',
            organisation: '',
            country: '',
            city: ''
        },
        invalidUsername:{
            type:false,
            msg:""
        },
        invalidFirstName:{
            type:false,
            msg:""
        },
        invalidLastName:{
            type:false,
            msg:""
        },
        invalidJobTitle:{
            type:false,
            msg:""
        },
        invalidOrganisation:{
            type:false,
            msg:""
        },
        invalidEmail:{
            type:false,
            msg:""
        },
        invalidCountry:{
            type:false,
            msg:""
        },
        invalidCity:{
            type:false,
            msg:""
        },
        invalidConfirm:{
            type:false,
            msg:""
        },
        invalidPassword:{
            type:false,
            msg:""
        },
        eyesImage:"./image/close.png",
        passwordType:"password",
        show: true
      }
    },
    methods: {
      onReset() {
        let subData ={
            username:this.form.username,
            password:this.form.password,
            confirm:this.form.confirm,
            email: this.form.email,
            firstName: this.form.firstName,
            lastName: this.form.lastName,
            jobTitle: this.form.jobTitle,
            organisation: this.form.organisation,
            country: this.form.country,
            city: this.form.city
        }
        //提交数据
        user.auth(subData).then((response) => {
            const data = response
            console.log(data);
            let code = data.code
            if(code == 0 || code == "0"){
                MessageBox.alert('The registration succeeds and the login page is displayed', 'prompt', {
                    confirmButtonText: 'ok',
                    callback: action => {
                        console.log("action="+action)
                        this.signIn();
                    }
                });
            }
            
        })
        // let res = register(subData);
        // console.log(res)
      },
      //跳转到登录页
      signIn(){
        this.$router.push({
            name:'login'
        });
      },
      //校验姓名
      checkUserName(){
        let username = this.form.username
        if(!isEmpty(username)){
            if(username.length<4){
                this.invalidUsername.type=true
                this.invalidUsername.msg="The username must contain at least four characters."
            }else{
                this.invalidUsername.type=false
                this.invalidUsername.msg=""
            }
        }else{
            this.invalidUsername.type=true
            this.invalidUsername.msg="The username is required."
        }
      },
      checkFirstName(){
        let firstName = this.form.firstName
        if(isEmpty(firstName)){
            this.invalidFirstName.type=true
            this.invalidFirstName.msg="The First Name is required."
        }else{
            this.invalidFirstName.type=false
            this.invalidFirstName.msg=""
        }
      },
      checkLastName(){
        let lastName = this.form.lastName
        if(isEmpty(lastName)){
            this.invalidLastName.type=true
            this.invalidLastName.msg="The Last Name is required."
        }else{
            this.invalidLastName.type=false
            this.invalidLastName.msg=""
        }
      },
      checkJobTitle(){
        let jobTitle = this.form.jobTitle
        if(isEmpty(jobTitle)){
            this.invalidJobTitle.type=true
            this.invalidJobTitle.msg="The Job Title is required."
        }else{
            this.invalidJobTitle.type=false
            this.invalidJobTitle.msg=""
        }
      },
      checkOrganisation(){
        let organisation = this.form.organisation
        if(isEmpty(organisation)){
            this.invalidOrganisation.type=true
            this.invalidOrganisation.msg="The Last Organisation is required."
        }else{
            this.invalidOrganisation.type=false
            this.invalidOrganisation.msg=""
        }
      },
      checkCountry(){
        let country = this.form.country
        if(isEmpty(country)){
            this.invalidCountry.type=true
            this.invalidCountry.msg="The Last Country is required."
        }else{
            this.invalidCountry.type=false
            this.invalidCountry.msg=""
        }
      },
      checkCity(){
        let city = this.form.city
        if(isEmpty(city)){
            this.invalidCity.type=true
            this.invalidCity.msg="The Last City is required."
        }else{
            this.invalidCity.type=false
            this.invalidCity.msg=""
        }
      },
      //校验邮箱
      checkmail(){
        if(!isEmpty(this.form.email)){
        let flag = checkEmail(this.form.email);
          if(!flag){
                this.invalidEmail.type=true
                this.invalidEmail.msg="This email address is not valid."
            }else{
                this.invalidEmail.type=false
                this.invalidEmail.msg=""
            }
        }else{
            this.invalidEmail.type=true
            this.invalidEmail.msg="The email is required."
        }
      },
      //校验密码
      checkPw(){
         //8位以上的字母与数字组合
        if(!isEmpty(this.form.password)){
            let flag = checkPassword(this.form.password);
            if(!flag){
                this.invalidPassword.type=true
                this.invalidPassword.msg="Use 6 ~ 20 characters."
            }else{
                this.invalidPassword.type=false
                this.invalidPassword.msg=""
            }
        }else{
            this.invalidPassword.type=true
            this.invalidPassword.msg="The Password is required."
        }
      },
      //确认密码
      confirmPw(){
        if(!isEmpty(this.form.password)&&!isEmpty(this.form.confirm)){
          if(this.form.password != this.form.confirm){
            this.invalidConfirm.type=true
            this.invalidConfirm.msg="Different passwords"
          }else{
            this.invalidConfirm.type=false
            this.invalidConfirm.msg=""
          }
        }
      },
      clickEyes(){
        this.eyesType = !this.eyesType
        if(this.eyesType){
          this.eyesImage = "./image/open.png"
          this.passwordType = "text"
        }else{
          this.eyesImage = "./image/close.png"
          this.passwordType = "password"
        }
      }
    }
}
</script>

<style>
.page {
    background: #fff;
    box-shadow: 0 2px 5px 0 rgb(0 0 0 / 16%), 0 2px 10px 0 rgb(0 0 0 / 12%);
    transition: box-shadow .25s;
    margin-top: 0;
    padding: 15px;
}
.p{
    padding-top: 3rem !important;
    padding-right: 20rem !important;
    padding-bottom: 3rem !important;
    padding-left: 20rem !important;
}
.invalid{
    width: 100%;
    margin-top: 0.25rem;
    font-size: 80%;
    color: #dc3545;
}
.eyes{
  height: 1rem;
}
.outer{
    background-color: #fff;
    border: 1px solid #e7eaf0;
    border-radius: 0.375rem;
    box-shadow: 0 1px 2px rgb(50 50 71 / 8%);
    color: #16192c;
    display: block;
}
.inner{
    border: 0px solid #ffffff !important;
    border-radius: 0.375rem !important;
    box-shadow: 0 0px 0px rgb(255 255 255) !important;
    display: inline-block !important;
}
</style>