#! /bin/bash
set -xe

if [ -d "results/" ]; then
  rm -rf results
fi
mkdir results

if [ -d "venv/" ]; then
  source venv/bin/activate
else
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
fi
cp configs/4h-1run/.experiments-config.yml .

python3 cli.py run-experiments -r
python3 cli.py eval-1-1 > results/01_unit.txt
python3 cli.py eval-1-2 --num-runs 1 --runtime 4
python3 cli.py eval-2 > results/02.txt
python cli.py eval-2-fp > results/02-fp.txt
python3 cli.py eval-3 --runtime 4 --num-runs 1
python3 cli.py eval-4 > results/04.txt
python3 cli.py eval-5 > results/05.txt

mv dice-fuzzing-cov.pdf results/02_fuzzing.pdf
mv dice-fuzzing-cov.png results/02_fuzzing.png
mv dice-fuzzing-cov.svg results/02_fuzzing.svg
mv 03-cov.pdf results/
mv 03-cov.png results/

