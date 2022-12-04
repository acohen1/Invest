"""
raw_parser.py uses spaCy natural language processing to parse raw financial data from
IEX Cloud API and return a pandas dataframe of the parsed data.
This module will be the workaround for the IEX Cloud API 4year lower limit for financials.
TODO: use IEX labelled data to train spaCy model to parse financial data
"""
import spacy
import pandas as pd
from fetch_data import get_raw_financials

class Raw_Parser:
    def __init__(self, symbol, range):
        """
        :param symbol: string of stock symbol
        :param range: number of years of data to retrieve
        """

        self.symbol = symbol
        self.range = range
        nlp = spacy.load('en_core_web_sm')
        ner = nlp.get_pipe('ner')

        #the first entry (0) is the most up to date (2022)
        #for faster testing, only 1 year of data is currently used
        raw_financials = get_raw_financials(self.symbol, self.range)
        raw_financials = raw_financials[0]

        # Initialize an empty string to store the concatenated dictionary values
        raw_financials_string = ''

        # Convert the dictionary values to a string
        for key, value in raw_financials.items():
            #convert any non-strings to string for concatonation
            if not isinstance(value, str):
                value = str(value)
            raw_financials_string += key + ': ' + value + '\n'

        # Pass the concatenated string to the nlp object and run the NER
        doc = ner(nlp.make_doc(raw_financials_string))
        self.entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]

        # We can filter the detected entities to only include those that are relevant to our specific values
        self.filtered_entities = [ent for ent in self.entities if ent['label'] in ['MONEY', 'PERCENT']]

        for ent in self.entities:
            print(ent['text'], ent['label'])










