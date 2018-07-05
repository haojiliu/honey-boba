<template>
  <div>
    <ul ref="reviews" class="list-group list-group-flush">
      <review-item v-bind:key="i" v-for="i in itemsLoaded" v-bind:reviewJson="reviewsJson[i-1]"></review-item>
    </ul>
    <div v-if="displayShowMoreButton" class="row align-items-center">
      <div id="leftHr" class="col">
        <hr align="right">
      </div>
      <div id="midHr" class="col-auto">
        <a v-if="itemsLoaded > 0" @click="loadMore(CONST_PAYLOAD_SIZE)" class="btn btn-link"><small>Show More</small></a>
        <a v-if="itemsLoaded === 0" @click="loadMore(CONST_PAYLOAD_SIZE)" class="btn btn-link"><small>Show Comments</small></a>
      </div>
      <div id="rightHr" class="col justify-content-center">
        <hr align="left">
      </div>
    </div>
  </div>
</template>
<script>
import ReviewItem from './ReviewItem'

export default {
  name: 'ReviewWidget',
  props: ['reviewsJson'],
  components: {
    ReviewItem
  },
  watch: {
    reviewsJson: function (newVal, oldVal) { // watch it
      // Re-render the reviews
      // display show more button again if leave a new review when there's 3 reviews already
      if (this.itemsLoaded === 3) {
        this.displayShowMoreButton = true
      } else if (this.itemsLoaded < 3) {
        this.itemsLoaded += 1
      } else {
        // if more than 3 reviews showing and show more button is there
        if (this.displayShowMoreButton) {
          // do nothing
        } else {
          // if showmore button is not there we are showing all reviews
          this.itemsLoaded += 1
        }
      }
    }
  },
  data () {
    return {
      itemsLoaded: 0,
      CONST_PAYLOAD_SIZE: 5,
      displayShowMoreButton: true
    }
  },
  methods: {
    loadMore (size) {
      if (size === -1) {
        // initial load all if /uploaded page
        this.itemsLoaded = this.reviewsJson.length
      } else if (this.itemsLoaded + size >= this.reviewsJson.length) {
        // make sure this.itemsLoaded is always smaller than reviewsJson size
        this.itemsLoaded = this.reviewsJson.length
      } else {
        this.itemsLoaded += size
      }
      // Hide the show more button
      if (this.itemsLoaded === this.reviewsJson.length) {
        this.displayShowMoreButton = false
      }
    }
  },
  mounted () {
    if (this.$route.params.uri) {
      // Initially load all reviews on /uploaded page
      this.loadMore(-1)
    } else {
      // Initially load 3 reviews on /designs page
      this.loadMore(3)
    }
  }
}
</script>
<style strict>
a.btn.btn-link {
  padding: 0;
}
small {
  font-size: 15px;
}
#leftHr {
  padding-right: 0px;
}
#rightHr {
  padding-left: 0px;
}
.list-group-item:last-child {
  border-bottom: 0;
}
</style>
