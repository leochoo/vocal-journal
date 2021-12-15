<script>
  import { onMount } from "svelte";
  import Plotly from "plotly.js-dist";

  export let data;
  console.log(data);
  let plotHeader = "PlotHeader";
  onMount(async () => {
    console.log("data", data);
    console.log("onMount");
    let plotDiv = document.getElementById("plotDiv");
    Plotly.newPlot(plotDiv, data, {}, { showSendToCloud: true });
  });
</script>

<main>
  <div id="plotDiv" style="width:100%; height:100%;" />
</main>
