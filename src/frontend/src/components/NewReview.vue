<template>
  <div>
    <form id="newReview">
      <div class="input-group">
        <textarea-autosize
          id="newReviewText"
          v-validate="'required|min:10'"
          name="review"
          rows="1"
          placeholder="Share your thoughts"
          class="form-control"
          ref="reviewText"
          v-model="reviewText"
          :max-height="350"
        ></textarea-autosize>
        <div class="input-group-append">
          <button id="send" @click="onSubmit" class="btn btn-outline-dark" type="button">Send</button>
        </div>
      </div>
      <small class="text-danger">{{ errors.first('review') }}</small>
    </form>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  props: ['uri'],
  data () {
    return {
      reviewText: ''
    }
  },
  methods: {
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
            that.$emit('newReviewPosted', that.uri)
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
#newReviewText {
  border-radius: 0;
}
#send {
  border-radius: 0;
}
#newReview {
  padding-top: 5px;
}
</style>
