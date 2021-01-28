import pandas as pd
from os import listdir
from os.path import isfile, join
import textract
import re
import spacy


class ResumeParser:

    def __init__(self, path):
        self.nlp = spacy.load('en')
        self.only_files = [f for f in listdir(path) if isfile(join(myPath, f))]

    def getName(self, input_string):
        """
        Function to get name from given string
        :param input_string: Resume in the form of String
        :return: Person name from given Resume
        """
        doc = self.nlp(input_string)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return str(ent).strip()

    def getEmail(self, input_string):
        """
        Function to get email id from given string
        :param input_string: Resume in the form of String
        :return: Email id from given Resume
        """
        regex_for_email = r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+'
        return re.findall(regex_for_email, input_string)

    def getPhoneNumber(self, input_string):
        """
        Function to get phone number from given string
        :param input_string: Resume in the form of String
        :return: Phone number from given Resume
        """
        regex_for_phone_no = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
        return re.findall(regex_for_phone_no, input_string)

    def save_details_to_CSV(self):
        """
        Function to read all the Resumes, extract name, email_id and phone number from it,
        and store it in CSV file
        """
        name = []
        email = []
        phone_no = []

        for file_name in self.only_files:
            try:
                input_string = textract.process(myPath + file_name).decode("utf-8").strip()
                phone_no.append(self.getPhoneNumber(input_string))
                email.append(self.getEmail(input_string))
                name.append(self.getName(input_string))

            except Exception as e:
                print(e)

        df = pd.DataFrame({'name': name, 'email': email, 'phone no': phone_no})
        df.to_csv("Data_From_Resume.csv")


if __name__ == '__main__':
    myPath = "/home/bridgelabz/BridgeLabz/Resume-Parser/Resumes/"
    rp = ResumeParser(myPath)
    rp.save_details_to_CSV()
    print("Done")
