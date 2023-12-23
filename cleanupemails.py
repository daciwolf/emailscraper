from pathlib import Path

UNCLEANED = Path(r'C:\Users\david\Documents\schoolsemails\top_level_emails.txt')
CLEANED = Path(r'C:\Users\david\Documents\schoolsemails\cleanedupemail.txt')


def remove_invalids(emails:[])-> []:
    return_list = []
    for email in emails:
        if 'google' in email or 'sentry' in email or '20' in email:
            pass
        else:
            return_list.append(email) 
    return return_list

def remove_duplicates(emails:[]) -> []: 
    return list(set(emails))

def cleaner() -> None:
    unclean = UNCLEANED.open('r')
    clean = CLEANED.open('a')
    for email in remove_duplicates(remove_invalids(unclean.readlines())):
        clean.write(email)
    clean.close() 
    unclean.close()

cleaner() 
