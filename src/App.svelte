<script lang="ts">
  import "bootswatch/dist/litera/bootstrap.min.css";
  import logo from "./assets/svelte.png";
  import Counter from "./lib/Counter.svelte";
  import Home from "./lib/Home.svelte";
  import Upload from "./lib/Upload.svelte";
  import Charts from "./lib/Charts.svelte";
  import { Router, Link, Route } from "svelte-routing";
</script>

<Router>
  <main>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <Link class="navbar-brand" to="">Vocal Journal</Link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarColor01"
          aria-controls="navbarColor01"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon" />
        </button>

        <div class="collapse navbar-collapse" id="navbarColor01">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <Link class="nav-link active" to="/"
                >Home
                <span class="visually-hidden">(current)</span>
              </Link>
            </li>
            <li class="nav-item">
              <Link class="nav-link" to="upload">Upload</Link>
            </li>
            <li class="nav-item">
              <Link class="nav-link" to="charts">Charts</Link>
            </li>
          </ul>
          <form class="d-flex">
            <input
              class="form-control me-sm-2"
              type="text"
              placeholder="Search"
            />
            <button class="btn btn-dark my-2 my-sm-0" type="submit"
              >Search</button
            >
          </form>
        </div>
      </div>
    </nav>
    <div>
      <Route path="upload" component={Upload} />
      <Route path="charts" component={Charts} />
      <Route path="/"><Home /></Route>
    </div>
  </main>
</Router>

<style>
  :root {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  }

  main {
    text-align: center;
    margin: 0 auto;
  }

  img {
    height: 16rem;
    width: 16rem;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4rem;
    font-weight: 100;
    line-height: 1.1;
    margin: 2rem auto;
    max-width: 14rem;
  }

  p {
    max-width: 14rem;
    margin: 1rem auto;
    line-height: 1.35;
  }

  @media (min-width: 480px) {
    h1 {
      max-width: none;
    }

    p {
      max-width: none;
    }
  }
</style>
