<template>
  <nav class="navbar fixed-top navbar-expand-sm navbar-dark bg-dark">
    <router-link class="navbar-brand" to="/">
      <!-- <img class="align-middle" src="https://s3.amazonaws.com/haoji/design-review/static/logo.png" width="30" alt=""> -->
      <span class="align-middle navBrand">AnonBeta</span>
    </router-link>
    <!-- <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button> -->
    <toggle-view v-if="this.$route.fullPath === '/' || this.$route.fullPath === '/designs'"></toggle-view>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav ml-auto navbar-right">
        <li class="nav-item active">
          <router-link class="nav-link" to="/upload"><span class="align-middle navItem">Upload</span></router-link>
        </li>
        <li class="nav-item active">
          <router-link class="nav-link" to="/designs"><span class="align-middle navItem">Designs</span></router-link>
        </li>
        <!-- <li class="nav-item active">
          <router-link class="nav-link" to="/uploaded/2c004ba7-b7c2-4db5-891c-c98c34a5acaa">Uploaded_1</router-link>
        </li>
        <li class="nav-item active">
          <router-link class="nav-link" to="/uploaded/a054b110-d915-4f00-ba4b-2f87407e5919">Uploaded_2</router-link>
        </li> -->
        <li class="nav-item active">
          <router-link class="nav-link" to="/faq"><span class="align-middle navItem">About</span></router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>
<script>
import ToggleView from './ToggleView'
export default {
  components: {
    ToggleView
  }
}
</script>
<style strict>
nav {
  /* z-index: 10; */
}
.collapse.in {
  display: block;
}
.navBrand {
  font-size: 28px;
  font-family: 'Encode Sans Condensed';
  font-weight: 800;
  color: rgb(255, 249, 239);
}
.navbar-brand {
  padding: 0;
}
a.nav-link {
  padding: 0;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  font-size: 16px;
}
.navbar {
  padding: 0;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  padding-top: 0.1rem;
  padding-bottom: 0.1rem;
  background-color: rgba(0, 0, 0, 0.93) !important;
}
#titleText {
  color: rgba(0, 0, 0, 0.79);
}
</style>
