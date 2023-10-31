import { api } from "boot/axios";
import { useQuasar } from "quasar";

const config = {
  headers: {},
};

export function getRooms(target, is_loading) {
  const url = "api/rooms/";
  loadData(url, target, is_loading);
}

export function getRoom(id) {
  const url = `api/rooms/${id}`;
  return getRequest(url);
}

export function updateRoom(id, payload) {
  const url = `api/rooms/${id}/`;
  return putRequest(url, payload);
}

export function deleteRoom(id) {
  const url = `api/rooms/${id}`;
  return deleteRequest(url);
}

export function getDevices(target, is_loading, filter) {
  const url = "api/devices/";

  if (typeof filter !== "undefined") {
    config.params = filter;
  }

  loadData(url, target, is_loading);
}

export function getRequest(url) {
  const request = api.get(url);
  return request;
}

export function putRequest(url, payload) {
  const request = api.put(url, payload);
  return request;
}

export function deleteRequest(url) {
  const request = api.delete(url);
  return request;
}

export function loadData(url, target, is_loading) {
  const $q = useQuasar();

  api
    .get(url, config)
    .then((response) => {
      target.value = response.data;
      if (typeof is_loading !== "undefined") {
        is_loading.value = false;
      }
    })
    .catch((reason) => {
      console.log(reason);
      console.log($q);
      $q.notify({
        color: "negative",
        position: "top",
        message: "Loading failed",
        icon: "report_problem",
      });
    });
}

export function setDevice(deviceid, state, brightness) {
  let url = `api/devices/${deviceid}/`;
  let payload = { state: state };

  if (typeof brightness !== "undefined") {
    payload.brightness = brightness;
  }

  console.log(payload);
  api.put(url, payload).then((response) => {
    console.log(response);
  });
}
