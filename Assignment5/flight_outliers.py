import time
import numpy as ny
import pandas as pd
import bs4
import time
import unicodedata
import re
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class DataFrame(object):

    def scrape_data(start_date, from_place, to_place, city_name):
            driver = webdriver.Chrome()

            driver.get('https://www.google.com/flights/explore/')

            from_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
            from_input.click()
            from_input_actions = ActionChains(driver)
            from_input_actions.send_keys(from_place)
            from_input_actions.send_keys(Keys.ENTER)
            from_input_actions.perform()
            time.sleep(0.5)
            to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
            to_input.click()
            to_input_actions = ActionChains(driver)
            to_input_actions.send_keys(city_name)
            to_input_actions.send_keys(Keys.ENTER)
            to_input_actions.perform()
            time.sleep(0.5)


            url=driver.current_url
            c_url=str(url)
            unicodedata.normalize('NFKD', url).encode('ascii','ignore')
            d=c_url.split(';')
            #print d[-1]
            new_url=c_url.replace(d[-1],"d="+start_date)
            #print new_url
            driver.get(new_url)
            time.sleep(0.5)

            results = driver.find_elements_by_class_name('LJTSM3-v-d')
            test = results[0]
            bars = test.find_elements_by_class_name('LJTSM3-w-x')
            data = []
            time.sleep(0.5)

            for bar in bars:
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.001)
                data.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
            time.sleep(0.5)


            df=pd.DataFrame(data)
            df.columns=['Price','Departure - Return Date']
            print df
            time.sleep(0.5)

    def scrape_data_90(start_date, from_place, to_place, city_name):
            t= str(start_date)
            p=t.split()
            #print p[0]
            #type(p[0])
            date=p[0]

            driver = webdriver.Chrome()
            driver.get('https://www.google.com/flights/explore/')

            from_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
            from_input.click()
            from_input_actions = ActionChains(driver)
            from_input_actions.send_keys(from_place)
            from_input_actions.send_keys(Keys.ENTER)
            from_input_actions.perform()
            time.sleep(0.5)

            to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
            to_input.click()
            to_input_actions = ActionChains(driver)
            to_input_actions.send_keys(city_name)
            to_input_actions.send_keys(Keys.ENTER)
            to_input_actions.perform()
            time.sleep(0.5)


            url=driver.current_url
            c_url=str(url)
            unicodedata.normalize('NFKD', url).encode('ascii','ignore')
            d=c_url.split(';')
            #print d[-1]
            new_url=c_url.replace(d[-1], date)
            #print new_url
            driver.get(new_url)
            time.sleep(0.5)

            results = driver.find_elements_by_class_name('LJTSM3-v-d')
            test = results[0]
            bars = test.find_elements_by_class_name('LJTSM3-w-x')
            data = []
            time.sleep(0.5)

            for bar in bars:
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.001)
                data.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text, test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
            time.sleep(0.5)

            df=pd.DataFrame(data)
            driver.get(new_url)

            page_for30_90days = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[4]/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div[5]/div')
            page_for30_90days.click()
            data_for30_90days = []
            time.sleep(0.5)


            results = driver.find_elements_by_class_name('LJTSM3-v-d')
            test = results[0]
            bars = test.find_elements_by_class_name('LJTSM3-w-x')
            time.sleep(0.5)

            for bar in bars:
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.001)
                data_for30_90days.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text, test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
            time.sleep(0.5)

            data_for60_90days = data_for30_90days[30:60]
            df = df.append(data_for60_90days)
            df.columns=['Price', 'Departure - Return Date']
            df.index = range(90)
            print df


    def task_3_dbscan(self, flight_data):
        flight_data['Price'] = flight_data['Price'].map(lambda x: re.sub("[^\d\.]", "", x))
        #print flight_data['Price']
        flight_data['Price'] = flight_data['Price'].astype('int64')
        x = len(flight_data['Price'])
        fig, ax = plt.subplots(figsize=(10,6))
        plt.scatter(ny.arange(x),flight_data['Price'])
        plt.show()

        px = [x for x in flight_data['Price']]
        ff = pd.DataFrame(px, columns=['price']).reset_index()

        X = StandardScaler().fit_transform(ff)
        db = DBSCAN(eps=0.4, min_samples=1).fit(X)

        labels = db.labels_
        clusters = len(set(labels))
        unique_labels = set(labels)
        colors = plt.cm.Spectral(ny.linspace(0, 1, len(unique_labels)))

        plt.subplots(figsize=(12,8))

        for k, c in zip(unique_labels, colors):
            class_member_mask = (labels == k)
            xy = X[class_member_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c, markeredgecolor='k', markersize=14)

        plt.title("Total Clusters: {}".format(clusters), fontsize=14, y=1.01)
        plt.show()


    scrape_data('2017-04-13', 'New York', 'Mexico', 'Veracruz')



















