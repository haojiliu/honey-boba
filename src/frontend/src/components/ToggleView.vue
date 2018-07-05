<template>
  <div>
    <toggle-button
      @change="onChangeView"
      :labels="{checked: '', unchecked: ''}"
      switchColor="black"
      :color="{checked: 'rgb(255, 249, 239)', unchecked: 'rgb(255, 249, 239)'}"
      width=35
      height=24
    />
    <span id="toggleViewText">switch view</span>
  </div>
</template>
<script>
import ToggleButton from 'vue-js-toggle-button/src/Button'
export default {
  components: {
    ToggleButton
  },
  methods: {
    onChangeView (e) {
      this.$store.commit('designs/toggleIsMasonry', e.value)
    }
  }
}
</script>
<style strict>
#toggleViewText {
  color: rgb(255, 249, 239);
  font-size: 14px;
}
.vue-js-switch {
  margin: 0;
}
</style>
