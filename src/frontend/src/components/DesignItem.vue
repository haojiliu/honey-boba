<template>
  <div class="">
    <img class="card-img-top" v-bind:src="designJson.thumbnail_uri">
    <div class="row">
      <div class="col-12 text-right">
        <a v-if="!isReported && !this.$route.params.uri"  @click="onReport" class="btn"><small class="text-muted">Report This</small></a>
        <small v-if="isReported && !this.$route.params.uri" class="text-success">Reported</small>
      </div>
      <div id="designDescContainer" class="col-12 text-center">
        <p id="designDescText" v-if="designJson.desc">{{designJson.desc}}</p>
        <!-- <small class="text-muted">Last updated: {{designJson.updated_at_utc}}</small> -->
      </div>

    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'DesignItem',
  props: ['designJson'],
  watch: {
    designJson: function (newVal, oldVal) { // watch it
      // Re-render the reviews
    }
  },
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
      if (confirm('You are going to report an inappropriate design')) {
        var that = this
        var formData = this._prepareFormData()
        axios.post('/api/report',
          formData
        ).then(function (resp) {
          that.isReported = true
          that.$emit('designReported')
          that.$store.commit('designs/deleteOneDesign', that.designJson)
        }).catch(function (resp) {
          console.log('FAILURE!!')
        })
      } else {
        // Do nothing!
      }
    }
  }
}
</script>
<style strict>
a.btn {
  padding: 0;
}
#designDescContainer {
  padding-left: 25px;
  padding-right: 25px;
}
#designDescText {
  font-family: "Encode Sans Condensed";
  background-color: rgba(255, 253, 248, 0.67);
}
</style>
