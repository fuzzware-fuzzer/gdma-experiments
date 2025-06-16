# Dice Unit Tests
In this directory, we evaluate the performance of GDMA against DICE on DICE Fuzzing tests.
In particular, we want to know: does GDMA perform at least as good as DICE on the DICE Unit tests (Section 6.4 in the paper)?

## Quick start
You need a finished fuzzing campaign.
Then run: `./eval-1-2.sh`

## Running the experiments
Refer to the top level for running the fuzzing campaign.

## Evaluating the results
Go to `scripts/` and execute `python3 cli.py eval-1-2 --num-runs 10 --runtime 24`.
Adapt the `--num-runs` and `--runtime` flags according to your fuzzing campaign parameters.
This outputs the coverage graphs for GDMA, Fuzzware, P2IM and DICE on the DICE Fuzzing tests.
Use `--help` to identify optional parameters and default values.

## Expected Results
We expect the coverage increase of GDMA over Fuzzware to be similar to the coverage increase of DICE over P2IM.
