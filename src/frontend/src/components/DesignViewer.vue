<template>
  <div v-if="this.$store.state.designs.isFetched" class="container-fluid" style="">
    <div class="oneDesign card card-body mx-auto d-block" v-bind:key="designJson.uri" v-for="designJson in designsJson">
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

export default {
  components: {
    ReviewWidget,
    NewReview,
    DesignItem
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
  beforeRouteEnter (to, from, next) {
    // called before the route that renders this component is confirmed.
    // does NOT have access to `this` component instance,
    // because it has not been created yet when this guard is called!
    console.log('before route enters design viewer!!')
    next(vm => {
      console.log(vm.$store.state.designs.isFetched)
    })
  },
  computed: {
    designsJson () {
      return this.$store.state.designs.all
    }
  },
  beforeCreate () {
    console.log('before creating design viewer component')
  },
  created () {
    console.log('design viewer created')
    if (!this.$store.state.designs.isFetched) {
      this.$store.dispatch('designs/initAllDesigns')
    } else {
      console.log('already fetched, not making api call to flask')
    }
  },
  beforeMount () {
    console.log('before mount...')
  },
  mounted () {
    console.log('design viewer mounted')
  },
  destroyed () {
    console.log('design viewer destroyed')
  },
  beforeDestroy () {
    console.log('design viewer about to be destroyed')
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
