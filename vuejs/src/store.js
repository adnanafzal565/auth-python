import { createStore } from "vuex"

export default createStore({
	state() {
		return {
			user: null
		}
	},

	mutations: {
		setUser(state, user) {
			state.user = user
		}
	},

	getters: {
		getUser(state) {
			return state.user
		}
	}
})