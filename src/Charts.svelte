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
  import { db } from "../firebase.js";

  let audioList = [];
  const q = query(
    collection(db, "audio"),
    // where("owner", "==", uid),
    orderBy("createdAt", "desc")
  );
  const unsubscribe = onSnapshot(q, (querySnapshot) => {
    var audios = [];
    querySnapshot.forEach((doc) => {
      const audioObject = {
        createdAt: doc.data().createdAt,
        audioURL: doc.data().audioURL,
      };
      audios = [...audios, audioObject];
      audioList = audios;
    });
  });

  // grab analysis data from firestore
  let analysisList = [];
  const analysisQuery = query(collection(db, "analysis"));
  const unsubscribe2 = onSnapshot(analysisQuery, (querySnapshot) => {
    var _analysis = [];
    querySnapshot.forEach((doc) => {
      const analysisObject = {
        id: doc.id,
        jitter: doc.data().jitter_local,
        shimmer: doc.data().shimmer_local,
        hnr: doc.data().HNR,
      };
      _analysis = [..._analysis, analysisObject];
      analysisList = _analysis;
    });
  });

  let plotHeader = "Jitter";

  let data = [
    {
      x: ["user1", "user2", "user3"],
      y: [0.1, 0.2, 0.3],
      type: "bar",
    },
  ];

  onMount(() => {
    let plotDiv = document.getElementById("plotDiv");
    Plotly.newPlot(plotDiv, data, {}, { showSendToCloud: true });
  });
</script>

<main>
  <h1>Charts</h1>
  <p>Audio file list</p>
  <ul>
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

    <p>Graphs</p>
    <div id="plotly">
      <div>
        <h1>{plotHeader}</h1>
      </div>
      <div id="plotDiv" />
    </div>
  </ul>
</main>
