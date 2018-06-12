<template>
  <nav class="navbar navbar-expand-sm navbar-dark bg-dark">
    <router-link class="navbar-brand" to="/"><img src="/static/yoshi.gif" width="40" alt="">Honey Boba</router-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav ml-auto navbar-right">
        <li class="nav-item active">
          <router-link class="nav-link" to="/upload">Upload</router-link>
        </li>
        <li class="nav-item active">
          <router-link class="nav-link" to="/designs">Designs</router-link>
        </li>
        <li class="nav-item active">
          <router-link class="nav-link" to="/uploaded/2c004ba7-b7c2-4db5-891c-c98c34a5acaa">Uploaded_1</router-link>
        </li>
        <li class="nav-item active">
          <router-link class="nav-link" to="/uploaded/a054b110-d915-4f00-ba4b-2f87407e5919">Uploaded_2</router-link>
        </li>
        <li class="nav-item active">
          <router-link class="nav-link" to="/faq">FAQ</router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>
