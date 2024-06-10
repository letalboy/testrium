<div style="display: flex; align-items: center;">
  <img src="https://github.com/letalboy/Spectrum/assets/63066865/cf9c60e7-9eba-474c-8cc1-b246e661fd5c" alt="Logo" width="200" height="200" style="margin-right: 20px;">
  <div>
    <h1>Spectrum</h1>
    <p>Spectrum is a versatile library designed to test and analyze systems like Misny. It provides tools for data processing, monitoring, and ensuring system integrity, making it an essential part of your development workflow.</p>
  </div>
</div>
<div>
    <p>Key points:</p>
    <ul>
        <li>Better Organization Of Tests</li>
        <li>Easy Test Of Async Or Paralelized Dependent Tests</li>
        <li>Historic Performance Comparation and Evaluation</li>
        <li>Allow Custom Behavior Though Callbacks Systems</li>
        <li>Allow Manipulation Of The Test Flows</li>
        <li>High COnfigurable And Expancible</li>
    </ul>
</div>

To use is simple:

1. activate the poetry shell using:

```shell
poetry shell
```

2. go the the test folder and run:

```shell
poetry run spectrum 
```

This should auto collect the test and run them automatically!

---

Base Idea:
- Read the folder of test folders
- Collect each one
- Run them based in the priority config file in the test toml if present
- Create a db to store tests results locally or if configured in the toml then send to a remote server
- Run the tests, save the results
- Compare the results witht he performance of the old tests to see if the test increase or decrese efficience.
- Create a way to evaluate the performance in multiple machines comparing the efficience without issues.

TODO:
- Create a mechanism to add events through a test
    - Events will allow to indentify if we complete the required step
    - Cross events, are events were we want to trace the process from one point to another and how much time it takes to
    this will be able to be done using a structure that generate a event hash for each event so then we can trace it to the 
    other place.