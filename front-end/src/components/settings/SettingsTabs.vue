<template>
  <Tabs :tabs="tabsList">

    <template v-slot:General>
      <SettingsGeneral/>
    </template>
    <template v-slot:User>
        <SettingsUser />
    </template>

    <template v-slot:Providers>
    <SettingsProviders />
    </template>

    <template v-slot:Lists>
      <SettingsLists />
    </template>

    <template v-slot:Logs>
      <SettingsLogs />
    </template>

    <template v-slot:Tasks>
      <SettingsTasks />
    </template>


    <template v-slot:About>
     <SettingsAbout />
    </template>
  </Tabs>
</template>

<script>
import Tabs from "@/components/ui/Tabs.vue";
import SettingsProviders  from "@/components/settings/SettingsProviders.vue";
import SettingsUser  from "@/components/settings/SettingsUser.vue";
import SettingsLogs  from "@/components/settings/SettingsLogs.vue";
import SettingsTasks  from "@/components/settings/SettingsTasks.vue";
import SettingsAbout  from "@/components/settings/SettingsAbout.vue";
import SettingsGeneral from "@/components/settings/SettingsGeneral.vue";
import SettingsLists from "@/components/settings/SettingsLists.vue";

export default {
  components: {
   Tabs, SettingsUser, SettingsProviders, SettingsLogs, SettingsTasks, SettingsGeneral, SettingsLists, SettingsAbout
  },
  data() {
    return {
      tabsList: [
        { title: "General" },
        { title: "User" },
        { title: "Providers" },
        { title: "Lists" },
        { title: "Logs" },
        { title: "Tasks" },
        { title: "About" }
      ]
    };
  }
};
</script>
