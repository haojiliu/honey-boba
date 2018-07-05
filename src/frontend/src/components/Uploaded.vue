<template>
  <div class="container-fluid">
    <div v-if="this.designJson" class="row">
      <div class="col-md-6">
        <div class="oneDesign card card-body mx-auto d-block">
          <design-item v-bind:designJson="designJson"></design-item>
          <review-widget v-bind:reviewsJson="designJson.reviews"></review-widget>
        </div>
      </div>
      <div class="col-md-6 hidden-sm">
        <div v-if="!this.isFileUpdated && this.$route.params.slug" class="alertCard card card-body mx-auto d-block">
          <div class="row d-flex align-items-top">
            <div class="col-12">
              <!-- <p v-if="this.isFileUpdated" class="lead"><strong>Your file was updated</strong></p> -->
              <p v-if="!this.isFileUpdated && this.$route.params.slug" class="" style="font-family:'Encode Sans Condensed'">Congratulations! Make sure to save this link for future reference. An email will be sent to you shortly.</p>
              <!-- <p v-if="!this.isFileUpdated && !this.$route.params.slug" class="lead"><strong><em>STOP! Make sure this is your design before making any changes</em></strong></p> -->
            </div>
          </div>
        </div>
        <email-confirmation v-bind:designJson="designJson" @emailConfirmed="onEmailConfirmed"></email-confirmation>
        <div v-if="this.isEmailConfirmed">
          <div v-if="!this.isDeleted">
            <design-uploader v-bind:designJson="designJson" @fileUpdated="onFileUpdated"></design-uploader>
            <update-design-info-widget v-bind:designJson="designJson"></update-design-info-widget>
          </div>
          <delete-design-widget v-bind:designJson="designJson"></delete-design-widget>
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
import EmailConfirmation from './EmailConfirmation'
import UpdateDesignInfoWidget from './UpdateDesignInfoWidget'
import DeleteDesignWidget from './DeleteDesignWidget'

export default {
  name: 'Uploaded',
  watch: {
    '$route' (to, from) {
      // react to route changes...
      this.tryGetDesign(to.params.uri)
    },
    designJson: function (newVal, oldVal) { // watch it
      // Re-render the reviews
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
    },
    isDeleted () {
      return this.designJson.is_deleted
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
  },
  mounted () {
  },
  destroyed () {
  },
  beforeDestroy () {
  }
}
</script>
<style strict>
.oneDesign {
  border: 0;
  padding-top: 0;
  padding-bottom: 0;
}
#deleteButton {
  border-radius: 0;
}
.alertCard {
  border-top: 0;
  border-bottom: 0;
  border-right: 0;
  border-radius: 0;
}
</style>
