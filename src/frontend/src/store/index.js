import Vue from 'vue'
import Vuex from 'vuex'
import designs from './modules/designs'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  modules: {
    designs
  },
  strict: debug
})
