<script lang="ts">
  import logo from "./assets/svelte.png";
  import Dashboard from "./Dashboard.svelte";
  import Upload from "./Upload.svelte";
  import Charts from "./Charts.svelte";
  import Login from "./Login.svelte";
  import { Router, Link, Route } from "svelte-routing";
  import { userStatus } from "./stores";
  import AccessDenied from "./AccessDenied.svelte";
  import {
    Dropdown,
    DropdownItem,
    DropdownMenu,
    DropdownToggle,
  } from "sveltestrap";

  let user_status;
  userStatus.subscribe((value) => {
    user_status = value;
  });
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
  />
</svelte:head>

<Router>
  <main>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <Link class="navbar-brand" to="">Vocal Journal</Link>
        <!-- <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarColor01"
          aria-controls="navbarColor01"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon" />
        </button> -->
        <Dropdown>
          <DropdownToggle caret>Dropdown</DropdownToggle>
          <DropdownMenu>
            <!-- <DropdownItem header>Header</DropdownItem> -->
            <!-- <DropdownItem>Some Action</DropdownItem> -->
            <!-- <DropdownItem disabled>Action (disabled)</DropdownItem> -->
            <!-- <DropdownItem divider /> -->
            <DropdownItem>Dashboard</DropdownItem>
            <DropdownItem>Upload</DropdownItem>
            <DropdownItem>Charts</DropdownItem>
          </DropdownMenu>
        </Dropdown>

        <div class="collapse navbar-collapse" id="navbarColor01">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <Link class="nav-link active" to="/"
                >Dashboard
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
          <Login />
          <!-- <form class="d-flex">
            <input
              class="form-control me-sm-2"
              type="text"
              placeholder="Search"
            />
            <button class="btn btn-dark my-2 my-sm-0" type="submit"
              >Search</button
            >
          </form> -->
        </div>
      </div>
    </nav>
    <div class="container">
      {#if user_status}
        <div>user_status: {user_status.displayName}</div>
        <Route path="upload" component={Upload} />
        <Route path="charts" component={Charts} />
        <Route path="/"><Dashboard /></Route>
      {:else}
        <!-- <Route path="/" component={Login} /> -->
        <Route path="/" component={AccessDenied} />
      {/if}
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
