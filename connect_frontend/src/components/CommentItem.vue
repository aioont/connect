<template>
    <div class="mb-6 flex items-center justify-between">
                 <div class="flex items-center space-x-6">
                     <img :src="comment.created_by.get_avatar" class="w-[40px] rounded-full">
 
                         <p>
                             <strong> 
               
                                 <RouterLink :to="{name: 'profile', params:{'id': comment.created_by.id}}"> {{ comment.created_by.name }} </RouterLink>
                             </strong>
                         </p>
                 </div>
 
                 <p class="text-gray-600"> {{ comment.created_at_formatted }} ago</p>
           </div>
 
           <img src="https://images.unsplash.com/photo-1661956602868-6ae368943878?ixlib=rb-4.0.3&ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2670&q=80" class="w-full rounded-lg"> 
           <p class="py-2">{{ comment.body }}</p>


 
     
 </template>
 
 
 
<script>
import { RouterLink } from 'vue-router'

export default {
    props: {
        comment: Object
    },
    components: { RouterLink }
}
</script>
 

















