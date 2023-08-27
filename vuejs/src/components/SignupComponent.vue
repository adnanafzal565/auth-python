<template>
    <div class="container" style="margin-top: 50px;">
        <div class="row">
            <div class="offset-md-3 col-md-6">

                <h2 style="margin-bottom: 30px; text-align: center;">Sign up</h2>

                <form method="POST" v-on:submit.prevent="signup">
                    <div class="form-group">
                        <label>Enter name</label>
                        <input type="text" class="form-control" name="name" required />
                    </div>

                    <br />

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

                    <input type="submit" v-bind:value="isLoading ? 'Loading...' : 'Register'" v-bind:disabled="isLoading" name="submit" class="btn btn-primary" />
                </form>
            </div>
        </div>
    </div>
</template>

<script>

    import axios from "axios"
    import swal from "sweetalert2"

    export default {
        name: "SignupComponent",

        data() {
            return {
                isLoading: false
            }
        },

        methods: {
            signup: async function () {
                const form = event.target;
                const formData = new FormData(form);

                this.isLoading = true;

                try {
                    const response = await axios.post(
                        this.$api_url + "/signup",
                        formData
                    );
                    
                    swal.fire("Signup", response.data.message, response.data.status)

                    if (response.data.status == "success") {
                        form.reset()

                        this.$router.push("/login")
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