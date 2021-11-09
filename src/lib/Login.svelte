<script>
  import { auth } from "../../firebase.js";
  import { signInAnonymously } from "firebase/auth";
</script>

<main>
  <button
    type="button"
    class="btn btn-dark"
    on:click={() => signInAnonymously(auth)}>Sign In Anonymously</button
  >
</main>
