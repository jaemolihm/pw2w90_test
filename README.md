# pw2w90\_test
Test suite for pw2wannier90.x program of Quantum ESPRESSO.

### How to run the tests
* Modify file `environment_variables` (program paths and run commands)
  * In the first run, set `GENERATE_REFERENCE` to true to generate reference data.
  * In later runs, set `GENERATE_REFERENCE` to false to skip reference data generation.
* Run tests by `./run_tests.sh`
  * All tests (except library mode test) are run by default
  * Specific tests can be run by passing the folder names (e.g. `./run_tests.sh fe gaas`)
  * SCDM tests can be run by calling `./run_tests.sh scdm`)

### Notes
* Requires python3 and python3 modules fortio and termcolor.
