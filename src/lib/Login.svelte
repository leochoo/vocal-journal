<script>
  import { auth } from "../../firebase.js";
  import { signInAnonymously } from "firebase/auth";
  import { authState } from "rxfire/auth";
  import { userStatus } from "../stores";

  let user_status;
  userStatus.subscribe((value) => {
    user_status = value;
  });

  let user;
  const unsubscribe = authState(auth).subscribe((u) => {
    user = u;
    console.log("user = u");
    userStatus.set(user);
    console.log("userStatus initial", { user_status });
  });
  function login() {
    signInAnonymously(auth);
  }
</script>

<main>
  {#if user_status}
    <button
      type="button"
      class="btn btn-dark"
      on:click={() => {
        console.log("clicked logout");
        auth.signOut();
        // userStatus.set(user);
        console.log("userStatus logout", { user_status });
      }}>Logout</button
    >
    <hr />
  {:else}
    <button type="button" class="btn btn-dark" on:click={login}>
      Sign In Anonymously
    </button>
  {/if}
</main>
