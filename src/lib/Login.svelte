<script>
  import { auth } from "../../firebase.js";
  import { signInAnonymously } from "firebase/auth";
  import { authState } from "rxfire/auth";
  let user;
  const unsubscribe = authState(auth).subscribe((u) => (user = u));
  function login() {
    signInAnonymously(auth);
  }
</script>

<main>
  {#if user}
    <button type="button" class="btn btn-dark" on:click={() => auth.signOut()}
      >Logout</button
    >
    <hr />
  {:else}
    <button type="button" class="btn btn-dark" on:click={login}>
      Sign In Anonymously
    </button>
  {/if}
</main>
