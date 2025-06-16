#! /bin/bash
file_path=$(readlink -f $0)
venv_path=`dirname $file_path`/../../scripts/venv/
req_path=`dirname $file_path`/../../scripts/requirements.txt
cli_path=`dirname $file_path`/../../scripts/cli.py
echo $venv_path
set -x

if [ -d "results/" ]; then
  rm -rf results
fi
mkdir results

if [ -d $venv_path ]; then
  source $venv_path/bin/activate
else
  python3 -m venv $venv_path
  source $venv_path/bin/activate
  pip install -r $req_path
fi


python $cli_path eval-1-1
