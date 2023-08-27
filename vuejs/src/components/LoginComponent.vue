<template>
    <div class="container" style="margin-top: 50px;">
        <div class="row">
            <div class="offset-md-3 col-md-6">

                <h2 style="margin-bottom: 30px; text-align: center;">Login</h2>

                <form method="POST" v-on:submit.prevent="login">

                    <div class="form-group">
                        <label>Enter email</label>
                        <input type="email" class="form-control" name="email" required />
                    </div>

                    <br />

                    <div class="form-group">
                        <label>Enter password</label>
                        <input type="password" class="form-control" name="password" required />
                    </div>

                    <br />

                    <input type="submit" v-bind:value="isLoading ? 'Loading...' : 'Login'" v-bind:disabled="isLoading" name="submit" class="btn btn-primary" />
                </form>
            </div>
        </div>
    </div>
</template>

<script>

    import axios from "axios"
    import swal from "sweetalert2"
    import store from "../store"

    export default {
        name: "LoginComponent",

        data() {
            return {
                isLoading: false
            }
        },

        methods: {
            login: async function () {
                const form = event.target;
                const formData = new FormData(form);

                this.isLoading = true;

                try {
                    const response = await axios.post(
                        this.$api_url + "/login",
                        formData
                    )

                    if (response.data.status == "success") {
                        // get access token from server
                        const access_token = response.data.access_token

                        // save in local storage
                        localStorage.setItem(this.$access_token_key, access_token)

                        store.commit("set_user", response.data.user)
                        form.reset()

                        this.$headers.headers.Authorization = "Bearer " + localStorage.getItem(this.$access_token_key)

                        // to go to home page without refreshing
                        this.$router.push("/")
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