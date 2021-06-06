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


### Library mode
* To run the library mode tests, both the reference (`QE_REF`) and test (`QE_TEST`) QE should be linked to the wannier library. (The instructions below are taken and modified based on https://gitlab.com/QEF/q-e/-/blob/develop/PP/examples/WAN90_example/README)
  1. Type `make lib` in the Wannier90 root directory.
  2. In the QE root directory, run `./configure` and modify `make.inc` as follows:
    * Add `-D__WANLIB` to the `MANUAL_DFLAGS` variable
    * Add a new variable `WANLIB` to specify location of Wannier library: `WANLIB = -L/path/wannier90 -lwannier`
    * Add `$(WANLIB)` to the `QELIBS` variable: `QELIBS = $(MBD_LIBS) ... $(WANLIB)`
  3. Compile QE
* I had to change `character(len=*)` in line 83 of `wannier_lib.F90` to `character(len=3)` to make QE run. I do not understand why this change is needed...

TODO: Add readme on cases which are covered. (better: use code coverage tool)
