<template>
    <h2 style="margin-bottom: 30px;">
    	<img v-bind:src="profileImage" style="width: 100px; height: 100px;
    		object-fit: cover; border-radius: 50%; margin-right: 10px;" />
    	My profile
    </h2>

    <form method="POST" v-on:submit.prevent="doSave" v-if="user != null" enctype="multipart/form-data">
        <div class="form-group">
            <label>Your name</label>
            <input type="text" class="form-control" name="name" v-model="user.name" required />
        </div>

        <br />

        <div class="form-group">
            <label>Profile image</label>
            <input type="file" class="form-control" name="profile_image" v-on:change="onProfileSelected" />
        </div>

        <input type="submit" v-bind:value="isLoading ? 'Loading...' : 'Save'" v-bind:disabled="isLoading"
        	name="submit" class="btn btn-success"
        	style="margin-top: 20px;" />
    </form>
</template>

<script>

	import axios from "axios"
	import swal from "sweetalert2"
	import store from "../store"

	export default {
		name: "MyProfileViewComponent",

		computed: {
			user() {
				return store.getters.getUser
			}
		},

		data() {
			return {
				isLoading: false,
				profileImage: ""
			}
		},

		methods: {
			async doSave() {
				const form = event.target
                const formData = new FormData(form)

                this.isLoading = true

                try {
                    const response = await axios.post(
                        this.$apiURL + "/save-profile",
                        formData,
                        this.$headers
                    )

                    if (response.data.status == "success") {
                    	swal.fire("Profile updated", response.data.message, "success")
                    	this.user.profile_image = response.data.file_location
                    } else {
                        swal.fire("Error", response.data.message, "error")
                    }
                } catch (exp) {
                    console.log(exp)
                } finally {
                    this.isLoading = false
                }
			},

			onProfileSelected() {
				const self = this
				const files = event.target.files

				if (files.length > 0) {
					var fileReader = new FileReader()
 
		            fileReader.onload = function (event) {
		            	self.profileImage = event.target.result
		            }
		 
		            fileReader.readAsDataURL(files[0])
				}
			}
		},

		mounted() {
			if (this.user != null) {
				this.profileImage = this.user.profile_image
			}
		},

		watch: {
			user (to, from) {
				if (to != null) {
					this.profileImage = this.user.profile_image
				}
			}
		}
	}
</script>