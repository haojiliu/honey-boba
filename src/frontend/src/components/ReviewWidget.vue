<template>
  <div>
    <div class="reviews">
      <!-- <h5>Oops, no review so far</h5> -->
      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-bind:key="reviewJson.timestamp" v-for="reviewJson in reviewsJson">
          <p class="text-left">{{reviewJson.body}}</p>
          <small class="text-right text-muted">{{reviewJson.timestamp}}</small>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReviewWidget',
  props: ['reviewsJson']
}
</script>
