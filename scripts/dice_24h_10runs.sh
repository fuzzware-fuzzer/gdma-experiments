#! /bin/bash
path=$(dirname "$0")
set -xe
echo $path

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

cp configs/24h-10runs/config.txt $path/../01-dice-comparison/02-real-firmware/01-evaluation/

python $path/cli.py run-dice -d

cp -r $path/../01-dice-comparison/02-real-firmware/01-evaluation/p2im_dice_results/ $path/results
