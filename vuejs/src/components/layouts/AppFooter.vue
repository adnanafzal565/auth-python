<template>
	<footer class="container-fluid" style="margin-top: 50px; background-color: #e9e9e9; padding: 25px;">
		<p class="text-center" style="margin-bottom: 0px;">
			&copy;<span v-text="year"></span>&nbsp;
			adnan-tech.com
		</p>
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