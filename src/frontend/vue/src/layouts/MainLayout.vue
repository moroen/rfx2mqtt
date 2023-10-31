<template>
  <q-layout view="lHh Lpr lFf">
    <q-toolbar class="bg-primary text-white q-my-md shadow-2">
      <q-btn to="/" flat round dense icon="menu" class="q-mr-sm" />
      <q-separator dark vertical inset />
      <NavigationRow> </NavigationRow>

      <q-toolbar-title class="q-pa-sm"> </q-toolbar-title>

      <q-btn flat round dense icon="more_vert" />
    </q-toolbar>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";
import NavigationRow from "components/NavigationRow.vue";

export default defineComponent({
  name: "MainLayout",

  components: {
    NavigationRow,
  },

  setup() {
    const leftDrawerOpen = ref(false);

    return {};
  },
});
</script>
