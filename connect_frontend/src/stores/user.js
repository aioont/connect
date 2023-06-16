import { defineStore } from 'pinia';
import axios from "axios";



export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    user: {
      isAuthenticated: false,
      id: null,
      name: null,
      email: null,
      access: null,
      refresh: null,
    },
  }),

    actions: {
        initStore() {
            console.log('initStore', localStorage.getItem('user.access'))

            if (localStorage.getItem('user.access')) {
                console.log('User has access!')

                this.user.access = localStorage.getItem('user.access')
                this.user.refresh = localStorage.getItem('user.refresh')
                this.user.id = localStorage.getItem('user.id')
                this.user.name = localStorage.getItem('user.name')
                this.user.email = localStorage.getItem('user.email')
              
                this.user.isAuthenticated = true

                this.refreshToken()

                console.log('Initialized user:', this.user)
            }
        },

        setToken(data) {
            console.log('setToken', data)

            this.user.access = data.access
            this.user.refresh = data.refresh
            this.user.isAuthenticated = true

            localStorage.setItem('user.access', data.access)
            localStorage.setItem('user.refresh', data.refresh)

            console.log('user.access: ', localStorage.getItem('user.access'))
        },

        removeToken() {
          console.log('removeToken')
      
          this.user.refresh = null
          this.user.access = null
          this.user.isAuthenticated = false
          this.user.id = null
          this.user.name = null
          this.user.email = null
      
          localStorage.setItem('user.access', null)
          localStorage.setItem('user.refresh', null)
          localStorage.setItem('user.id', null)
          localStorage.setItem('user.name', null)
          localStorage.setItem('user.email', null)
    
      },      

      setUserInfo(user) {
        console.log('setUserInfo', user)

        this.user.id = user.id
        this.user.name = user.name
        this.user.email = user.email
    

        localStorage.setItem('user.id', this.user.id)
        localStorage.setItem('user.name', this.user.name)
        localStorage.setItem('user.email', this.user.email)


        console.log('User', this.user)
    },

    refreshToken() {
        axios.post('/api/refresh/', {
            refresh: this.user.refresh
        })
            .then((response) => {
                this.user.access = response.data.access

                localStorage.setItem('user.access', response.data.access)

                axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
            })
            .catch((error)=>{
                console.log(error)

                this.removeToken()
            })
    },

},
});