<template>
  <div class="oneDesign card card-body mx-auto d-block">
    <design-item v-bind:designJson="designJson" @designReported="onReported"></design-item>
    <review-widget :ref="'review-'+designJson.uri" v-bind:uri="designJson.uri" v-bind:reviewsJson="designJson.reviews"></review-widget>
    <new-review v-bind:uri="designJson.uri"></new-review>
  </div>
</template>
<script>
/* eslint-disable */
import ReviewWidget from './ReviewWidget'
import NewReview from './NewReview'
import DesignItem from './DesignItem'

export default {
  props: ['designJson'],
  components: {
    ReviewWidget,
    NewReview,
    DesignItem
  },
  methods: {
    onReported () {
      this.$emit('close')
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
