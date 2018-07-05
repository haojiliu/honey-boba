<template>
  <div class="designUploadCard card card-body mx-auto d-block">
    <div v-if="!this.$route.params.uri" class="row d-flex align-items-top">
      <div class="col-12 mb-2">
        <input v-model="name" v-validate="'alpha_spaces'" type="text" name="name" class="form-control" placeholder="Enter a name to best describe this design [Optional]">
        <!-- <small class="form-text text-muted">Enter a name to best describe this design</small> -->
        <small class="text-danger">{{ errors.first('name') }}</small>
      </div>
      <div class="col-12 mb-2">
        <input v-model="desc" v-validate="'alpha_spaces'" type="text" name="desc" class="form-control" placeholder="Description [Optional]">
        <!-- <small class="form-text text-muted">Enter a name to best describe this design</small> -->
        <small class="text-danger">{{ errors.first('desc') }}</small>
      </div>
      <div class="col-12 mb-2">
        <input v-model="email" v-validate="'required|email'" type="email" name="email" class="form-control" placeholder="Enter email">
        <small class="text-danger">{{ errors.first('email') }}</small>
        <input v-model="emailConfirmation" type="email" name="confirmEmail" class="form-control mt-1" placeholder="Confirm your email">
        <small v-if="emailConfirmation !== email" class="text-danger">Email doesn't match</small>
        <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else. Enter if you want to receive notifications when other people comment on this design</small>
      </div>
    </div>
    <div class="row d-flex align-items-top">
      <div class="col-12 mb-2">
        <input v-validate="{required: true, image: true, size: 10240}" type="file" name="file" ref="file" v-on:change="handleFileUpload" class="form-control-file" aria-describedby="uploadHelp">
        <small id="uploadHelp" class="form-text text-muted">Make sure you upload a .jpg or .png file.</small>
        <small class="text-danger">{{ errors.first('file') }}</small>
      </div>
      <!-- <div class="g-recaptcha" data-sitekey="6LcwUV8UAAAAAJo2f_MbbAbJTdr8xFpw1T4Naxpy"></div> -->
      <div v-if="this.uri.length === 0" class="col-12 mb-2" id="recaptcha">
        <vue-recaptcha @verify="onVerify" sitekey="6LcwUV8UAAAAAJo2f_MbbAbJTdr8xFpw1T4Naxpy"></vue-recaptcha>
      </div>
      <div class="col-12">
        <button v-if="!this.$route.params.uri" id='uploadButton' class="btn btn-dark btn-block" @click="uploadFile">Upload</button>
        <button v-else id='uploadButton' class="btn btn-dark btn-block" @click="uploadFile">Update File</button>
        <div v-if="errorMsg.length === 0 && lastUploadAt">
          <p v-if="!this.$route.params.uri" class="float-right text-success">Submitted at: {{lastUploadAt}}</p>
          <p v-else class="float-right text-success">Updated</p>
        </div>
        <div v-if="errorMsg.length>0">
          <p class="float-right text-danger">{{errorMsg}}</p>
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
  props: [],
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
      name: '',
      desc: '',
      lastUploadAt: '',
      isRecaptchaVerified: false,
      gRecaptchaResp: '',
      errorMsg: '',
      emailConfirmation: ''
    }
  },
  methods: {
    onVerify (response) {
      this.isRecaptchaVerified = true
      this.gRecaptchaResp = response
    },
    _prepareFormData () {
      let formData = new FormData()
      formData.append('file', this.file)
      formData.append('email', this.email)
      formData.append('name', this.name)
      formData.append('desc', this.desc)
      formData.append('uri', this.uri)
      formData.append('g-recaptcha-response', this.gRecaptchaResp)
      return formData
    },
    uploadFile () {
      if (this.emailConfirmation !== this.email) {
        return
      }
      this.$validator.validateAll().then(result => {
        if (!result) {
          // do stuff if not valid.
        } else {
          NProgress.start()
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
            NProgress.done()
            if (resp.data.status === 0) {
              // redirect only on /upload new ones, not update existing ones
              if (that.uri.length === 0) {
                that.$router.push('/uploaded/' + resp.data.uri + '/i')
              } else {
                that.lastUploadAt = new Date(Date.now())
                that.$emit('fileUpdated')
              }
            } else {
              that.errorMsg = resp.data.errors
            }
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
<style>
#uploadButton {
  border-radius: 0;
  background-color: rgba(0, 0, 0, 0.93);
}
.designUploadCard {
  /* border: 0; */
}
</style>
