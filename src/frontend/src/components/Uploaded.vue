<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-6">
        <div class="card card-body mx-auto d-block">
          <div class="row d-flex align-items-top">
            <div class="col-12">
              <p class="lead"><strong><em>STOP! Make sure this is your design before making any changes</em></strong></p>
            </div>
          </div>
        </div>
        <div class="card card-body mx-auto d-block">
          <div class="row d-flex align-items-top">
            <div class="col-6">
              <h4>Remove this design</h4>
              <small class="text-muted">We will permanently delete all the data associated with this design. This action is not recoverable</small>
            </div>
            <div class="col-6">
              <button @click="deleteDesign" class="btn btn-warning float-right" role="button">Delete It!</button>
            </div>
          </div>
        </div>
        <design-uploader></design-uploader>
      </div>
      <div class="col-6">
        <div class="card card-body mx-auto d-block">
          <img class="card-img-top" v-bind:src="designJson.thumbnail_uri">
          <p class="text-muted text-right">Last updated at {{designJson.updated_at_utc}}</p>
          <review-widget v-bind:reviewsJson="designJson.reviews"></review-widget>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import ReviewWidget from './ReviewWidget'
import DesignUploader from './DesignUploader'
import axios from 'axios'

export default {
  name: 'Uploaded',
  watch: {
    '$route' (to, from) {
      // react to route changes...
      console.log('route changed from ' + from.params.uri + ' to ' + to.params.uri)
    }
  },
  components: {
    ReviewWidget,
    DesignUploader
  },
  computed: {
    designJson () {
      return this.$store.getters['designs/getDesignByUri'](this.$route.params.uri)
    }
  },
  methods: {
    _prepareFormData () {
      let formData = new FormData()
      formData.append('uri', this.designJson.uri)
      return formData
    },
    deleteDesign () {
      console.log('going to delete a design')
      var formData = this._prepareFormData()
      axios.post('/api/delete',
        formData
      ).then(function (resp) {
        console.log(resp.data)
        console.log('delete design succeeded')
      }).catch(function (resp) {
        console.log('FAILURE!!')
      })
    }
  }
}
</script>
<style></style>
