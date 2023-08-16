<!-- List Client Fields -->
<h2 class="text-lg font-semibold mt-8 mb-4">Client Fields</h2>
<ul v-if="clientFields.length">
<li v-for="field in clientFields" :key="field.clientFieldId" class="mb-2">
    {{ field.name }} ({{ field.clientFieldId }}, {{ field.defaultValue }})
    <button @click="openEditModal(field)" class="btn btn-secondary">Edit</button>
    <button @click="deleteClientField(field.clientFieldId)" class="btn btn-danger">Delete</button>
</li>
</ul>
<script setup lang="ts">
</script>
