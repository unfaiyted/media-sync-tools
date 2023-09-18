
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
import Sidebar from "./components/ui/Sidebar.vue"
import Header from "./components/ui/Header.vue"
import AppHydrate from "@/components/ui/AppHydrate.vue";
const userStore = useUserStore();

userStore.initUser();

const date = '__DATE__';
const timeAgo = useTimeAgo(date);
</script>
