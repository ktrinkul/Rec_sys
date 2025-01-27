#!python3

import re
import csv
from bs4 import BeautifulSoup
import requests
import pytest


class Movies():
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def read_file(self):
        with open(self.file_path) as file:
            header = next(file)
            self.data = file.readlines()
    
    def count_errors(self, error_filename = 'error.txt'):
        error_file = open(error_filename, "w")
        count_errors = 0

        for line in self.data:

            if '""' in line:
                error_file.write(f"Double name: {line}\n")
                count_errors+=1

            elif '"' in line:
                line_split = line.split('"')
                line_eng_nat_name = line_split[1].split('(')

                if ',' in line_eng_nat_name[0]:
                    error_file.write(f"Error in 1st name: {line}")
                    count_errors+=1
            
                if ',' in line_eng_nat_name[1]:
                    error_file.write(f"Error in 2nd name: {line}")
                    count_errors+=1
            
            elif not re.match(r'^(.*)\s*\(\d{4}\)\s*$', line.split(',')[1]):
                error_file.write(f"Not mentioned year: {line}")
                count_errors+=1
        return count_errors/len(self.data) * 100


def read_title(target_movie_id):
    title = None

    with open('./data/links.csv', mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)

        for line in reader:
            if line[0] == target_movie_id: 
                return line[1]
          
def read_name(title_id):
    headers = {"User-Agent": "Mozilla/5.0 Chrome/58.0.3029.110 Safari/537.36"}
    url = f'https://www.imdb.com/title/tt{title_id}/'
    
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    if soup.find('div', class_='sc-ec65ba05-1 fUCCIx'):
        name = soup.find('div', class_='sc-ec65ba05-1 fUCCIx').text
        return name[len('Original title: '):]
    else:
        return soup.find('span', class_='hero__primary-text').text
    

class Test:
    @pytest.fixture
    def setup(self):
        # Movies
        self.data_movie = Movies('./data/movies.csv')
        self.data_movie.read_file()

    # test_Movies_read_file
    def test_Movies_read_file_types_1(self, setup):
        assert isinstance(self.data_movie.data, list)

    def test_Movies_read_file_list_types(self, setup):
        for item in self.data_movie.data:
            assert isinstance(item, str)

    def test_Movies_read_file_sort(self, setup):
        with open('./data/movies.csv') as file:
            header = next(file)
            for data_line in range(1000):
                assert self.data_movie.data[data_line] == file.readline()
    
    # test_Movies_count_errors  
    def test_Movies_count_errors_types(self, setup):
        percent = self.data_movie.count_errors()
        assert isinstance(percent, float) 
