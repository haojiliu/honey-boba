<template>
  <div class="card card-body mx-auto d-block">
    <div class="row d-flex align-items-top">
      <div class="col-8">
        <input v-model="email" name="email" v-validate="'required|email'" type="email" class="form-control" placeholder="Enter the email used for this design">
        <div>
          <small class="text-danger">{{ errors.first('email') }}</small>
        </div>
        <!-- <small class="text-muted">Let's make sure it's your design</small> -->
      </div>
      <div class="col-4">
        <div v-if="!isEmailConfirmed">
          <button id="confirmEmailButton" @click="onConfirmEmail" class="btn btn-outline-primary float-right" role="button">Confirm</button>
        </div>
        <div v-else>
          <p class="float-right text-success">Confirmed</p>
        </div>
      </div>
    </div>
    <div class="row d-flex align-items-top">
      <div class="col-12" v-if="errorMsg.length>0">
        <p class="text-danger">{{errorMsg}}</p>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  props: ['designJson'],
  data () {
    return {
      email: '',
      isEmailConfirmed: false,
      errorMsg: ''
    }
  },
  methods: {
    _prepareFormData () {
      let formData = new FormData()
      formData.append('email', this.email)
      formData.append('uid', this.designJson.uid)
      return formData
    },
    onConfirmEmail () {
      this.errorMsg = ''
      this.$validator.validateAll().then(result => {
        if (!result) {
          // do stuff if not valid.
        } else {
          var formData = this._prepareFormData()
          var that = this
          axios.post('/api/auth/email',
            formData
          ).then(function (resp) {
            if (resp.data.status === 0) {
              that.isEmailConfirmed = true
              that.$emit('emailConfirmed')
            } else {
              that.errorMsg = resp.data.errors
            }
          }).catch(function (resp) {
            console.log('FAILURE!!')
          })
        }
      })
    }
  }
}
</script>
<style strict>
#confirmEmailButton {
  border-radius: 0;
}
</style>
