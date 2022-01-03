<script>
  import Plotly from "plotly.js-dist";
  import { onMount } from "svelte";
  import {
    collection,
    addDoc,
    doc,
    query,
    where,
    onSnapshot,
    orderBy,
  } from "firebase/firestore";
  import { db } from "../../firebase.js";
  import { userStatus } from "../stores";

  let user_status;
  userStatus.subscribe((value) => {
    user_status = value;
  });

  // let audioList = [];
  // const q = query(
  //   collection(db, "audio"),
  //   // where("owner", "==", uid),
  //   orderBy("createdAt", "desc")
  // );
  // const unsubscribe2 = onSnapshot(q, (querySnapshot) => {
  //   var audios = [];
  //   querySnapshot.forEach((doc) => {
  //     const audioObject = {
  //       createdAt: doc.data().createdAt,
  //       audioURL: doc.data().audioURL,
  //     };
  //     audios = [...audios, audioObject];
  //     audioList = audios;
  //   });
  // });

  // grab analysis data from firestore
  let analysisList = [];

  const analysisQuery = query(
    collection(db, "analysis"),
    where("uid", "==", user_status.uid)
    // orderBy("createdAt", "desc")
  );
  const unsubscribe = onSnapshot(analysisQuery, (querySnapshot) => {
    var _analysis = [];
    querySnapshot.forEach((doc) => {
      const analysisObject = {
        displayName: doc.data().displayName,
        jitter: doc.data().jitter_local,
        shimmer: doc.data().shimmer_local,
        hnr: doc.data().HNR,
      };

      // check if an object with the same displayName already exists
      const index = _analysis.findIndex(
        (obj) => obj.displayName === analysisObject.displayName
      );
      // if it exists, skip it, else append data to array
      if (index === -1) {
        _analysis = [..._analysis, analysisObject];
      }
    });
    analysisList = _analysis;
    console.log("_analysis", _analysis);
    updatePlot();
  });

  function updatePlot() {
    console.log("updatePlot");
    // extract jsh into arrays
    let displayNameList = [];
    let jitterList = [];
    let shimmerList = [];
    let hnrList = [];

    analysisList.forEach((analysis) => {
      displayNameList = [...displayNameList, analysis.displayName];
      jitterList = [...jitterList, analysis.jitter];
      shimmerList = [...shimmerList, analysis.shimmer];
      hnrList = [...hnrList, analysis.hnr];
    });

    // drawspecific plot for jitter, shimmer, and hnr
    drawSpecificPlot(displayNameList, jitterList, "jitterDiv");
    drawSpecificPlot(displayNameList, shimmerList, "shimmerDiv");
    drawSpecificPlot(displayNameList, hnrList, "hnrDiv");
  }

  function drawSpecificPlot(xList, yList, parameterDivString) {
    let data = [
      {
        x: xList,
        y: yList,
        type: "bar",
      },
    ];
    let targetDiv = document.getElementById(parameterDivString);
    Plotly.react(targetDiv, data, {}, { showSendToCloud: true });
  }

  // $: {

  //   Plotly.newPlot(plotDiv, data, {}, { showSendToCloud: true });
  // }

  onMount(() => {
    console.log("onMount render");
  });
</script>

<main>
  <h1>My Plots</h1>
  <!-- <p>Audio file list</p> -->
  <!-- <ul>
    {#each audioList as audio}
      <li>{audio.audioURL}</li>
    {/each}
  </ul>
  <p>Analysis data</p>
  <ul>
    {#each analysisList as analysis}
      <li>User: {analysis.id}</li>
      <ul>
        <li>Jitter: {analysis.jitter}</li>
        <li>Shimmer: {analysis.shimmer}</li>
        <li>HNR: {analysis.hnr}</li>
      </ul>
    {/each}
  </ul> -->
  <div id="plotly">
    <h3>Jitter</h3>
    <div id="jitterDiv" />
    <h3>Shimmer</h3>
    <div id="shimmerDiv" />
    <h3>HNR</h3>
    <div id="hnrDiv" />

    <!-- <div bind:this={plotDiv} /> -->
    <!-- <JshPlot data={analysisList} /> -->
  </div>
</main>
