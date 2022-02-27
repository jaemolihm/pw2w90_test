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

### Library mode
* To run the library mode tests, both the reference (`QE_REF`) and test (`QE_TEST`) QE should be linked to the wannier library. (The instructions below are taken and modified based on https://gitlab.com/QEF/q-e/-/blob/develop/PP/examples/WAN90_example/README)
  1. Type `make lib` in the Wannier90 root directory.
  2. In the QE root directory, run `./configure` and modify `make.inc` as follows:
    * Add `-D__WANLIB` to the `MANUAL_DFLAGS` variable
    * Add a new variable `WANLIB` to specify location of Wannier library: `WANLIB = -L/path/wannier90 -lwannier`
    * Add `$(WANLIB)` to the `QELIBS` variable: `QELIBS = $(MBD_LIBS) ... $(WANLIB)`
  3. Compile QE
* I had to change `character(len=*)` in line 83 of `wannier_lib.F90` to `character(len=3)` to make QE run. I do not understand why this change is needed...

### Code coverage
* To compute the coverage, follow these steps. Note that you should use GNU compilers.
  1. Add `-fprofile-arcs -ftest-coverage` to the compilation command and add `-lgcov --coverage` to the linking command (only for `pw2wannier90`). Compile the program.
  2. Run tests.
    * To obtain coverage for reference QE, one needs to set `GENERATE_REFERENCE=true`
  3. Go to directory `coverage` and run `./create_coverage.sh`.
  4. Inspect `output/index.html`.
* Code coverage for my refactoring of pw2wannier90.x (https://gitlab.com/jmlihm/q-e/-/tree/pw2wan) is available here.
  * [ref QE](https://raw.githack.com/jaemolihm/pw2w90_test/master/coverage/output_ref/src/pw2wannier90.f90.gcov.html) (QE develop branch as of 2021.11.23)
  * [new QE](https://raw.githack.com/jaemolihm/pw2w90_test/master/coverage/output/src/pw2wannier90.f90.gcov.html) (my refactoring of pw2wannier90.x (https://gitlab.com/jmlihm/q-e/-/tree/pw2wan))
  * [new QE serial](https://raw.githack.com/jaemolihm/pw2w90_test/master/coverage/output_serial/src/pw2wannier90.f90.gcov.html) (my refactoring of pw2wannier90.x compiled without MPI (https://gitlab.com/jmlihm/q-e/-/tree/pw2wan))
  * The source HTML file is `coverage/output/index.html` and `coverage/output_ref/index.html`.


### Notes
* Requires python3 and python3 modules fortio and termcolor.
* I cound not run library mode with gcc (even after the change noted above) due to the error:
```
Program received signal SIGSEGV: Segmentation fault - invalid memory reference.

Backtrace for this error:
#0  0x7f081d03e2ed in ???
#1  0x7f081d03d503 in ???
#2  0x7f081c49bf1f in ???
#3  0x7f081c5ebcf4 in ???
#4  0x55714363e11a in wannier_setup_
  at ../wannier_lib.F90:114
#5  0x55714308213b in setup_nnkp_
  at /home/jmlihm/program/qe-dev-gcc/PP/src/pw2wannier90.f90:605
#6  0x5571430a6e4d in pw2wannier90
  at /home/jmlihm/program/qe-dev-gcc/PP/src/pw2wannier90.f90:470
#7  0x55714306f48e in main
  at /home/jmlihm/program/qe-dev-gcc/PP/src/pw2wannier90.f90:102
```
