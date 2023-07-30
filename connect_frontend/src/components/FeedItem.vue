<template>
   <div class="mb-6 flex items-center justify-between">
                <div class="flex items-center space-x-6">
                    <img :src="post.created_by.get_avatar" class="w-[40px] rounded-full">

                        <p>
                            <strong> 
              
                                <RouterLink :to="{name: 'profile', params:{'id': post.created_by.id}}"> {{ post.created_by.name }} </RouterLink>
                            </strong>
                        </p>
                </div>

                <p class="text-gray-600"> {{ post.created_at_formatted }}</p>
          </div>

          <template v-if="post.attachments.length">
            <img v-for="image in post.attachments" v-bind:key="image.id" :src="image.get_image" class="w-full mb-4 rounded-xl">
          </template>

          <p class="py-2 break-words">{{ post.body }}</p>

          <div class="my-6 flex justify-between">
        <div class="flex space-x-6 items-center">
            <div class="flex items-center space-x-2" @click="likePost(post.id)">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"></path>
                </svg>  
                
                <span class="text-gray-500 text-xs"> {{ post.likes_count }} likes</span>
            </div>
            
            <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z"></path>
                </svg> 

                <RouterLink :to="{ name: 'postview',params: {'id': post.id}}" class="text-gray-500 text-xs"> {{ post.comments_count }} comments</RouterLink>
            </div>

            <div v-if="post.is_private" class="flex items-center space-x-2 text-gray-500 text-xs">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                </svg>

                <span>Is private</span>
            </div>
        </div>
        
        <div>
            <div @click="toggleExtraModel">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"></path>
                </svg>
            </div>   
        </div>   
    </div>  

    <div v-if="showExtraModel">
        <div class="flex space-x-6 items-center">
            <div 
                class="flex items-center space-x-2" 
                @click="deletePost"
                v-if="userStore.user.id == post.created_by.id"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash text-red-500" viewBox="0 0 16 16">
                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
                    <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
                </svg> 
                
                <span class="text-red-500 text-xs">Delete post </span>
            </div>
      
            <div 
                class="flex items-center space-x-2" 
                @click="reportPost"
                v-if="userStore.user.id != post.created_by.id"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-flag text-orange-500" viewBox="0 0 16 16">
                    <path d="M14.778.085A.5.5 0 0 1 15 .5V8a.5.5 0 0 1-.314.464L14.5 8l.186.464-.003.001-.006.003-.023.009a12.435 12.435 0 0 1-.397.15c-.264.095-.631.223-1.047.35-.816.252-1.879.523-2.71.523-.847 0-1.548-.28-2.158-.525l-.028-.01C7.68 8.71 7.14 8.5 6.5 8.5c-.7 0-1.638.23-2.437.477A19.626 19.626 0 0 0 3 9.342V15.5a.5.5 0 0 1-1 0V.5a.5.5 0 0 1 1 0v.282c.226-.079.496-.17.79-.26C4.606.272 5.67 0 6.5 0c.84 0 1.524.277 2.121.519l.043.018C9.286.788 9.828 1 10.5 1c.7 0 1.638-.23 2.437-.477a19.587 19.587 0 0 0 1.349-.476l.019-.007.004-.002h.001M14 1.221c-.22.078-.48.167-.766.255-.81.252-1.872.523-2.734.523-.886 0-1.592-.286-2.203-.534l-.008-.003C7.662 1.21 7.139 1 6.5 1c-.669 0-1.606.229-2.415.478A21.294 21.294 0 0 0 3 1.845v6.433c.22-.078.48-.167.766-.255C4.576 7.77 5.638 7.5 6.5 7.5c.847 0 1.548.28 2.158.525l.028.01C9.32 8.29 9.86 8.5 10.5 8.5c.668 0 1.606-.229 2.415-.478A21.317 21.317 0 0 0 14 7.655V1.222z"/>
                </svg>
                
                <span class="text-orange-500 text-xs">Report post </span>
            </div>
        </div> 
        
        
    </div>

    
</template>


<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

export default {
    props: {
        post: Object
    },

    emits: ['deletePost'],

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    data() {
        return {
            showExtraModel: false
        }
    },

    methods: {
        likePost(id) {
            axios
                .post(`/api/posts/${id}/like/`)
                .then(response => {
                    if (response.data.message == "Liked a post") {
                        this.post.likes_count += 1;
                        //console.log("Like post", response.data)
                    }
                })
                .catch(error => {
                    console.log("Error in adding like to post", error);
                });
        },
        toggleExtraModel() {
            this.showExtraModel = !this.showExtraModel
        },
        deletePost() {
            // console.log("Post deleted !", this.post.id)

            this.$emit('deletePost', this.post.id)
            axios
                .delete(`/api/posts/${this.post.id}/delete/`)
                .then(response => {
                    console.log(response.data);
                    this.toastStore.showToast(5000, 'The post was deleted', 'bg-emerald-500')

                })
                .catch(error => {
                    console.log('Error in deleting post : ', error);
                })
        },
        reportPost() {
            console.log("Post reported !");

            axios
                .post(`/api/posts/${this.post.id}/report/`)
                .then(response => {
                    console.log(response.data);
                    this.toastStore.showToast(5000, 'The post was reported', 'bg-emerald-500')

                })
                .catch(error => {
                    console.log('Error in deleting post : ', error);
                })

        }
    },
    components: { RouterLink }
}

</script>

