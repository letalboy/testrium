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
