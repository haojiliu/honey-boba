import api from '../../api/main'

// initial state
const state = {
  all: [],
  isFetched: false,
  isMasonry: false
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
  toggleIsMasonry (state, isMasonry) {
    state.isMasonry = isMasonry
  },
  touchThumbnail (state, uri) {
    const design = state.all.find(design => design.uri === uri)
    design.thumbnail_uri += '?' + new Date().getTime()
  },
  setDesigns (state, designs) {
    state.all = designs
    state.isFetched = true
  },
  setOneDesign (state, design) {
    state.all.unshift(design)
  },
  deleteOneDesign (state, design) {
    var index = state.all.indexOf(design)
    if (index > -1) {
      state.all.splice(index, 1)
    }
  },
  setOneReview (state, dataObj) {
    const design = state.all.find(design => design.uri === dataObj.uri)
    design.reviews = dataObj.reviews
  },
  setDesc (state, payload) {
    const design = state.all.find(design => design.uri === payload.uri)
    design.desc = payload.val
  },
  setIsDeleted (state, payload) {
    const design = state.all.find(design => design.uri === payload.uri)
    design.is_deleted = payload.val
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
