#! /bin/bash
set -x

if [ -d "venv/" ]; then
  source venv/bin/activate
else
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
fi

python3 cli.py run-experiments -r -d
python cli.py eval-4-hooks -f -d
