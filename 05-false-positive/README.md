# P2IM Unit Tests
In this directory, we evaluate the false positive rate of GDMA on the P2IM Unit Tests, which all have no DMA mechanism (Section 6.3).

## Quick start
You need a finished fuzzing campaign.
Then run: `./eval-5.sh`

## Running the experiments
Refer to the top level for running the fuzzing campaign.

## Evaluating the results
Go to `scripts/` and execute `python3 cli.py eval-5`.
This checks if any `dma_config.yml` file exists for any target.

### Expected results
We expect no false positives.
