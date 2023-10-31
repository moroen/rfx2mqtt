<template>
  <q-page padding>


    <div class="q-pa-md">
    <q-table
      title="Devices"
      :loading="is_loading"
      :rows="data"
      :columns="columns"
      row-key="id"
      :pagination="pagination"
      hide-no-data
    >
    <template v-slot:body-cell-state="props">
    <q-td :props="props">
    <StateDisplay
      :row="props.row"
    ></StateDisplay></q-td>
    </template>
    </q-table>
  </div>

  </q-page>
</template>

<script setup>

import { ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

import { getDevices }  from "components/common/transport"

import StateDisplay  from "components/StateDisplay.vue"

const data = ref([])
const is_loading = ref(true)
const $q = useQuasar()

const config = {
  headers:{

  }
};

const columns = [
  {
    name: "Id",
    label: "Id",
    field: "id",
    align: "left",
    sortable: true,
  },
  {
    name: "Name",
    label: "Name",
    field: "name",
    align: "left",
    sortable: true,
  },
  {
    name: "Ident",
    label: "Ident",
    field: "ident",
    align: "left",
    sortable: true,
  },
  {
    name: "Unit",
    label: "Unit",
    field: "unit",
    align: "left",
    sortable: false,
  },
  {
    name: "Room",
    label: "Room",
    field: "room_name",
    align: "left",
    sortable: true,
  }



  ,
  { name: 'state', label: 'State', field: 'state', align: "right" }
]

const components = []

const pagination = {
        rowsPerPage: 10
}


const props=defineProps(["room"])

console.log(props.room)

let filter = {}

if (typeof props.room !== "undefined") {
    filter.room=1
  }

getDevices(data, is_loading, filter)

</script>
