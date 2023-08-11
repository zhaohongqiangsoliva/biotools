<template>
  <b-container class="mt">
    <div class="container page my-5 p-5" style="">
        <h2>Account Settings</h2>
        Please fill out the form below to change your account settings or your password.
        <br>
        <br>

        <h4>Personal Information</h4>

        <input name="username" type="hidden" value="fansp">

        <div class="form-group">
            <label for="firstName" class="control-label">First Name:<img class="asterisk" :src="imgUrls.asterisk" ></label>
            <input id="firstName" name="firstName" type="text" class="form-control col-sm-3" v-model="user.firstName">
            <div class="invalid-feedback"></div>
        </div>

        <div class="form-group">
            <label for="lastName" class="control-label">Last Name:<img class="asterisk" :src="imgUrls.asterisk" ></label>
            <input id="lastName" name="lastName" type="text" class="form-control col-sm-3" v-model="user.lastName">
            <div class="invalid-feedback"></div>
        </div>

        <div class="form-group">
            <label for="email" class="control-label">E-Mail:<img class="asterisk" :src="imgUrls.asterisk" ></label>
            <input id="email" name="email" type="text" class="form-control col-sm-3" v-model="user.email">
            <div class="invalid-feedback"></div>
        </div>

        <div class="form-group">
            <label for="jobTitle" class="control-label">Job Title:<img class="asterisk" :src="imgUrls.asterisk" ></label>
            <input id="jobTitle" name="jobTitle" type="text" class="form-control col-sm-3" v-model="user.jobTitle">
            <div class="invalid-feedback"></div>
        </div>

        <div class="form-group">
            <label for="organisation" class="control-label">Organisation:<img class="asterisk" :src="imgUrls.asterisk" ></label>
            <input id="organisation" name="organisation" type="text" class="form-control col-sm-3" v-model="user.organisation">
            <div class="invalid-feedback"></div>
        </div>

        <div class="form-group">
            <label for="country" class="control-label">Country:<img class="asterisk" :src="imgUrls.asterisk" ></label>
            <input id="country" name="country" type="text" class="form-control col-sm-3" v-model="user.country">
            <div class="invalid-feedback"></div>
        </div>

        <div class="form-group">
            <label for="city" class="control-label">City:<img class="asterisk" :src="imgUrls.asterisk" ></label>
            <input id="city" name="city" type="text" class="form-control col-sm-3" v-model="user.city">
            <div class="invalid-feedback"></div>
        </div>

        <h4>Change password</h4>

        <div class="form-group">
            <label for="password" class="control-label">New Password:</label>
            <input id="password" name="password" type="password" class="form-control col-sm-3" v-model="user.password">
            <div class="invalid-feedback"></div>
        </div>

        <div class="form-group">
            <label for="confirmNewPassword" class="control-label">New Password (again):</label>
            <input id="confirmNewPassword" name="confirmNewPassword" type="password" class="form-control col-sm-3" v-model="user.confirmNewPassword">
            <div class="invalid-feedback"></div>
        </div>

        <div class="form-group">
            <button class="btn btn-primary" type="submit" @click="update">Update Account</button>

        </div>
        <hr>
        <h3>Delete Account</h3>
        <p>Once you delete your user account, there is no going back. Please be certain.</p>
        <div class="control-group">
            <div class="controls">
                <button class="btn btn-danger" id="delete_account">Delete Account</button>
            </div>
        </div>
    </div>
  </b-container>
</template>

<script>
import  {user} from '@/api'
export default {
    name:"profile",
    data () {
        return {
            imgUrls:{
                asterisk:"./image/asterisk.png"
            },
            user:{
                city: "",
                country: "",
                email: "",
                firstName: "",
                jobTitle: "",
                lastName: "",
                organisation: "",
                password: "",
            },
            msgBox: null
        }
    },
    methods: {
        getUserMsg(){
            user.querythisuser(null).then((response) => {
                let code = response.code
                if(code === "0" || code === 0){
                    let data = response.data
                    
                    this.user.city = data.city
                    this.user.country = data.country
                    this.user.email = data.email
                    this.user.firstName = data.firstName
                    this.user.jobTitle = data.jobTitle
                    this.user.lastName = data.lastName
                    this.user.organisation = data.organisation
                }
            })
        },
        update(){
            this.msgBox = ''
            this.$bvModal.msgBoxConfirm('Are you sure to modify it?', {
                title: 'Please Confirm',
                size: 'sm',
                buttonSize: 'sm',
                okVariant: 'danger',
                okTitle: 'YES',
                cancelTitle: 'NO',
                footerClass: 'p-2',
                hideHeaderClose: false,
                centered: true
            })
            .then(value => {
                this.msgBox = value
                //确定修改时
                if(value){
                    let subData ={
                        password:this.user.password,
                        email: this.user.email,
                        firstName: this.user.firstName,
                        lastName: this.user.lastName,
                        jobTitle: this.user.jobTitle,
                        organisation: this.user.organisation,
                        country: this.user.country,
                        city: this.user.city
                    }
                    //提交数据
                    user.update(subData).then((response) => {
                        let code = response.code
                        if(code === "0" || code === 0){
                            this.getUserMsg()
                        }
                    })
                }
            })
            .catch(err => {
                console.log(err);
            })
            
        }
    },
    mounted () {
        this.getUserMsg()
    }


}
</script>

<style>
    .asterisk{
    width: 0.5rem;
    }
</style>