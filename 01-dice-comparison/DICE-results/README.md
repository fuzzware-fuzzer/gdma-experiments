# DICE Unit Test
These are the DICE results of the DICE Unit Test set. The set and the eval scripts are part of the [DICE github repository](https://github.com/RiS3-Lab/DICE-DMA-Emulation/tree/master/DICE-Evaluation/ARM/Unit-Test).  
To replicate download the repository, set everything up, apply the the patch from below and use the `runbatch.py` script to run the evalutation.  

Furthermore I added two files: `stream_configs.txt` and `buffer_accesses.txt`, which contain information on the stream configurations extracted by DICE and all detected buffer accesses for each sample.
This information is part of each target specific file in the dma_trace directory.
To replicate these files either grep for `DMA Stream configuration identified` (stream_configs.txt) or `Access to` (buffer_accesses.txt).



# Patches
```
diff --git a/DICE-Evaluation/ARM/Unit-Test/runbatch.py b/DICE-Evaluation/ARM/Unit-Test/runbatch.py
index c27d544..f192b74 100755
--- a/DICE-Evaluation/ARM/Unit-Test/runbatch.py
+++ b/DICE-Evaluation/ARM/Unit-Test/runbatch.py
@@ -20,7 +20,7 @@ from os import getcwd
 from os.path import isfile, join
 import subprocess

-firmpath="./firmware"
+firmpath="./Firmware/Binaries-DICE"
 runpath = getcwd()+"/run.py"
 out_path = "./revision2"

@@ -38,4 +38,4 @@ for f in files:
         if key in f:
             print("Processing: {}".format(f) )
             subprocess.call([runpath, mcu, firmpath +"/"+f, out_path])
-           break
+            break
```




