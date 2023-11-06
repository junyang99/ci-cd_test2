<template>
    <v-app>
        <v-container>
            <div id="app">
                <div style="padding-top: 75px; padding-bottom: 50px;">
                <div class="container ms-auto d-flex flex-column align-items-center">
                    <img id="login-icon" src="../assets/logo.svg">
                </div>

                <form class="container ms-auto login-input" @submit.prevent="handleFormSubmit">
                    <div class="mb-3">
                        <label for="exampleInputEmail1" class="form-label">Enter Username:</label>
                        <input v-model="userInput" type="text" class="form-control" id="exampleInputEmail1" placeholder="Enter your username">
                    </div>

                    <div>
                        <p> Current userInput: {{ userInput }} </p>
                        <p> Form submission status: {{ formSubmitted }} </p>
                    </div>

                    <button type="submit" class="btn no-hover-effect login-btn">Login</button>

                    <!-- <div v-if="formSubmitted">
                        <div v-if="userInput == 'staff'"> -->
                            <!-- <p>hooray staff</p> -->
                            <!-- <router-link to="/overallListing">Go to Overall Listing</router-link> -->
                        <!-- </div>

                        <div v-if="userInput == 'hr'"> -->
                            <!-- <p>hooray hr</p> -->
                            <!-- <router-link to="/myProfile">Go to Overall Listing</router-link> -->
                        <!-- </div>
                    </div> -->

                    <!-- <button @click="login()" type="submit" class="btn no-hover-effect login-btn">Login</button> -->
                </form>
                </div>

                <!-- <router-view /> -->

                <main>
                    <div>
                        <router-view></router-view>
                    </div>
                </main>
                
            </div>
        </v-container>
    </v-app>
</template>

<script>
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
import '@fortawesome/fontawesome-free/css/all.css';

export default {
  name: "LoginPage",
  data() {
    return {
      userInput: "",
      formSubmitted: false
    };
  },

  methods: {
    handleFormSubmit() {
      this.formSubmitted = true;
    },
  }
};
</script>

<style @scoped>
    /* @import '@/assets/styling/login.css'; */
    @import '../assets/styling/login.css';
    @import '../assets/styling/styles.css';
    @import '../assets/styling/nav.css';
    @import '../assets/styling/search.css';
    @import '../assets/styling/filter.css';
    @import '../assets/styling/overall_listing.css';
    @import '../assets/styling/role_listing.css';
</style>