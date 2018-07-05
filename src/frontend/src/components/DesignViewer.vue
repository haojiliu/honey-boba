<template>
  <div v-if="this.$store.state.designs.isFetched" class="container-fluid" style="">
    <div v-if="this.$store.state.designs.isMasonry">
      <masonry-view v-bind:designsJson="designsJson"></masonry-view>
    </div>
    <div v-else class="oneDesign card card-body mx-auto d-block" v-bind:key="designJson.uri" v-for="designJson in designsJson">
      <design-item v-bind:designJson="designJson"></design-item>
      <review-widget :ref="'review-'+designJson.uri" v-bind:uri="designJson.uri" v-bind:reviewsJson="designJson.reviews"></review-widget>
      <new-review v-bind:uri="designJson.uri" @newReviewPosted="onNewReviewPosted"></new-review>
    </div>
  </div>
</template>
<script>
/* eslint-disable */
import ReviewWidget from './ReviewWidget'
import NewReview from './NewReview'
import DesignItem from './DesignItem'
import MasonryView from './MasonryView'

export default {
  components: {
    ReviewWidget,
    NewReview,
    DesignItem,
    MasonryView
  },
  methods: {
    onNewReviewPosted (uri) {
      // scroll page to the new review
      var reviewEl = this.$refs['review-'+uri][0]
      // not supported on safari
      // reviewEl.$el.scrollIntoView({
      //   behavior: 'smooth',
      //   block: 'center',
      //   inline: 'nearest'
      // });
      // not supported on firefox
      reviewEl.$el.scrollIntoViewIfNeeded()
    },
  },
  computed: {
    designsJson () {
      return this.$store.state.designs.all
    }
  },
  beforeCreate () {
  },
  created () {
    if (!this.$store.state.designs.isFetched) {
      this.$store.dispatch('designs/initAllDesigns')
    } else {
    }
  }
}
</script>
<style>
.oneDesign {
  border: 0;
  padding-top: 0;
  padding-bottom: 0;
}
</style>
