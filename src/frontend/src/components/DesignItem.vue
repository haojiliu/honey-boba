<template>
  <div class="">
    <img class="card-img-top" v-bind:src="designJson.thumbnail_uri">
    <div class="row">
      <div class="col-6 text-left">
        <small class="text-muted">Last updated: {{designJson.updated_at_utc}}</small>
      </div>
      <div class="col-6 text-right">
        <a v-if="!isReported && !this.$route.params.uri"  @click="onReport" class="btn"><small class="text-primary">Report This</small></a>
        <small v-if="isReported && !this.$route.params.uri" class="text-succeeded">Reported</small>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'DesignItem',
  props: ['designJson'],
  data () {
    return {
      isReported: false
    }
  },
  methods: {
    _prepareFormData () {
      let formData = new FormData()
      formData.append('uri', this.designJson.uri)
      return formData
    },
    onReport () {
      var that = this
      console.log('going to report this design!')
      var formData = this._prepareFormData()
      axios.post('/api/report',
        formData
      ).then(function (resp) {
        console.log(resp.data)
        console.log('report a design succeeded')
        that.isReported = true
      }).catch(function (resp) {
        console.log('FAILURE!!')
      })
    }
  }
}
</script>
<style strict>
a.btn {
  padding: 0;
}
</style>
