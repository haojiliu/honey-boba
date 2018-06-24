<template>
  <nav class="navbar navbar-expand-sm navbar-dark bg-dark">
    <router-link class="navbar-brand" to="/"><img class="align-middle" src="/static/logo.png" width="30" alt="">
      <span class="align-middle navBrand">Honey Boba</span>
    </router-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav ml-auto navbar-right">
        <li class="nav-item active">
          <router-link class="nav-link" to="/upload" style="font-family: 'PT Sans'"><span class="align-middle navItem">Upload</span></router-link>
        </li>
        <li class="nav-item active">
          <router-link class="nav-link" to="/designs" style="font-family:'Fugaz One'"><span class="align-middle navItem">Designs</span></router-link>
        </li>
        <!-- <li class="nav-item active">
          <router-link class="nav-link" to="/uploaded/2c004ba7-b7c2-4db5-891c-c98c34a5acaa">Uploaded_1</router-link>
        </li>
        <li class="nav-item active">
          <router-link class="nav-link" to="/uploaded/a054b110-d915-4f00-ba4b-2f87407e5919">Uploaded_2</router-link>
        </li> -->
        <li class="nav-item active">
          <router-link class="nav-link" to="/faq" style="font-family:Arial"><span class="align-middle navItem">About</span></router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>
<style strict>
.navBrand {
  font-size: 28px;
  font-family: 'Anton';
}
.navbar-brand {
  padding: 0;
}
.navbar {
  padding: 0;
  padding-left: 0.5rem;
  padding-right: 2rem;
}
</style>
