const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/IndexPage.vue") }],
  },
  {
    path: "/devices",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/DevicesPage.vue") }],
  },
  {
    path: "/rooms",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/RoomsPage.vue") }],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
