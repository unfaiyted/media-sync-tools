

<template>
    <UserManagement />
    <div class="space-y-4">
        <label class="block">
            Enable remote access:
            <input type="checkbox" class="ml-2">
        </label>

        <div class="space-y-2">
            <div class="font-semibold">Default Permissions:</div>
            <label><input type="checkbox" class="mr-2">Create Lists</label>
            <label><input type="checkbox" class="mr-2">Edit Lists</label>
            <label><input type="checkbox" class="mr-2">Delete Lists</label>
            <label><input type="checkbox" class="mr-2">Create Users</label>
            <label><input type="checkbox" class="mr-2">Can edit providers</label>
            <!-- ... other permissions ... -->
        </div>
    </div>
</template>


<script lang="ts">
import UserManagement from "@/components/admin/UserManager.vue";

export default {
    name: 'SettingsUser',
    components: {UserManagement},

    setup() {

        return {

        };
    }
};
</script>
