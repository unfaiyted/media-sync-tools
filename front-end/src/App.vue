
<template>
    <AppHydrate>
    <div id="app" class="bg-gray-200 min-h-screen">
        <Header />
        <div class="flex">
            <Sidebar />
            <router-view class="flex-grow bg-gray-100" />
        </div>
    </div>
    </AppHydrate>
</template>


<script lang="ts" setup>
import { useTimeAgo } from '@vueuse/core';
import { useUserStore } from '@/store/user';
import ReloadPrompt from '@/pwa/ReloadPrompt.vue';
import ServiceWorker from './components/ServiceWorker.vue';
import Sidebar from "./components/ui/Sidebar.vue"
import Header from "./components/ui/Header.vue"
import AppHydrate from "@/components/ui/AppHydrate.vue";
const userStore = useUserStore();

userStore.initUser();

const date = '__DATE__';
const timeAgo = useTimeAgo(date);
</script>

<!--<template>-->
<!--    <el-container>-->
<!--        <el-header>-->
<!--            <Header />-->
<!--        </el-header>-->
<!--        <el-main class="main">-->
<!--            <RouterView />-->
<!--            <br />-->
<!--            <ServiceWorker />-->
<!--            <br />-->
<!--            <div>Built at: {{ date }} ({{ timeAgo }})</div>-->
<!--        </el-main>-->
<!--        <el-footer>-->
<!--            <Footer />-->
<!--        </el-footer>-->
<!--    </el-container>-->
<!--    <ReloadPrompt />-->
<!--</template>-->
<!--<style lang="scss">-->
<!--#app {-->
<!--    font-family: Avenir, Helvetica, Arial, sans-serif;-->

<!--    -webkit-font-smoothing: antialiased;-->
<!--    -moz-osx-font-smoothing: grayscale;-->
<!--    text-align: center;-->
<!--    line-height: 150%;-->
<!--}-->

<!--.main {-->
<!--    min-height: 500px;-->
<!--}-->

<!--.sw-msg {-->
<!--    margin-top: 20px;-->
<!--}-->
<!--</style>-->
