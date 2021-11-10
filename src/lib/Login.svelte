<script>
  import { auth } from "../../firebase.js";
  import { signInAnonymously } from "firebase/auth";
  import { authState } from "rxfire/auth";
  import { userStatus } from "../stores";
  // let user_status;
  // const unsubscribe = authState(auth).subscribe((u) => (user_status = u));

  let user;
  const unsubscribe = authState(auth).subscribe((u) => {
    user = u;
    console.log("user = u");
    userStatus.set(user);
    console.log("userStatus initial", { userStatus });
  });
  function login() {
    signInAnonymously(auth);
  }
</script>

<main>
  {#if user}
    <button
      type="button"
      class="btn btn-dark"
      on:click={() => {
        console.log("clicked logout");
        auth.signOut();
        // userStatus.set(user);
        console.log("userStatus logout", { userStatus });
      }}>Logout</button
    >
    <hr />
  {:else}
    <button type="button" class="btn btn-dark" on:click={login}>
      Sign In Anonymously
    </button>
  {/if}
</main>
