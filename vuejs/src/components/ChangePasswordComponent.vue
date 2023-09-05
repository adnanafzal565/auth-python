<template>
	<h2 style="margin-bottom: 30px;">
    	Change password
    </h2>

    <form method="POST" v-on:submit.prevent="changePassword">

    	<div class="row">
    		<div class="col-md-5">
    			<div class="form-group">
		            <label>Current password</label>
		            <input type="password" class="form-control" name="password" required />
		        </div>

		        <br />

		        <div class="form-group">
		            <label>New password</label>
		            <input type="password" class="form-control" name="new_password" required />
		        </div>

		        <br />

		        <div class="form-group">
		            <label>Confirm password</label>
		            <input type="password" class="form-control" name="confirm_password" required />
		        </div>

		        <br />

		        <input type="submit" v-bind:value="isLoading ? 'Loading...' : 'Change'" v-bind:disabled="isLoading"
		        	name="submit" class="btn btn-success" />
    		</div>
    	</div>
    </form>
</template>

<script>

	import axios from "axios"
	import swal from "sweetalert2"

	export default {
		name: "ChangePasswordComponent",

		data() {
			return {
				isLoading: false
			}
		},

		methods: {
			async changePassword() {
				const form = event.target
                const formData = new FormData(form)

                this.isLoading = true

                try {
                    const response = await axios.post(
                        this.$apiURL + "/change-password",
                        formData,
                        this.$headers
                    )

                    if (response.data.status == "success") {
                    	swal.fire("Password updated", response.data.message, "success")
                    	form.reset()
                    } else {
                        swal.fire("Error", response.data.message, "error")
                    }
                } catch (exp) {
                    console.log(exp)
                } finally {
                    this.isLoading = false
                }
			}
		}
	}
</script>