<template>

	<footer class="container-fluid">

		<div style="padding: 15px; background-color: cadetblue;
			margin-top: 50px;">
			<p class="text-center" style="margin-bottom: 0px; color: white;">
				For customizations contact:
				<b class="highlight">support@adnan-tech.com</b>
				Or
				WhatsApp: <b class="highlight">+92 310 5461304</b>
			</p>
		</div>

		<!-- <div style="background-color: #e9e9e9; padding: 25px;">
			<p class="text-center" style="margin-bottom: 0px;">
				&copy;<span v-text="year"></span>&nbsp;
				adnan-tech.com
			</p>
		</div> -->

	</footer>
</template>

<script>

	export default {
		name: "AppFooter",

		data() {
			return {
				year: new Date().getFullYear()
			}
		}
	}
</script>

<style scoped>
	.container-fluid {
		padding-left: 0px;
		padding-right: 0px;
	}
	
	footer {
		position: fixed;
		bottom: 0px;
	}

	.highlight {
		background-color: white;
	    color: cadetblue;
	    padding-left: 5px;
	    padding-right: 5px;
	    border-radius: 5px;
	}
</style>