<script>
  import { storage, db } from "../firebase.js";
  import { userStatus } from "./stores";

  import {
    ref,
    uploadBytes,
    uploadBytesResumable,
    getDownloadURL,
  } from "firebase/storage";
  import { doc, setDoc, addDoc, collection } from "firebase/firestore";

  let loading = false;
  let newAudio = null;
  let recorder = null;

  let uploadStatus = "";

  let user_status;
  userStatus.subscribe((value) => {
    user_status = value;
  });

  async function record() {
    newAudio = null;

    const stream = await navigator.mediaDevices.getUserMedia({
      audio: true,
      video: false,
    });

    const options = { mimeType: "audio/webm" };
    const recordedChunks = [];
    recorder = new MediaRecorder(stream, options);

    recorder.addEventListener("dataavailable", (e) => {
      if (e.data.size > 0) {
        recordedChunks.push(e.data);
      }
    });

    recorder.addEventListener("stop", () => {
      newAudio = new Blob(recordedChunks, { type: "audio/wav" });
      console.log(newAudio);
    });

    recorder.start();
  }

  async function stop() {
    recorder.stop();
    recorder = null;
  }

  function createDownloadLink(blob) {
    console.log(blob);
  }

  // upload audio to Firebase storage and get download url
  async function upload() {
    if (newAudio) {
      const storageRef = ref(
        storage,
        "audio/" + user_status.uid + "/" + Date.now().toString()
      );
      const metadata = {
        contentType: "audio/wav",
      };
      const uploadTask = uploadBytesResumable(storageRef, newAudio, metadata);
      // 'file' comes from the Blob or File API
      // uploadBytes(storageRef, newAudio).then((snapshot) => {
      //   console.log("Uploaded a blob or file!");
      //   uploadStatus = "Uploaded the audio!";
      // });

      // Register three observers:
      // 1. 'state_changed' observer, called any time the state changes
      // 2. Error observer, called on failure
      // 3. Completion observer, called on successful completion
      uploadTask.on(
        "state_changed",
        (snapshot) => {
          // Observe state change events such as progress, pause, and resume
          // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
          const progress =
            (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
          console.log("Upload is " + progress + "% done");
          switch (snapshot.state) {
            case "paused":
              console.log("Upload is paused");
              break;
            case "running":
              console.log("Upload is running");
              break;
          }
        },
        (error) => {
          // Handle unsuccessful uploads
        },
        () => {
          // Handle successful uploads on complete
          // For instance, get the download URL: https://firebasestorage.googleapis.com/...
          getDownloadURL(uploadTask.snapshot.ref).then((downloadURL) => {
            console.log("File available at", downloadURL);
            // upload to audios collection in firestore
            saveURL(downloadURL);
          });
        }
      );
    }
  }

  async function saveURL(downloadURL) {
    const currTime = Date.now();
    const newAudioURL = await addDoc(collection(db, "audio"), {
      createdAt: currTime,
      audioURL: downloadURL,
    });
    console.log("newAudioURL", newAudioURL);

    triggerCloudFunction(currTime, downloadURL);

    // local testing
    // triggerLocalFunction(downloadURL);
  }

  async function triggerCloudFunction(currTime, downloadURL) {
    console.log("CLOUD triggered");
    const url =
      "https://asia-northeast1-vocal-journal.cloudfunctions.net/parselmouth";
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        createdAt: currTime,
        lastUpdated: currTime, // need to fix later
        audioURL: downloadURL,
        uid: user_status.uid,
        displayName: user_status.displayName,
        label: "",
        notes: "",
      }),
    });
    // console.log(response);
    const data = await response.json();
    // const data = await response.body.values;
    console.log("CLOUD data: ", data);
  }

  async function triggerLocalFunction(downloadURL) {
    console.log("LOCAL triggered");
    // console.log("downloadURL", downloadURL);
    const localURL = "http://127.0.0.1:5001";
    const response = await fetch(localURL, {
      method: "POST",
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        audioURL: downloadURL,
        uid: user_status.uid,
        displayName: user_status.displayName,
      }),
    });
    const data = await response.json();
    console.log("LOCAL data: ", data);
    // const data = await response.body.values;
  }
</script>

<main>
  <h1>Upload</h1>
  <h5>Record Audio</h5>

  {#if !recorder}
    <button on:click={() => record()} class="button is-info"
      >Record Voice</button
    >
  {:else}
    <button on:click={() => stop()} class="button is-danger">Stop</button>
  {/if}

  <br />

  {#if newAudio}
    <audio controls src={URL.createObjectURL(newAudio)} />
    <button type="text" on:click={() => upload()}>Send</button>
  {/if}

  <div>{uploadStatus}</div>

  <hr />
</main>
