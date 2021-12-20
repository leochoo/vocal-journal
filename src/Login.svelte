<script>
  import { auth } from "../firebase.js";
  import {
    signInAnonymously,
    GoogleAuthProvider,
    signInWithPopup,
  } from "firebase/auth";
  import { authState } from "rxfire/auth";
  import { userStatus } from "./stores";

  let user_status;
  userStatus.subscribe((value) => {
    user_status = value;
  });

  let user;
  const unsubscribe = authState(auth).subscribe((u) => {
    user = u;
    userStatus.set(user);
    console.log("user_status subscribed", { user_status });
  });

  async function anonymousLogin() {
    console.log("log in");
    await signInAnonymously(auth);
  }

  async function googleLogin() {
    const provider = new GoogleAuthProvider();
    await signInWithPopup(auth, provider);
  }

  async function logout() {
    console.log("log out");
    await auth.signOut();
  }
</script>

<main>
  {#if user_status}
    hello
    <button type="button" class="btn btn-dark" on:click={logout}>Logout</button>
    <hr />
  {:else}
    <button type="button" class="btn btn-dark" on:click={anonymousLogin}>
      Sign In Anonymously
    </button>
    <img
      on:click={googleLogin}
      src="./src/assets/btn_google_signin_dark_normal_web@2x.png"
      alt="Google Login"
      id="glogin"
    />
  {/if}
</main>
