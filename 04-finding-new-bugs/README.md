# 04 Finding new Bugs

Experiments showing that DMA modeling can uncover bugs that where previously not known (Section 6.6).
Two different firmware targets where tested:
1. Contiki-NG 6LoWPAN stack
2. MbedOS Bluetooth via HCI commands

## Quick start
You need a finished fuzzing campaign.
Then run: `./eval-4.sh`

## Time to Crash
This table describes the computation resources that where required to generate the first crash.
The runs used a manual generic configuration.

| Target | # Fuzzing Instances | Seconds until Crash |
| ------ | ------------------- | ------------------- |
| CVE-2023-48229 |           1 |                1500 |
| CVE-2024-48981 |           5 |                3540 |
| CVE-2024-48982 |          10 |              103080 |
| CVE-2024-48983 |          10 |                2700 |
| CVE-2024-48985 |           5 |                3300 |
| CVE-2024-48986 |          10 |               39600 |

## Bug Descriptions

| CVE Identifier | Software | Version | Description |
| -------------- | -------- | ------- | ----------- |
| CVE-2023-48229 | Contiki-NG |    <= 4.9 | Out of bounds write while reading a IEEE 802.15.4 frame. |
| CVE-2024-48981 |    Mbed-OS | <= 6.17.0 | Out of bounds write due to missing size validation of HCI frames. |
| CVE-2024-48982 |    Mbed-OS | <= 6.17.0 | Integer wrap around leading to out of bounds write while reading HCI frames. |
| CVE-2024-48983 |    Mbed-OS | <= 6.17.0 | Integer overflow leading to out of bounds write while allocating memory. |
| CVE-2024-48985 |    Mbed-OS | <= 6.17.0 | Missing error handling after failed allocation leading to out of bounds write. |
| CVE-2024-48986 |    Mbed-OS | <= 6.17.0 | The dynamically sized data field in HCI vendor specific event is not considered. This leads to an insufficiently large buffer being allocated and the following copy operation creates an out of bounds write. |

## Running the reproducers
Relying on the fuzzer to find the bugs again is unreliable, in particular for the longer-running targets.
Instead, we provide reproducing environments for all bugs, in the form of the GDMA models at that point plus input that triggers the bug.
You can find these reproduction environments in the `reproducer` folder of each target.
To confirm that these reproducing environments indeed crash the firmware, execute `python3 cli.py eval-4`.
Use `--help` to identify optional parameters and default values.

### Expected Results
All reproducers crash the respective targets.

## Manual investigation
For 2 targets, we provide specially-crafted configurations that print `Heureka` to the log if the specific conditions of the bug are triggered.
Run `python cli.py eval-4-hooks` to run these special configurations.

### Expected Results
`Heureka` is printed to GDMA logs, and the script reports finding it.
