#! /bin/bash
set -x

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
cp configs/test-run/.experiments-config.yml .

python3 cli.py run-experiments -r
