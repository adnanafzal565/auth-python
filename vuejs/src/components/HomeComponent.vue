<template>
	<div class="container">
		<div class="row">
			<div class="col-md-12">
				
			</div>
		</div>
	</div>
</template>

<script>
	
	import axios from "axios"
	import swal from "sweetalert2"

	export default {
		name: "HomeComponent",

		data() {
			return {
				data: []
			}
		},

		methods: {
			async getData() {
				const formData = new FormData()
				formData.append("timezone", Intl.DateTimeFormat().resolvedOptions().timeZone)

				try {
					const response = await axios.post(
						this.$api_url + "/fetch-data",
						formData,
						this.$headers
					)

					if (response.data.status == "success") {
						this.data = response.data.data
					}
				} catch (exp) {
					// if (exp?.response?.statusText) {
					// 	swal.fire("Error", exp.response.statusText, "error")
					// }
				}
			}
		},

		mounted() {
			this.getData()
		}
	}
</script>