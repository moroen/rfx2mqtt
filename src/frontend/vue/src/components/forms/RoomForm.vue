<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card>


      <q-card-section>
        <div class="text-h6">{{ props.title }}</div>
        <div><q-input v-model="row.name" label="Name"></q-input></div>
      </q-card-section>


      <q-card-actions align="right">
        <q-btn color="secondary" label="Cancel" @click="onDialogCancel" />
        <q-btn color="secondary" label="Save" @click="onOK" />
      </q-card-actions>
    </q-card>

  </q-dialog>
</template>

<script setup>
import { ref } from "vue";
import { useDialogPluginComponent } from 'quasar'
defineEmits(useDialogPluginComponent.emits)

const props = defineProps(["row", "title"]);

const row = ref(props.row)

const { dialogRef, onDialogCancel, onDialogHide, onDialogOK } =
  useDialogPluginComponent()

console.log(props.row.name)

function onOK() {
  onDialogOK(row.value)
}


</script>
