#!/usr/bin/env python
# coding: utf-8

# <h1>1. Business Problem </h1>

# <h2> 1.1 Problem Description </h2>

# <p>
# Netflix is all about connecting people to the movies they love. To help customers find those movies, they developed world-class movie recommendation system: CinematchSM. Its job is to predict whether someone will enjoy a movie based on how much they liked or disliked other movies. Netflix use those predictions to make personal movie recommendations based on each customer’s unique tastes. And while <b>Cinematch</b> is doing pretty well, it can always be made better.
# </p>
# <p>Now there are a lot of interesting alternative approaches to how Cinematch works that netflix haven’t tried. Some are described in the literature, some aren’t. We’re curious whether any of these can beat Cinematch by making better predictions. Because, frankly, if there is a much better approach it could make a big difference to our customers and our business.</p>
# <p> Credits: https://www.netflixprize.com/rules.html </p>

# <h2> 1.2 Problem Statement </h2>

# <p>
# Netflix provided a lot of anonymous rating data, and a prediction accuracy bar that is 10% better than what Cinematch can do on the same training data set. (Accuracy is a measurement of how closely predicted ratings of movies match subsequent actual ratings.) 
# </p>

# <h2> 1.3 Sources </h2>

# <ul>
# <li> https://www.netflixprize.com/rules.html</li>
# <li> https://www.kaggle.com/netflix-inc/netflix-prize-data</li>
# <li> Netflix blog: https://medium.com/netflix-techblog/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429 (very nice blog)</li>
# <li>surprise library: http://surpriselib.com/ (we use many models from this library)</li>
# <li>surprise library doc: http://surprise.readthedocs.io/en/stable/getting_started.html (we use many models from this library)</li>
# <li>installing surprise: https://github.com/NicolasHug/Surprise#installation </li>
# <li> Research paper: http://courses.ischool.berkeley.edu/i290-dm/s11/SECURE/a1-koren.pdf (most of our work was inspired by this paper)</li>
# <li> SVD Decomposition : https://www.youtube.com/watch?v=P5mlg91as1c </li>
# </ul>

# <h2>1.4 Real world/Business Objectives and constraints  </h2>

# Objectives:
# 1. Predict the rating that a user would give to a movie that he ahs not yet rated.
# 2. Minimize the difference between predicted and actual rating (RMSE and MAPE)
# <br>
# 
# Constraints:
# 1. Some form of interpretability.

# <h1> 2. Machine Learning Problem </h1>

# <h2>2.1 Data </h2>

# <h3> 2.1.1 Data Overview </h3>

# <p> Get the data from : https://www.kaggle.com/netflix-inc/netflix-prize-data/data </p>
# <p> Data files : 
# <ul> 
# <li> combined_data_1.txt </li>
# <li> combined_data_2.txt </li>
# <li> combined_data_3.txt </li>
# <li> combined_data_4.txt </li>
# <li> movie_titles.csv </li>
# </ul>
# <pre>  
# The first line of each file [combined_data_1.txt, combined_data_2.txt, combined_data_3.txt, combined_data_4.txt] contains the movie id followed by a colon. Each subsequent line in the file corresponds to a rating from a customer and its date in the following format:
# 
# CustomerID,Rating,Date
# 
# MovieIDs range from 1 to 17770 sequentially.
# CustomerIDs range from 1 to 2649429, with gaps. There are 480189 users.
# Ratings are on a five star (integral) scale from 1 to 5.
# Dates have the format YYYY-MM-DD.
# </pre>

# <h3> 2.1.2 Example Data point </h3>

# <pre>
# 1:
# 1488844,3,2005-09-06
# 822109,5,2005-05-13
# 885013,4,2005-10-19
# 30878,4,2005-12-26
# 823519,3,2004-05-03
# 893988,3,2005-11-17
# 124105,4,2004-08-05
# 1248029,3,2004-04-22
# 1842128,4,2004-05-09
# 2238063,3,2005-05-11
# 1503895,4,2005-05-19
# 2207774,5,2005-06-06
# 2590061,3,2004-08-12
# 2442,3,2004-04-14
# 543865,4,2004-05-28
# 1209119,4,2004-03-23
# 804919,4,2004-06-10
# 1086807,3,2004-12-28
# 1711859,4,2005-05-08
# 372233,5,2005-11-23
# 1080361,3,2005-03-28
# 1245640,3,2005-12-19
# 558634,4,2004-12-14
# 2165002,4,2004-04-06
# 1181550,3,2004-02-01
# 1227322,4,2004-02-06
# 427928,4,2004-02-26
# 814701,5,2005-09-29
# 808731,4,2005-10-31
# 662870,5,2005-08-24
# 337541,5,2005-03-23
# 786312,3,2004-11-16
# 1133214,4,2004-03-07
# 1537427,4,2004-03-29
# 1209954,5,2005-05-09
# 2381599,3,2005-09-12
# 525356,2,2004-07-11
# 1910569,4,2004-04-12
# 2263586,4,2004-08-20
# 2421815,2,2004-02-26
# 1009622,1,2005-01-19
# 1481961,2,2005-05-24
# 401047,4,2005-06-03
# 2179073,3,2004-08-29
# 1434636,3,2004-05-01
# 93986,5,2005-10-06
# 1308744,5,2005-10-29
# 2647871,4,2005-12-30
# 1905581,5,2005-08-16
# 2508819,3,2004-05-18
# 1578279,1,2005-05-19
# 1159695,4,2005-02-15
# 2588432,3,2005-03-31
# 2423091,3,2005-09-12
# 470232,4,2004-04-08
# 2148699,2,2004-06-05
# 1342007,3,2004-07-16
# 466135,4,2004-07-13
# 2472440,3,2005-08-13
# 1283744,3,2004-04-17
# 1927580,4,2004-11-08
# 716874,5,2005-05-06
# 4326,4,2005-10-29
# </pre>

# <h2>2.2 Mapping the real world problem to a Machine Learning Problem </h2>

# <h3> 2.2.1 Type of Machine Learning Problem </h3>

# <pre>
# For a given movie and user we need to predict the rating would be given by him/her to the movie. 
# The given problem is a Recommendation problem 
# It can also seen as a Regression problem 
# </pre>

# <h3> 2.2.2 Performance metric </h3>

# <ul>
# <li> Mean Absolute Percentage Error: https://en.wikipedia.org/wiki/Mean_absolute_percentage_error </li>
# <li> Root Mean Square Error: https://en.wikipedia.org/wiki/Root-mean-square_deviation </li>
# </ul>
# 

# <h3> 2.2.3 Machine Learning Objective and Constraints </h3>

# 1. Minimize RMSE.
# 2. Try to provide some interpretability.

# In[1]:


# this is just to know how much time will it take to run this entire ipython notebook 
from datetime import datetime
# globalstart = datetime.now()
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('nbagg')

import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

import seaborn as sns
sns.set_style('whitegrid')
import os
from scipy import sparse
from scipy.sparse import csr_matrix

from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import random


#  

# <h1> 3. Exploratory Data Analysis </h1>

# <h2> 3.1 Preprocessing</h2> 

# <h3>3.1.1 Converting / Merging whole data to required format: u_i, m_j, r_ij</h3>

# In[5]:


start = datetime.now()
#if data.csv not exist it will go inside if
if not os.path.isfile('data.csv'):
    # Create a file 'data.csv' before reading it
    # Read all the files in netflix and store them in one big file('data.csv')
    # We re reading from each of the four files and appendig each rating to a global file 'train.csv'
    data = open('data.csv', mode='w')
    
    row = list()
    files=['data_folder/combined_data_1.txt','data_folder/combined_data_2.txt', 
           'data_folder/combined_data_3.txt', 'data_folder/combined_data_4.txt']
    for file in files:
        print("Reading ratings from {}...".format(file))
        with open(file) as f:
            for line in f: 
                del row[:] # you don't have to do this.
                line = line.strip()
                if line.endswith(':'):
                    # All below are ratings for this movie, until another movie appears.
                    movie_id = line.replace(':', '')
                else:
                    row = [x for x in line.split(',')]
                    row.insert(0, movie_id)
                    data.write(','.join(row))
                    data.write('\n')
        print("Done.\n")
    data.close()
print('Time taken :', datetime.now() - start)


#  

# In[2]:


print("creating the dataframe from data.csv file..")
df = pd.read_csv('data.csv', sep=',', 
                       names=['movie', 'user','rating','date'])
df.date = pd.to_datetime(df.date)
print('Done.\n')

# we are arranging the ratings according to time.
print('Sorting the dataframe by date..')
df.sort_values(by='date', inplace=True)
print('Done..')


# In[3]:


df.head()


# In[4]:


df.describe()['rating']


# <h3>3.1.2 Checking for NaN values </h3>

# In[5]:


# just to make sure that all Nan containing rows are deleted..
print("No of Nan values in our dataframe : ", sum(df.isnull().any()))


# <h3>3.1.3 Removing Duplicates </h3>

# In[6]:


dup_bool = df.duplicated(['movie','user','rating'])
dups = sum(dup_bool) # by considering all columns..( including timestamp)
print("There are {} duplicate rating entries in the data..".format(dups))


#  

#  <h3>3.1.4 Basic Statistics (#Ratings, #Users, and #Movies)</h3>

# In[7]:


print("Total data ")
print("-"*50)
print("\nTotal no of ratings :",df.shape[0])
print("Total No of Users   :", len(np.unique(df.user)))
print("Total No of movies  :", len(np.unique(df.movie)))


# <h2>3.2 Spliting data into Train and Test(80:20) </h2>

# In[8]:


#spliting whole data into train and test and storing it in train and test csv
if not os.path.isfile('train.csv'):
    # create the dataframe and store it in the disk for offline purposes..
    df.iloc[:int(df.shape[0]*0.80)].to_csv("train.csv", index=False)

if not os.path.isfile('test.csv'):
    # create the dataframe and store it in the disk for offline purposes..
    df.iloc[int(df.shape[0]*0.80):].to_csv("test.csv", index=False)

train_df = pd.read_csv("train.csv", parse_dates=['date'])
test_df = pd.read_csv("test.csv")


# <h3>3.2.1 Basic Statistics in Train data (#Ratings, #Users, and #Movies)</h3>

# In[9]:


# movies = train_df.movie.value_counts()
# users = train_df.user.value_counts()
print("Training data ")
print("-"*50)
print("\nTotal no of ratings :",train_df.shape[0])
print("Total No of Users   :", len(np.unique(train_df.user)))
print("Total No of movies  :", len(np.unique(train_df.movie)))


# <h3>3.2.2 Basic Statistics in Test data (#Ratings, #Users, and #Movies)</h3>

# In[10]:


print("Test data ")
print("-"*50)
print("\nTotal no of ratings :",test_df.shape[0])
print("Total No of Users   :", len(np.unique(test_df.user)))
print("Total No of movies  :", len(np.unique(test_df.movie)))


#  <h2> 3.3 Exploratory Data Analysis on Train data </h2>

#  

# In[11]:


# method to make y-axis more readable
def human(num, units = 'M'):
    units = units.lower()
    num = float(num)
    if units == 'k':
        return str(num/10**3) + " K"
    elif units == 'm':
        return str(num/10**6) + " M"
    elif units == 'b':
        return str(num/10**9) +  " B"


# <h3> 3.3.1 Distribution of ratings </h3>

# In[16]:


fig, ax = plt.subplots()
plt.title('Distribution of ratings over Training dataset', fontsize=15)
sns.countplot(train_df.rating)
ax.set_yticklabels([human(item, 'M') for item in ax.get_yticks()])
ax.set_ylabel('No. of Ratings(Millions)')

plt.show()


# <p style="font-size:13px"> <b>Add new column (week day) to the data set  for analysis.</b></p>

# In[12]:


# It is used to skip the warning ''SettingWithCopyWarning''.. 
pd.options.mode.chained_assignment = None  # default='warn'

train_df['day_of_week'] = train_df.date.dt.weekday_name

train_df.tail()


# <h3> 3.3.2 Number of Ratings per a month </h3>

# In[18]:


ax = train_df.resample('m', on='date')['rating'].count().plot()
ax.set_title('No of ratings per month (Training data)')
plt.xlabel('Month')
plt.ylabel('No of ratings(per month)')
ax.set_yticklabels([human(item, 'M') for item in ax.get_yticks()])
plt.show()


#  

# <h3> 3.3.3 Analysis on the Ratings given by user </h3>

# In[19]:


no_of_rated_movies_per_user = train_df.groupby(by='user')['rating'].count().sort_values(ascending=False)

no_of_rated_movies_per_user.head()


# In[20]:


fig = plt.figure(figsize=plt.figaspect(.5))

ax1 = plt.subplot(121)
sns.kdeplot(no_of_rated_movies_per_user, shade=True, ax=ax1)
plt.xlabel('No of ratings by user')
plt.title("PDF")

ax2 = plt.subplot(122)
sns.kdeplot(no_of_rated_movies_per_user, shade=True, cumulative=True,ax=ax2)
plt.xlabel('No of ratings by user')
plt.title('CDF')

plt.show()


# In[21]:


no_of_rated_movies_per_user.describe()


# > _There,  is something interesting going on with the quantiles.._

# In[22]:


quantiles = no_of_rated_movies_per_user.quantile(np.arange(0,1.01,0.01), interpolation='higher')


# In[23]:


plt.title("Quantiles and their Values")
quantiles.plot()
# quantiles with 0.05 difference
plt.scatter(x=quantiles.index[::5], y=quantiles.values[::5], c='orange', label="quantiles with 0.05 intervals")
# quantiles with 0.25 difference
plt.scatter(x=quantiles.index[::25], y=quantiles.values[::25], c='m', label = "quantiles with 0.25 intervals")
plt.ylabel('No of ratings by user')
plt.xlabel('Value at the quantile')
plt.legend(loc='best')

# annotate the 25th, 50th, 75th and 100th percentile values....
for x,y in zip(quantiles.index[::25], quantiles[::25]):
    plt.annotate(s="({} , {})".format(x,y), xy=(x,y), xytext=(x-0.05, y+500)
                ,fontweight='bold')


plt.show()


# In[24]:


quantiles[::5]


# __how many ratings at the last 5% of all ratings__??

# In[25]:


print('\n No of ratings at last 5 percentile : {}\n'.format(sum(no_of_rated_movies_per_user>= 749)) )


# <h3> 3.3.4 Analysis of ratings of a movie given by a user </h3>

# In[26]:


no_of_ratings_per_movie = train_df.groupby(by='movie')['rating'].count().sort_values(ascending=False)

fig = plt.figure(figsize=plt.figaspect(.5))
ax = plt.gca()
plt.plot(no_of_ratings_per_movie.values)
plt.title('# RATINGS per Movie')
plt.xlabel('Movie')
plt.ylabel('No of Users who rated a movie')
ax.set_xticklabels([])

plt.show()


# - __It is very skewed.. just like nunmber of ratings given per user.__
#     
#     
#     - There are some movies (which are very popular) which are rated by huge number of users.
#     
#     - But most of the movies(like 90%) got some hundereds of ratings.

# <h3> 3.3.5 Number of ratings on each day of the week</h3>

# In[28]:


fig, ax = plt.subplots()
sns.countplot(x='day_of_week', data=train_df, ax=ax)
plt.title('No of ratings on each day...')
plt.ylabel('Total no of ratings')
plt.xlabel('')
ax.set_yticklabels([human(item, 'M') for item in ax.get_yticks()])
plt.show()


# In[29]:


start = datetime.now()
fig = plt.figure(figsize=plt.figaspect(.45))
sns.boxplot(y='rating', x='day_of_week', data=train_df)
plt.show()
print(datetime.now() - start)


# In[30]:


avg_week_df = train_df.groupby(by=['day_of_week'])['rating'].mean()
print(" AVerage ratings")
print("-"*30)
print(avg_week_df)
print("\n")


#  

# <h3> 3.3.6 Creating sparse matrix from data frame </h3>

# <table>
# <tr>
# <td>
# <img src='http://www.techscript24.com/admin/UI/assets/img/BlogsImage/data_c.jpg' width='250px' align=left/>
# </td>
# <td>
# <img src='http://www.techscript24.com/admin/UI/assets/img/BlogsImage/arrow.jpg' width='60px' align=left/>
# </td>
# <td>
# <img src='http://www.techscript24.com/admin/UI/assets/img/BlogsImage/data_sparse_c.jpg' width='400px' align=left/>
# </td>
# </tr>
# </table>

# <h4> 3.3.6.1 Creating sparse matrix from train data frame </h4>

# In[13]:


start = datetime.now()
if os.path.isfile('train_sparse_matrix.npz'):
    print("It is present in your pwd, getting it from disk....")
    # just get it from the disk instead of computing it
    train_sparse_matrix = sparse.load_npz('train_sparse_matrix.npz')
    print("DONE..")
else: 
    print("We are creating sparse_matrix from the dataframe..")
    # create sparse_matrix and store it for after usage.
    # csr_matrix(data_values, (row_index, col_index), shape_of_matrix)
    # It should be in such a way that, MATRIX[row, col] = data
    train_sparse_matrix = sparse.csr_matrix((train_df.rating.values, (train_df.user.values,
                                               train_df.movie.values)),)
    
    print('Done. It\'s shape is : (user, movie) : ',train_sparse_matrix.shape)
    print('Saving it into disk for furthur usage..')
    # save it into disk
    sparse.save_npz("train_sparse_matrix.npz", train_sparse_matrix)
    print('Done..\n')

print(datetime.now() - start)


# <p><b>The Sparsity of Train Sparse Matrix</b></p>

# In[32]:


# here it means 99.83.... % of matrix has zero value 
us,mv = train_sparse_matrix.shape
elem = train_sparse_matrix.count_nonzero()

print("Sparsity Of Train matrix : {} % ".format(  (1-(elem/(us*mv))) * 100) )


# <h4> 3.3.6.2 Creating sparse matrix from test data frame </h4>

# In[14]:


start = datetime.now()
if os.path.isfile('test_sparse_matrix.npz'):
    print("It is present in your pwd, getting it from disk....")
    # just get it from the disk instead of computing it
    test_sparse_matrix = sparse.load_npz('test_sparse_matrix.npz')
    print("DONE..")
else: 
    print("We are creating sparse_matrix from the dataframe..")
    # create sparse_matrix and store it for after usage.
    # csr_matrix(data_values, (row_index, col_index), shape_of_matrix)
    # It should be in such a way that, MATRIX[row, col] = data
    test_sparse_matrix = sparse.csr_matrix((test_df.rating.values, (test_df.user.values,
                                               test_df.movie.values)))
    
    print('Done. It\'s shape is : (user, movie) : ',test_sparse_matrix.shape)
    print('Saving it into disk for furthur usage..')
    # save it into disk
    sparse.save_npz("test_sparse_matrix.npz", test_sparse_matrix)
    print('Done..\n')
    
print(datetime.now() - start)


# <p><b>The Sparsity of Test data Matrix</b></p>

# In[34]:


us,mv = test_sparse_matrix.shape
elem = test_sparse_matrix.count_nonzero()

print("Sparsity Of Test matrix : {} % ".format(  (1-(elem/(us*mv))) * 100) )


# <h3>3.3.7 Finding Global average of all movie ratings, Average rating per user, and Average rating per movie</h3>

# In[15]:


# get the user averages in dictionary (key: user_id/movie_id, value: avg rating)

def get_average_ratings(sparse_matrix, of_users):
    
    # average ratings of user/axes
    ax = 1 if of_users else 0 # 1 - User axes,0 - Movie axes

    # ".A1" is for converting Column_Matrix to 1-D numpy array 
    sum_of_ratings = sparse_matrix.sum(axis=ax).A1
    # Boolean matrix of ratings ( whether a user rated that movie or not)
    is_rated = sparse_matrix!=0
    # no of ratings that each user OR movie..
    no_of_ratings = is_rated.sum(axis=ax).A1
    
    # max_user  and max_movie ids in sparse matrix 
    u,m = sparse_matrix.shape
    # creae a dictonary of users and their average ratigns..
    average_ratings = { i : sum_of_ratings[i]/no_of_ratings[i]
                                 for i in range(u if of_users else m) 
                                    if no_of_ratings[i] !=0}

    # return that dictionary of average ratings
    return average_ratings


# <h4> 3.3.7.1 finding global average of all movie ratings </h4>

# In[16]:


train_averages = dict()
# get the global average of ratings in our train set.
train_global_average = train_sparse_matrix.sum()/train_sparse_matrix.count_nonzero()
train_averages['global'] = train_global_average
train_averages


# <h4> 3.3.7.2 finding average rating per user</h4>

# In[17]:


train_averages['user'] = get_average_ratings(train_sparse_matrix, of_users=True)
print('\nAverage rating of user 10 :',train_averages['user'][10])


# <h4> 3.3.7.3 finding average rating per movie</h4>

# In[18]:


train_averages['movie'] =  get_average_ratings(train_sparse_matrix, of_users=False)
print('\n AVerage rating of movie 15 :',train_averages['movie'][15])


#  

# <h4> 3.3.7.4 PDF's & CDF's of Avg.Ratings of Users & Movies (In Train Data)</h4>

# In[19]:


start = datetime.now()
# draw pdfs for average rating per user and average
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=plt.figaspect(.5))
fig.suptitle('Avg Ratings per User and per Movie', fontsize=15)

ax1.set_title('Users-Avg-Ratings')
# get the list of average user ratings from the averages dictionary..
user_averages = [rat for rat in train_averages['user'].values()]
sns.distplot(user_averages, ax=ax1, hist=False, 
             kde_kws=dict(cumulative=True), label='Cdf')
sns.distplot(user_averages, ax=ax1, hist=False,label='Pdf')

ax2.set_title('Movies-Avg-Rating')
# get the list of movie_average_ratings from the dictionary..
movie_averages = [rat for rat in train_averages['movie'].values()]
sns.distplot(movie_averages, ax=ax2, hist=False, 
             kde_kws=dict(cumulative=True), label='Cdf')
sns.distplot(movie_averages, ax=ax2, hist=False, label='Pdf')

plt.show()
print(datetime.now() - start)


# <h3> 3.3.8 Cold Start problem </h3>

# <h4> 3.3.8.1 Cold Start problem with Users</h4>

# In[20]:


total_users = len(np.unique(df.user))
users_train = len(train_averages['user'])
new_users = total_users - users_train

print('\nTotal number of Users  :', total_users)
print('\nNumber of Users in Train data :', users_train)
print("\nNo of Users that didn't appear in train data: {}({} %) \n ".format(new_users,
                                                                        np.round((new_users/total_users)*100, 2)))


# > We might have to handle __new users__ ( ___75148___ ) who didn't appear in train data.

# <h4> 3.3.8.2 Cold Start problem with Movies</h4>

# In[21]:


total_movies = len(np.unique(df.movie))
movies_train = len(train_averages['movie'])
new_movies = total_movies - movies_train

print('\nTotal number of Movies  :', total_movies)
print('\nNumber of Users in Train data :', movies_train)
print("\nNo of Movies that didn't appear in train data: {}({} %) \n ".format(new_movies,
                                                                        np.round((new_movies/total_movies)*100, 2)))


# > We might have to handle __346 movies__ (small comparatively) in test data

#  

# <h2> 3.4 Computing Similarity matrices </h2>

# <h3> 3.4.1 Computing User-User Similarity matrix </h3>

# 1. Calculating User User Similarity_Matrix is __not very easy__(_unless you have huge Computing Power and lots of time_) because of number of. usersbeing lare.
# 
#     * You can try if you want to. Your system could crash or the program stops with **Memory Error**
# 

# <h4> 3.4.1.1 Trying with all dimensions (17k dimensions per user) </h4>

# In[22]:


from sklearn.metrics.pairwise import cosine_similarity


def compute_user_similarity(sparse_matrix, compute_for_few=False, top = 100, verbose=False, verb_for_n_rows = 20,
                            draw_time_taken=True):
    no_of_users, _ = sparse_matrix.shape
    # get the indices of  non zero rows(users) from our sparse matrix
    row_ind, col_ind = sparse_matrix.nonzero()
    row_ind = sorted(set(row_ind)) # we don't have to
    time_taken = list() #  time taken for finding similar users for an user..
    
    # we create rows, cols, and data lists.., which can be used to create sparse matrices
    rows, cols, data = list(), list(), list()
    if verbose: print("Computing top",top,"similarities for each user..")
    
    start = datetime.now()
    temp = 0
    
    for row in row_ind[:top] if compute_for_few else row_ind:
        temp = temp+1
        prev = datetime.now()
        
        # get the similarity row for this user with all other users
        sim = cosine_similarity(sparse_matrix.getrow(row), sparse_matrix).ravel()
        # We will get only the top ''top'' most similar users and ignore rest of them..
        top_sim_ind = sim.argsort()[-top:]
        top_sim_val = sim[top_sim_ind]
        
        # add them to our rows, cols and data
        rows.extend([row]*top)
        cols.extend(top_sim_ind)
        data.extend(top_sim_val)
        time_taken.append(datetime.now().timestamp() - prev.timestamp())
        if verbose:
            if temp%verb_for_n_rows == 0:
                print("computing done for {} users [  time elapsed : {}  ]"
                      .format(temp, datetime.now()-start))
            
        
    # lets create sparse matrix out of these and return it
    if verbose: print('Creating Sparse matrix from the computed similarities')
    #return rows, cols, data
    
    if draw_time_taken:
        plt.plot(time_taken, label = 'time taken for each user')
        plt.plot(np.cumsum(time_taken), label='Total time')
        plt.legend(loc='best')
        plt.xlabel('User')
        plt.ylabel('Time (seconds)')
        plt.show()
        
    return sparse.csr_matrix((data, (rows, cols)), shape=(no_of_users, no_of_users)), time_taken      


# In[43]:


## we are not going to run it on whole data it will gives us memory error so we willl try it on 100 see 3.4.1.2
start = datetime.now()
u_u_sim_sparse, _ = compute_user_similarity(train_sparse_matrix, compute_for_few=True, top = 100,
                                                     verbose=True)
print("-"*100)
print("Time taken :",datetime.now()-start)


# <h4> 3.4.1.2 Trying with reduced dimensions (Using TruncatedSVD for dimensionality reduction of user vector)</h4>

#  

# * We have  **405,041 users** in out training set and computing similarities between them..( **17K dimensional vector..**) is time consuming..
# 
# 
# - From above plot, It took roughly __8.88 sec__ for computing simlilar users for __one user__
#     
#     
# - We have __405,041 users__ with us in training set.
# 
# 
# - ${ 405041 \times 8.88 = 3596764.08  \sec } =  59946.068 \min = 999.101133333 \text{ hours}
# = 41.629213889 \text{ days}...$
# 
#     - Even if we run on 4 cores parallelly (a typical system now a days), It will still take almost __10 and 1/2__ days.
#     
#  IDEA:  Instead, we will try to reduce the dimentsions using SVD, so that __it might__ speed up the process...

# In[ ]:


from datetime import datetime
from sklearn.decomposition import TruncatedSVD

start = datetime.now()

# initilaize the algorithm with some parameters..
# All of them are default except n_components. n_itr is for Randomized SVD solver.
netflix_svd = TruncatedSVD(n_components=500, algorithm='randomized', random_state=15)
trunc_svd = netflix_svd.fit_transform(train_sparse_matrix)

print(datetime.now()-start)


# Here,
# 
# 
# - $\sum \longleftarrow$ (netflix\_svd.**singular\_values\_** )
# 
# 
# - $\bigvee^T \longleftarrow$ (netflix\_svd.**components_**)
# 
# 
# - $\bigcup$ is not returned. instead **Projection_of_X** onto the new vectorspace is returned. 
# 
# 
# - It uses **randomized svd** internally, which returns **All 3 of them saperately**. Use that instead.. 

# In[ ]:


expl_var = np.cumsum(netflix_svd.explained_variance_ratio_)


# In[ ]:


fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=plt.figaspect(.5))

ax1.set_ylabel("Variance Explained", fontsize=15)
ax1.set_xlabel("# Latent Facors", fontsize=15)
ax1.plot(expl_var)
# annote some (latentfactors, expl_var) to make it clear
ind = [1, 2,4,8,20, 60, 100, 200, 300, 400, 500]
ax1.scatter(x = [i-1 for i in ind], y = expl_var[[i-1 for i in ind]], c='#ff3300')
for i in ind:
    ax1.annotate(s ="({}, {})".format(i,  np.round(expl_var[i-1], 2)), xy=(i-1, expl_var[i-1]),
                xytext = ( i+20, expl_var[i-1] - 0.01), fontweight='bold')

change_in_expl_var = [expl_var[i+1] - expl_var[i] for i in range(len(expl_var)-1)]
ax2.plot(change_in_expl_var)



ax2.set_ylabel("Gain in Var_Expl with One Additional LF", fontsize=10)
ax2.yaxis.set_label_position("right")
ax2.set_xlabel("# Latent Facors", fontsize=20)

plt.show()


# In[ ]:


for i in ind:
    print("({}, {})".format(i, np.round(expl_var[i-1], 2)))


#  
# > I think 500 dimensions is good enough 
# 
# ---------
# 
# -  By just taking __(20 to 30)__ latent factors, explained variance that we could get is __20 %__. 
# 
# - To take it to __60%__, we have to take  __almost 400 latent factors__. It is not fare.
# 
# 
# 
# - It basically is the __gain of variance explained__, if we ___add one additional latent factor to it.___
# 
# 
# - By adding one by one latent factore too it, the ___gain in expained variance__ with that addition is decreasing. (Obviously, because they are sorted that way).
# - ___LHS Graph___:
#     - __x__ --- ( No of latent factos ),
#     - __y__ --- ( The variance explained by taking x latent factors)
# 
# 
# 
# - __More decrease in the line (RHS graph) __:
#     - We  are getting more expained variance than before.
# - __Less decrease in that line (RHS graph)__  :
#     - We are not getting benifitted from adding latent factor furthur. This is what is shown in the plots.
# 
# 
# - ___RHS Graph___:
#     - __x__ --- ( No of latent factors ),
#     - __y__ --- ( Gain n Expl_Var by taking one additional latent factor) 

# In[ ]:


# Let's project our Original U_M matrix into into 500 Dimensional space...
start = datetime.now()
trunc_matrix = train_sparse_matrix.dot(netflix_svd.components_.T)
print(datetime.now()- start)


# In[ ]:


type(trunc_matrix), trunc_matrix.shape


# * Let's convert this to actual sparse matrix and store it for future purposes

# In[46]:


if not os.path.isfile('trunc_sparse_matrix.npz'):
    # create that sparse sparse matrix
    trunc_sparse_matrix = sparse.csr_matrix(trunc_matrix)
    # Save this truncated sparse matrix for later usage..
    sparse.save_npz('trunc_sparse_matrix', trunc_sparse_matrix)
else:
    trunc_sparse_matrix = sparse.load_npz('trunc_sparse_matrix.npz')


# In[47]:


trunc_sparse_matrix.shape


# In[ ]:


#getting memory error
start = datetime.now()
trunc_u_u_sim_matrix, _ = compute_user_similarity(trunc_sparse_matrix, compute_for_few=True, top=50, verbose=True, 
                                                 verb_for_n_rows=10)
print("-"*50)
print("time:",datetime.now()-start)


# **: This is taking more time for each user than Original one.**

# - from above plot, It took almost __12.18__ for computing simlilar users for __one user__
#     
#     
# - We have __405041 users__ with us in training set.
# 
# 
# - ${ 405041 \times 12.18 ==== 4933399.38 \sec } ====  82223.323 \min ==== 1370.388716667 \text{ hours}
# ==== 57.099529861 \text{ days}...$
# 
#     - Even we run on 4 cores parallelly (a typical system now a days), It will still take almost __(14 - 15) __ days.
# 

# - __Why did this happen...??__
# 
# 
#     - Just think about it. It's not that difficult.
# 
# ---------------------------------_( sparse & dense..................get it ?? )_-----------------------------------

# __Is there any other way to compute user user similarity..??__

# -An alternative is to compute similar users for a particular user,  whenenver required (**ie., Run time**)
#     - We maintain a binary Vector for users, which tells us whether we already computed or not..
#     - ***If not*** : 
#         - Compute top (let's just say, 1000) most similar users for this given user, and add this to our datastructure, so that we can just access it(similar users) without recomputing it again.
#         - 
#     - ***If It is already Computed***:
#         - Just get it directly from our datastructure, which has that information.
#         - In production time, We might have to recompute similarities, if it is computed a long time ago. Because user preferences changes over time. If we could maintain some kind of Timer, which when expires, we have to update it ( recompute it ). 
#         - 
#     - ***Which datastructure to use:***
#         - It is purely implementation dependant. 
#         - One simple method is to maintain a **Dictionary Of Dictionaries**.
#             - 
#             - **key    :** _userid_ 
#             - __value__: _Again a dictionary_
#                 - __key__  : _Similar User_
#                 - __value__: _Similarity Value_

# <h3> 3.4.2 Computing Movie-Movie Similarity matrix </h3>

# In[25]:


start = datetime.now()
if not os.path.isfile('movie_movie_sim_sparse.npz'):
    print("It seems you don't have that file. Computing movie_movie similarity...")
    start = datetime.now()
    m_m_sim_sparse = cosine_similarity(X=train_sparse_matrix.T, dense_output=False)
    print("Done..")
    # store this sparse matrix in disk before using it. For future purposes.
    print("Saving it to disk without the need of re-computing it again.. ")
    sparse.save_npz("movie_movie_sim_sparse.npz", m_m_sim_sparse)
    print("Done..")
else:
    print("It is there, We will get it.")
    m_m_sim_sparse = sparse.load_npz("m_m_sim_sparse.npz")
    print("Done ...")

# print("It's a ",m_m_sim_sparse.shape," dimensional matrix")

print(datetime.now() - start)


# In[26]:


m_m_sim_sparse.shape


# - Even though we have similarity measure of each movie, with all other movies, We generally don't care much about least similar movies.
# 
# 
# - Most of the times, only top_xxx similar items matters. It may be 10 or 100.
# 
# 
# - We take only those top similar movie ratings and store them  in a saperate dictionary.

# In[27]:


movie_ids = np.unique(m_m_sim_sparse.nonzero()[1])


# In[28]:


start = datetime.now()
similar_movies = dict()
for movie in movie_ids:
    # get the top similar movies and store them in the dictionary
    sim_movies = m_m_sim_sparse[movie].toarray().ravel().argsort()[::-1][1:]
    similar_movies[movie] = sim_movies[:100]
print(datetime.now() - start)

# just testing similar movies for movie_15
similar_movies[15]


#  

# <h3> 3.4.3 Finding most similar movies using similarity matrix </h3>

# __ Does Similarity really works as the way we expected...? __ <br>
# _Let's pick some random movie and check for its similar movies...._

# In[29]:


# First Let's load the movie details into soe dataframe..
# movie details are in 'netflix/movie_titles.csv'

movie_titles = pd.read_csv("movie_titles.csv", sep=',', header = None,
                           names=['movie_id', 'year_of_release', 'title'], verbose=True,
                      index_col = 'movie_id', encoding = "ISO-8859-1")

movie_titles.head()


# <p style='font-size:15px'><b>Similar Movies for 'Vampire Journals'</b></p>

# In[30]:


mv_id = 67

print("\nMovie ----->",movie_titles.loc[mv_id].values[1])

print("\nIt has {} Ratings from users.".format(train_sparse_matrix[:,mv_id].getnnz()))

print("\nWe have {} movies which are similarto this  and we will get only top most..".format(m_m_sim_sparse[:,mv_id].getnnz()))


# In[31]:


similarities = m_m_sim_sparse[mv_id].toarray().ravel()

similar_indices = similarities.argsort()[::-1][1:]

similarities[similar_indices]

sim_indices = similarities.argsort()[::-1][1:] # It will sort and reverse the array and ignore its similarity (ie.,1)
                                               # and return its indices(movie_ids)


# In[32]:


plt.plot(similarities[sim_indices], label='All the ratings')
plt.plot(similarities[sim_indices[:100]], label='top 100 similar movies')
plt.title("Similar Movies of {}(movie_id)".format(mv_id), fontsize=20)
plt.xlabel("Movies (Not Movie_Ids)", fontsize=15)
plt.ylabel("Cosine Similarity",fontsize=15)
plt.legend()
plt.show()


#  

#  

# __Top 10 similar movies__

# In[33]:


movie_titles.loc[sim_indices[:10]]


#  

#  > Similarly, we can ___find similar users___ and compare how similar they are. 

#  

#  

#  <h1> 4.  Machine Learning Models </h1>

# <img src='http://www.techscript24.com/admin/UI/assets/img/BlogsImage/models.jpg' width=500px>

# In[53]:


def get_sample_sparse_matrix(sparse_matrix, no_users, no_movies, path, verbose = True):
    """
        It will get it from the ''path'' if it is present  or It will create 
        and store the sampled sparse matrix in the path specified.
    """

    # get (row, col) and (rating) tuple from sparse_matrix...
    row_ind, col_ind, ratings = sparse.find(sparse_matrix)
    users = np.unique(row_ind)
    movies = np.unique(col_ind)

    print("Original Matrix : (users, movies) -- ({} {})".format(len(users), len(movies)))
    print("Original Matrix : Ratings -- {}\n".format(len(ratings)))

    # It just to make sure to get same sample everytime we run this program..
    # and pick without replacement....
    np.random.seed(15)
    sample_users = np.random.choice(users, no_users, replace=False)
    sample_movies = np.random.choice(movies, no_movies, replace=False)
    # get the boolean mask or these sampled_items in originl row/col_inds..
    mask = np.logical_and( np.isin(row_ind, sample_users),
                      np.isin(col_ind, sample_movies) )
    
    sample_sparse_matrix = sparse.csr_matrix((ratings[mask], (row_ind[mask], col_ind[mask])),
                                             shape=(max(sample_users)+1, max(sample_movies)+1))

    if verbose:
        print("Sampled Matrix : (users, movies) -- ({} {})".format(len(sample_users), len(sample_movies)))
        print("Sampled Matrix : Ratings --", format(ratings[mask].shape[0]))

    print('Saving it into disk for furthur usage..')
    # save it into disk
    sparse.save_npz(path, sample_sparse_matrix)
    if verbose:
            print('Done..\n')
    
    return sample_sparse_matrix


# <h2> 4.1 Sampling Data </h2>

# <h3>4.1.1 Build sample train data from the train data</h3>

# In[139]:


# load 3.3.6.1 cell for getting train_sparse_matrix
# train_sparse_matrix = sparse.load_npz('train_sparse_matrix.npz')
# test_sparse_matrix = sparse.load_npz('test_sparse_matrix.npz')
# above are the matrix for all the users and movies
# train_sparse_matrix.shape


# In[140]:


# As we know train_sparse_matrix contains matrix for user and movies lets take user and movies from it 
start = datetime.now()
path = "sample_train_sparse_matrix.npz"
if os.path.isfile(path):
    print("It is present in your pwd, getting it from disk....")
    # just get it from the disk instead of computing it
    sample_train_sparse_matrix = sparse.load_npz(path)
    print("DONE..")
else: 
    # get 10k users and 1k movies from available data 
    sample_train_sparse_matrix = get_sample_sparse_matrix(train_sparse_matrix, no_users=10000, no_movies=1000,path = path)

print(datetime.now() - start)


# <h3>4.1.2 Build sample test data from the test data</h3>

# In[141]:


start = datetime.now()

path = "sample_test_sparse_matrix.npz"
if os.path.isfile(path):
    print("It is present in your pwd, getting it from disk....")
    # just get it from the disk instead of computing it
    sample_test_sparse_matrix = sparse.load_npz(path)
    print("DONE..")
else:
    # get 5k users and 500 movies from available data 
    sample_test_sparse_matrix = get_sample_sparse_matrix(test_sparse_matrix, no_users=5000, no_movies=500,path = path)
print(datetime.now() - start)


#  

# <h2>4.2 Finding Global Average of all movie ratings, Average rating per User, and Average rating per Movie (from sampled train)</h2>

# In[142]:


sample_train_averages = dict()


# <h3>4.2.1 Finding Global Average of all movie ratings</h3>

# In[143]:


# get the global average of ratings in our train set.
global_average = sample_train_sparse_matrix.sum()/sample_train_sparse_matrix.count_nonzero()
sample_train_averages['global'] = global_average
sample_train_averages


# <h3>4.2.2 Finding Average rating per User</h3>

# In[144]:


sample_train_averages['user'] = get_average_ratings(sample_train_sparse_matrix, of_users=True)
print('\nAverage rating of user 1515220 :',sample_train_averages['user'][1515220])


# <h3>4.2.3 Finding Average rating per Movie</h3>

# In[145]:


sample_train_averages['movie'] =  get_average_ratings(sample_train_sparse_matrix, of_users=False)
print('\n AVerage rating of movie 15153 :',sample_train_averages['movie'][15153])


#  

# <h2> 4.3 Featurizing data </h2>

# In[146]:


print('\n No of ratings in Our Sampled train matrix is : {}\n'.format(sample_train_sparse_matrix.count_nonzero()))
print('\n No of ratings in Our Sampled test  matrix is : {}\n'.format(sample_test_sparse_matrix.count_nonzero()))


# <h3> 4.3.1 Featurizing data for regression problem </h3>

# <h4> 4.3.1.1 Featurizing train data </h4>

# In[147]:


# get users, movies and ratings from our samples train sparse matrix
sample_train_users, sample_train_movies, sample_train_ratings = sparse.find(sample_train_sparse_matrix)


# In[71]:


# sample_train_ratings.shape


# In[148]:


############################################################
# It took me almost 26 hours to prepare this train dataset on my pc.#
############################################################
start = datetime.now()
if os.path.isfile('reg_train.csv'):
    print("File already exists you don't have to prepare again..." )
else:
    print('preparing {} tuples for the dataset..\n'.format(len(sample_train_ratings)))
    with open('reg_train.csv', mode='w') as reg_data_file:
        count = 0
        for (user, movie, rating)  in zip(sample_train_users, sample_train_movies, sample_train_ratings):
            st = datetime.now()
        #     print(user, movie)    
            #--------------------- Ratings of "movie" by similar users of "user" ---------------------
            # compute the similar Users of the "user"        
            user_sim = cosine_similarity(sample_train_sparse_matrix[user], sample_train_sparse_matrix).ravel()
            top_sim_users = user_sim.argsort()[::-1][1:] # we are ignoring 'The User' from its similar users.
            # get the ratings of most similar users for this movie
            top_ratings = sample_train_sparse_matrix[top_sim_users, movie].toarray().ravel()
            # we will make it's length "5" by adding movie averages to .
            top_sim_users_ratings = list(top_ratings[top_ratings != 0][:5])
            top_sim_users_ratings.extend([sample_train_averages['movie'][movie]]*(5 - len(top_sim_users_ratings)))
        #     print(top_sim_users_ratings, end=" ")    


            #--------------------- Ratings by "user"  to similar movies of "movie" ---------------------
            # compute the similar movies of the "movie"        
            movie_sim = cosine_similarity(sample_train_sparse_matrix[:,movie].T, sample_train_sparse_matrix.T).ravel()
            top_sim_movies = movie_sim.argsort()[::-1][1:] # we are ignoring 'The User' from its similar users.
            # get the ratings of most similar movie rated by this user..
            top_ratings = sample_train_sparse_matrix[user, top_sim_movies].toarray().ravel()
            # we will make it's length "5" by adding user averages to.
            top_sim_movies_ratings = list(top_ratings[top_ratings != 0][:5])
            top_sim_movies_ratings.extend([sample_train_averages['user'][user]]*(5-len(top_sim_movies_ratings))) 
        #     print(top_sim_movies_ratings, end=" : -- ")

            #-----------------prepare the row to be stores in a file-----------------#
            row = list()
            row.append(user)
            row.append(movie)
            # Now add the other features to this data...
            row.append(sample_train_averages['global']) # first feature
            # next 5 features are similar_users "movie" ratings
            row.extend(top_sim_users_ratings)
            # next 5 features are "user" ratings for similar_movies
            row.extend(top_sim_movies_ratings)
            # Avg_user rating
            row.append(sample_train_averages['user'][user])
            # Avg_movie rating
            row.append(sample_train_averages['movie'][movie])

            # finalley, The actual Rating of this user-movie pair...
            row.append(rating)
            count = count + 1

            # add rows to the file opened..
            reg_data_file.write(','.join(map(str, row)))
            reg_data_file.write('\n')        
            if (count)%10000 == 0:
                # print(','.join(map(str, row)))
                print("Done for {} rows----- {}".format(count, datetime.now() - start))


print(datetime.now() - start)


# In[ ]:





# __Reading from the file to make a Train_dataframe__

# In[149]:


reg_train = pd.read_csv('reg_train.csv', names = ['user', 'movie', 'GAvg', 'sur1', 'sur2', 'sur3', 'sur4', 'sur5','smr1', 'smr2', 'smr3', 'smr4', 'smr5', 'UAvg', 'MAvg', 'rating'], header=None)
reg_train.head()


# -----------------------
# 
# - __GAvg__ : Average rating of all the ratings 
# 
# 
# - __Similar users rating of this movie__:
#     - sur1, sur2, sur3, sur4, sur5 ( top 5 similar users who rated that movie.. )
#     
# 
# 
# - __Similar movies rated by this user__:
#     - smr1, smr2, smr3, smr4, smr5 ( top 5 similar movies rated by this movie.. )
# 
# 
# - __UAvg__ : User's Average rating
# 
# 
# - __MAvg__ : Average rating of this movie
# 
# 
# - __rating__ : Rating of this movie by this user.
# 
# -----------------------

#  

# <h4> 4.3.1.2 Featurizing test data </h4>

# In[150]:


# get users, movies and ratings from the Sampled Test 
sample_test_users, sample_test_movies, sample_test_ratings = sparse.find(sample_test_sparse_matrix)


# In[151]:


sample_train_averages['global']


# In[152]:


start = datetime.now()

if os.path.isfile('reg_test.csv'):
    print("It is already created...")
else:

    print('preparing {} tuples for the dataset..\n'.format(len(sample_test_ratings)))
    with open('reg_test.csv', mode='w') as reg_data_file:
        count = 0 
        for (user, movie, rating)  in zip(sample_test_users, sample_test_movies, sample_test_ratings):
            st = datetime.now()

        #--------------------- Ratings of "movie" by similar users of "user" ---------------------
            #print(user, movie)
            try:
                # compute the similar Users of the "user"        
                user_sim = cosine_similarity(sample_train_sparse_matrix[user], sample_train_sparse_matrix).ravel()
                top_sim_users = user_sim.argsort()[::-1][1:] # we are ignoring 'The User' from its similar users.
                # get the ratings of most similar users for this movie
                top_ratings = sample_train_sparse_matrix[top_sim_users, movie].toarray().ravel()
                # we will make it's length "5" by adding movie averages to .
                top_sim_users_ratings = list(top_ratings[top_ratings != 0][:5])
                top_sim_users_ratings.extend([sample_train_averages['movie'][movie]]*(5 - len(top_sim_users_ratings)))
                # print(top_sim_users_ratings, end="--")

            except (IndexError, KeyError):
                # It is a new User or new Movie or there are no ratings for given user for top similar movies...
                ########## Cold STart Problem ##########
                top_sim_users_ratings.extend([sample_train_averages['global']]*(5 - len(top_sim_users_ratings)))
                #print(top_sim_users_ratings)
            except:
                print(user, movie)
                # we just want KeyErrors to be resolved. Not every Exception...
                raise



            #--------------------- Ratings by "user"  to similar movies of "movie" ---------------------
            try:
                # compute the similar movies of the "movie"        
                movie_sim = cosine_similarity(sample_train_sparse_matrix[:,movie].T, sample_train_sparse_matrix.T).ravel()
                top_sim_movies = movie_sim.argsort()[::-1][1:] # we are ignoring 'The User' from its similar users.
                # get the ratings of most similar movie rated by this user..
                top_ratings = sample_train_sparse_matrix[user, top_sim_movies].toarray().ravel()
                # we will make it's length "5" by adding user averages to.
                top_sim_movies_ratings = list(top_ratings[top_ratings != 0][:5])
                top_sim_movies_ratings.extend([sample_train_averages['user'][user]]*(5-len(top_sim_movies_ratings))) 
                #print(top_sim_movies_ratings)
            except (IndexError, KeyError):
                #print(top_sim_movies_ratings, end=" : -- ")
                top_sim_movies_ratings.extend([sample_train_averages['global']]*(5-len(top_sim_movies_ratings)))
                #print(top_sim_movies_ratings)
            except :
                raise

            #-----------------prepare the row to be stores in a file-----------------#
            row = list()
            # add usser and movie name first
            row.append(user)
            row.append(movie)
            row.append(sample_train_averages['global']) # first feature
            #print(row)
            # next 5 features are similar_users "movie" ratings
            row.extend(top_sim_users_ratings)
            #print(row)
            # next 5 features are "user" ratings for similar_movies
            row.extend(top_sim_movies_ratings)
            #print(row)
            # Avg_user rating
            try:
                row.append(sample_train_averages['user'][user])
            except KeyError:
                row.append(sample_train_averages['global'])
            except:
                raise
            #print(row)
            # Avg_movie rating
            try:
                row.append(sample_train_averages['movie'][movie])
            except KeyError:
                row.append(sample_train_averages['global'])
            except:
                raise
            #print(row)
            # finalley, The actual Rating of this user-movie pair...
            row.append(rating)
            #print(row)
            count = count + 1

            # add rows to the file opened..
            reg_data_file.write(','.join(map(str, row)))
            #print(','.join(map(str, row)))
            reg_data_file.write('\n')        
            if (count)%1000 == 0:
                #print(','.join(map(str, row)))
                print("Done for {} rows----- {}".format(count, datetime.now() - start))
    print("",datetime.now() - start)  


# __Reading from the file to make a test dataframe __

# In[153]:


reg_test_df = pd.read_csv('reg_test.csv', names = ['user', 'movie', 'GAvg', 'sur1', 'sur2', 'sur3', 'sur4', 'sur5',
                                                          'smr1', 'smr2', 'smr3', 'smr4', 'smr5',
                                                          'UAvg', 'MAvg', 'rating'], header=None)
reg_test_df.head(4)


# -----------------------
# 
# - __GAvg__ : Average rating of all the ratings 
# 
# 
# - __Similar users rating of this movie__:
#     - sur1, sur2, sur3, sur4, sur5 ( top 5 simiular users who rated that movie.. )
#     
# 
# 
# - __Similar movies rated by this user__:
#     - smr1, smr2, smr3, smr4, smr5 ( top 5 simiular movies rated by this movie.. )
# 
# 
# - __UAvg__ : User AVerage rating
# 
# 
# - __MAvg__ : Average rating of this movie
# 
# 
# - __rating__ : Rating of this movie by this user.
# 
# -----------------------

#  

# <h3> 4.3.2 Transforming data for Surprise models</h3>

# In[154]:


from surprise import Reader, Dataset


# <h4> 4.3.2.1 Transforming train data </h4>

# - We can't give raw data (movie, user, rating) to train the model in Surprise library.
# 
# 
# - They have a saperate format for TRAIN and TEST data, which will be useful for training the models like SVD, KNNBaseLineOnly....etc..,in Surprise.
# 
# 
# - We can form the trainset from a file, or from a Pandas  DataFrame. 
# http://surprise.readthedocs.io/en/stable/getting_started.html#load-dom-dataframe-py 

# In[155]:


# It is to specify how to read the dataframe.
# for our dataframe, we don't have to specify anything extra..
reader = Reader(rating_scale=(1,5))

# create the traindata from the dataframe...
train_data = Dataset.load_from_df(reg_train[['user', 'movie', 'rating']], reader)

# build the trainset from traindata.., It is of dataset format from surprise library..
trainset = train_data.build_full_trainset() 


# <h4> 4.3.2.2 Transforming test data </h4>

# - Testset is just a list of (user, movie, rating) tuples. (Order in the tuple is impotant) 

# In[156]:


testset = list(zip(reg_test_df.user.values, reg_test_df.movie.values, reg_test_df.rating.values))
testset[:3]


# <h2> 4.4 Applying Machine Learning models </h2>

#  

# -  Global dictionary that stores rmse and mape for all the models....
# 
#     - It stores the metrics in a dictionary of dictionaries
# 
#     > __keys__ : model names(string)
# 
#     > __value__: dict(__key__ : metric, __value__ : value ) 

# In[157]:


models_evaluation_train = dict()
models_evaluation_test = dict()

models_evaluation_train, models_evaluation_test


#  

#  > __Utility functions for running regression models__

# In[158]:


# to get rmse and mape given actual and predicted ratings..
def get_error_metrics(y_true, y_pred):
    rmse = np.sqrt(np.mean([ (y_true[i] - y_pred[i])**2 for i in range(len(y_pred)) ]))
    mape = np.mean(np.abs( (y_true - y_pred)/y_true )) * 100
    return rmse, mape

###################################################################
###################################################################
def run_xgboost(algo,  x_train, y_train, x_test, y_test, verbose=True):
    """
    It will return train_results and test_results
    """
    
    # dictionaries for storing train and test results
    train_results = dict()
    test_results = dict()
    
    
    # fit the model
    print('Training the model..')
    start =datetime.now()
    algo.fit(x_train, y_train, eval_metric = 'rmse')
    print('Done. Time taken : {}\n'.format(datetime.now()-start))
    print('Done \n')

    # from the trained model, get the predictions....
    print('Evaluating the model with TRAIN data...')
    start =datetime.now()
    y_train_pred = algo.predict(x_train)
    # get the rmse and mape of train data...
    rmse_train, mape_train = get_error_metrics(y_train.values, y_train_pred)
    
    # store the results in train_results dictionary..
    train_results = {'rmse': rmse_train,
                    'mape' : mape_train,
                    'predictions' : y_train_pred}
    
    #######################################
    # get the test data predictions and compute rmse and mape
    print('Evaluating Test data')
    y_test_pred = algo.predict(x_test) 
    rmse_test, mape_test = get_error_metrics(y_true=y_test.values, y_pred=y_test_pred)
    # store them in our test results dictionary.
    test_results = {'rmse': rmse_test,
                    'mape' : mape_test,
                    'predictions':y_test_pred}
    if verbose:
        print('\nTEST DATA')
        print('-'*30)
        print('RMSE : ', rmse_test)
        print('MAPE : ', mape_test)
        
    # return these train and test results...
    return train_results, test_results
    


# > __Utility functions for Surprise modes__

# In[159]:


# it is just to makesure that all of our algorithms should produce same results
# everytime they run...

my_seed = 15
random.seed(my_seed)
np.random.seed(my_seed)

##########################################################
# get  (actual_list , predicted_list) ratings given list 
# of predictions (prediction is a class in Surprise).    
##########################################################
def get_ratings(predictions):
    actual = np.array([pred.r_ui for pred in predictions])
    pred = np.array([pred.est for pred in predictions])
    
    return actual, pred

################################################################
# get ''rmse'' and ''mape'' , given list of prediction objecs 
################################################################
def get_errors(predictions, print_them=False):

    actual, pred = get_ratings(predictions)
    rmse = np.sqrt(np.mean((pred - actual)**2))
    mape = np.mean(np.abs(pred - actual)/actual)

    return rmse, mape*100

##################################################################################
# It will return predicted ratings, rmse and mape of both train and test data   #
##################################################################################
def run_surprise(algo, trainset, testset, verbose=True): 
    '''
        return train_dict, test_dict
    
        It returns two dictionaries, one for train and the other is for test
        Each of them have 3 key-value pairs, which specify ''rmse'', ''mape'', and ''predicted ratings''.
    '''
    start = datetime.now()
    # dictionaries that stores metrics for train and test..
    train = dict()
    test = dict()
    
    # train the algorithm with the trainset
    st = datetime.now()
    print('Training the model...')
    algo.fit(trainset)
    print('Done. time taken : {} \n'.format(datetime.now()-st))
    
    # ---------------- Evaluating train data--------------------#
    st = datetime.now()
    print('Evaluating the model with train data..')
    # get the train predictions (list of prediction class inside Surprise)
    train_preds = algo.test(trainset.build_testset())
    # get predicted ratings from the train predictions..
    train_actual_ratings, train_pred_ratings = get_ratings(train_preds)
    # get ''rmse'' and ''mape'' from the train predictions.
    train_rmse, train_mape = get_errors(train_preds)
    print('time taken : {}'.format(datetime.now()-st))
    
    if verbose:
        print('-'*15)
        print('Train Data')
        print('-'*15)
        print("RMSE : {}\n\nMAPE : {}\n".format(train_rmse, train_mape))
    
    #store them in the train dictionary
    if verbose:
        print('adding train results in the dictionary..')
    train['rmse'] = train_rmse
    train['mape'] = train_mape
    train['predictions'] = train_pred_ratings
    
    #------------ Evaluating Test data---------------#
    st = datetime.now()
    print('\nEvaluating for test data...')
    # get the predictions( list of prediction classes) of test data
    test_preds = algo.test(testset)
    # get the predicted ratings from the list of predictions
    test_actual_ratings, test_pred_ratings = get_ratings(test_preds)
    # get error metrics from the predicted and actual ratings
    test_rmse, test_mape = get_errors(test_preds)
    print('time taken : {}'.format(datetime.now()-st))
    
    if verbose:
        print('-'*15)
        print('Test Data')
        print('-'*15)
        print("RMSE : {}\n\nMAPE : {}\n".format(test_rmse, test_mape))
    # store them in test dictionary
    if verbose:
        print('storing the test results in test dictionary...')
    test['rmse'] = test_rmse
    test['mape'] = test_mape
    test['predictions'] = test_pred_ratings
    
    print('\n'+'-'*45)
    print('Total time taken to run this algorithm :', datetime.now() - start)
    
    # return two dictionaries train and test
    return train, test


#  

# <h3> 4.4.1 XGBoost with initial 13 features </h3>

# In[160]:


import xgboost as xgb
from scipy.stats import randint as sp_randint
from scipy import stats
from sklearn.model_selection import RandomizedSearchCV


# In[162]:


# prepare Train data
x_train = reg_train.drop(['user','movie','rating'], axis=1)
y_train = reg_train['rating']

# Prepare Test data
x_test = reg_test_df.drop(['user','movie','rating'], axis=1)
y_test = reg_test_df['rating']

# Hyperparameter tuning 
params = {'learning_rate' :stats.uniform(0.01,0.2),
             'n_estimators':sp_randint(100,1000),
             'max_depth':sp_randint(1,10),
             'min_child_weight':sp_randint(1,8),
             'gamma':stats.uniform(0,0.02),
             'subsample':stats.uniform(0.6,0.4),
             'reg_alpha':sp_randint(0,200),
             'reg_lambda':stats.uniform(0,200),
             'colsample_bytree':stats.uniform(0.6,0.3)}


# initialize Our first XGBoost model...
xgbreg = xgb.XGBRegressor(silent=True, n_jobs= -1, random_state=15)
start =datetime.now()
print('Tuning parameters: \n')
xgb_best = RandomizedSearchCV(xgbreg, param_distributions= params,refit=False, scoring = "neg_mean_squared_error", 
                              cv =3,n_jobs = -1)
xgb_best.fit(x_train, y_train)
best_para = xgb_best.best_params_
first_xgb = xgbreg.set_params(**best_para)
print('Time taken to tune:{}\n'.format(datetime.now()-start))
###########################################################################################################################

train_results, test_results = run_xgboost(first_xgb, x_train, y_train, x_test, y_test)

# store the results in models_evaluations dictionaries
models_evaluation_train['first_algo'] = train_results
models_evaluation_test['first_algo'] = test_results

xgb.plot_importance(first_xgb)
plt.show()


#  

# <h3> 4.4.2 Suprise BaselineModel </h3>
#     
# 

# In[163]:


from surprise import BaselineOnly 


# __Predicted_rating : ( baseline prediction ) __
# 
#     -  http://surprise.readthedocs.io/en/stable/basic_algorithms.html#surprise.prediction_algorithms.baseline_only.BaselineOnly 
#  >$   \large {\hat{r}_{ui} = b_{ui} =\mu + b_u + b_i} $
# 
# 
# - $\pmb \mu $ : Average of all rating in training data.
# - $\pmb b_u$ : User bias
# - $\pmb b_i$ : Item bias (movie biases) 

# __Optimization function ( Least Squares Problem ) __
# 
#     - http://surprise.readthedocs.io/en/stable/prediction_algorithms.html#baselines-estimates-configuration 
# 
# > $ \large \sum_{r_{ui} \in R_{train}} \left(r_{ui} - (\mu + b_u + b_i)\right)^2 +
# \lambda \left(b_u^2 + b_i^2 \right).\text {        [mimimize } {b_u, b_i]}$ 

# In[164]:


# options are to specify.., how to compute those user and item biases
bsl_options = {'method': 'sgd',
               'learning_rate': .001
               }
bsl_algo = BaselineOnly(bsl_options=bsl_options)
# run this algorithm.., It will return the train and test results..
bsl_train_results, bsl_test_results = run_surprise(bsl_algo, trainset, testset, verbose=True)


# Just store these error metrics in our models_evaluation datastructure
models_evaluation_train['bsl_algo'] = bsl_train_results 
models_evaluation_test['bsl_algo'] = bsl_test_results


#  

# <h3> 4.4.3 XGBoost with initial 13 features + Surprise Baseline predictor </h3>

# __Updating Train Data__

# In[165]:


# add our baseline_predicted value as our feature..
reg_train['bslpr'] = models_evaluation_train['bsl_algo']['predictions']
reg_train.head(2) 


# __Updating Test Data__

# In[166]:


# add that baseline predicted ratings with Surprise to the test data as well
reg_test_df['bslpr']  = models_evaluation_test['bsl_algo']['predictions']

reg_test_df.head(2)


# In[167]:


# prepare train data
x_train = reg_train.drop(['user', 'movie','rating'], axis=1)
y_train = reg_train['rating']

# Prepare Test data
x_test = reg_test_df.drop(['user','movie','rating'], axis=1)
y_test = reg_test_df['rating']

##########################################################################################################################
params = {'learning_rate' :stats.uniform(0.01,0.2),
             'n_estimators':sp_randint(100,1000),
             'max_depth':sp_randint(1,10),
             'min_child_weight':sp_randint(1,8),
             'gamma':stats.uniform(0,0.02),
             'subsample':stats.uniform(0.6,0.4),
             'reg_alpha':sp_randint(0,200),
             'reg_lambda':stats.uniform(0,200),
             'colsample_bytree':stats.uniform(0.6,0.3)}


# initialize XGBoost model...
xgbreg = xgb.XGBRegressor(silent=True, n_jobs=-1, random_state=15)
start =datetime.now()
print('Tuning parameters: \n')
xgb_best = RandomizedSearchCV(xgbreg, param_distributions= params,refit=False, n_jobs=-1,scoring = "neg_mean_squared_error",
                              cv = 3)
xgb_best.fit(x_train, y_train)
best_para = xgb_best.best_params_
###########################################################################################################################

xgb_bsl = xgbreg.set_params(**best_para)
print('Time taken to tune:{}\n'.format(datetime.now()-start))

train_results, test_results = run_xgboost(xgb_bsl, x_train, y_train, x_test, y_test)

# store the results in models_evaluations dictionaries
models_evaluation_train['xgb_bsl'] = train_results
models_evaluation_test['xgb_bsl'] = test_results

xgb.plot_importance(xgb_bsl)
plt.show()


#  

#  

# <h3> 4.4.4 Surprise KNNBaseline predictor </h3>

# In[168]:


from surprise import KNNBaseline


# - KNN BASELINE
#     - http://surprise.readthedocs.io/en/stable/knn_inspired.html#surprise.prediction_algorithms.knns.KNNBaseline 

# - PEARSON_BASELINE SIMILARITY
#     - http://surprise.readthedocs.io/en/stable/similarities.html#surprise.similarities.pearson_baseline 

# - SHRINKAGE
#     - _2.2 Neighborhood Models_ in http://courses.ischool.berkeley.edu/i290-dm/s11/SECURE/a1-koren.pdf 

# - __predicted Rating__ : ( ___ based on User-User similarity ___ )
# 
# \begin{align} \hat{r}_{ui} = b_{ui} + \frac{ \sum\limits_{v \in N^k_i(u)}
# \text{sim}(u, v) \cdot (r_{vi} - b_{vi})} {\sum\limits_{v \in
# N^k_i(u)} \text{sim}(u, v)} \end{align}
# 
# - $\pmb{b_{ui}}$ -  _Baseline prediction_ of (user,movie) rating
# 
# - $ \pmb {N_i^k (u)}$ - Set of __K similar__ users (neighbours) of __user (u)__ who rated __movie(i)__  
# 
# - _sim (u, v)_ - __Similarity__ between users __u and v__  
#     - Generally, it will be cosine similarity or Pearson correlation coefficient. 
#     - But we use __shrunk Pearson-baseline correlation coefficient__, which is based on the pearsonBaseline similarity ( we take base line predictions instead of mean rating of user/item)
#        

#  

# - __ Predicted rating __ ( based on Item Item similarity ):
#  \begin{align} \hat{r}_{ui} = b_{ui} + \frac{ \sum\limits_{j \in N^k_u(i)}\text{sim}(i, j) \cdot (r_{uj} - b_{uj})} {\sum\limits_{j \in N^k_u(j)} \text{sim}(i, j)} \end{align}
# 
#     -  ___Notations follows same as above (user user based predicted rating ) ___

#   <h4> 4.4.4.1 Surprise KNNBaseline with user user similarities</h4>

# In[169]:


# we specify , how to compute similarities and what to consider with sim_options to our algorithm
sim_options = {'user_based' : True,
               'name': 'pearson_baseline',
               'shrinkage': 100,
               'min_support': 2
              } 
# we keep other parameters like regularization parameter and learning_rate as default values.
bsl_options = {'method': 'sgd'} 

knn_bsl_u = KNNBaseline(k=40, sim_options = sim_options, bsl_options = bsl_options)
knn_bsl_u_train_results, knn_bsl_u_test_results = run_surprise(knn_bsl_u, trainset, testset, verbose=True)

# Just store these error metrics in our models_evaluation datastructure
models_evaluation_train['knn_bsl_u'] = knn_bsl_u_train_results 
models_evaluation_test['knn_bsl_u'] = knn_bsl_u_test_results


# <h4> 4.4.4.2 Surprise KNNBaseline with movie movie similarities</h4>

# In[170]:


# we specify , how to compute similarities and what to consider with sim_options to our algorithm

# 'user_based' : Fals => this considers the similarities of movies instead of users

sim_options = {'user_based' : False,
               'name': 'pearson_baseline',
               'shrinkage': 100,
               'min_support': 2
              } 
# we keep other parameters like regularization parameter and learning_rate as default values.
bsl_options = {'method': 'sgd'}


knn_bsl_m = KNNBaseline(k=40, sim_options = sim_options, bsl_options = bsl_options)

knn_bsl_m_train_results, knn_bsl_m_test_results = run_surprise(knn_bsl_m, trainset, testset, verbose=True)

# Just store these error metrics in our models_evaluation datastructure
models_evaluation_train['knn_bsl_m'] = knn_bsl_m_train_results 
models_evaluation_test['knn_bsl_m'] = knn_bsl_m_test_results


#  

# <h3> 4.4.5 XGBoost with initial 13 features + Surprise Baseline predictor + KNNBaseline predictor </h3>

# - - - First we will run XGBoost with predictions from both KNN's ( that uses User\_User and Item\_Item similarities along with our previous features.
# 
#  
# - - - Then we will run XGBoost with just predictions form both knn models and preditions from our baseline model. 

# __Preparing Train data __

# In[171]:


# add the predicted values from both knns to this dataframe
reg_train['knn_bsl_u'] = models_evaluation_train['knn_bsl_u']['predictions']
reg_train['knn_bsl_m'] = models_evaluation_train['knn_bsl_m']['predictions']

reg_train.head(2)


# __Preparing Test data  __

# In[172]:


reg_test_df['knn_bsl_u'] = models_evaluation_test['knn_bsl_u']['predictions']
reg_test_df['knn_bsl_m'] = models_evaluation_test['knn_bsl_m']['predictions']

reg_test_df.head(2)


# In[173]:


# prepare the train data....
x_train = reg_train.drop(['user', 'movie', 'rating'], axis=1)
y_train = reg_train['rating']

# prepare the train data....
x_test = reg_test_df.drop(['user','movie','rating'], axis=1)
y_test = reg_test_df['rating']


params = {'learning_rate' :stats.uniform(0.01,0.2),
             'n_estimators':sp_randint(100,1000),
             'max_depth':sp_randint(1,10),
             'min_child_weight':sp_randint(1,8),
             'gamma':stats.uniform(0,0.02),
             'subsample':stats.uniform(0.6,0.4),
             'reg_alpha':sp_randint(0,200),
             'reg_lambda':stats.uniform(0,200),
             'colsample_bytree':stats.uniform(0.6,0.3)}



# Declare  XGBoost model...
xgbreg = xgb.XGBRegressor(silent=True, n_jobs=-1, random_state=15)
start =datetime.now()
print('Tuning parameters: \n')
xgb_best = RandomizedSearchCV(xgbreg, param_distributions= params,refit=False, scoring = "neg_mean_squared_error",n_jobs=-1,
                              cv = 3)
xgb_best.fit(x_train, y_train)
best_para = xgb_best.best_params_

xgb_knn_bsl = xgbreg.set_params(**best_para)
print('Time taken to tune:{}\n'.format(datetime.now()-start))

train_results, test_results = run_xgboost(xgb_knn_bsl, x_train, y_train, x_test, y_test)

# store the results in models_evaluations dictionaries
models_evaluation_train['xgb_knn_bsl'] = train_results
models_evaluation_test['xgb_knn_bsl'] = test_results


xgb.plot_importance(xgb_knn_bsl)
plt.show()


# <h3> 4.4.6 Matrix Factorization Techniques </h3>

# <h4> 4.4.6.1 SVD Matrix Factorization User Movie intractions </h4>

# In[174]:


from surprise import SVD


# http://surprise.readthedocs.io/en/stable/matrix_factorization.html#surprise.prediction_algorithms.matrix_factorization.SVD 

# - __ Predicted Rating : __
#     - 
#     - $ \large  \hat r_{ui} = \mu + b_u + b_i + q_i^Tp_u $
#     
#         - $\pmb q_i$ - Representation of item(movie) in latent factor space
#         
#         - $\pmb p_u$ - Representation of user in new latent factor space
#         
# 

# - A BASIC MATRIX FACTORIZATION MODEL in  https://datajobs.com/data-science-repo/Recommender-Systems-[Netflix].pdf

# - __Optimization problem with user item interactions and regularization (to avoid overfitting)__
#     - 
#     - $\large \sum_{r_{ui} \in R_{train}} \left(r_{ui} - \hat{r}_{ui} \right)^2 +
# \lambda\left(b_i^2 + b_u^2 + ||q_i||^2 + ||p_u||^2\right) $

# In[175]:


# initiallize the model
svd = SVD(n_factors=100, biased=True, random_state=15, verbose=True)
svd_train_results, svd_test_results = run_surprise(svd, trainset, testset, verbose=True)

# Just store these error metrics in our models_evaluation datastructure
models_evaluation_train['svd'] = svd_train_results 
models_evaluation_test['svd'] = svd_test_results


#  

#   <h4> 4.4.6.2 SVD Matrix Factorization with implicit feedback from user ( user rated movies ) </h4>

# In[176]:


from surprise import SVDpp


# - ----->  2.5 Implicit Feedback in http://courses.ischool.berkeley.edu/i290-dm/s11/SECURE/a1-koren.pdf

# - __ Predicted Rating : __
#     - 
#     - $ \large \hat{r}_{ui} = \mu + b_u + b_i + q_i^T\left(p_u +
#     |I_u|^{-\frac{1}{2}} \sum_{j \in I_u}y_j\right) $ 

#  - $ \pmb{I_u}$ --- the set of all items rated by user u
# 
# - $\pmb{y_j}$ --- Our new set of item factors that capture implicit ratings.  

# - __Optimization problem with user item interactions and regularization (to avoid overfitting)__
#     - 
#     - $ \large \sum_{r_{ui} \in R_{train}} \left(r_{ui} - \hat{r}_{ui} \right)^2 +
# \lambda\left(b_i^2 + b_u^2 + ||q_i||^2 + ||p_u||^2 + ||y_j||^2\right) $ 

# In[177]:


# initiallize the model
svdpp = SVDpp(n_factors=50, random_state=15, verbose=True)
svdpp_train_results, svdpp_test_results = run_surprise(svdpp, trainset, testset, verbose=True)

# Just store these error metrics in our models_evaluation datastructure
models_evaluation_train['svdpp'] = svdpp_train_results 
models_evaluation_test['svdpp'] = svdpp_test_results


#  

#  

# <h3> 4.4.7 XgBoost with 13 features + Surprise Baseline + Surprise KNNbaseline + MF Techniques </h3>

# __Preparing Train data__

# In[178]:


# add the predicted values from both knns to this dataframe
reg_train['svd'] = models_evaluation_train['svd']['predictions']
reg_train['svdpp'] = models_evaluation_train['svdpp']['predictions']

reg_train.head(2) 


# __Preparing Test data  __

# In[179]:


reg_test_df['svd'] = models_evaluation_test['svd']['predictions']
reg_test_df['svdpp'] = models_evaluation_test['svdpp']['predictions']

reg_test_df.head(2) 


#  

# In[180]:


# prepare x_train and y_train
x_train = reg_train.drop(['user', 'movie', 'rating',], axis=1)
y_train = reg_train['rating']

# prepare test data
x_test = reg_test_df.drop(['user', 'movie', 'rating'], axis=1)
y_test = reg_test_df['rating']

##########################################################################################################################
params = {'learning_rate' :stats.uniform(0.01,0.2),
             'n_estimators':sp_randint(100,1000),
             'max_depth':sp_randint(1,10),
             'min_child_weight':sp_randint(1,8),
             'gamma':stats.uniform(0,0.02),
             'subsample':stats.uniform(0.6,0.4),
             'reg_alpha':sp_randint(0,200),
             'reg_lambda':stats.uniform(0,200),
             'colsample_bytree':stats.uniform(0.6,0.3)}


# Declare  XGBoost model...
xgbreg = xgb.XGBRegressor(silent=True, n_jobs=-1, random_state=15)
start =datetime.now()
print('Tuning parameters: \n')
xgb_best = RandomizedSearchCV(xgbreg, param_distributions= params,refit=False, scoring = "neg_mean_squared_error",n_jobs=-1,
                              cv = 3)
xgb_best.fit(x_train, y_train)
best_para = xgb_best.best_params_
###########################################################################################################################

xgb_final = xgbreg.set_params(**best_para)
print('Time taken to tune:{}\n'.format(datetime.now()-start))

train_results, test_results = run_xgboost(xgb_final, x_train, y_train, x_test, y_test)

# store the results in models_evaluations dictionaries
models_evaluation_train['xgb_final'] = train_results
models_evaluation_test['xgb_final'] = test_results


xgb.plot_importance(xgb_final)
plt.show()


# <h3> 4.4.8 XgBoost with Surprise Baseline + Surprise KNNbaseline + MF Techniques </h3>

# In[181]:


# prepare train data
x_train = reg_train[['knn_bsl_u', 'knn_bsl_m', 'svd', 'svdpp']]
y_train = reg_train['rating']

# test data
x_test = reg_test_df[['knn_bsl_u', 'knn_bsl_m', 'svd', 'svdpp']]
y_test = reg_test_df['rating']

############################################################################################################################
params = {'learning_rate' :stats.uniform(0.01,0.2),
             'n_estimators':sp_randint(100,1000),
             'max_depth':sp_randint(1,10),
             'min_child_weight':sp_randint(1,8),
             'gamma':stats.uniform(0,0.02),
             'subsample':stats.uniform(0.6,0.4),
             'reg_alpha':sp_randint(0,200),
             'reg_lambda':stats.uniform(0,200),
             'colsample_bytree':stats.uniform(0.6,0.3)}


# Declare  XGBoost model...
xgbreg = xgb.XGBRegressor(silent=True, n_jobs=-1, random_state=15)
start =datetime.now()
print('Tuning parameters: \n')
xgb_best = RandomizedSearchCV(xgbreg, param_distributions= params,refit=False, scoring = "neg_mean_squared_error",n_jobs=-1,
                              cv = 3)
xgb_best.fit(x_train, y_train)
best_para = xgb_best.best_params_
###########################################################################################################################

xgb_all_models = xgbreg.set_params(**best_para)
train_results, test_results = run_xgboost(xgb_all_models, x_train, y_train, x_test, y_test)

# store the results in models_evaluations dictionaries
models_evaluation_train['xgb_all_models'] = train_results
models_evaluation_test['xgb_all_models'] = test_results

xgb.plot_importance(xgb_all_models)
plt.show()


#  

#  

# <h2> 4.5 Comparision between all models </h2>

# ### With tuned Hyperparameter model Performance

# In[187]:


pd.DataFrame(models_evaluation_test).to_csv('tuned_small_sample_results.csv')
models = pd.read_csv('tuned_small_sample_results.csv', index_col=0)
models.loc['rmse'].sort_values()


# ### Plot of Train and Test RMSE of tunned Hyperparameter model Performance

# In[257]:


train_performance = pd.DataFrame(models_evaluation_train)
test_performance = pd.DataFrame(models_evaluation_test)
performance_dataframe = pd.DataFrame({'Train':train_performance.loc["rmse"],'Test':test_performance.loc["rmse"]})
performance_dataframe.plot(kind = "bar",grid = True)
plt.title("Train and Test RMSE of all Models")
plt.ylabel("Error Values")
plt.show()


# ## Conclusion 
# - According to our ploblem statment Netflix is all about connecting people to the movies they love. To help customers find those movies, they developed world-class movie recommendation system: CinematchSM. Its job is to predict whether someone will enjoy a movie based on how much they liked or disliked other movies. Netflix use those predictions to make personal movie recommendations based on each customer’s unique tastes.
# - Lets Start ->
#     1. As we know we have dataset which contains MovieIDs range from 1 to 17770 sequentially. CustomerIDs range from 1 to 2649429, with gaps. There are 480189 users.Ratings are on a five star (integral) scale from 1 to 5. Dates have the format YYYY-MM-DD. And as we can see that we have data are in different formate and we need to make it in a format so that we are able apply models on it. And for that what we are doing as we are puting it all the file and merging movies with users and their rating in single dataframe.
#     2. So after doing all this we will do some EDA on whole dataset, so that we will able to visualise our dataset like distribition of the ratings,what is the avg rating of the movie or avg rating given by the users to the movie and lot more
#     3. After that we we split our data in train and test which is in ratio of 80:20 and try to to EDA on it. And then we are creating MF of user and movies and make it sparse as we can see our data frame is more than 90% sparse which means very less non zero value in the matrix. and we will do this for our both train and test data set. 
#     4. And then we try Computing Similarity matrices for both user-user similarity and movie-movie similarity but as we can see calculating Similarity_Matrix is not very easy(unless we have huge Computing Power and lots of time) because of number of. users and movies being large. 
#     5. In above points as we have true to compute similarity but it doest works and after we try some other methods like dim reductions and try to compute but unfortunatly it also doest works and as we can see it taking more time and memory than our above method amd the ple is due to dense matrix. so at last what we do we will try to compute similar users for a particular user, whenenver required (ie., Run time) so that at one time we are not going to compte similarity for the whole users/ movies we will do it at run time when ever required for that pertifular user/ movie. And after that we just try to see that it really works or not and we jut got a awsome result. As we can see we have provied a movie id that with movie name Vampire Journals and we got a good result which is similar type movie which we have provied as input. 
#     6. After doing lots of stuff now we will work with different machine learning models and try to compare results of all that and but before that lets first sample our data set because we have lots of data and if we work with all data it will take lots of time so first we will samle our data and then we will introduce with some feature engineering which we are going to use it as a feature on our machine learning models.
#     7. As we can see in given diagream its shown that in this case study we are using a need lib that is surpise lib with paralell to xgboost models with perform matrix RMSE and MAPE with some hyperparameter tuning on xgboost.
