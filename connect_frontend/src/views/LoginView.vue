<template>
    <div class="max-w-7xl mx-auto">
      <div class="grid gap-4 md:grid-cols-2">
        <div class="main-left">
          <div class="p-12 bg-white border border-gray-200 rounded-lg">
            <h1 class="mb-6 text-2xl">Login</h1>
            <p class="mb-6 text-gray-500">
              How do you feel today? Let's connect with your connections.
            </p>
            <p class="font-bold">
              Don't have an account?
              <RouterLink to="signup" class="underline">Click here</RouterLink>
              to create one!
            </p>
          </div>
        </div>
  
        <div class="main-right">
          <div class="p-12 bg-white border border-gray-200 rounded-lg">
            <form class="space-y-6" @submit.prevent="submitForm">
              <div>
                <label for="email">E-mail</label><br>
                <input
                  id="email"
                  type="email"
                  v-model="form.email"
                  placeholder="Your e-mail address"
                  class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
                >
              </div>
  
              <div>
                <label for="password">Password</label><br>
                <input
                  id="password"
                  type="password"
                  v-model="form.password"
                  placeholder="Your password"
                  class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
                >
              </div>
  
              <template v-if="errors.length > 0">
                <div class="bg-red-300 text-white rounded-lg p-6">
                  <p v-for="error in errors" :key="error">{{ error }}</p>
                </div>
              </template>
  
              <div>
                <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Log in</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>



<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  setup() {
    const userStore = useUserStore()
    return {
      userStore
    }
  },
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      errors: [],
      errorMessage: ''
    }
  },
  methods: {
    async submitForm() {
      this.errors = [];
      if (this.form.email === '') {
        this.errors.push('Your e-mail is missing');
      }
      if (this.form.password === '') {
        this.errors.push('Your password is missing');
      }
      if (this.errors.length === 0) {
        try {
          const response = await axios.post('/api/login/', this.form);
          this.userStore.setToken(response.data);
          axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;

          // Make the GET request to /api/me/ with the CSRF token included
          const csrfResponse = await axios.get('/api/csrf-token/');
          const csrfToken = csrfResponse.data.csrfToken;
          const headers = {
            'X-CSRFToken': csrfToken,
          };

          // Get the user details from the server
          const meResponse = await axios.get('/api/me/', { withCredentials: true, headers });
          const userDetails = meResponse.data;
          
          comsole.log('meResponse : ', meResponse, 'user Details : ', userDetails)

          // Check if the response contains the user details
          if (userDetails && userDetails.id && userDetails.name && userDetails.email) {
            this.userStore.setUserInfo(userDetails);
            this.$router.push('/feed');
          } else {
            this.errorMessage = 'Server failed to fetch user details. Please try again.';
            // Handle the case when the response does not contain the expected user details
          }
        } catch (error) {
          if (error.response && error.response.status === 403) {
            console.log('Unauthorized access. Please login.', error.response);
            // Handle unauthorized access error, such as redirecting to a login page
          } else {
            console.log('Error reason 500 string object calling man:', error);
            this.errorMessage = 'An error occurred while fetching user details. Please try again.';
            // Handle other errors
          }
        }
      }
    }
  }
}
</script>
