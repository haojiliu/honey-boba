import api from '../../api/main'

// initial state
const state = {
  all: [],
  isFetched: false
}

// getters
const getters = {
  getDesignByUri: (state) => (uri) => {
    return state.all.find(design => design.uri === uri)
  }
}

// actions
const actions = {
  initAllDesigns ({ commit }) {
    api.getDesigns(designs => {
      commit('setDesigns', designs)
    })
  },
  refreshOneReview ({ commit }, uri) {
    api.refreshOneReview(reviews => {
      commit('setOneReview', {reviews, uri})
    }, uri)
  },
  getOneDesign ({ commit }, uri) {
    api.getOneDesign(design => {
      commit('setOneDesign', design)
    }, uri)
  }
}

// mutations
const mutations = {
  setDesigns (state, designs) {
    state.all = designs
    state.isFetched = true
  },
  setOneDesign (state, design) {
    state.all.push(design)
  },
  setOneReview (state, dataObj) {
    const design = state.all.find(design => design.uri === dataObj.uri)
    design.reviews = dataObj.reviews
    console.log(state.all)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
