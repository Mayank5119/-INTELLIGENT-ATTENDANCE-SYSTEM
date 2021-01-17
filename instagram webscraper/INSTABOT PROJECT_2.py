#!/usr/bin/env python
# coding: utf-8

# # INSTAGRAM WEBSCRAPER

# In[1]:


from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import matplotlib.pyplot as plt


# In[2]:


driver = webdriver.Chrome(executable_path = "give path of chrome webdriver")


# In[3]:


driver.get('https://www.instagram.com/')


# # LOGGING IN 

# In[4]:


def login():
    a=driver.find_element_by_name('username')
    Username='SAMPLE USENAME'
    a.send_keys(Username)
    p=driver.find_element_by_name('password')
    Password='SAMPLE PASSWORD'
    p.send_keys(Password)
    log=driver.find_element_by_xpath("//div[text()='Log In']")
    log.click()
    time.sleep(10)
    try:
        driver.find_elements_by_xpath("//div[@class = 'mt3GC']/button")[1].click()
    except NoSuchElementException:
        pass
    


# In[5]:


login()


# # Q1. From the list of instagram handles you obtained when you searched ‘food’ in previous project. Open the first 10 handles and find the top 5 which have the highest number of followers

# In[6]:


def visit(name): #Function to visit any profile on instagram
    typeField = driver.find_element_by_xpath("//input[contains(@class, 'XTCLo')]") #Finding the input search field
    typeField.clear() #Clearing the input field if already typed
    print("Searching a profile", name)
    typeField.send_keys(name) #Entering the profile name
    waitNext = WebDriverWait(driver, 30)
    waitNext.until(EC.element_to_be_clickable((By.CLASS_NAME, "Ap253")))
    account = driver.find_elements_by_class_name("Ap253") 
    for j in account:
        if(j.text == name):
            j.click()
            time.sleep(3)
            return
def FollowersNumber():
    time.sleep(2)
    Number = driver.find_elements_by_class_name("g47SY")
    #time.sleep(2)
    exact = Number[1].get_attribute("title")
    if("," in exact):
        k = ""
        a = exact.split(",")
        for j in range(len(a)):
            k = k + a[j]
        intExact = int(k)
        return intExact
    else:
        intExact = int(exact)
        return intExact
        
typeField = driver.find_element_by_xpath("//input[contains(@class, 'XTCLo')]") #I have to proceed to input box now
typeField.send_keys("food") # Typing food in the searchbox

wait = WebDriverWait(driver, 30) #Waiting for 10 seconds
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Ap253"))) #Precaution if something happens

accName = driver.find_elements_by_class_name("Ap253") #Finding the class which contains data
count = 1 #To count the number of accounts

accountList = []

for i in range(len(accName)):
    if("#" not in accName[i].text and accName[i].text != "Food Garage HUDA"  and count <= 10): 
        accountList.append(accName[i].text)
        count += 1 #Increasing count by 1 on printing account name
        
accountFollowers = {}

for i in range (len(accountList)):
    
    visit(accountList[i])
    exactFollowers = FollowersNumber()
    
    accountFollowers[accountList[i]] = exactFollowers
sortedDict = {k: v for k, v in sorted(accountFollowers.items(), key=lambda item: item[1], reverse = True)}
profiles = list(sortedDict.keys())
print()
print("Top 5 profiles are")
print()
topFive = []
for j in range(5):
    topFive.append(profiles[j])
    print(profiles[j])


# # Q2.Now Find the number of posts these handles have done in the previous 3 days.

# # Q3.Depict this information using a suitable graph.

# In[9]:


import time
postNumber = []
for i in topFive:
    search=driver.find_element_by_xpath("//input[@placeholder='Search']")
    search.send_keys(i)
    time.sleep(4)
    namey=driver.find_element_by_class_name('Ap253')
    i='https://instagram.com/'+namey.text+'/'
    driver.get(i)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_9AhH0")))
    imageLikes = driver.find_element_by_class_name("_9AhH0")
    imageLikes.click()
    wait = WebDriverWait(driver, 30) #Waiting for 30 seconds
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_97aPb ")))
    count = 0
    while True:
        duration = driver.find_element_by_xpath("//time[contains(@class, '_1o9PC')]")
        if('HOUR' in duration.text  or '1 DAY' in duration.text or '2 DAYS' in duration.text or '3 DAYS' in duration.text or 'SECOND' in duration.text or 'MINUTES' in duration.text):
            count += 1
            waitNext = WebDriverWait(driver, 30)
            waitNext.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, '_65Bje')]"))) #Precaution if something happens
            nextButton = driver.find_element_by_xpath("//a[contains(@class, '_65Bje')]") #next button for next image preview
            nextButton.click() #clicking next button
            wait = WebDriverWait(driver, 30) #Waiting for 30 seconds
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_97aPb ")))
        else:
            ImageClose = driver.find_elements_by_class_name("wpO6b")
            ImageClose[-1].click()
            break
            
    postNumber.append(count)
plt.bar(topFive, postNumber)
plt.xticks(rotation=90)
plt.xlabel("Usernames")
plt.ylabel("No. of Posts")
plt.show()


# # Q1. Open the 5 handles you obtained in the last question, and scrape the content of the first 10 posts of each handle.

# # Q2. Prepare a list of all words used in all the scraped posts and calculate the frequency of each word.

# # Q3. Create a csv file with two columns : the word and its frequency

# In[11]:


import pandas as pd
allWords = []
hashtags = []
for i in topFive:
    count = 1
    search=driver.find_element_by_xpath("//input[@placeholder='Search']")
    search.send_keys(i)
    time.sleep(4)
    namey=driver.find_element_by_class_name('Ap253')
    i='https://instagram.com/'+namey.text+'/'
    driver.get(i)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_9AhH0")))
    imageLikes = driver.find_element_by_class_name("_9AhH0")
    imageLikes.click()
    while(count <= 10):
        wait = WebDriverWait(driver, 30) #Waiting for 10 seconds
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "C4VMK")))
        
        contentFind = driver.find_element_by_xpath("//div[contains(@class, 'C4VMK')]/span").get_attribute('textContent').strip().split(" ")
        for content in contentFind:
            allWords.append(content)
        for hashes in driver.find_elements_by_xpath('//div[contains(@class, "C4VMK")]/span//a'):
            hashtags.append(hashes.get_attribute('innerHTML'))
        waitNext = WebDriverWait(driver, 30)
        waitNext.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, '_65Bje')]"))) #Precaution if something happens
        nextButton = driver.find_element_by_xpath("//a[contains(@class, '_65Bje')]") #next button for next image preview
        nextButton.click() #clicking next button
        count += 1
    driver.back()
    driver.back()
    time.sleep(1)
    
df = pd.DataFrame()
final = pd.DataFrame()
df["Words"] = allWords
frequency = list(df['Words'].value_counts().values)
final.to_csv('Hashtags.csv')
words = list(df['Words'].value_counts().index)
final["Words"] = words
final["Frequency"] = frequency
final.to_csv('Hashtags.csv')
print("CSV file has been created")


# # Q4. Now, find the hashtags that were most popular among these bloggers

# # Q5. Plot a Pie Chart of the top 5 hashtags obtained and the number of times they were used by these bloggers in the scraped posts.

# In[12]:


hashTags = []
for i in hashtags:
    if(i[0] == "#"):
        hashTags.append(i[1:])
hashTagCount = pd.DataFrame()
hashTagCount["hashtags"] = hashTags

tag = list(hashTagCount['hashtags'].value_counts().index)[0:6]
frequent = list(hashTagCount['hashtags'].value_counts().values)[0:6]
print("Top 5 hashtags are: ")
print()
for i in range(len(tag)):
    print(tag[i], frequent[i])
plt.pie(frequent, labels = tag, autopct='%.2f%%', shadow=True)
plt.title('Pie Chart')
plt.show()


# # Q1. Find out the likes of the top 10 posts of the 5 handles obtained earlier.

# In[13]:


TotalList = []
for user in topFive:
    count = 1
    search=driver.find_element_by_xpath("//input[@placeholder='Search']")
    search.send_keys(user)
    time.sleep(4)
    namey=driver.find_element_by_class_name('Ap253')
    i='https://instagram.com/'+namey.text+'/'
    driver.get(i)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_9AhH0")))
    imageLikes = driver.find_element_by_class_name("_9AhH0")
    imageLikes.click()
    TotalLikes = 0
    while(count <= 10):
        try:
            wait = WebDriverWait(driver, 6) #Waiting for 10 seconds
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Nm9Fw')]/button/span")))
            likeFind = driver.find_element_by_xpath('//div[contains(@class, "Nm9Fw")]/button/span')#
            currentLikes = likeFind.text
        except:
            wait = WebDriverWait(driver, 10) #Waiting for 10 seconds
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "vcOH2")))
            viewFind = driver.find_element_by_class_name('vcOH2')
            viewFind.click()
            wait = WebDriverWait(driver, 10) #Waiting for 10 seconds
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'vJRqr')]/span")))
            likeFind = driver.find_element_by_xpath('//div[contains(@class, "vJRqr")]/span')#
            currentLikes = likeFind.text
            body = driver.find_element_by_class_name('QhbhU')#QhbhU
            body.click()
            
        if("," in currentLikes):
            k = ""
            a = currentLikes.split(",")
            for j in range(len(a)):
                k = k + a[j]
            currentLikes = int(k)
        else:
            currentLikes = int(currentLikes)
        TotalLikes = TotalLikes + currentLikes
        waitNext = WebDriverWait(driver, 30)
        waitNext.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, '_65Bje')]"))) #Precaution if something happens
        nextButton = driver.find_element_by_xpath("//a[contains(@class, '_65Bje')]") #next button for next image preview
        nextButton.click()
        count += 1
    TotalList.append(TotalLikes)
    ImageClose = driver.find_elements_by_class_name("wpO6b")
    ImageClose[-1].click()
print("Likes for the handles are: ")
print()
for i in range(5):
    print(profiles[i], TotalList[i])


# # Q2. Calculate the average likes for a handle.

# In[14]:


import numpy as np
TotalList = np.array(TotalList)
avgLikes = (TotalList/10) #Finding out average likes of the first 10 posts
print("Average likes for handles are: ")
print()
for i in range(5):
    print(profiles[i], avgLikes[i])


# # Q3. Divide the average likes obtained from the number of followers of the handle to get the average followers:like ratio of each handle.

# In[15]:


NumberOfFollowers = list(sortedDict.values())[:5]
followersLikes = NumberOfFollowers / avgLikes  #Finding the followers:likes ratio
print("Followers : Likes Ratio is: ")
print()
for i in range(5):
    print(profiles[i], followersLikes[i])


# # Q4. Create a bar graph to depict the above obtained information.

# In[16]:


plt.bar(topFive, followersLikes)    #Plotting the bar graph of the above information
plt.xticks(rotation=45)
plt.xlabel('Users', size=12)
plt.ylabel('Average followers to likes ratio', size=12)  
plt.show()


# In[ ]:




