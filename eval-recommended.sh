#! /bin/bash
file_path=$(readlink -f $0)
venv_path=`dirname $file_path`/scripts/venv/
scripts_path=`dirname $file_path`/scripts/
req_path=`dirname $file_path`/scripts/requirements.txt
cli_path=`dirname $file_path`/scripts/cli.py
set -xe

if [ -d "$scripts_path/results/" ]; then
  rm -rf $scripts_path/results
fi
mkdir $scripts_path/results

if [ ! -e "$venv_path/bin/activate" ]; then
  rm -rf "$venv_path"
fi

if [ -d "$venv_path" ]; then
  source "$venv_path/bin/activate"
else
  python3 -m venv "$venv_path"
  source "$venv_path/bin/activate"
  pip install -r "$req_path"
fi


cp $scripts_path/configs/12h-3runs/.experiments-config.yml $scripts_path
cp $scripts_path/configs/12h-3runs/config.txt $scripts_path/../01-dice-comparison/02-real-firmware/01-evaluation/


python3 $cli_path run-experiments -r
python3 $cli_path eval-1-1 > $scripts_path/results/01_unit.txt
python3 $cli_path eval-1-2 --num-runs 3 --runtime 12
python3 $cli_path eval-2 > $scripts_path/results/02.txt
python $cli_path eval-2-fp > $scripts_path/results/02-fp.txt
python3 $cli_path eval-3 --runtime 12 --num-runs 3
python3 $cli_path eval-4 > $scripts_path/results/04.txt
python3 $cli_path eval-5 > $scripts_path/results/05.txt

mv dice-fuzzing-cov.pdf $scripts_path/results/01_02_fuzzing.pdf
mv dice-fuzzing-cov.png $scripts_path/results/01_02_fuzzing.png
mv dice-fuzzing-cov.svg $scripts_path/results/01_02_fuzzing.svg
mv 03-cov.pdf $scripts_path/results/
mv 03-cov.png $scripts_path/results/
