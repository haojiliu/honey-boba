<template>
  <div>
    <div class="card card-body mx-auto d-block" v-bind:key="designJson.uri" v-for="designJson in designsJson">
      <img class="card-img-top" v-bind:src="designJson.thumbnail_uri">
      <p class="text-muted text-right">Last updated at {{designJson.updated_at_utc}}</p>
      <review-widget v-bind:reviewsJson="designJson.reviews"></review-widget>
      <new-review v-bind:uri="designJson.uri"></new-review>
    </div>
  </div>
</template>
<script>
/* eslint-disable */
import ReviewWidget from './ReviewWidget'
import NewReview from './NewReview'

export default {
  components: {
    ReviewWidget,
    NewReview
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
