import { createStore } from "vuex"

export default createStore({
	state() {
		return {
			user: null
		}
	},

	mutations: {
		set_user(state, user) {
			state.user = user
		}
	},

	getters: {
		get_user(state) {
			return state.user
		}
	}
})