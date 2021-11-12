<script>
  import { storage } from "../../firebase.js";
  import { ref, uploadBytes } from "firebase/storage";

  let loading = false;
  let newAudio = null;
  let recorder = null;

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
      newAudio = new Blob(recordedChunks);
      console.log(newAudio);
    });

    recorder.start();
  }
  async function stop() {
    recorder.stop();
    recorder = null;
  }

  // upload audio to Firebase storage and get download url
  async function upload() {
    if (newAudio) {
      const storageRef = ref(storage, "audio");

      // 'file' comes from the Blob or File API
      uploadBytes(storageRef, newAudio).then((snapshot) => {
        console.log("Uploaded a blob or file!");
      });

      // const uploadTask = storageRef.child(new Date().getTime()).put(newAudio);
      // uploadTask.on(
      //   "state_changed",
      //   (snapshot) => {
      //     // Observe state change events such as progress, pause, and resume
      //     // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
      //     const progress =
      //       (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
      //     console.log("Upload is " + progress + "% done");
      //     switch (snapshot.state) {
      //       case "paused": // or 'paused'
      //         console.log("Upload is paused");
      //         break;
      //       case "running": // or 'running'
      //         console.log("Upload is running");
      //         break;
      //     }
      //   },
      //   (error) => {
      //     // Handle unsuccessful uploads
      //     console.log(error);
      //   },
      //   () => {
      //     // Handle successful uploads on complete
      //     // For instance, get the download URL: https://firebasestorage.googleapis.com/...
      //     uploadTask.snapshot.ref.getDownloadURL().then((downloadURL) => {
      //       console.log("File available at", downloadURL);
      //       document.getElementById("audio-url").value = downloadURL;
      //     });
      //   }
      //   );
      // }
    }
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
  {/if}

  <hr />

  <button type="text" on:click={() => upload()}>Send</button>
</main>
