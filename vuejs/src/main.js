import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from "vue-router"

import HomeComponent from "./components/HomeComponent.vue"
import SignupComponent from "./components/SignupComponent.vue"
import LoginComponent from "./components/LoginComponent.vue"
import MyProfileComponent from "./components/MyProfileComponent.vue"

const app = createApp(App)
app.config.globalProperties.$apiURL = "http://127.0.0.1:8000"
app.config.globalProperties.$accessTokenKey = "accessToken"
app.config.globalProperties.$headers = {
	headers: {
		"Authorization": "Bearer " + localStorage.getItem("accessToken")		
	}
}

const routes = [
	{ path: "/my-profile", component: MyProfileComponent },
	{ path: "/login", component: LoginComponent },
	{ path: "/signup", component: SignupComponent },
	{ path: "/", component: HomeComponent }
]

const router = createRouter({
	history: createWebHistory(),
	routes
})

app.use(router)

app.mixin({
	methods: {
		addOrUpdateURLParam (key, value) {
		    const searchParams = new URLSearchParams(window.location.search)
		    searchParams.set(key, value)
		    const newRelativePathQuery = window.location.pathname + "?" + searchParams.toString()
		    history.pushState(null, "", newRelativePathQuery)
		}
	}
})

app.mount('#app')
