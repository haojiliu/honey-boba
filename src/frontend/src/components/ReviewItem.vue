<template>
  <li class="list-group-item">
    <p class="text-left">{{reviewJson.body}}</p>
    <small class="text-right text-muted">{{reviewJson.timestamp}}</small>
  </li>
</template>
<script>
export default {
  name: 'ReviewItem',
  props: ['reviewJson']
}
</script>
<style strict>
.list-group-item {
  padding-bottom: 0;
}
</style>
