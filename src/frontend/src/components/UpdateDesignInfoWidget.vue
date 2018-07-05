<template>
  <div class="card card-body mx-auto d-block">
    <div class="row d-flex align-items-top">
      <div class="col-12 mb-2">
        <small class="text-muted">Name:</small>
        <input v-model="name" v-validate="" type="text" name="name" class="form-control" placeholder="Enter a name to best describe this design [Optional]">
        <!-- <small class="form-text text-muted">Enter a name to best describe this design</small> -->
        <small class="text-danger">{{ errors.first('name') }}</small>
      </div>
      <div class="col-12 mb-2">
        <small class="text-muted">Description:</small>
        <input v-model="desc" v-validate="" type="text" name="desc" class="form-control" placeholder="Description [Optional]">
        <!-- <small class="form-text text-muted">Enter a name to best describe this design</small> -->
        <small class="text-danger">{{ errors.first('desc') }}</small>
      </div>
      <div class="col-12">
        <button id='updateButton' class="btn btn-dark btn-block" @click="onUpdate">Update Info</button>
        <div v-if="errorMsg.length === 0 && updatedAt">
          <p class="float-right text-success">Updated</p>
        </div>
        <div v-if="errorMsg.length > 0">
          <p class="float-right text-danger">{{errorMsg}}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'UpdateDesignInfoWidget',
  props: ['designJson'],
  data () {
    return {
      errorMsg: '',
      updatedAt: ''
    }
  },
  computed: {
    desc: {
      // getter
      get: function () {
        return this.designJson.desc
      },
      // setter
      set: function (newValue) {
        var payload = {
          uri: this.$route.params.uri,
          val: newValue
        }
        this.$store.commit('designs/setDesc', payload)
      }
    },
    name: {
      // getter
      get: function () {
        return this.designJson.name
      },
      // setter
      set: function (newValue) {
        var payload = {
          uri: this.$route.params.uri,
          val: newValue
        }
        this.$store.commit('designs/setName', payload)
      }
    }
  },
  methods: {
    _prepareUpdateFormData () {
      let formData = new FormData()
      formData.append('name', this.name)
      formData.append('uri', this.$route.params.uri)
      formData.append('desc', this.desc)
      return formData
    },
    onUpdate () {
      this.errorMsg = ''
      this.$validator.validateAll().then(result => {
        if (!result) {
          // do stuff if not valid.
        } else {
          var formData = this._prepareUpdateFormData()
          var that = this
          axios.post('/api/update',
            formData
          ).then(function (resp) {
            if (resp.data.status === 0) {
              that.updatedAt = new Date(Date.now())
            } else {
              that.errorMsg = resp.data.errors
            }
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
#updateButton {
  border-radius: 0;
  background-color: rgba(0, 0, 0, 0.93);
}
</style>
