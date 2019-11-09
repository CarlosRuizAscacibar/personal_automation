import main
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--single_job", "-s", help="Choose a cron job to execute")

args = parser.parse_args()

if args.single_job:
    if args.single_job == 'evo':
        main.evo_weekly()
    if args.single_job == 'fotocasa':
        main.fotocasa_periodic_scrap()
    if args.single_job == 'fotocasa_update_all':
        main.fotocasa_update_all()
else:
    print("single_job is mandatory")

