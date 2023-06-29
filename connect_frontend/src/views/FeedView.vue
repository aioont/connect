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

        <div v-for="post in posts" v-bind:key="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
          <FeedItem v-bind:post="post" />
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
