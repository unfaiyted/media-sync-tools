<template>
    <Modal :isOpen="showLibraryManagerModal"
           @close="showLibraryManagerModal = false"
           @do-action="addLibrary"
           @cancel-action="closeLibraryModal">
        <LibraryManager :config="config" />


    </Modal>
</template>

<script>

</script>
