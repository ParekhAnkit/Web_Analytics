import time
import numpy as np
import pandas as pd
import bs4
import time
import unicodedata
import re
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean, chebyshev, cityblock
from sklearn.preprocessing import MinMaxScaler
from decimal import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import statistics


class DataFrame(object):

    def scrape_data(start_date, from_place, to_place, city_name):

        driver = webdriver.Chrome()

        driver.get('https://www.google.com/flights/explore/')

        #start_date="2017-04-28"

        from_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
        from_input.click()
        from_input_actions = ActionChains(driver)
        from_input_actions.send_keys("New York")
        from_input_actions.send_keys(Keys.ENTER)
        from_input_actions.perform()
        time.sleep(0.9)

        to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
        to_input.click()
        to_input_actions = ActionChains(driver)
        to_input_actions.send_keys("Veracruz")
        to_input_actions.send_keys(Keys.ENTER)
        to_input_actions.perform()
        time.sleep(0.9)

        url=driver.current_url
        c_url=str(url)
        unicodedata.normalize('NFKD', url).encode('ascii','ignore')
        d=c_url.split(';')
        #print d[-1]
        new_url=c_url.replace(d[-1],"d="+start_date)
        #print new_url
        driver.get(new_url)
        time.sleep(0.05)

        results = driver.find_elements_by_class_name('LJTSM3-v-d')
        test = results[0]
        bars = test.find_elements_by_class_name('LJTSM3-w-x')
        time.sleep(0.05)
        data = []
        time.sleep(0.05)

        for bar in bars:
            ActionChains(driver).move_to_element(bar).perform()
            time.sleep(0.1)
            data.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text, test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
            time.sleep(0.05)

        df=pd.DataFrame(data)
        df.columns=['Price','Departure - Return Date']
        print df

    def scrape_data_90(start_date, from_place, to_place, city_name):

        driver = webdriver.Chrome()

        driver.get('https://www.google.com/flights/explore/')

        #start_date="2017-04-28"

        from_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
        from_input.click()
        from_input_actions = ActionChains(driver)
        from_input_actions.send_keys("New York")
        from_input_actions.send_keys(Keys.ENTER)
        from_input_actions.perform()
        time.sleep(0.9)

        to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
        to_input.click()
        to_input_actions = ActionChains(driver)
        to_input_actions.send_keys("Veracruz")
        to_input_actions.send_keys(Keys.ENTER)
        to_input_actions.perform()
        time.sleep(0.9)

        url=driver.current_url
        c_url=str(url)
        unicodedata.normalize('NFKD', url).encode('ascii','ignore')
        d=c_url.split(';')
        #print d[-1]
        new_url=c_url.replace(d[-1],"d="+start_date)
        #print new_url
        driver.get(new_url)
        time.sleep(0.05)

        results = driver.find_elements_by_class_name('LJTSM3-v-d')
        test = results[0]
        bars = test.find_elements_by_class_name('LJTSM3-w-x')
        time.sleep(0.05)
        data = []
        time.sleep(0.05)

        for bar in bars:
            ActionChains(driver).move_to_element(bar).perform()
            time.sleep(0.1)
            data.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text, test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
            time.sleep(0.005)
        time.sleep(0.5)

        df=pd.DataFrame(data)
        #df.columns=['Price','Departure - Return Date']
        #print df

        driver.get(new_url)
        time.sleep(0.9)

        page_for30_90days=driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[4]/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div[5]/div')
        page_for30_90days.click()
        time.sleep(0.001)
        data_for30_90days=[]

        time.sleep(0.9)

        results = driver.find_elements_by_class_name('LJTSM3-v-d')
        test = results[0]
        time.sleep(0.001)
        bars = test.find_elements_by_class_name('LJTSM3-w-x')

        for bar in bars:
            ActionChains(driver).move_to_element(bar).perform()
            time.sleep(0.1)
            data_for30_90days.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text, test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
            time.sleep(0.05)
        time.sleep(0.5)

        data_for60_90days = data_for30_90days[30:60]
        df = df.append(data_for60_90days)
        df.columns=['Price','Departure - Return Date']
        df.index = range(90)
        print df
        time.sleep(0.5)
        return df


    def task_3_dbscan(flight_data):
        prices=flight_data["Price"]
        x=range(90)
        i=0
        for price in prices:
            prices[i] = re.sub('[\$,]', '', price)
            prices[i]=float(prices[i])
            i=i+1

        #print prices

        plt.scatter(x, prices)
        plt.show()

        def calculate_noise_points(X, labels, quiet=False):
            lbls = np.unique(labels)

            noise_points = [X[labels==num, :] for num in lbls if num == -1]
            cluster_means = [np.mean(X[labels==num, :], axis=0) for num in lbls if num != -1]


            #if not quiet:
                #print "Cluster labels: {}".format(np.unique(lbls))
                #print "Cluster Means: {}".format(cluster_means)

            return noise_points


        def calculate_cluster_means(X, labels, quiet=False):
            lbls = np.unique(labels)

            cluster_means = [np.mean(X[labels==num, :], axis=0) for num in lbls if num != -1]

            #if not quiet:
                #print "Cluster labels: {}".format(np.unique(lbls))
                #print "Cluster Means: {}".format(cluster_means)

            return cluster_means

        def print_3_distances(noise_point, cluster_means):
            # euclidean
            dist = [euclidean(noise_point, cm) for cm in cluster_means]
            print "Euclidean distance: {}".format(dist)

            # chebyshev
            dist = [chebyshev(noise_point, cm) for cm in cluster_means]
            print "Chebysev distance: {}".format(dist)

            # cityblock
            dist = [cityblock(noise_point, cm) for cm in cluster_means]
            print "Cityblock (Manhattan) distance: {}".format(dist)

        def plot_the_clusters(X, dbscan_model, noise_point=None, set_size=True, markersize=14):

            labels = dbscan_model.labels_
            clusters = len(set(labels))
            unique_labels = set(labels)
            colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

            if set_size:
                plt.subplots(figsize=(12,8))

            for k, c in zip(unique_labels, colors):
                class_member_mask = (labels == k)
                xy = X[class_member_mask]
                plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c, markeredgecolor='k', markersize=markersize)

            #if noise_point is not None:
                #plt.plot(noise_point[0], noise_point[1], 'xr', markersize=markersize+3)

            plt.title("Total Clusters: {}".format(clusters), fontsize=14, y=1.01)

            plt.show()
            return colors, unique_labels

        def do_yo_thang(X, dbscan_model):
            #cluster_means = calculate_cluster_means(X, dbscan_model.labels_)
            #print_3_distances(noise_point, cluster_means)
            np = calculate_noise_points(X, dbscan_model.labels_)
            #print np
            return plot_the_clusters(X, dbscan_model, np)

        x=range(90)
        x=pd.Series(x)
        fare = MinMaxScaler(feature_range=(-3, 3)).fit_transform(prices[:, None])
        day = MinMaxScaler(feature_range=(-2, 2)).fit_transform(x[:, None])
        X_ss = np.concatenate([day, fare], axis=1)
        db_ss = DBSCAN(eps=0.60, min_samples=5).fit(X_ss)
        do_yo_thang(X_ss, db_ss)


        def find_mistake_point(X, label, noise_points, cluster_mean, prices):
            c=[]
            Z=[]
            p=[]
            q=[]
            r=[]
            s=[]
            y=[]
            g=0
            #print X[1]
            #print X
            x=X.tolist()
            #print x
            n=[]
            #ncprice=[]
            for i in range(len(x)):
                #q[i]=[round(x[i],6)]
                for item in x[i]:
                    p.append(round(item,6))
                    q.append(round(item,8))
            #print p
            for i in range(0,len(p),2):
                #print p[i]
                #print p[i+1]
                Z.append([p[i],p[i+1]])
                y.append([q[i],q[i+1]])

            #print Z[1]
                #print x[i]
            #for f in x:
                #print f
                #y=round(f,6)
            #print "yo"
            #print y
            #print noise_points
            for s in noise_points:
                #print len(noise_points)
                for a in s:
                    #print a
                    #print len(s)
                    ncprice=[]
                    #ncprice[:]=[]
                    #print a
                    dist = [euclidean(a, cm) for cm in cluster_mean]
                    #print dist
                    #print type(dist)

                    #print "Euclidean distance: {}".format(dist)
                    #min = []
                    minimum = dist.index(min(dist))
                    #print minimum
                    lbls = np.unique(label.labels_)
                    nearest_cluster = [X[label.labels_==num, :] for num in lbls if num == minimum]
                    #print "ss"
                    #print nearest_cluster
                    #print "ss"
                    #print type(nearest_cluster)

                    n=nearest_cluster
                    #print "ss"
                    #print n[0]
                    for points in range(len(n)):
                        #print type(points)
                        for item in n[0][points]:
                            r.append(round(item,6))

                    for i in range(0,len(p),2):
                #print p[i]
                #print p[i+1]
                        c.append([p[i],p[i+1]])

                    #print "this"
                    #print c
                    #print Z[0]
                    #print "br"
                    #print c[0]
                    del ncprice[:]
                    #print "check"
                    #print ncprice
                    for i in range(len(c)):
                        if i==0:
                            ncprice=[]
                        #print c[i]
                        #print type(c[i])
                        ncprice.append(Z.index(c[i]))
                    #print len(ncprice)
                    #ncprice=[]
                    #print ncprice
                    #ncprice=[]
                    s=[]
                    for index in ncprice:
                        #print prices[index]
                        s.append(prices[index])
                    #print len(ncprice)
                    Mean=np.mean(s)
                    #print Mean
                    Std=np.std(s)
                    Std=(2*Std)
                    #print Std
                    #print y
                    #print "out"
                    #print a
                    a=a.tolist()
                    a = [float(Decimal("%.8f" % e)) for e in a]
                    #print a
                    index_of_out=y.index(a)
                    #print index_of_out
                    outlier=prices[index_of_out]
                    #print "outl"
                    #print outlier
                    diff=max(Std,50)
                    #print diff
                    price_diff=Mean-diff
                    #print price_diff
                    if outlier < price_diff:
                        print outlier
                        print flight_data.loc[[index_of_out],['Price','Departure - Return Date']]
                        g=1
            if g==0:
                print "No mistake prices"



                                #print it
                        #print "this"
                        #print c
                    #print nearest_cluster




                            #c.append(p)
                            #print type(i)
                        #print type(p)
                        #print nearest_cluster
                        #p = np.array(map(list,d),dtype='float')
                    #for points in nearest_cluster:
                        #p = ["%.6f" % i for i in points ]
                        #c.append(p)
                    #print c
                        #a=X.tolist()
                            #print type(i)
                        #b=[np.array(points).tolist()]
                        #for items in a:

                            #a = ["%.6f" % i for i in items]
                            #c=c.append(a)
                            #print c
                        #for items in b:
                            #b = ["%.6f" % i for i in items]
                        #print b
                        #print b
                        #print a


                        #ncprice = a.index(b)

                    #print ncprice
                    #b=StandardScaler().fit.inverse_transform(X)
                    #print b
                    #px = [x for x in df['price']]
                    #ff = pd.DataFrame(px, columns=['price']).reset_index()
                    #two_Std = (2*np.std(nearest_cluster, axis=1))
                    #pf = pd.concat([, pd.DataFrame(label.labels_, columns=['cluster'])], axis=1)

                    #print pf
                    #print two_Std
                    #compare = max(, 50)
                    #if price< (clusters_price_mean-(two_Std)
                          # return
        cm = calculate_cluster_means(X_ss, db_ss.labels_)
        n = calculate_noise_points(X_ss, db_ss.labels_)
        #print n
        find_mistake_point(X_ss, db_ss, n, cm, prices )





    def task_3_IQR(flight_data):
        data=flight_data["Price"]
        prices=data.tolist()
        outliers=[]
        out=[]
        sorting = sorted(prices)
        mid = len(sorting) / 2
        if (len(sorting) % 2 != 0):

            q1 = statistics.median(sorting[:mid])
            q3 = statistics.median(sorting[mid + 1:])

        else:

            q1 = statistics.median(sorting[:mid])
            q3 = statistics.median(sorting[mid:])

        IQR=q3-q1
        lower_range=q1-(1.5*IQR)

        upper_range=q3+(1.5*IQR)

        for price in prices:
            if lower_range<=price<=upper_range:
                continue
            else:
                outliers.append(price)
        if len(outliers)>0:
            for outlier in outliers:

                out_price = flight_data[prices.index(outlier):(prices.index(outlier)+1)]['Price']
                out_price_list=out_price.values.tolist()
                out_date = flight_data[prices.index(outlier):(prices.index(outlier)+1)]['Departure - Return Date']
                out_date_list=out_date.tolist()
                outliers.append([out_price_list[0], out_date_list])
                out = pd.DataFrame(outliers, columns=['Price', 'Departure - Return Date'])
        if len(out)>0:
            print out
        else:
            print "NO outliers"
        fig = plt.figure(1, figsize=(7, 7))
        ax = fig.add_subplot(111)
        bp = ax.boxplot(prices)
        plt.show(block=True)




    #scrape_data_90('2017-05-01', 'New York', 'Mexico', 'Veracruz')

    data=scrape_data_90('2017-05-08', 'New York', 'Mexico', 'Veracruz')

    task_3_dbscan(data)

    task_3_IQR(data)

















