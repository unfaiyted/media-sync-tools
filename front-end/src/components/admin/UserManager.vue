<template>
    <div class="p-6">
        <!-- Create & Update User -->
        <h2 class="text-lg font-semibold mb-4" v-if="!editingUser">Create User</h2>
        <h2 class="text-lg font-semibold mb-4" v-else>Update User</h2>

        <div class="mb-4">
            <input v-model="currentUser.email" class="input" placeholder="Email">
        </div>
        <div class="mb-4">
            <input v-model="currentUser.name" class="input" placeholder="Name">
        </div>
        <div class="mb-4">
            <input v-model="currentUser.password" type="password" class="input" placeholder="Password">
        </div>
        <button v-if="!editingUser" @click="createUser" class="btn btn-primary">Create User</button>
        <button v-else @click="saveUserUpdate" class="btn btn-primary">Save Changes</button>

        <!-- List Users -->
        <h2 class="text-lg font-semibold mt-8 mb-4">Users</h2>
        <ul v-if="users.length">
            <li v-for="user in users" :key="user.userId" class="mb-2">
                {{ user.name }} ({{ user.email }})
                <button @click="editUser(user)" class="btn btn-secondary">Edit</button>
                <button @click="deleteUser(user.userId)" class="btn btn-danger">Delete</button>
            </li>
        </ul>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { createUser, fetchUser, fetchUsers, updateUser, deleteUser } from "@/api/users";
import { User } from "@/models";

export default defineComponent({
    data() {
        return {
            users: [] as User[],
            currentUser: {
                email: "",
                name: "",
                password: ""
            } as User,
            editingUser: false
        };
    },
    async mounted() {
        this.users = await fetchUsers();
    },
    methods: {
        async createUser() {
            await createUser(this.currentUser);
            this.users = await fetchUsers();
            this.clearForm();
        },
        async editUser(user: User) {
            this.currentUser = { ...user };
            this.editingUser = true;
        },
        async saveUserUpdate() {
            await updateUser(this.currentUser);
            this.users = await fetchUsers();
            this.clearForm();
            this.editingUser = false;
        },
        async deleteUser(userId: string | undefined) {
            await deleteUser(userId);
            this.users = this.users.filter(user => user.userId !== userId);
        },
        clearForm() {
            this.currentUser = {
                email: "",
                name: "",
                password: ""
            } as User;
        }
    }
});
</script>

<style scoped>
/* Add your Tailwind CSS classes and custom styles here */
</style>
