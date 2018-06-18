<template>
  <div class="card card-body mx-auto d-block">
    <div class="row d-flex align-items-top">
      <div v-if="this.$route.params.uri" class="col-12">
        <h4>Update it</h4>
      </div>
    </div>
    <div v-if="!this.$route.params.uri" class="row d-flex align-items-top">
      <div class="col-12 mb-2">
        <input v-model="title" v-validate="'required'" type="text" name="title" class="form-control" placeholder="Give it a name">
        <small class="form-text text-muted">Enter a name to best describe this design</small>
        <small class="text-danger">{{ errors.first('title') }}</small>
      </div>
      <div class="col-12 mb-2">
        <input v-model="email" v-validate="'email'" type="email" name="email" class="form-control" aria-describedby="emailHelp" placeholder="Enter email">
        <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else. Enter if you want to receive notifications when other people comment on this design</small>
        <small class="text-danger">{{ errors.first('email') }}</small>
      </div>
    </div>
    <div class="row d-flex align-items-top">
      <div class="col-12 mb-2">
        <small id="uploadHelp" class="form-text text-muted">Make sure you upload a .jpg or .png file.</small>
        <input v-validate="{required: true, image: true, size: 10240}" type="file" name="file" ref="file" v-on:change="handleFileUpload" class="form-control-file" aria-describedby="uploadHelp">
        <small class="text-danger">{{ errors.first('file') }}</small>
      </div>
      <!-- <div class="g-recaptcha" data-sitekey="6LcwUV8UAAAAAJo2f_MbbAbJTdr8xFpw1T4Naxpy"></div> -->
      <div v-if="this.uri.length === 0" class="col-12 mb-2" id="recaptcha">
        <vue-recaptcha @verify="onVerify" sitekey="6LcwUV8UAAAAAJo2f_MbbAbJTdr8xFpw1T4Naxpy"></vue-recaptcha>
      </div>
      <div class="col-12">
        <button class="btn btn-dark btn-block" @click="uploadFile">Upload</button>
        <div v-if="lastUploadAt">
          <p class="float-right text-success">Last uploaded at: {{lastUploadAt}}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import VueRecaptcha from 'vue-recaptcha'

export default {
  name: 'DesignUploader',
  components: { VueRecaptcha },
  computed: {
    uri () {
      if (this.$route.params.uri) {
        return this.$route.params.uri
      }
      return ''
    }
  },
  data () {
    return {
      file: null,
      email: '',
      title: '',
      lastUploadAt: '',
      isRecaptchaVerified: false,
      gRecaptchaResp: ''
    }
  },
  methods: {
    onVerify (response) {
      console.log(response)
      this.isRecaptchaVerified = true
      this.gRecaptchaResp = response
      console.log('recaptcha verified!')
    },
    _prepareFormData () {
      let formData = new FormData()
      formData.append('file', this.file)
      formData.append('email', this.email)
      formData.append('title', this.title)
      formData.append('uri', this.uri)
      formData.append('g-recaptcha-response', this.gRecaptchaResp)
      return formData
    },
    uploadFile () {
      this.$validator.validate().then(result => {
        if (!result) {
          // do stuff if not valid.
        } else {
          var formData = this._prepareFormData()
          var that = this
          axios.post('/api/upload',
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
          ).then(function (resp) {
            that.lastUploadAt = new Date(Date.now())
            console.log(resp.data)
          }).catch(function (resp) {
            console.log('FAILURE!!')
          })
        }
      })
    },

    handleFileUpload () {
      this.file = this.$refs.file.files[0]
    }
  }
}
</script>
