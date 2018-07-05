<template>
<div>
  <modals-container/>
  <div v-masonry transition-duration="0.3s" item-selector=".grid-item" column-width=".grid-sizer" percentPosition="true">
    <div class="grid-sizer"></div>
    <div v-masonry-tile class="grid-item" v-bind:key="designJson.uri" v-for="designJson in designsJson">
      <div class="imgWrapper">
        <img :id="'masonryImg-'+designJson.uri" @click="onClickImg(designJson)" class="card-img-top" v-bind:src="designJson.thumbnail_uri">
      </div>
    </div>
  </div>
</div>
</template>
<script>
import DesignItemModal from './DesignItemModal.vue'

export default {
  components: {DesignItemModal},
  props: ['designsJson'],
  watch: {
    designsJson: function (newVal, oldVal) { // watch it
      // Re-render the reviews
    }
  },
  methods: {
    onClickImg (designJson) {
      var widthVal = '45%'
      // var img = document.getElementById('masonryImg-'+designJson.uri).naturalWidth
      // console.log(img)
      // console.log($(img))
      // console.log($(img).naturalWidth)
      // if (img.naturalWidth > img.naturalHeight) {
      //   widthVal = '65%'
      // }

      this.$modal.show(DesignItemModal, {
        designJson: designJson
      }, {
        draggable: false,
        width: widthVal,
        height: 'auto',
        scrollable: true,
        pivotY: 0.5
      })
    }
  }
}
</script>
<style strict>
.grid-sizer,
.grid-item { width: 20%; }
/* 2 columns */
.grid-item--width2 { width: 40%; }
.imgWrapper {
  padding: 5px;
}
.v--modal-box {
  margin-top: 10px;
}
#modals-container {
  position: relative;
  z-index: 1031;
}
</style>
