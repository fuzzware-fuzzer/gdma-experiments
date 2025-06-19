# GDMA-Experiments 
This repository contains the artifacts to reproduce the evaluation for the paper **GDMA: Fully Automated DMA Rehosting via Iterative Type Overlays**.

# Directory Layout
| Subdirectory   | Section  | Experiment | Description |
| -------------- | -------- | -----------| ----------- |
| [01-dice-comparison/01-unit-tests/](01-dice-comparison/01-unit-tests/)       | 6.4 | Evaluation of GDMA on DICE Unit tests | Evaluate if GDMA performs at least as good as DICE on the DICE Unit tests (Table 7)|
| [01-dice-comparison/02-real-firmware/](01-dice-comparison/02-real-firmware/) | 6.4 | Evaluation of GDMA on DICE Coverage tests | Compare coverage improvement of GDMA over Fuzzware with coverage improvement of DICE over P2IM (Figure 7) |
| [02-extended-test-suite/](02-extended-test-suite/) | 6.2/6.3 | Evaluation of GDMA on Diverse Dataset | Investigate if GDMA can successfully find all 6 types of DMA |
| [03-coverage-experiments/](03-coverage-experiments/) | 6.5 | GDMA fuzzing performance on Example Applications | Investigation of coverage improvement of GDMA (Figure 6)|
| [04-finding-new-bugs/](04-finding-new-bugs/) | 6.6 | Bug Case Studies | GDMA fuzzing Contiki-NG and MbedOS for new bugs |
| [05-false-positive/](05-false-positive/) | 6.3 | False Positive Analysis on P2IM Unit Tests | Rehost all P2IM Unit Tests to check if GDMA mistakenly identifies DMA in one of the samples |
| [src](src) | 6.2 |  Source directory for all targets | The subdirectories in this directory contain the required files and instructions to rebuild / obtain the targets that are part of the fuzzing campaigns.

# Setup
## Install docker
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
sudo groupadd docker
sudo usermod -aG docker $USER
```

Now reboot

## Install other dependencies

Tools:
```
sudo apt-get install curl ca-certificates patchelf texinfo automake gcc zstd pip zip python3-venv
```

Fuzzware with GDMA (with docker installed):
```
git clone --recurse-submodules -b DMA https://github.com/fuzzware-fuzzer/fuzzware.git

cd fuzzware && ./build_docker.sh
```

## Prepare the system for fuzzing
```
sudo su
echo 512 > /proc/sys/fs/inotify/max_user_instances
echo 524288 > /proc/sys/fs/inotify/max_user_watches
echo core >/proc/sys/kernel/core_pattern
cd /sys/devices/system/cpu
echo performance | tee cpu*/cpufreq/scaling_governor
exit
```

# Quick start
```
./eval-recommended.sh
```
This takes around 11 days to complete (if you have 26 cores).

# Checking for progress
The fuzzing campaign consumes most of the required evaluation time.
To inspect progress, check the directory of the experiment (e.g. `02-extended-test-suite/` or `01-dice-comparison/02-real-firmware/`)
If it contains an `output` folder, then the fuzzer has at least started there. 
If the next experiment also contains an `output` folder, then the fuzzer has completed the previous experiment.

# Detailed setup/manual configuration

## Running the experiments
All experiments are run from the `scripts/` directory.
Install `requirements.txt`, then use `python cli.py --help` to check your options.

## Full evaluation + Fuzzing campaign
If you want to fully reproduce our results, the easiest way is to execute one of our wrapper scripts in the `scripts` directory, e.g. `rerun_experiments_24h_10runs.sh`.
This performs a fuzzing campaign on all targets and automatically evaluates the results, placing them in the `results` directory.

## Rebuilding the new samples (Diverse Dataset/Example Applications)
Execute `python cli.py build-2/build-3 --help` to check your options for rebuilding the Diverse Dataset.
### Requirements
Install docker and add your user to the docker group.
Install the following dependencies:
`docker, curl, ca-certificates, patchelf, texinfo,automake, gcc, zstd, pip, zip, python3-venv`
All experiments tested on Ubuntu 22.04

You can rebuild the diverse dataset in one of two ways:
1. Using the IDEs
2. Using docker saves

#### Using the IDEs
This requires you to download `ModusToolbox_3.2.0.16028-linux-install.deb` from Cypress/Infineon and `mcuxpressoide-11.10.0_3148.x86_64.deb.bin` from NXP and place them in the `ides` folder.

#### Using docker saves
This requires you to download the docker saves that we provide and unpack them in the `docker-saves` directory.
 
### Building the samples
Now that you have the required files, you can build the samples. 
1. Using IDEs: `python cli.py build-2/build-3`
1. Using docker: `python cli.py build-2/build-3 -d`

### Expected results
You should get one sample per target.
Investigate if they differ from the provided firmware with `python cli.py update-2/update-3 -pd`.
Use `python cli.py update-2/update-3 -u` to move them to use them for evaluation.

## Rerunning DICE on the DICE Fuzzing targets.
Similar to above, this comes in two flavors:
1. From scratch
2. Using docker saves

Execute `python cli.py run-dice` to build everything from scratch. 
If you want to use an existing `dice_docker.tar.zstd`, place it in the `docker-saves` folder and execute `python cli.py run-dice -d`.

# Adapting the evaluation
If you want to run parts of the evaluation individually, the easiest way is to use the various options of the `cli.py` script in the `scripts` directory.
Execute a sub-option with `--help` to get infos about flags and default values.

`cli.py` can configure everything, except for the fuzzing campaign parameters.
If you want to use a custom configuration for the GDMA fuzzing campaigns, modify `.experiments-config.yml` to your needs.
You need to run `python cli.py run-experiments -r` (note the `-r`) to run with updated configurations.

You need to edit `01-dice-comparison/02-real-firmware/01-evaluation/config.txt` to configure the fuzzing campaign parameters of any DICE reruns.

