from sklearn.neighbors import KDTree
import numpy as np
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.neighbors import KDTree
from sklearn import datasets
from collections import Counter



class Knn:

    def __init__(self,X,y,k):
        self.data=X
        self.n=k
        self.labels=y
    def predict(self,data_point):

        result=[]

        def is_numeric(obj):
            attrs = ['__add__', '__sub__', '__mul__', '__div__', '__pow__']
            return all(hasattr(obj, attr) for attr in attrs)

        if is_numeric(self.data):
            kdt = KNeighborsClassifier(n_neighbors=self.n, algorithm='kd_tree', metric='euclidean')
            kdt.fit(self.data,self.labels)
            result=kdt.predict(data_point)
            #print result
            dist,ind = kdt.kneighbors(data_point,n_neighbors=self.n, return_distance=True)
            print dist
            print ind

            for points,elements in zip(result,dist):
                m=np.mean(elements)
                sum=0
                for i in elements:
                    sum=sum+((i-m)/self.n)
                answer=(m,sum)
                print answer

            #print type(self.labels)

            # for index in ind:

            # print result

        else:
            kdt = KNeighborsRegressor(n_neighbors=self.n, algorithm='kd_tree', metric='euclidean')
            kdt.fit(self.data,self.labels)
            result=kdt.predict(data_point)
            count = Counter(self.labels)
            for points in result:
                posterior = count[points]/self.n
                answer=(points,posterior)
                print answer

iris = datasets.load_iris()
train = iris.data
labels=iris.target
#print len(train)
#print type(labels)
#q=np.random.random((5, 3))
#print q
#print len(q)

X=[train]

        #knn = KNeighborsClassifier()
        #knn.predict
z=np.array(X)
#print z[0]


#print train
pred=train[:1]


kd=Knn(iris.data,iris.target,3)
kd.predict(pred)


