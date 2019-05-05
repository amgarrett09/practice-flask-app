export const state = () => ({
  loggedInUser: null,
  authToken: ''
})

export const mutations = {
  SET_TOKEN(state, token) {
    state.authToken = token
  },
  SET_USER(state, username) {
    state.loggedInUser = username
  }
}

export const actions = {
  login({ commit }, payload) {
    commit('SET_TOKEN', payload.token)
    commit('SET_USER', payload.username)
  }
}
