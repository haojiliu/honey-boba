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
  }
}

// mutations
const mutations = {
  setDesigns (state, designs) {
    console.log('going to set designs')
    state.all = designs
    state.isFetched = true
  },

  updateDesign (state, uri, designInfo) {
    const design = state.all.find(product => design.uri === uri)
    console.log('going to update design ' + design.uri)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
