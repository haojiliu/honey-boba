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
      // Everytime one single design is requested, force refresh the thumbnail image
      commit('touchThumbnail', design.uri)
    }, uri)
  }
}

// mutations
const mutations = {
  touchThumbnail (state, uri) {
    console.log('touching thumbnail ...')
    const design = state.all.find(design => design.uri === uri)
    console.log(design)
    design.thumbnail_uri += '?' + new Date().getTime()
    console.log(design.thumbnail_uri)
  },
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
  },
  setDesc (state, payload) {
    const design = state.all.find(design => design.uri === payload.uri)
    design.desc = payload.val
  },
  setName (state, payload) {
    const design = state.all.find(design => design.uri === payload.uri)
    design.name = payload.val
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
