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

  export let plotHeader = "";

  export let data = [
    {
      x: ["giraffes", "orangutans", "monkeys"],
      y: [20, 14, 23],
      type: "bar",
    },
  ];

  onMount(() => {
    let plotDiv = document.getElementById("plotDiv");
    let Plot = new Plotly.newPlot(plotDiv, data, {}, { showSendToCloud: true });

    var TESTER = document.getElementById("tester");
    Plotly.newPlot(
      TESTER,
      [
        {
          x: [1, 2, 3, 4, 5],
          y: [1, 2, 4, 8, 16],
        },
      ],
      {
        margin: { t: 0 },
      }
    );
  });
</script>

<main>
  <h1>Charts</h1>
  <ul>
    {#each audioList as audio}
      <li>{audio.audioURL}</li>
    {/each}
  </ul>
  <div id="tester" style="width:600px;height:250px;" />
  <div id="plotly">
    <div>
      <h1>{plotHeader}</h1>
    </div>
    <div id="plotDiv"><!-- Plotly chart will be drawn inside this DIV --></div>
  </div>
</main>
