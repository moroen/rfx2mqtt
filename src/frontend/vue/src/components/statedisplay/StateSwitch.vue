<template>

      <q-btn-toggle @update:model-value="onStateUpdate" v-model="state" color="white" text-color="black"
        toggle-color="blue" toggle-text-color="white" rounded unelevated glossy :options="[
          { label: 'Off', value: false },
          { label: 'On', value: true },
        ]" />

</template>

<script setup>
import { ref } from 'vue'

import { setDevice } from '../common/transport';

const props=defineProps(["id", "state"])

const state = ref(props.state)

function onStateUpdate(value) {
  setDevice(props.id, value)
}



</script>
