<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      

      <div class="main-center col-span-3 space-y-4">
        <div class="bg-white border border-gray-200 rounded-lg">
          <form v-on:submit.prevent="submitForm" method="post">
            <div class="p-4">
                <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
            </div>

            <div class="p-4 border-t border-gray-100 flex justify-between">
              <a href="#" class="inline-block py-2 px-4 bg-gray-600 text-white rounded-lg">Attach image</a>

              <button class="inline-block py-2 px-4 bg-purple-600 text-white rounded-lg">Post</button>
            </div>
          </form>
        </div>

        <div 
            v-for="post in posts" 
            v-bind:key="post.id" 
            class="p-4 bg-white border border-gray-200 rounded-lg"
        >
           <FeedItem v-bind:post="post" />
          



          <div class="my-6 flex justify-between">
            <div class="flex space-x-6">
              <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                </svg>  
                <span class="text-gray-500 text-xs">82 likes</span>
              </div>

              <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
                </svg> 
                <span class="text-gray-500 text-xs">0 comments</span>
              </div>
            </div>

            <div>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
              </svg>   
            </div>   
          </div>  
        </div>
      </div>

      <div class="main-right col-span-1 space-y-4">
        <PeopleYouMayKnow />
        <Trends />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';
import Trends from '../components/Trends.vue';
import FeedItem from '../components/FeedItem.vue';

export default {
  name: 'FeedView',
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
  },
  data() {
    return {
      posts: [],
      body: '',
    };
  },
  mounted() {
    this.getFeed();
  },
  methods: {
    getFeed() {
      axios
        .get('/api/posts/')
        .then(response => {
          console.log('data', response.data);
          this.posts = response.data;
        })
        .catch(error => {
          console.log('Error in api post:', error);
        });
    },
    deletePost(id) {
      this.posts = this.posts.filter(post => post.id !== id);
    },

    submitForm() {
        console.log('submitForm', this.body)

        axios
            .post('/api/posts/create/', {
              'body': this.body
            })
            .then(response => {
                console.log('data', response.data)
                this.posts.unshift(response.data)
                this.body = ''
            })
            .catch(error => {
                console.log('error', error)
            })
    }
  },
};
</script>
