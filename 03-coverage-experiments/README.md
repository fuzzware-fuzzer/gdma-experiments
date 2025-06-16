# Example applications
In this directory, we evaluate the impact of GDMA on coverage.
To that end, we introduce 2 example applications per type of previously unsupported DMA (Section 6.5).
Each sample uses DMA.

## Quick start
You need a finished fuzzing campaign.
Then run: `./eval-3.sh`

## Running the experiments
Refer to the top level for running the fuzzing campaign.

## Coverage impact
Execute `python3 cli.py eval-3 --runtime 24 --num-runs 10` to plot the coverage of the fuzzing campaign.
Use `--help` to identify optional parameters and default values.

### Expected Results
We expect GDMA to outperform Fuzzware on all targets.
