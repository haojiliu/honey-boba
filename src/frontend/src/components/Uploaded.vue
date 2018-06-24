<template>
  <div class="container-fluid">
    <div v-if="this.designJson" class="row">
      <div class="col-6">
        <div class="oneDesign card card-body mx-auto d-block">
          <design-item v-bind:designJson="designJson"></design-item>
          <review-widget v-bind:reviewsJson="designJson.reviews"></review-widget>
        </div>
      </div>
      <div class="col-6">
        <email-confirmation v-bind:designJson="designJson" @emailConfirmed="onEmailConfirmed"></email-confirmation>
        <div v-if="this.isFileUpdated || this.$route.params.slug" class="card card-body mx-auto d-block">
          <div class="row d-flex align-items-top">
            <div class="col-12">
              <p v-if="this.isFileUpdated" class="lead"><strong><em>Your file was updated</em></strong></p>
              <p v-if="!this.isFileUpdated && this.$route.params.slug" class="lead"><strong><em>Woohoo! You uploaded a design!</em></strong></p>
              <!-- <p v-if="!this.isFileUpdated && !this.$route.params.slug" class="lead"><strong><em>STOP! Make sure this is your design before making any changes</em></strong></p> -->
            </div>
          </div>
        </div>
        <design-uploader v-bind:designJson="designJson" @fileUpdated="onFileUpdated"></design-uploader>
        <update-design-info-widget v-bind:designJson="designJson"></update-design-info-widget>
        <delete-design-widget v-bind:designJson="designJson"></delete-design-widget>
      </div>
    </div>
    <div v-else></div>
  </div>
</template>
<script>
import ReviewWidget from './ReviewWidget'
import DesignUploader from './DesignUploader'
import DesignItem from './DesignItem'
import EmailConfirmation from './EmailConfirmation'
import UpdateDesignInfoWidget from './UpdateDesignInfoWidget'
import DeleteDesignWidget from './DeleteDesignWidget'

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
      console.log('inside uploaded val changed!!')
    }
  },
  components: {
    ReviewWidget,
    DesignUploader,
    DesignItem,
    EmailConfirmation,
    UpdateDesignInfoWidget,
    DeleteDesignWidget
  },
  data () {
    return {
      isFileUpdated: false,
      isEmailConfirmed: false
    }
  },
  computed: {
    designJson () {
      return this.$store.getters['designs/getDesignByUri'](this.$route.params.uri)
    }
  },
  methods: {
    onEmailConfirmed () {
      this.isEmailConfirmed = true
    },
    onFileUpdated () {
      // disable the cache on the image
      this.$store.commit('designs/touchThumbnail', this.designJson.uri)
      this.isFileUpdated = true
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
<style strict>
.oneDesign {
  border: 0;
  padding-top: 0;
}
#deleteButton {
  border-radius: 0;
}
</style>
