from pathlib import Path
import os
import subprocess


DIR = Path(os.path.realpath(__file__)).parent.parent.parent


def main(args):
    # rerunning dice happens in 3 steps:
    # 1. setup dice
    setup_path = os.path.join(DIR, "01-dice-comparison/02-real-firmware/00-docker-setup")
    execution_path = os.path.join(DIR, "01-dice-comparison/02-real-firmware/01-evaluation")
    dice_path = os.path.join(setup_path, "create_dice.sh") 
    p2im_path = os.path.join(setup_path, "create_p2im.sh") 
    env = {}
    if args.use_docker and args.export_images:
        print("Please only specify either -d or -e")
        exit()
    if args.use_docker:
        env["IMPORT_IMAGES"]="1"
    if args.export_images:
        env["EXPORT_IMAGES"]="1"
    if not args.use_docker:
        r = subprocess.run(["bash", "create_dice.sh"], stdout=subprocess.PIPE, cwd=setup_path)
        # this setup fails easily, lets for now check if "All done" is in stdout
        if not b"All done!" in r.stdout:
            print("setup_dice.sh failed, this needs manual inspection. Please rerun {dice_path} manually and make sure that all requirements are installed.")
            exit()
        else:
            print("DICE setup passed!")
        r = subprocess.run(["bash", "create_p2im.sh"], stdout=subprocess.PIPE, cwd=setup_path) #, shell=True)
        # this setup fails easily, lets for now check if "All done" is in stdout
        if not b"All done!" in r.stdout:
            print(f"setup_p2im.sh failed, this needs manual inspection. Please rerun {p2im_path} maually and make sure that all requirements are installed.")
            exit()
        else:
            print(f"P2IM setup passed!")
    r = subprocess.run(["bash", "build_docker.sh"], stdout=subprocess.PIPE, cwd=setup_path, env=env)
    # only difference: the path. The script is also called build_docker.sh
    # it takes a config from the same path
    r = subprocess.run(["bash", "build_docker.sh"], cwd=execution_path)





if __name__=="__main__":
    main(None)
