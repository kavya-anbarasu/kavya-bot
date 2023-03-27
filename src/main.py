
import argparse
import csv
import os
from secret_psycher_parser import send_secrets_to_psychers


def main(args):
    tournament_name = input("Enter tournament name: ")
    season = input("Enter season: ")

    print(args.manual)

    if(args.manual):
        save_csv_path = os.path.join(os.path.dirname(__file__), "../pairings",
                                 f"{tournament_name}_{season}_manual_pairings.csv")
    else:
        save_csv_path = os.path.join(os.path.dirname(__file__), "../pairings",
                                 f"{tournament_name}_{season}_pairings.csv")

    if os.path.exists(save_csv_path):
        overwrite = input(f"File {save_csv_path} already exists, would you like to generate new pairings? (y/n) ")
        if overwrite == "y":
            print("Ok. Will generate new pairings.")
        else:
            view_pairing = input("Would you like to check an existing pairing? (y/n) ")
            while view_pairing == "y":
                psycher = input("Enter psycher email: ")
                with open(save_csv_path, 'r') as f:
                    reader = csv.reader(f)
                    pairings = dict(reader)
                    print(f"Psycher {psycher} is psyching {pairings[psycher]}")
                    view_pairing = input("Would you like to view another existing pairing? (y/n) ")
            print("Exiting...")
            return

    email_subject = f"[sMITe] {tournament_name} Secret Psycher Assignment!"
    change_subject = input(f"This is the current subject line: {email_subject}. Would you like to change it? (y/n) ")
    if change_subject == "y":
        email_subject = input("Enter new subject line: ")

    email_closing = ("MWAHAHAHA you have probably noticed by now, but I have infiltrated all of the responses and \
                     scrambled them up into anagrams. Good luck figuring out what your person wants now. MWAHAHAHA\
                     But, because I am a ~benevolent bot~, if you really need help, respond to this email asking me\
                     for help and I will send you the unscrambled version. <br> <br> HAPPY APRIL FOOLS (｀∀´)Ψ', <br> Kavya Bot")
    change_closing = input(f"This is the current closing: {email_closing}. Would you like to change it? (y/n) ")
    if change_closing == "y":
        email_closing = input("Enter new closing: ")

    print(f"!!!!!!!!!{args.april_fools}")
    send_secrets_to_psychers(args.path_to_csv, tournament_name,
                             email_subject, email_closing, save_csv_path,
                             TESTING=args.test,
                             MAKE_MANUAL_PAIRINGS=args.manual,
                             APRIL_FOOLS=args.april_fools)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send secret psycher emails")
    parser.add_argument("path_to_csv", type=str, help="Path to csv file")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("-mp", "--manual", nargs=2, action="append", help="List of tuples of psycher and secret psycher")  # noqa: E501
    parser.add_argument("-af", "--april_fools", action="store_true", help="Run in april fools mode")  # noqa: E501
    args = parser.parse_args()
    main(args)
