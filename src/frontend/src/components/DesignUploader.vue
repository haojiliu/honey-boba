<template>
  <div class="card card-body mx-auto d-block">
    <div class="row d-flex align-items-top">
      <div class="col-12">
        <h4 v-if="this.$route.params.uri">Update it</h4>
      </div>
    </div>
    <div v-if="!this.$route.params.uri" class="row d-flex align-items-top">
      <div class="col-12">
        <input v-model="email" type="email" class="form-control" aria-describedby="emailHelp" placeholder="Enter email">
        <small id="emailHelp" class="text-muted">We'll never share your email with anyone else. Enter if you want to receive notifications when other people reply to this design</small>
      </div>
    </div>
    <div class="row d-flex align-items-top">
      <div class="col-12">
        <input type="file" ref="file" v-on:change="handleFileUpload" class="form-control-file" id="file" aria-describedby="uploadHelp">
        <small id="uploadHelp" class="form-text text-muted">Make sure you upload a .jpg or .pdf file.</small>
      </div>
      <button class="btn btn-dark btn-block" @click="uploadFile">Upload</button>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'DesignUploader',
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
      email: ''
    }
  },
  methods: {
    _prepareFormData () {
      let formData = new FormData()
      formData.append('file', this.file)
      formData.append('email', this.email)
      formData.append('uri', this.uri)
      return formData
    },
    uploadFile () {
      var formData = this._prepareFormData()
      axios.post('/api/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      ).then(function (resp) {
        console.log(resp.data)
      }).catch(function (resp) {
        console.log('FAILURE!!')
      })
    },

    handleFileUpload () {
      this.file = this.$refs.file.files[0]
    }
  }
}
</script>
