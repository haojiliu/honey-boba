<template>
<div class="card card-body mx-auto d-block">
  <div class="row d-flex align-items-top">
    <div v-if="!this.designJson.is_deleted" class="col-6">
      <h4>Remove this design</h4>
      <small class="text-muted">We will remove this design from all visible outlets. This action is recoverable.</small>
    </div>
    <div v-else class="col-6">
      <h4>Activate this design</h4>
      <small class="text-muted">This design was removed, click to add it back to all visible outlets.</small>
    </div>
    <div class="col-6">
      <button v-if="!this.designJson.is_deleted" id="deleteButton" @click="onDelete" class="btn btn-outline-danger float-right" role="button">Delete It!</button>
      <button v-else id="deleteButton" @click="onActivate" class="btn btn-outline-success float-right" role="button">Activate</button>
    </div>
  </div>
</div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'DeleteDesignWidget',
  props: ['designJson'],
  methods: {
    _prepareDeleteFormData () {
      let formData = new FormData()
      formData.append('uri', this.designJson.uri)
      return formData
    },
    onDelete () {
      if (confirm('The design will be removed from this website')) {
        var that = this
        var formData = this._prepareDeleteFormData()
        axios.post('/api/delete',
          formData
        ).then(function (resp) {
          var payload = {
            uri: that.designJson.uri,
            val: true
          }
          that.$store.commit('designs/setIsDeleted', payload)
        }).catch(function (resp) {
          console.log('FAILURE!!')
        })
      } else {
        // do nothing
      }
    },
    onActivate () {
      if (confirm('The design will be added back to the website')) {
        var that = this
        var formData = this._prepareDeleteFormData()
        axios.post('/api/activate',
          formData
        ).then(function (resp) {
          var payload = {
            uri: that.designJson.uri,
            val: false
          }
          that.$store.commit('designs/setIsDeleted', payload)
        }).catch(function (resp) {
          console.log('FAILURE!!')
        })
      } else {
        // do nothing
      }
    }
  }
}
</script>
<style strict>
#deleteButton {
  border-radius: 0;
}
</style>
