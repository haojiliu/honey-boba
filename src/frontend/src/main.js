// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import VeeValidate from 'vee-validate'
import VueTextareaAutosize from 'vue-textarea-autosize'
import VModal from 'vue-js-modal'
import {VueMasonryPlugin} from 'vue-masonry'

Vue.use(VModal, { dynamic: true })

Vue.use(VueMasonryPlugin)

NProgress.configure({ showSpinner: false })

Vue.use(VeeValidate, {
  events: ''
})

Vue.use(VueTextareaAutosize)

Vue.config.productionTip = false

// eslint-disable-next-line
var vm = new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App></App>'
})
