<template>
  <q-td>
    <q-btn-group flat>
      <q-btn v-if="props.edit" @click="onEdit" size="s" icon="edit" />
      <q-btn  v-if="props.delete" @click="onDelete" size="s" icon="delete" />
      <q-btn size="s" icon="update" />
    </q-btn-group>
  </q-td>
</template>

<script setup>
import { useQuasar } from "quasar";


const $q = useQuasar();

const props = defineProps(["row", "delete", "edit", "success", "fail"]);

console.log(props.row);

function onEdit() {
  console.log("edit");
  props.edit(props.row.id)
}

function onDelete() {
  $q.dialog({
    title: "Confirm",
    message: `Really delete "${props.row.name}"?`,
    cancel: true,
    persistent: true,
  })
    .onOk(() => {
      props
        .delete(props.row.id)
        .then((response) => {
          if (typeof props.success !== "undefined") {
            props.success(response);
          } else {
            console.log("Delete success");
          }
        })
        .catch((reason) => {
          if (typeof props.fail !== "undefined") {
            props.fail(reason);
          } else {
            console.error(reason);
          }
        });
      console.log(">>>> OK");
    })
    .onOk(() => {
      console.log(">>>> second OK catcher");
    })
    .onCancel(() => {
      console.log(">>>> Cancel");
    })
    .onDismiss(() => {
      console.log("I am triggered on both OK and Cancel");
    });
}
</script>
