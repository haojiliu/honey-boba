<template>
  <div class="container-fluid">
    <div v-if="this.designJson" class="row">
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
              <div v-if="!isDeleted">
                <button @click="deleteDesign" class="btn btn-outline-danger float-right" role="button">Delete It!</button>
              </div>
              <div v-else>
                <p class="float-right text-success">Deleted</p>
              </div>
            </div>
          </div>
        </div>
        <design-uploader></design-uploader>
      </div>
      <div class="col-6">
        <div class="card card-body mx-auto d-block">
          <design-item v-bind:designJson="designJson"></design-item>
          <review-widget v-bind:reviewsJson="designJson.reviews"></review-widget>
        </div>
      </div>
    </div>
    <div v-else></div>
  </div>
</template>
<script>
import ReviewWidget from './ReviewWidget'
import DesignUploader from './DesignUploader'
import DesignItem from './DesignItem'
import axios from 'axios'

export default {
  name: 'Uploaded',
  watch: {
    '$route' (to, from) {
      // react to route changes...
      this.tryGetDesign(to.params.uri)
    },
    designJson: function (newVal, oldVal) { // watch it
      // Re-render the reviews
      console.log('val changed!!')
    }
  },
  components: {
    ReviewWidget,
    DesignUploader,
    DesignItem
  },
  data () {
    return {
      isDeleted: false
    }
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
      var that = this
      console.log('going to delete a design')
      var formData = this._prepareFormData()
      axios.post('/api/delete',
        formData
      ).then(function (resp) {
        that.isDeleted = true
      }).catch(function (resp) {
        console.log('FAILURE!!')
      })
    },
    tryGetDesign (uri) {
      if (this.$store.getters['designs/getDesignByUri'](uri) === undefined) {
        this.$store.dispatch('designs/getOneDesign', uri)
      }
    }
  },
  created () {
    this.tryGetDesign(this.$route.params.uri)
  },
  beforeMount () {
    console.log('before mount...')
  },
  mounted () {
    console.log(' mounted')
  },
  destroyed () {
    console.log('uploaded destroyed')
  },
  beforeDestroy () {
    console.log('uploaded about to be destroyed')
  }
}
</script>
<style strict></style>
