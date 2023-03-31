import os
import random
import pandas as pd
from tqdm import tqdm

from sending_email import gmail_send_message
from april_fools.april_fools import create_anagrams


def make_pairings(df):
    '''
    Take df list and randomly match every email with another
    '''
    print("Generating pairings...")

    pairings = {}

    emails_head = df.tolist()
    emails_tail = emails_head.copy()

    while len(emails_head) > 0:
        psycher = emails_head.pop(random.randint(0, len(emails_head) - 1))
        psychee = emails_tail[random.randint(0, len(emails_tail) - 1)]

        while psycher == psychee:
            psychee = emails_tail[random.randint(0, len(emails_tail) - 1)]
        emails_tail.remove(psychee)

        pairings[psycher] = psychee

    assert sorted(pairings.keys()) == sorted(df.tolist()), "Psychers are repeated or missing!"  # noqa: E501
    assert sorted(pairings.values()) == sorted(df.tolist()), "Psychees are repeated or missing!"  # noqa: E501
    for psycher in pairings:
        assert psycher != pairings[psycher], "Psycher and psychee are the same!"  # noqa: E501

    return pairings


def save_pairings_to_csv(pairings, path_to_csv):
    print(path_to_csv)
    with open(path_to_csv, 'w') as f:
        for psycher in pairings:
            f.write(f"{psycher},{pairings[psycher]}\n")

    print(f"Pairings saved to {path_to_csv}!")


def send_secrets_to_psychers(path_to_csv, tournament_name, email_subject=None,
                             email_closing=None, save_csv_path="./",
                             TESTING=False, MAKE_MANUAL_PAIRINGS=None,
                             APRIL_FOOLS=False):
    df = pd.read_csv(path_to_csv)

    if TESTING:  # create pairings but don't send emails
        pairings = make_pairings(df['Email Address'])
        # save_pairings_to_csv(pairings, save_csv_path)
        raise Exception("TESTING is True, not sending emails!")

    if MAKE_MANUAL_PAIRINGS:
        pairings = {}
        for pairing in MAKE_MANUAL_PAIRINGS:
            pairings[pairing[0]] = pairing[1]
        # save_pairings_to_csv(pairings, save_csv_path)
        # raise Exception("MANUAL PAIRING TESTING!")

    else:
        pairings = make_pairings(df['Email Address'])
        save_pairings_to_csv(pairings, save_csv_path)

    for psycher in tqdm(pairings):
        if df[df['Email Address'] == psycher].empty:  # should not hit when using real data
            psycher_name = "[code is broken, email kavya please]"
            print(f"Psycher {psycher} not found in {path_to_csv}! Look into this.")  # noqa: E501
        else:
            psycher_name = df[df['Email Address'] == psycher].iloc[0, 2]

        person_to_psych = pairings[psycher]
        person_to_psych_name = df[df['Email Address'] == person_to_psych].iloc[0, 2]

        email_body = f"Hi {psycher_name}! <br><br>" \
            f"For {tournament_name}, the person you will be psyching is <b>{person_to_psych_name}</b>! " \
            "Here are their responses to the form: <br> <p style=\"margin-left\">"
        email_to = psycher
        secrets = df[df['Email Address'] == person_to_psych]

        for i, secret in enumerate(secrets):
            if i < 3:
                continue
            res = secrets[secret].item()
            if (APRIL_FOOLS and not (i > secrets.shape[1] - 3)):  # trying to preserve last two questions (allergies and other) # noqa: E501
                try:
                    res = create_anagrams(res)
                except Exception:
                    pass
                finally:
                    email_body += f"<b>{secret}</b> <br> {res}<br>"  # noqa: E501
            else:
                email_body += f"<b>{secret}</b> <br> {res}<br>"
        email_body += "</p>"
        email_body += email_closing

        gmail_send_message(email_subject, email_body, email_to)


if __name__ == "__main__":
    email_subject = "[sMITe] NYM Secret Psycher Assignment TEST TEST TEST!"
    email_closing = "Happy Psyching!! <br> Kavya Bot"
    send_secrets_to_psychers("/Users/kanbarasu/Downloads/nym_secret_psycher.csv", "NYM",
                             email_subject, email_closing,
                             os.path.join(os.path.dirname(os.getcwd()), "data", "NYM_S23_pairings.csv"),
                             TESTING=True)
