<template>
  <div id="app">
    <navigation-bar></navigation-bar>
    <div id="mainWrapper">
      <router-view></router-view>
    </div>
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
  font-family: 'Roboto', 'PT Serif', 'Slabo', 'PT Sans', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
#mainWrapper {
  margin-top: 50px;
}
.card {
  margin: 20px;
  max-width: 800px;
  padding: 1rem;
}
p {
  margin: 0;
}
html {
  font-size: 1rem;
}
@include media-breakpoint-up(sm) {
  html {
    font-size: 1.2rem;
  }
}

@include media-breakpoint-up(md) {
  html {
    font-size: 1.4rem;
  }
}

@include media-breakpoint-up(lg) {
  html {
    font-size: 1.6rem;
  }
}
</style>
