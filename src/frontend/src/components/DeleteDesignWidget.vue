<template>
<div class="card card-body mx-auto d-block">
  <div class="row d-flex align-items-top">
    <div class="col-6">
      <h4>Remove this design</h4>
      <small class="text-muted">We will permanently delete all the data associated with this design. This action is not recoverable</small>
    </div>
    <div class="col-6">
      <div v-if="!isDeleted">
        <button v-if="isEmailConfirmed" id="deleteButton" @click="onDelete" class="btn btn-outline-danger float-right" role="button">Delete It!</button>
        <button v-else id="deleteButton" @click="onDelete" class="btn btn-outline-danger float-right" role="button" disabled>Delete It!</button>
      </div>
      <div v-else>
        <p class="float-right text-success">Deleted</p>
      </div>
    </div>
  </div>
</div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'DeleteDesignWidget',
  props: ['designJson', 'isEmailConfirmed'],
  data () {
    return {
      isDeleted: false
    }
  },
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
          that.isDeleted = true
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
