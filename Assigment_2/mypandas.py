from collections import OrderedDict
import datetime
class DataFrame(object):
    def __init__(self, list_of_lists, header=True):

        # This is used to generalise if data contains header we would like to separate it from values and store it in a
        # different variable if else loops provides option to do so.
        if header:
            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]
            # First for loop is used to obtain list from list of lists; second for loop is used to get string from list.
            # s.strip() is used to remove trailing and leading white spaces from string.
            self.data = [[string1.strip() for string1 in list1] for list1 in self.data]
            self.data1 = self.data
            self.header1 = self.header
            generated_header = []

            for index, column in enumerate(self.header):
                generated_header.append(self.header[index])

            # Check if there are duplicates
            Duplicates = [x for n, x in enumerate(generated_header) if x in generated_header[:n]]

            # This if loop will execute only if duplicates is not empty (Task 1)
            if Duplicates:
                raise Exception('Headers are Repeating')

        else:

            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]

            # First for loop is used to obtain list from list of lists; second for loop is used to get string from list.
            # s.strip() is used to remove trailing and leading white spaces from string.
            self.data = [[string1.strip() for string1 in list1] for list1 in self.data]
            generated_header = []

            for index, column in enumerate(self.header):
                generated_header.append(self.header[index])

            # Check if there are duplicates
            Duplicates = [x for n, x in enumerate(generated_header) if x in generated_header[:n]]

            # This if loop will execute only if duplicates is not empty (Task 1)
            if Duplicates:
                raise Exception('Headers are Repeating')
            self.header = ['column' + str(index + 1) for index, column in enumerate(data[0])]
            self.data = list_of_lists
        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]

    def __getitem__(self, item):
        # For Only Rows
        if isinstance(item, (int, slice)):
            return self.data[item]

        # For Only Columns
        elif isinstance(item, (str, unicode)):
            return [row[item] for row in self.data]

        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):
                if isinstance(item[0], list):
                    rows = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rows = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rows]
                    elif all(isinstance(thing, (str, unicode)) for thing in item[1]):
                        return [[row[column_name] for column_name in item[1]] for row in rows]
                    else:
                        raise TypeError('Unsure of the type of data input !!!!')
                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rows]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], (str, unicode)):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I dont\'t know how to handle this !!!!')
        # Only for list of Column Names
        elif isinstance(item, list):
            return [[row[column_name] for column_name in item] for row in self.data]

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value == value]
        else:
            return [row for row in self.data if row[column_name] == value]

    def min(self, column_name):
        if isinstance(column_name, (str, unicode)):
            if column_name == 'Transaction_date' or column_name == 'Account_Created' or column_name == 'Last_Login':
                temp = [row[column_name] for row in self.data]
                compare = datetime.datetime.strptime(temp[0], "%m/%j/%y %H:%M")
                Min = int(str(compare.month)+str(compare.day)+str(compare.year)+str(compare.hour)+str(compare.minute))
                for i in range(len(temp)):
                    temp0 = datetime.datetime.strptime(temp[i], "%m/%j/%y %H:%M")
                    compare0 = int(str(temp0.month)+str(temp0.day)+str(temp0.year)+str(temp0.hour)+str(temp0.minute))
                    if compare0 <= Min:
                        Min = compare0
                MINN =str(Min)
                m = (MINN[0:1] + '/' + MINN[1:2] + '/' + MINN[2:6] + ' ' + '00' + ':' + MINN[6:8])  # fomatting
                return m
            else:
                try:
                    temp1 = [float(row[column_name]) for row in self.data]  # for min  data without timestamp
                    minimum = min(float(s) for s in temp1)
                    return minimum
                except:
                    raise Exception('Data Type is invalid because the function expects an integer value')
        else:
            raise Exception('Invalid Column is passed ..')

    def max(self, column_name):
        if isinstance(column_name, (str, unicode)):
            if column_name == 'Transaction_date' or column_name == 'Account_Created' or column_name == 'Last_Login':
                temp2 = [row[column_name] for row in self.data]
                MAX = 0
                for i in range(len(temp2)):
                    temp3 = datetime.datetime.strptime(temp2[i], "%m/%j/%y %H:%M")
                    compare = int(str(temp3.month)+str(temp3.day)+str(temp3.year)+str(temp3.hour)+str(temp3.minute))
                    if compare >= MAX:
                        MAX = compare
                ma = str(MAX)
                maz= (ma[0:1]+'/'+ma[1:3]+'/'+ma[3:7]+' '+ma[7:9]+':'+ma[9:11])  # fomatting
                return maz
            else:
                try:
                    temp4 = [float(row[column_name]) for row in self.data]  # for max  data without timestamp
                    maximum = max(float(s) for s in temp4)
                    return maximum
                except:
                    raise Exception('Data Type is invalid because the function expects an integer value')
        else:
            raise Exception('Invalid Column is passed !!!!')

    def mean(self, column_name):
        if isinstance(column_name, (str, unicode)):
            try:
                temp5 = [float(row[column_name]) for row in self.data]
                mean_value = sum(temp5)/len(temp5)
                return mean_value
            except:
                raise Exception('Data Type is invalid because the function expects an integer value')
        else:
            raise Exception('Invalid Column is passed !!!!')

    def median(self, column_name):
        if isinstance(column_name, (str, unicode)):
            try:
                temp6 = [float(row[column_name]) for row in self.data]
                temp6 = sorted(temp6)
                if len(temp6) %2 == 1:
                    Med = temp6[((len(temp6) + 1)/2)-1]
                else:
                    Med = float(sum(temp6[(len(temp6)/2)-1:(len(temp6)/2)+1]))/2.0
                return Med
            except:
                raise Exception('Data Type is invalid because the function expects an integer value')
        else:
            raise Exception('Invalid Column is passed !!!!')

     #Finds  Standard deviation
    def std(self, column_name):
        if isinstance(column_name, (str, unicode)):
            try:
                temp7 = [float(row[column_name]) for row in self.data]
                Mean = sum(temp7) / len(temp7)
                STD_DEV = sum((x - Mean)**2 for x in temp7)
                STD_DEV = (STD_DEV/len(temp7))**0.5
                return STD_DEV
            except:
                raise Exception('Data Type is invalid because the function expects an integer value')
        else:
            raise Exception('Invalid Column is passed ..')

    def add_rows(self, list_of_lists):
        if isinstance(list_of_lists, list):
            if len(list_of_lists) == len(self.header):
                self.data1.append(list_of_lists)
                self.data = [OrderedDict(zip(self.header1, row)) for row in self.data1]
                temp1 = [row for row in self.data]
                return temp1
            else:
                raise Exception('Number of Column\'s in entered should be same as that of exiting data..')
        else:
            raise Exception('Invalid Input ..')


    def add_columns(self, list_of_values, column_name):
        if len(list_of_values) == len(self.data):
            for l in range(len(list_of_values)):
                self.data1[l].append(list_of_values[l])
                self.header1.append(column_name)
            self.data = [OrderedDict(zip(self.header1, row)) for row in self.data1]
            return_data_frame = [row for row in self.data]
            return return_data_frame
        else:
            raise Exception('Number of elements in column should be equal to number of rows in the existing data..')



# Open the CSV file and read lines
csvfile = open('SalesJan2009.csv')
lines = csvfile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]

# Fixing excessive column splits
Things = lines[559].split('"')
temp = Things[1]
temp = temp.replace(',', '')
Things[1] = temp
data[559] = Things[0].split(',')[:-1] + [Things[1]] + Things[2].split(',')[1:]

# To define variable to call the class
Df = DataFrame(data)
Column_Name = Df['Price']
#Find min of a column
Minimum_Value = Df.min('Transaction_date')
#Find max of a column
Maximum_Value = Df.max('Transaction_date')
#Find mean of a column
Mean_Value = Df.mean('Latitude')
#find median of a column
Median_Value = Df.median('Price')
#find Standard deviation of a column
Standard_Deviation = Df.std('Price')
#taking values to check for addition of columns is proper
list_of_column_entries = list(xrange(998))
#add columns
Data_after_addition = Df.add_columns(list_of_column_entries, 'temp')
#add rows
Rows_After_Addition = Df.add_rows(['1/5/09 4:10', 'Product1', '1200', 'Mastercard', 'Nicola', 'Roodepoort','Gauteng', 'South Africa', '1/5/09 2:33', '1/7/09 5:13', '-26.1666667', '27.8666667'])

# Check if it returns int_index rows
Int_Index = Df[997]

# Check if it passes range of rows
Slices = Df[4:10]

# Get item as df[row, column]
Tupled = Df[:, 2]
Tupled_slices = Df[0:5, 3:5]
Tupled_bits = Df[[1, 4], [1, 4]]
Df = DataFrame(list_of_lists=data[1:], header=False)

# Fetch column by names
Column_Name = Df['column1']
Column_Name_List = Df[['column1', 'column5']]

# Fetch Rows and Columns_By_name
Named_rows_columns = Df[:5, 'column5']
Named_rows_List_columns = Df[:5, ['column5', 'column7']]

rowz = Df.get_rows_where_column_has_value('Payment_Type', 'Visa', index_only=True)

c = 2+2
