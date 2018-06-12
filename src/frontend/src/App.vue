<template>
  <div id="app">
    <navigation-bar></navigation-bar>
    <router-view></router-view>
  </div>
</template>
<script>
import NavigationBar from './components/NavigationBar'
export default {
  name: 'App',
  components: {
    NavigationBar
  }
}
</script>

<style strict>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.card {
  margin: 20px;
  max-width: 800px;
}
p {
  margin: 0;
}
</style>
