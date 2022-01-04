<script>
  import JshPlot from "./components/MyPlots.svelte";
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

  // grab analysis data from firestore
  let analysisList = [];

  const analysisQuery = query(
    collection(db, "analysis"),
    orderBy("createdAt", "desc")
  );
  const unsubscribe = onSnapshot(analysisQuery, (querySnapshot) => {
    var _analysis = [];
    querySnapshot.forEach((doc) => {
      const analysisObject = {
        createdAt: doc.data().createdAt,
        audioURL: doc.data().audioURL,
        uid: doc.data().uid,
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
      // _analysis = [..._analysis, analysisObject];
    });
    analysisList = _analysis;
    console.log("_analysis", _analysis);
    updatePlot();
  });

  let min_jitter;
  let max_jitter;

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

    min_jitter = Math.min(...jitterList);
    max_jitter = Math.max(...jitterList);

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
  function format_time(s) {
    const dtFormat = new Intl.DateTimeFormat("en-US", {
      dateStyle: "short",
      timeStyle: "full",
      timeZone: "JST",
    });

    return dtFormat.format(s);
  }

  onMount(() => {
    console.log("onMount render");
  });
</script>

<main>
  <h1>Charts</h1>
  <div id="plotly">
    <h3>Jitter</h3>
    <div id="jitterDiv" />
    <table>
      <tr>
        <th>Created At</th>
        <th>Display Name</th>
        <th>Jitter</th>
      </tr>
      {#each analysisList as analysis}
        <tr>
          <td>{format_time(analysis.createdAt)}</td>
          <td>{analysis.displayName}</td>
          <td>{analysis.jitter}</td>
          <td>
            <audio controls>
              <source src={analysis.audioURL} type="audio/wav" />
            </audio>
          </td>
          <!-- label lowest jitter as best and highest as worst -->
          {#if analysis.jitter == min_jitter}
            <td>Best</td>
          {:else if analysis.jitter == max_jitter}
            <td>Worst</td>
          {:else}
            <td />
          {/if}
        </tr>
      {/each}
    </table>
    <h3>Shimmer</h3>
    <div id="shimmerDiv" />
    <h3>HNR</h3>
    <div id="hnrDiv" />

    <!-- <div bind:this={plotDiv} /> -->
    <!-- <JshPlot data={analysisList} /> -->
  </div>
</main>
