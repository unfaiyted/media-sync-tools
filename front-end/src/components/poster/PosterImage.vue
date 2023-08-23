<template>
    <div class="flex flex-col h-full">

        <div class="poster">
            <img v-if="poster" :src="poster.url" alt="Poster"  />
        </div>

        <div>
           TEXT: {{ JSON.stringify(poster.text)}}
        </div>
        <div>
            BACKGROUND: {{ JSON.stringify(poster.background)}}
            </div>
        <div>
            GRADIENT:  {{ JSON.stringify(poster.gradient)}}
        </div>
         <div>
            ICON:  {{ JSON.stringify(poster.icon)}}
        </div>
        <div>
            BORDER:  {{ JSON.stringify(poster.border)}}
        </div>

       <div>
           URL: {{ JSON.stringify(poster.url)}}
       </div>


    </div>
</template>

<style scoped>

.poster {
    width: 400px;
    height: 600px;
    background-color: #f2f2f2;
    margin: 20px auto;
    position: relative;
}

.poster img {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
}


</style>

<script lang="ts">
import {MediaPoster} from "@/models";


export default {
    components: {},
    props: {
      poster: {
        type: Object as () => MediaPoster,
        required: true
      }
    },
  watch: {
    poster: function(newPoster: MediaPoster) {
      this.poster = newPoster;
    }
  },
    methods: {
    }
}
</script>
