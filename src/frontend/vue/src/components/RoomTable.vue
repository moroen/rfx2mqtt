<template>
  <q-page padding>
    <q-table
      title="Rooms"
      :rows="data"
      :columns="columns"
      :pagination="pagination"
      row-key="id"
      hide-no-data
    >
      <template v-slot:top-right>
        <div class="q-pa-md q-gutter-sm">
          <q-btn square color="secondary" icon="add" />
        </div>
      </template>

      <template v-slot:body-cell-actions="props">
        <action-bar
          :row="props.row"
          :success="success"
          :fail="failed"
          :delete="deleteRoom"
          :edit="editRoom"
        >
        </action-bar>
      </template>
    </q-table>
  </q-page>
</template>

<script setup>
import { ref } from "vue";
import { api } from "boot/axios";
import { useQuasar } from "quasar";

import { getRooms, getRoom, deleteRoom, updateRoom } from "src/components/common/transport";

import ActionBar from "src/components/ActionBar.vue";
import RoomForm from "src/components/forms/RoomForm.vue";

const data = ref([]);
const $q = useQuasar();

const pagination = {
  rowsPerPage: 10,
};

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

function success() {
  getRooms(data);
}

function failed() {
  console.log("Failed");
}

function editRoom(id) {
  console.log("do edit")

  const room = getRoom(id)
  .then ((result) => {
    console.log(result)
    $q.dialog({
    component: RoomForm,
    componentProps: {
      title: "Edit room",
      row: result.data,
    },

  }).onOk((result) => {
    console.log('OK')
    console.log(result)
    updateRoom(id, result)
    .then ((result) => {
      getRooms(data)
    })
    .catch ((reason) => {
      console.log(reason)
    })
  })
  })
  .catch((reason) => {
    console.log(reason)
  })


}

getRooms(data);
</script>
