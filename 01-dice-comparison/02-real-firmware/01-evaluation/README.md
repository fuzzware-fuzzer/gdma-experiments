# README
This directory contains the necessary files for the actual evaluation of DICE and P2IM. 
The assumption is that you already loaded (or built) the docker with the tag `dice_tag`. 

# Running the evaluation
To run the evaluation just run the `build_docker.sh` script. It will copy the `config.txt` to the `dice_tag` docker and kick of the `do_eval.sh` script in the docker, which loads the configuration and starts fuzzing.

After fuzzing the `do_eval.sh` script calculates the coverage results and moves everything to the directory `p2im_dice_results` which is mounted in the docker (when the evaluation has terminated you can find the collected results in there.)

The `build_docker.sh` script then proceeds to rename the results to fit with the target names from Fuzzware, and moves all `out.txt` files, which contain the plotting information to `../02-results`. This overwrites any previous results stored there.

# Config format
To allow for a flexible configuration regarding the duration, fuzzing iterations and available cores we opted for a simple configuration format:
```
<Runtime>
<Number of cores available>
<Iterations>
<Target1>
...
<TargetN>
```

By default a configuration, which runs every target 10 times for 24 hours on 50 cores is loaded. If you run the DICE/P2IM evaluation standalone, you need to adapt the configuration to your liking. `./config-presets` contains some default configs. 

When you run the evaluation from the toplevel script, this is done automatically.
