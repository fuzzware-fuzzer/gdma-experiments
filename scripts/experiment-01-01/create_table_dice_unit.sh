sudo chmod 777 /home/user/
pip install latextable texttable
python3 scripts/experiment-01-01/create_table.py --dice-file 01-dice-comparison/DICE-results/ground_truth_dice_perspective.yml --groundtruth 01-dice-comparison/01-unit-tests/ground_truth.yml --gpdma-run $@
