<template>
  <div>
    <div>
      <!-- <input type="email" class="form-control" aria-describedby="emailHelp" placeholder="Enter email to receive updates"> -->
      <!-- <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else. Enter if you want to receive notifications when other people reply to this thread</small> -->
    </div>
    <div id="newReview">
      <div class="input-group mb-3">
        <textarea v-model="reviewText" class="form-control newReviewText" name="reviewText" rows="1" placeholder="Help Each Other!"></textarea>
        <div class="input-group-append">
          <button @click="submitReview" class="btn btn-secondary" type="button">Send</button>
        </div>
      </div>
      <div>
        <small id="newReviewHelp" class="form-text text-muted text-right">Constructive reviews do the most help!</small>
      </div>
    </div>
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
    submitReview () {
      var formData = this._prepareFormData()
      axios.post('/api/review',
        formData
      ).then(function (resp) {
        console.log(resp.data)
        console.log('post review succeeded')
      }).catch(function (resp) {
        console.log('FAILURE!!')
      })
    }
  }
}
</script>
<style strict>
#newReview{
  margin-top: 10px;
}
</style>
