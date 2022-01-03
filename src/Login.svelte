<script>
  import { auth } from "../firebase.js";
  import {
    signInAnonymously,
    GoogleAuthProvider,
    signInWithPopup,
  } from "firebase/auth";
  import { authState } from "rxfire/auth";
  import { userStatus } from "./stores";
  import { db } from "../firebase";
  import {
    collection,
    addDoc,
    query,
    where,
    getDoc,
    updateDoc,
    doc,
    setDoc,
  } from "firebase/firestore";

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

  async function googleLogin() {
    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);
    addUser(result.user);
  }

  async function addUser(user) {
    const userRef = doc(db, "users", user.uid);
    const docSnap = await getDoc(userRef);
    if (docSnap.exists()) {
      await updateDoc(userRef, {
        updatedAt: new Date(),
      });
      console.log("Updated user info");
    } else {
      await setDoc(userRef, {
        displayName: user.displayName,
        email: user.email,
        photoURL: user.photoURL,
        uid: user.uid,
        createdAt: new Date(),
        updatedAt: new Date(),
      });
      console.log("New User to firestore");
    }
  }

  async function logout() {
    console.log("log out");
    await auth.signOut();
  }
</script>

<main>
  {#if user_status}
    <button type="button" class="btn btn-dark" on:click={logout}>Logout</button>
    <hr />
  {:else}
    <!-- <button type="button" class="btn btn-dark" on:click={anonymousLogin}>
      Sign In Anonymously
    </button> -->
    <img
      on:click={googleLogin}
      src="./src/assets/btn_google_signin_dark_normal_web@2x.png"
      alt="Google Login"
      id="glogin"
    />
  {/if}
</main>
