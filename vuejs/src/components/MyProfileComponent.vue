<template>
	<div class="container">
		<div class="row">
			<div class="col-md-4">
				<ul class="list-group">
					<li v-bind:class="'list-group-item ' + (page == 'profile' ? 'active' : '')">
						<a href="javascript:void(0)" v-on:click="gotoComponent('profile')">My profile</a>	
					</li>

					<li v-bind:class="'list-group-item ' + (page == 'change-password' ? 'active' : '')">
						<a href="javascript:void(0)" v-on:click="gotoComponent('change-password')">Change password</a>
					</li>
				</ul>
			</div>

			<div class="col-md-8">
				<MyProfileViewComponent v-if="page == 'profile'" />
				<ChangePasswordComponent v-if="page == 'change-password'" />
			</div>
		</div>
	</div>
</template>

<script>

	import MyProfileViewComponent from "./MyProfileViewComponent.vue"
	import ChangePasswordComponent from "./ChangePasswordComponent.vue"

	export default {
		name: "MyProfileComponent",

		components: {
			MyProfileViewComponent,
			ChangePasswordComponent
		},

		data() {
			return {
				page: "profile"
			}
		},

		methods: {
			gotoComponent(component) {
				this.page = component
				this.addOrUpdateURLParam("page", component)
			}
		}
	}
</script>

<style scoped>
	.list-group-item.active a {
		color: white;
	}
	.list-group-item a {
		color: initial;
		text-decoration: none;
	}
</style>