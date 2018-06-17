<template>
  <div>
    <form id="newReview">
      <div class="input-group">
        <textarea-autosize
          v-validate="'required|min:10'"
          name="reviewText"
          rows="1"
          placeholder="Share your thoughts"
          class="form-control"
          ref="reviewText"
          v-model="reviewText"
          :max-height="350"
        ></textarea-autosize>
        <div class="input-group-append">
          <button v-if="isRecaptchaVerified" @click="onSubmit" class="btn btn-outline-primary" type="button">Send</button>
          <button v-else class="btn btn-outline-dark" type="button" disabled>Send</button>
        </div>
      </div>
      <small class="text-danger">{{ errors.first('reviewText') }}</small>
      <!-- <div class="g-recaptcha" data-sitekey="6LcwUV8UAAAAAJo2f_MbbAbJTdr8xFpw1T4Naxpy"></div> -->
      <div v-if="this.reviewText.length > 10" id="recaptcha">
        <vue-recaptcha @verify="onRecaptchaVerified" sitekey="6LcwUV8UAAAAAJo2f_MbbAbJTdr8xFpw1T4Naxpy"></vue-recaptcha>
      </div>
    </form>
  </div>
</template>
<script>
import axios from 'axios'
import VueRecaptcha from 'vue-recaptcha'

export default {
  props: ['uri'],
  components: { VueRecaptcha },
  data () {
    return {
      reviewText: '',
      isRecaptchaVerified: false
    }
  },
  methods: {
    onRecaptchaVerified () {
      this.isRecaptchaVerified = true
      console.log('recaptcha verified on ' + this.uri)
    },
    _prepareFormData () {
      let formData = new FormData()
      formData.append('reviewText', this.reviewText)
      formData.append('uri', this.uri)
      return formData
    },
    onSubmit () {
      var that = this
      this.$validator.validate().then(result => {
        if (!result) {
          // do stuff if not valid.
        } else {
          var formData = this._prepareFormData()
          axios.post('/api/review',
            formData
          ).then(function (resp) {
            that.$store.dispatch('designs/refreshOneReview', that.uri)
            that.reviewText = ''
            that.isRecaptchaVerified = false
            console.log(resp.data)
            console.log('post review succeeded')
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
textarea.form-control {
  border-left: none;
  border-top: none;
}
#newReview {
  padding-top: 5px;
}
#recaptcha {
  padding-top: 10px;
}
</style>
