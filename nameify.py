import csv
import random
import string

class Nameify:

    # lower case alpha numeric constant
    ALNUM = string.printable[0:62]

    def __init__(self, file = 'names.csv', debug = False):
        self.names = self.load_names(file)

    def load_names(self, file):
        names = []
        with open(file) as names_file:
            csv_reader = csv.reader(names_file)
            for row in csv_reader:
                names.append(row[0])
        return names

    def generate_url(self):
        url = ''
        name_pos = random.randint(1,5)
        for i in range(1,6):
            if i == name_pos:
                if i == 1:
                    url+= f'{random.choice(self.names)}-'
                elif i == 5:
                    url+= f'-{random.choice(self.names)}'
                else:
                    url+= f'-{random.choice(self.names)}-'
            else:
                url+= random.choice(self.ALNUM)
        return url