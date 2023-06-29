<template>
   <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div class="main-center col-span-3 space-y-4">
         <div class="p-4 bg-white border border-gray-200 rounded-lg">
            <h2 class="text-xl">Trend <b>#{{ $route.params.id }} </b></h2>
         </div>

        <div 
            v-for="post in posts" 
            v-bind:key="post.id" 
            class="p-4 bg-white border border-gray-200 rounded-lg"
        >
           <FeedItem v-bind:post="post" />
          
        </div>
      </div>
    </div>
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
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
    };
  },

  mounted() {
    this.getFeed();
  },

  watch: { 
      '$route.params.id': {
          handler: function() {
              this.getFeed()
          },
          deep: true,
          immediate: true
      }
  },

  methods: {
    getFeed() {
      axios
        .get(`/api/posts/?trend=${this.$route.params.id}`)
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

    
  },
};
</script>