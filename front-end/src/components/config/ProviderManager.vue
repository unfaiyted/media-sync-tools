<template>
    <div class="p-6">
        <!-- Create Config Client -->
           <h2 class="text-lg font-semibold mb-4 text-white">Create Provider Instance</h2>
        <div class="mb-4">
            <input v-model="newConfigClient.label" class="block appearance-none w-full bg-gray-700 border border-gray-600 text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500" placeholder="Label">
        </div>
      <div class="mb-4">
        <select v-model="newConfigClient.clientId"
                @change="changeClient"
                class="block appearance-none w-full bg-gray-700 border border-gray-600 text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500">
          <option selected value="">Select provider...</option>
            <option v-for="client in possibleClients" :key="client.clientId" :value="client.clientId">
            {{ toReadableString(client.name) }}
          </option>
        </select>
      </div>
<div class="mb-4" v-if="newConfigClient.clientId">
   <ProviderFieldGenerator :editing-fields="newConfigClient" :client-fields="clientFields"
                                              :handle-input-change="handleInputChange"
                              :get-default-value="getDefaultValue"
                      />
</div>
        <!-- Add other input fields here for other properties of ConfigClient -->
      <button @click="createConfigClient" class="btn btn-primary">Add Provider</button>

        <!-- List Config Clients -->
        <h2 class="text-md font-semibold mt-8 mb-4 text-white">Configured Providers</h2>
        <ul v-if="configClients.length">
            <li v-for="config in configClients" :key="config.configClientId" class="mb-2">
                {{ config.label }}
                <button @click="openEditModal(config)" class="btn btn-secondary">Edit</button>
                <button @click="deleteConfigClient(config.configClientId)" class="btn btn-danger">Delete</button>
            </li>
        </ul>

        <!-- Update Config Client Modal -->
        <transition name="modal" enter-active-class="transition-opacity ease-out duration-300" leave-active-class="transition-opacity ease-in duration-300">
            <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center">
                <div class="modal-overlay absolute inset-0 bg-gray-900 opacity-75" @click="closeEditModal"></div>
                <div class="modal-container bg-white w-1/2 mx-auto p-6 rounded shadow-lg">
                    <h3 class="text-lg font-semibold mb-4">Edit Config Client</h3>
                    <div class="mb-4">
                        <input v-model="editingConfigClient.label" class="input" placeholder="Label">
                    </div>
                    <!-- Add other input fields here for editing -->

                    <!-- Dynamic input generation for clientFields -->

                  <ProviderFieldGenerator :editing-fields="editingFields" :client-fields="clientFields"
                                             :handle-input-change="handleInputChange"
                            :get-default-value="getDefaultValue"
                     />


<!--                    <div class="flex justify-end">
                        <button @click="updateConfigClient" class="btn btn-primary">Update</button>
                        <button @click="closeEditModal" class="btn btn-secondary ml-2">Cancel</button>
                    </div>-->
                </div>
            </div>
        </transition>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import {Client as MediaClient, ClientField, Config, ConfigClient, ConfigClientFieldsValue} from "@/models";
import {
    createConfigClient,
    deleteConfigClient,
    fetchClientFieldValuesByClientId,
    fetchConfigClientsByConfigId, fetchFieldsValueByConfigId,
    updateConfigClient
} from "@/api/configs";
import {fetchClientFieldByClientId, fetchClients, updateConfigClientFieldsValue} from "@/api/clients";
import ProviderFieldGenerator from "@/components/config/ProviderFieldGenerator.vue";
import {toReadableString} from "../../utils/string";


type EditingFieldsType = {
    [key: string]: string;
};

export default defineComponent({
  components: {ProviderFieldGenerator},
    props: {
        config: {
            type: Object as () => Config,
            required: true
        } // Define the prop for the client object
    },
    data() {
        return {
            newConfigClient: {
                label: "",
                clientId: "",
                // initialize other properties here
            } as ConfigClient,
            configClients: [] as ConfigClient[],
            editingConfigClient: {} as ConfigClient,
            showEditModal: false,
            clientFields: [] as ClientField[],
            possibleClients: [] as MediaClient[],
            editingFields: {
            } as EditingFieldsType,
            defaultValues: {
            } as EditingFieldsType,
            configClientFieldValues: [] as ConfigClientFieldsValue[]
        };
    },
    async mounted() {
        // Fetching all configClients for this demo. Adjust as necessary.

        this.possibleClients = await fetchClients(); // Fetch the list of clients when the component mounts
        this.configClients = await fetchConfigClientsByConfigId(this.config.configId);
        this.configClientFieldValues = await fetchFieldsValueByConfigId(this.config.configId);
        console.log(this.possibleClients);
    },
    methods: {
      toReadableString,
         async handleInputChange(field: ClientField) {
             if(this.editingConfigClient.configClientId === undefined) {
                 console.error("Config client ID is undefined");
                 return;
             }

            const dataToUpdate: ConfigClientFieldsValue = {
                configClientFieldId:  field.clientFieldId, // you should have some logic or data property to know the ID
                clientField: field,
                configClientId:  this.editingConfigClient.configClientId, // fill this in based on your component data
                value: this.editingFields[field.name]
            };

            try {
                await updateConfigClientFieldsValue(dataToUpdate);
                // maybe show a success message or some other logic after saving
            } catch (error) {
                console.error("Error updating value:", error);
                // maybe show an error message to the user
            }
        },
        async createConfigClient() {
            console.log("Creating config client:", this.newConfigClient);

            if(!this.config || !this.config.configId) {
                console.error("No config provided");
                return;
            }

            this.newConfigClient = {
                ...this.newConfigClient,
              configClientId: crypto.randomUUID(),
                configId: this.config.configId
            }

            await createConfigClient(this.newConfigClient);

            // save the update for the client fields
            for (const field of this.clientFields) {
                const dataToUpdate: ConfigClientFieldsValue = {
                    configClientFieldId:  field.clientFieldId, // you should have some logic or data property to know the ID
                    clientField: field,
                    configClientId:  this.newConfigClient.configClientId, // fill this in based on your component data
                    value: this.newConfigClient[field.name]
                };

                console.log("Updating config client field value:", dataToUpdate);
                try {
                    await updateConfigClientFieldsValue(dataToUpdate);
                    // maybe show a success message or some other logic after saving
                } catch (error) {
                    console.error("Error updating value:", error);
                    // maybe show an error message to the user
                }
            }


            // configured providers list
            this.configClients = await fetchConfigClientsByConfigId(this.config.configId);


            // reset
            this.newConfigClient = {
                label: "",
                clientId: "",
                // initialize other properties here
            } as ConfigClient;
        },
        async updateConfigClient() {
            const config = await updateConfigClient(this.editingConfigClient);
            const index = this.configClients.findIndex(cfg => cfg.configClientId === this.editingConfigClient.configClientId);
            if (index !== -1) {
                this.configClients[index] = config;
            }
            this.closeEditModal();
        },
        async deleteConfigClient(configClientId: string | undefined) {
            await deleteConfigClient(configClientId);
            this.configClients = this.configClients.filter(cfg => cfg.configClientId !== configClientId);
        },
        async openEditModal(config: ConfigClient) {
            this.editingConfigClient = { ...config };
            this.clientFields = await fetchClientFieldByClientId(config.clientId);

            this.defaultValues = await this.fetchDefaultValues();
            // Here, fetch the field values for the given config client
            this.configClientFieldValues = await fetchFieldsValueByConfigId(config.configClientId);

            // Now, map the fetched values to the editingFields and defaultValues
            for (const valueObj of this.configClientFieldValues) {
                if (valueObj.clientField) {
                    this.editingFields[valueObj.clientField.name] = valueObj.value;
                    this.defaultValues[valueObj.clientField.name] = valueObj.value;
                }
            }
            this.showEditModal = true;
        },
       async changeClient() {
            this.clientFields = await fetchClientFieldByClientId(this.newConfigClient.clientId);
            this.configClientFieldValues = await fetchFieldsValueByConfigId(this.newConfigClient.configClientId);
            this.defaultValues = await this.fetchDefaultValues();

             for (const valueObj of this.configClientFieldValues) {
                if (valueObj.clientField) {
                    this.editingFields[valueObj.clientField.name] = valueObj.value;
                    this.defaultValues[valueObj.clientField.name] = valueObj.value;
                }
            }
        },
        async fetchDefaultValues() {
            for (const field of this.clientFields) {
                console.log("Fetching default value for field:", field)
                const fieldValues = await fetchClientFieldValuesByClientId(this.editingConfigClient.configClientId); // Assuming you have a function to fetch the field value
                console.log("Fetched value:", fieldValues)
                const value = fieldValues.filter((val: ConfigClientFieldsValue) => val.configClientFieldId === field.clientFieldId)[0];
                console.log("Value:", value);
                try{
                    this.defaultValues[field.clientFieldId] = value.value || ''; // Store the fetched value in the defaultValues data property
                } catch (error) {
                    console.log("Error fetching default value:", error);
                }
            }
            return this.defaultValues;
        },
        getDefaultValue(field: ClientField): string | undefined {
             if(field.clientFieldId === undefined) {
                 console.error("Client field ID is undefined");
                 return;
             }
            return this.defaultValues[field.clientFieldId] || field.defaultValue || 'Enter value';
        },
        closeEditModal() {
            this.showEditModal = false;
            this.editingConfigClient = {} as ConfigClient;
        }
    }
});
</script>

<style scoped>
/* Add your Tailwind CSS classes and custom styles here */
.modal-container {
    z-index: 1000;
}
</style>
