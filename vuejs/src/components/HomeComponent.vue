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
				//
			}
		},

		mounted() {
			this.getData()
		}
	}
</script>