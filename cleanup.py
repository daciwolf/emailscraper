from pathlib import Path

SCHOOLNAMES = Path(r'C:\Users\david\Documents\schoolsemails\schoolnames.txt')

CLEANEDNAMES = Path(r'C:\Users\david\Documents\schoolsemails\cleanednames.txt')

def extract_names(schoolnames, cleanednames) -> None:
    schoolnames = schoolnames.open('r')
    cleanednames = cleanednames.open('w')
    for line in schoolnames.readlines(): 
        if line.startswith('<loc>'):
            url = line.strip()[5:-6]
            cleanednames.write(url[url.rfind('/')+1:]+ '\n')
    schoolnames.close()
    cleanednames.close()

if __name__ == '__main__':
    extract_names(SCHOOLNAMES, CLEANEDNAMES)
