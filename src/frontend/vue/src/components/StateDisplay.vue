<template>
  <div v-if="props.row.devicetype=='Switch'">
    <StateSwitch
      :state="props.row.state"
      :id="props.row.id"></StateSwitch>
  </div>
  <div v-else-if="props.row.devicetype=='Light'">
    <StateLight
      :state="props.row.state"
      :id="props.row.id"
      :brightness="props.row.brightness"
      ></StateLight>

  </div>
  <div v-else-if="props.row.devicetype=='Temperature'">
   {{ props.row.temp }}&deg;/ {{ props.row.humidity }}%
  </div>
  <div v-else>
  {{ props.row.state }}
  </div>
</template>

<script setup>
import { ref } from 'vue'

import StateSwitch from "components/statedisplay/StateSwitch.vue"
import StateLight from "components/statedisplay/StateLight.vue"

const props=defineProps(["row"])

const state = ref(props.row.state)

</script>
