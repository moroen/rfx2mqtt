<template>
  <q-page padding>
    <room-table></room-table>
  </q-page>
</template>

<script setup>
import { ref } from "vue";
import { api } from "boot/axios";
import { useQuasar } from "quasar";

import { getRooms } from "src/components/common/transport";

import RoomTable from "src/components/RoomTable.vue";

const data = ref([]);
const $q = useQuasar();

const columns = [
  {
    name: "id",
    label: "Id",
    field: "id",
    align: "left",
    sortable: true,
    classes: "q-table--col-auto-width",
    headerClasses: "q-table--col-auto-width",
  },
  {
    name: "name",
    label: "Name",
    field: "name",
    align: "left",
    sortable: true,
  },
  {
    name: "actions",
    // label: "Actions",
    field: "name",
    align: "left",
    classes: "q-table--col-auto-width",
    headerClasses: "q-table--col-auto-width",
  },
];

getRooms(data);
</script>
