<template>
    <div class="q-pa-md example-row-equal-width">
    <div class="row">
      <div class="col-6">
      <q-btn-toggle
        @update:model-value="onStateUpdate"
        v-model="state"
        color="blue"
        text-color="white"
        toggle-color="orange"
        toggle-text-color="black"
        rounded
        unelevated
        glossy
        :options="[
          {label: 'Off', value: false},
          {label: 'On', value: true},
        ]"
      />
    </div>

      <div class="col-4"><q-badge color="secondary">
      {{ brightness }}</q-badge>
</div>
      </div>
      <div class="row">
        <div class="col"><q-slider @change="onUpdate" v-model="brightness" :min="0" :max="100" :color="sliderColor"/>
      </div>

    </div>
  </div>
</template>

<script setup>
import { Loading } from 'quasar';
import { ref } from 'vue'
import { setDevice } from '../common/transport';

const props=defineProps(["id", "state", "brightness"])

const state = ref(props.state)
const brightness = ref(props.brightness)
const sliderColor = ref(props.state ? "yellow":"black")

console.log(props)

function onStateUpdate(value) {
  state.value = value
  sliderColor.value= value ? "yellow" : "black"
  setDevice(props.id, value, brightness.value)
}

function onUpdate(value) {
  onStateUpdate(true)
}


</script>
