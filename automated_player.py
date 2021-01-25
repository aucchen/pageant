#!/usr/bin/env python

import os
import random

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')

# automated player for dendry using selenium
def test(output_path='output.txt', dump_stats=1, script_path='transcript.txt', data_path='data.json'):
    script = []
    transcript = ''
    current_paragraphs = set()
    #options = Options()
    #options.headless = True
    #driver = webdriver.Firefox(options=options)
    driver = webdriver.PhantomJS()
    driver.get('file://' + file_path)
    link_divs = driver.find_elements_by_xpath('//ul[@class="choices"]//li')
    data = driver.execute_script('return JSON.stringify(window.dendryUI.dendryEngine.getExportableState(), null, 2);');
    print(data)
    while len(link_divs) > 0:
        link_divs = driver.find_elements_by_xpath('//ul[@class="choices"]//li')
        # find main text: find all text elements under <div id="content"> 
        content_text = driver.find_elements_by_xpath('//div[@id="read-marker"]/following-sibling::p')
        if len(content_text) == 0:
            if len(driver.find_elements_by_id('read-marker')) == 0:
                content_text = driver.find_elements_by_xpath('//div[@id="content"]/p')
        for i, paragraph in enumerate(content_text):
            if len(paragraph.text.strip()) == 0:
                continue
            # filter paragraphs based on whether they're seen
            if i == 0 and paragraph.text not in current_paragraphs:
                current_paragraphs = set()
                if dump_stats:
                    data = driver.execute_script('return JSON.stringify(window.dendryUI.dendryEngine.getExportableState(), null, 2);');
                    transcript += '\n\nDATA:\n' + data
                transcript += '\n'
            current_paragraphs.add(paragraph.text)
            print('\n ', paragraph.text)
            transcript += '\n ' + paragraph.text
        for link in link_divs:
            print('\n -', link.text)
            transcript += '\n -' + link.text
        # click on a random link
        links = driver.find_elements_by_xpath('//ul[@class="choices"]//a')
        if len(links) == 0:
            break
        link_choice = random.choice(links)
        print('\n>>> ' + link_choice.text)
        script.append(link_choice.text)
        transcript += '\n>>> ' + link_choice.text
        link_choice.click()
        # TODO: save/dump stats somewhere?
    data = driver.execute_script('return JSON.stringify(window.dendryUI.dendryEngine.getExportableState(), null, 2);');
    transcript += '\nFINAL DATA:\n' + data
    print(data)
    driver.quit()
    with open(output_path, 'w') as f:
        f.write(transcript)
    with open(script_path, 'w') as f:
        for line in script:
            f.write(line + '\n')
    with open(data_path, 'w') as f:
        f.write(data)
    return transcript


def test_with_script(script_path, output_path='script_output.txt', dump_stats=0, data_path='data.json', use_headless=True, script_output_path=None):
    """
    tests with a script: a script is a list of link text strings, each indicating the link text to click on.
    """
    script_data = []
    script_output = []
    with open(script_path) as f:
        for line in f.readlines():
            script_data.append(line.strip())
    transcript = ''
    current_paragraphs = set()
    #options = Options()
    #options.headless = use_headless
    #driver = webdriver.Firefox(options=options)
    driver = webdriver.PhantomJS()
    driver.get('file://' + file_path)
    link_divs = driver.find_elements_by_xpath('//ul[@class="choices"]//li')
    data = driver.execute_script('return JSON.stringify(window.dendryUI.dendryEngine.getExportableState(), null, 2);');
    print(data)
    script_location = 0
    while len(link_divs) > 0:
        link_divs = driver.find_elements_by_xpath('//ul[@class="choices"]//li')
        # find main text: find all text elements under <div id="content"> 
        content_text = driver.find_elements_by_xpath('//div[@id="read-marker"]/following-sibling::p')
        if len(content_text) == 0:
            if len(driver.find_elements_by_id('read-marker')) == 0:
                content_text = driver.find_elements_by_xpath('//div[@id="content"]/p')
        for i, paragraph in enumerate(content_text):
            if len(paragraph.text.strip()) == 0:
                continue
            # filter paragraphs based on whether they're seen
            if i == 0 and paragraph.text not in current_paragraphs:
                current_paragraphs = set()
                if dump_stats:
                    data = driver.execute_script('return JSON.stringify(window.dendryUI.dendryEngine.getExportableState(), null, 2);');
                    transcript += '\n\nDATA:\n' + data
                transcript += '\n'
            current_paragraphs.add(paragraph.text)
            #print('\n ', paragraph.text)
            transcript += '\n ' + paragraph.text
        for link in link_divs:
            #print('\n -', link.text)
            transcript += '\n -' + link.text
        # click on link indicated by script
        links = driver.find_elements_by_xpath('//ul[@class="choices"]//a')
        if len(links) == 0:
            break
        link_choice = random.choice(links)
        # if the link text is not in the script, then just continue randomly.
        has_link_text = False
        for link in links:
            if script_data and link.text == script_data[0]:
            #    print('\nSCRIPT LINE #' + str(script_location) + ' ' + link.text + '\n')
                transcript += '\nSCRIPT LINE #' + str(script_location) + ' ' + link.text + '\n'
                script_location += 1
                script_data = script_data[1:]
                link_choice = link
                has_link_text = True
                break
        #if not has_link_text and len(links) > 1:
            #print('WARNING: link not found in script')
        script_output.append(link_choice.text)
        #print('\n>>> ' + link_choice.text)
        transcript += '\n>>> ' + link_choice.text
        link_choice.click()
    data = driver.execute_script('return JSON.stringify(window.dendryUI.dendryEngine.getExportableState(), null, 2);');
    transcript += '\nFINAL DATA:\n' + data
    print(data)
    driver.quit()
    with open(output_path, 'w') as f:
        f.write(transcript)
    with open(data_path, 'w') as f:
        f.write(data)
    if script_output_path is not None:
        with open(script_output_path, 'w') as f:
            for line in script_output:
                f.write(line + '\n')
    return transcript


def random_n_tests(n, dump_stats=0, starting_index=0):
    for i in range(n):
        i = starting_index + i
        output_path = 'random_test_outputs/{:03d}_output.txt'.format(i)
        script_path = 'random_test_outputs/{:03d}_script.txt'.format(i)
        data_path = 'random_test_outputs/{:03d}_data.txt'.format(i)
        test(output_path=output_path, script_path=script_path, data_path=data_path,
                dump_stats=dump_stats)


def random_n_script_tests(n, script_path, dump_stats=0, starting_index=0):
    """Starts n random tests from a script."""
    for i in range(n):
        i = starting_index + i
        output_path = 'scripted_test_outputs/{:03d}_output.txt'.format(i)
        script_output_path = 'scripted_test_outputs/{:03d}_script.txt'.format(i)
        data_path = 'scripted_test_outputs/{:03d}_data.txt'.format(i)
        test_with_script(
                script_path=script_path,
                output_path=output_path,
                script_output_path=script_output_path,
                data_path=data_path,
                dump_stats=dump_stats)



if __name__ == '__main__':
    print(file_path)
    #random_n_tests(20, starting_index=51)
    #test_with_script('standard_runs/emily.txt', output_path='standard_runs/emily_output.txt', data_path='standard_runs/emily_data.txt')
    random_n_script_tests(10, 'standard_runs/basic_script.txt')
