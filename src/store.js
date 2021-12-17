import { writable } from "svelte/store";

export const currentUser = writable({
  isLoggedIn: false,
  user: null,
});
