<template>
    <div :class="sidebarClass" class="bg-gray-900 text-white min-h-screen px-4 py-6 space-y-4 transition-all duration-300 sidebar">
        <router-link v-for="(link, index) in sidebarLinks" :key="index" :to="link.to" class="flex items-center py-2 px-3 rounded hover:bg-gray-700">
            <component :is="link.icon" class="w-5 h-5 mr-2" />
            <span>{{ link.text }}</span>
            <template v-if="link.sublinks">
                <div v-show="isCollapsed" class="pl-6 space-y-1">
                    <router-link v-for="(sublink, subIndex) in link.sublinks" :key="subIndex" :to="sublink.to" class="block py-1 px-2 rounded hover:bg-gray-700">
                        {{ sublink.text }}
                    </router-link>
                </div>
            </template>
        </router-link>
    </div>
</template>


<script lang="ts">
import { LinkIcon, DocumentTextIcon, UserIcon, CogIcon, UsersIcon, TvIcon} from '@heroicons/vue/24/outline';

// TODO: Add a section for Providers

interface Sublink {
    to: string;
    text: string;
    icon: string;
}

interface Link {
    to: string;
    text: string;
    icon?: any;
    sublinks?: Sublink[];
}

export default defineComponent({
    data() {
        return {
            sidebarLinks: [
                { to: '/', text: 'Dashboard', icon: LinkIcon },
                { to: '/poster', text: 'Posters', icon: DocumentTextIcon },
                { to: '/settings', text: 'Settings', icon: CogIcon },
                { to: '/providers', text: 'Provider Lists', icon: TvIcon },
                { to: '/lists', text: 'Media Lists', icon: TvIcon },
                { to: '/users', text: 'Users', icon: UserIcon},
                {
                    text: 'Admin',
                    icon: UsersIcon,
                    to: '/admin',
                    sublinks: [
                        { to: '/admin/users', text: 'Users', icon: UserIcon },
                        { to: '/admin/settings', text: 'Settings', icon: CogIcon },
                    ],
                },
                // Add other links
            ] as Link[],
            isCollapsed: false
        };
    },
    methods: {
        toggleCollapse() {
            this.isCollapsed = !this.isCollapsed;
        }
    },
    computed: {
        sidebarClass() {
            return {
                'w-64': !this.isCollapsed,
                'w-20': this.isCollapsed,
            };
        },
    },
});
</script>

<style scoped>
/* Add your custom styles here */
.sidebar {
  width: 250px;
  min-width: 250px;
}
</style>
