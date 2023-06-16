<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div class="col-span-1">
        <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
          <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">

          <p class="font-bold">{{ user.name }}</p>

          <div class="mt-6 flex space-x-8 justify-around">
            <RouterLink :to="{ name: 'friends', params: { id: user.id } }" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink>
            <p class="text-xs text-gray-500">120 posts</p>
          </div>

          <div class="mt-6" v-if="userStore.user.id !== user.id">
            <button class="inline-block py-4 px-6 bg-purple-600 text-xs text-white rounded-lg" @click="sendFriendshipRequest">Send friendship request</button>
          </div>
          <div class="mt-6" v-if="userStore.user.id === user.id">
            <button class="inline-block py-4 px-6 bg-red-600 text-xs text-white rounded-lg" @click="logout">Logout</button>
          </div>

        </div>
      </div>

      <div class="col-span-2 space-y-4">
        <div class="bg-white border border-gray-200 rounded-lg" v-if="userStore.user.id === user.id">
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

        <div v-for="post in posts" :key="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
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
import { useUserStore } from '@/stores/user';
import FeedItem from '../components/FeedItem.vue';
import { useToastStore } from '@/stores/toast';

export default {
  name: 'FeedView',
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
  },
  data() {
    return {
      posts: [],
      user: {
        id: null
      },
      body: '',
    };
  },
  mounted() {
    this.getFeed();
  },
  watch: {
    '$route.params.id': {
      handler() {
        this.getFeed();
      },
      deep: true,
      immediate: true,
    },
  },
  methods: {
    sendFriendshipRequest() {
      axios
        .post(`/api/friends/${this.$route.params.id}/request/`)
        .then(response => {
          console.log('data', response.data);
          if (response.data.message === 'Friend Reqeust Already Send') {
            this.toastStore.showToast(5000, 'The request has already been sent!', 'bg-red-300');
          } else {
            this.toastStore.showToast(5000, 'The request has been sent', 'bg-emerald-300');
          }
        })
        .catch(error => {
          console.log('Error in sending request', error);
        });
    },
    getFeed() {
      axios
        .get(`/api/posts/profile/${this.$route.params.id}/`)
        .then(response => {
          console.log('data', response.data);
          this.posts = response.data.posts;
          this.user = response.data.user;
        })
        .catch(error => {
          console.log('Error in api post:', error);
        });
    },
    deletePost(id) {
      this.posts = this.posts.filter(post => post.id !== id);
    },
    submitForm() {
      console.log('submitForm', this.body);
      axios
        .post('/api/posts/create/', {
          body: this.body,
        })
        .then(response => {
          console.log('data', response.data);
          this.posts.unshift(response.data);
          this.body = '';
        })
        .catch(error => {
          console.log('error', error);
        });
    },

    logout() {
      console.log('Logout');
      this.userStore.removeToken()
      this.$router.push('/login/')
  },
}
};
</script>
