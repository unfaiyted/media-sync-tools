<template>
    <div class="sidebar">
        <PanelMenu :model="items"></PanelMenu>
        <Button label="Add Provider" class="p-mt-2"></Button>
    </div>
</template>

<script>
import PanelMenu  from 'primevue/panelmenu';

export default {
    components: {
        PanelMenu,
    },
    data() {
        return {
            items: [], // This will hold the structure for the PanelMenu
            providers: {
                // ... Your provider data here
            },
        };
    },
    created() {
        // Generate items for PanelMenu
        this.generateMenuItems();
    },
    methods: {
        generateMenuItems() {
            // For LibraryProvider
            const libraryProviders = this.providers.LibraryProvider.map(provider => {
                return {
                    label: `${provider.name} (${provider.libraries.length})`,
                    items: provider.libraries.map(library => ({
                        label: library.name,
                        icon: 'pi pi-refresh', // This can be a sync icon
                        command: () => {
                            this.toggleSync(library);
                        },
                    }))
                };
            });

            // For ListProvider
            const listProviders = this.providers.ListProvider.map(provider => {
                return {
                    label: provider.name,
                    items: provider.lists.slice(0,5).map(list => ({
                        label: list.name,
                        command: () => {
                            this.goToListPage(list.mediaId);
                        },
                    }))
                };
            });

            // For PosterProvider
            const posterProviders = this.providers.PosterProvider.map(provider => {
                return {
                    label: provider.name,
                };
            });

            // Populate items
            this.items = [
                {
                    label: 'Libraries',
                    items: libraryProviders
                },
                {
                    label: 'Lists',
                    items: listProviders
                },
                {
                    label: 'Posters',
                    items: posterProviders
                }
            ];
        },
        toggleSync(library) {
            // Implement sync logic here
        },
        goToListPage(mediaId) {
            // Implement navigation logic here
        }
    }
}
</script>
