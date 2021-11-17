<script>
  // import Recorder from "./opus-recorder/recorder";
  import Recorder from "opus-recorder";

  // import encoderPath from "opus-recorder/dist/encoderWorker.min.js";

  import { storage, db } from "../firebase.js";
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
  let newWav = null;

  let uploadStatus = "";

  async function record() {
    newAudio = null;
    newWav = null;

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
      newWav = new Blob(recordedChunks, { type: "audio/wav" });
      console.log(newWav);
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
      const storageRef = ref(storage, "audio_" + Date.now().toString());
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
    const newAudioURL = await addDoc(collection(db, "audio"), {
      createdAt: Date.now(),
      audioURL: downloadURL,
    });
    console.log(newAudioURL);
    // trigger cloud function
    testTriggerCloudFunction();
  }

  async function testTriggerCloudFunction() {
    const response = await fetch(
      "http://asia-northeast1-vocal-journal.cloudfunctions.net/function-0"
    );
    // console.log(response);
    const data = await response.json();
    // const data = await response.body.values;
    console.log("data: ", data);
  }

  let monitorGain = 0;
  let recordingGain = 1;
  let numberOfChannels = 1;
  let bitDepth = 16;

  let opusRecorder = null;
  let opusWavBlob = null;

  let opusWavURL = "";

  function recordOpus() {
    opusRecorder = new Recorder({
      monitorGain: monitorGain,
      recordingGain: recordingGain,
      numberOfChannels: numberOfChannels,
      wavBitDepth: bitDepth,
      encoderPath: "public/opus-recorder/encoderWorker.js",
    });

    opusRecorder.start();

    opusRecorder.onstart = () => {
      console.log("recordOpus started");
    };

    opusRecorder.ondataavailable = function (typedArray) {
      var dataBlob = new Blob([typedArray], { type: "audio/wav" });
      var fileName = new Date().toISOString() + ".wav";
      var url = URL.createObjectURL(dataBlob);
      console.log("recordOpus ondataavailable", url);
      opusWavURL = url;
      opusWavBlob = dataBlob;
    };

    console.log(opusRecorder);
  }

  function stopOpus() {
    opusRecorder.stop();
    console.log("recordOpus stopped");
    console.log(opusRecorder);
  }
  async function upload2() {
    if (opusWavBlob) {
      const storageRef = ref(storage, "audio_" + Date.now().toString());
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

  <button type="text" on:click={() => testTriggerCloudFunction()}
    >Test Trigger</button
  >
  <hr />

  <h5>Record Audio with Opus Recorder</h5>
  <button type="text" on:click={() => recordOpus()}>Record</button>
  <button type="text" on:click={() => stopOpus()}>Stop</button>
  <audio controls src={opusWavURL} />
  {#if opusWavBlob}
    <button type="text" on:click={() => upload2()}>Send</button>
  {/if}

  <!-- <button type="text" on:click={() => playOpus()}>Play</button> -->
</main>
