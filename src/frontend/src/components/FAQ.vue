<template>
  <div class="container-fluid">
    <div class="faqCard card card-body mr-auto d-block">
      <h2>Hi</h2>
      <p>welcome to Honey Boba, an anonymous platform for amateur graphic designers. We support originality and creativity by offering complete Anonymity and Neutrality.</p>
      <!-- <p>What is <strong>Anonymity</strong>? Well, think about how websites require you to sign up before you can do almost any meaningful things about it? Sites ask for registration really is a good thing, it helps the site to make targeted campaigns easier, better analyze the user behaviors, and planning the strategies accordingly. Users also get the benefits of having a "personal box" on each site they use, at the sacrifice of anonymity, of course. Now the real question is, do you value all the conveniences over anonymity? Let's get behind the company and observe how mant things they are doing behind-the-scene with your "online identity" at their company:</p>
      <p>What is <strong>Neutrality</strong>?</p> -->
    </div>
    <div class="faqCard card card-body mr-auto d-block">
      <div class="col-sm-10">
        <!-- <small class="text-danger">Your comment is completely anonymous</small> -->
      </div>
      <div class="row d-flex align-items-top">
        <div class="col-sm-10">
          <textarea
            ref="comments"
            name="comments"
            v-validate="'required|min:10'"
            rows="3"
            placeholder="Share your thoughts with the team"
            class="form-control"
            v-model="comments"
          ></textarea>
          <small class="text-danger">{{ errors.first('comments') }}</small>
          <div v-if="comments.length === 0 && isSent">
            <small class="text-success">Submitted, thank you for your feedback!</small>
          </div>
        </div>
        <div class="col-sm-2">
          <button @click="onSend" class="btn btn-outline-success float-right" role="button">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'Faq',
  data () {
    return {
      isSent: false,
      comments: ''
    }
  },
  methods: {
    _prepareFormData () {
      let formData = new FormData()
      formData.append('body', this.comments)
      return formData
    },
    onSend () {
      var that = this
      this.isSent = false
      this.$validator.validate().then(result => {
        if (!result) {
          // do stuff if not valid.
        } else {
          var formData = this._prepareFormData()
          axios.post('/api/dev',
            formData
          ).then(function (resp) {
            that.comments = ''
            that.isSent = true
            console.log(resp.data)
            console.log('post comments succeeded')
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
button.btn {
  border-radius: 0;
}
textarea.form-control {
  border-radius: 0;
}
.faqCard {
  border: 0;
  margin-bottom: 0;
  padding-bottom: 0;
}
</style>
