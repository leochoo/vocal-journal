import { writable } from "svelte/store";

export const userStatus = writable(null);

export const currentUser = writable({
  isLoggedIn: false,
  user: null,
});
