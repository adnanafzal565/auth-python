import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from "vue-router"

import HomeComponent from "./components/HomeComponent.vue"
import SignupComponent from "./components/SignupComponent.vue"
import LoginComponent from "./components/LoginComponent.vue"

const app = createApp(App)
app.config.globalProperties.$api_url = "http://127.0.0.1:8000"
app.config.globalProperties.$access_token_key = "access_token"
app.config.globalProperties.$headers = {
	headers: {
		"Authorization": "Bearer " + localStorage.getItem("access_token")		
	}
}

const routes = [
	{ path: "/login", component: LoginComponent },
	{ path: "/signup", component: SignupComponent },
	{ path: "/", component: HomeComponent }
]

const router = createRouter({
	history: createWebHistory(),
	routes
})

app.use(router)
app.mount('#app')
