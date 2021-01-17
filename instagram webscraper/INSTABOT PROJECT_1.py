#!/usr/bin/env python
# coding: utf-8

# # INSTAGRAM WEBSCRAPER

# In[1]:


from selenium import webdriver
driver=webdriver.Chrome(executable_path='give path of chrome webdriver')
from selenium.webdriver.support import expected_conditions
import time 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


# In[2]:


driver.get('https://www.instagram.com/')


# # Logging into Instagram

# In[3]:


def login():
    a=driver.find_element_by_name('username')
    Username='username'
    a.send_keys(Username)
    p=driver.find_element_by_name('password')
    Password='password'
    p.send_keys(Password)
    log=driver.find_element_by_xpath("//div[text()='Log In']")
    log.click()
    time.sleep(10)
    try:
        driver.find_elements_by_xpath("//div[@class = 'mt3GC']/button")[1].click()
    except NoSuchElementException:
        pass
    


# In[4]:


time.sleep(10)
login()


# # Searching query

# In[10]:


def search_pages(textsearch):
    search=driver.find_element_by_xpath("//input[@placeholder='Search']")
    search.send_keys(textsearch)
    namey=[]
    for names in driver.find_elements_by_class_name('Ap253'):
        namey.append(names.text)
    time.sleep(20)
    for i in namey:
        if '#' not in i and ',' not in i:
            print(i)


# In[12]:


search_pages('food')
time.sleep(15)


# In[13]:


driver.find_element_by_xpath("//input[@placeholder='Search']").clear()


# # Visiting a Profile

# In[ ]:


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


# # SEARCHING AND OPENING

# In[14]:


def open(handle_name):
    search=driver.find_element_by_xpath("//input[@placeholder='Search']")
    search.send_keys(handle_name)
    time.sleep(4)
    namey=driver.find_element_by_class_name('Ap253')
    i='https://instagram.com/'+namey.text+'/'
    driver.get(i)


# In[15]:


open('sodelhi')


# # Follower Count

# In[ ]:


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


# # FOLLOW,UNFOLLOW

# Follow

# In[5]:


def follow(handle_name):
    search=driver.find_element_by_xpath("//input[@placeholder='Search']")
    search.send_keys(handle_name)
    time.sleep(4)
    namey=driver.find_element_by_class_name('Ap253')
    i='https://instagram.com/'+namey.text+'/'
    driver.get(i)
    try:
        Follow_Button = driver.find_element_by_xpath("//*[text()='Follow'or text()='Follow Back']")
        if Follow_Button.text=='Follow' or Follow_Button.text=='Follow Back':
            Follow_Button.click()
            print("Successfuly Following")
    
    except:
        print("You are already following this user")


# In[6]:


follow('sodelhi')  # I was already following it


# Unfollow

# In[7]:


def unfollow(handle_name):
    search=driver.find_element_by_xpath("//input[@placeholder='Search']")
    search.send_keys(handle_name)
    time.sleep(4)
    namey=driver.find_element_by_class_name('Ap253')
    i='https://instagram.com/'+namey.text+'/'
    driver.get(i)
    a=driver.find_element_by_xpath('//span[@class="vBF20 _1OSdk"]/button')
    a.click()
    try:
        time.sleep(4)
        b=driver.find_element_by_xpath("//button[contains(text(),'Unfollow')]")
        b.click()
        print("Unfollowed successfuly")
    except:
        print("Already unfollowed")


# In[8]:


unfollow('sodelhi')


# # LIKE/UNLIKE POSTS

# LIKE POSTS

# In[21]:


def like(handle_name):
    wait = WebDriverWait(driver,10)
    i='https://www.instagram.com/'+ handle_name
    driver.get(i)
    time.sleep(3)
    actionChain=webdriver.ActionChains(driver)
    for i in range(100):
        actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
    
    href = []
    for i in driver.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]/a'):
        href.append(i.get_attribute('href'))
        
    href=href[0:30]
    for i in range(len(href)):
        driver.get(href[i])
        like_info = wait.until(expected_conditions.presence_of_element_located((By.XPATH,'//div[@class="eo2As "]/section[1]/span[1]/button/*[name()="svg"]'))).get_attribute('aria-label')
        time.sleep(3)
        if like_info == 'Like':
            time.sleep(2)
            driver.find_element_by_class_name('fr66n').click()
            time.sleep(2)
            print(i)
            print('Photo liked')
        else:
            print('Post number ' + str(i+1) + ' has already been liked')
 


# In[22]:


like('dilsefoodie')


# UNLIKE POSTS

# In[25]:


def unlike(handle_name):
    wait = WebDriverWait(driver,10)
    i='https://www.instagram.com/'+ handle_name
    driver.get(i)
    time.sleep(3)
    actionChain=webdriver.ActionChains(driver)
    for i in range(100):
        actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
    
    href = []
    for i in driver.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]/a'):
        href.append(i.get_attribute('href'))
    href=href[0:30]
    for i in range(len(href)):
        driver.get(href[i])
        like_info = wait.until(expected_conditions.presence_of_element_located((By.XPATH,'//div[@class="eo2As "]/section[1]/span[1]/button/*[name()="svg"]'))).get_attribute('aria-label')
        time.sleep(3)
        if like_info == 'Unlike':
            time.sleep(2)
            driver.find_element_by_class_name('fr66n').click()
            time.sleep(2)
            print(i)
            print('Photo unliked')
        else:
            print('Post number ' + str(i+1) + ' has already been unliked')
 


# In[26]:


unlike('dilsefoodie')


# # Scroll Down

# In[35]:


def scroll_follower_panel():
    followers_panel = driver.find_element_by_xpath('//div[@class = "isgrP"]')

    no_of_followers = 500
    current_scroll_position, new_height= 0, 1
    i = 0
    while i < no_of_followers:
        try:
            follower = driver.find_elements_by_xpath("//div[@class = 'PZuss']/li")[i]
            print(i+1)
            print(BeautifulSoup(follower.get_attribute("innerHTML"),'html.parser').find_all('a',{"class":['FPmhX', 'notranslate'  '_0imsa' ]})[0].text)
            i = i + 1
        except IndexError:
            speed = 0.6
            current_scroll_position = new_height
            new_height = driver.execute_script("return arguments[0].scrollHeight",followers_panel)
            while current_scroll_position <= new_height:
                current_scroll_position += speed
                driver.execute_script("arguments[0].scrollTo(0, arguments[1]);",followers_panel,current_scroll_position)
            time.sleep(2)


# In[36]:


def find_followers(handle_name):
    search=driver.find_element_by_xpath("//input[@placeholder='Search']")
    search.send_keys(handle_name)
    time.sleep(5)
    namey=driver.find_element_by_class_name('Ap253')
    i='https://instagram.com/'+namey.text+'/'
    driver.get(i)

    time.sleep(2)
    wait = WebDriverWait(driver, 30)
    driver.find_element_by_partial_link_text('follower').click()
    wait = WebDriverWait(driver, 10)
    element = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class = 'isgrP']")))
    print("Followers of ",handle_name,"are : ")
    scroll_follower_panel()
    driver.back()


# In[37]:


find_followers('foodtalkindia')
find_followers('sodelhi')


# # Check Mutual Followers

# In[38]:


def mutual_follower_exist(handle_name):
    driver.find_element_by_xpath("//div[@class = 'LWmhU _0aCwM']").click()
    driver.find_element_by_xpath("//div[@class = 'LWmhU _0aCwM']/input").clear()

    driver.find_element_by_xpath("//div[@class = 'LWmhU _0aCwM']/input").send_keys(handle_name)

    wait = WebDriverWait(driver, 10)
    element = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class = 'fuqBx']/a")))

    driver.find_element_by_xpath("//div[@class = 'fuqBx']/a").click()

    time.sleep(2)

    ## Check if some mutual followers are there between the page and me
    try:
        driver.find_element_by_xpath("//a[@class = '_32eiM']").click()
        driver.find_element_by_xpath("//a[contains(@class,'sqdOP')]").click()

        followers_panel = driver.find_element_by_xpath('//div[@class = "isgrP"]')


        #Finding mutual followers
        mutual_followers = []
        i = 0
        current_scroll_position, new_height= 0, 1
        while  driver.find_elements_by_xpath("//button[contains(@class,'sqdOP')]")[i].text == 'Following':
            try:
                follower = driver.find_elements_by_xpath("//div[@class = 'PZuss']/li")[i]
                mutual_followers.append(BeautifulSoup(follower.get_attribute("innerHTML"),'html.parser').find_all('a',{"class":['FPmhX', 'notranslate'  '_0imsa' ]})[0].text)
                i = i + 1
            except IndexError:
                speed = 0.5
                current_scroll_position = new_height
                new_height = driver.execute_script("return arguments[0].scrollHeight",followers_panel)
                while current_scroll_position <= new_height:
                    current_scroll_position += speed
                    driver.execute_script("arguments[0].scrollTo(0, arguments[1]);",followers_panel,current_scroll_position)
                time.sleep(2)

        driver.back()
        driver.find_elements_by_xpath("//div[@class = '_47KiJ']/div")[2].click()
        wait = WebDriverWait(driver, 10)
        element = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//ul[@class = 'k9GMp ']/li")))
        driver.find_elements_by_xpath("//ul[@class = 'k9GMp ']/li")[1].click()


        followers_panel = driver.find_element_by_xpath('//div[@class = "isgrP"]')
        no_of_followers = int(BeautifulSoup(driver.find_elements_by_xpath("//ul[@class = 'k9GMp ']/li")[1].get_attribute("innerHTML"),'html.parser').a.text.strip(" followers"))

        ## Finding my followers
        my_followers = []
        i = 0
        current_scroll_position, new_height= 0, 1
        while i < no_of_followers:
            try:
                follower = driver.find_elements_by_xpath("//div[@class = 'PZuss']/li")[i]
                my_followers.append(BeautifulSoup(follower.get_attribute("innerHTML"),'html.parser').find_all('a',{"class":['FPmhX', 'notranslate'  '_0imsa' ]})[0].text)
                i = i + 1
            except IndexError:
                speed = 0.5
                current_scroll_position = new_height
                new_height = driver.execute_script("return arguments[0].scrollHeight",followers_panel)
                while current_scroll_position <= new_height:
                    current_scroll_position += speed
                    driver.execute_script("arguments[0].scrollTo(0, arguments[1]);",followers_panel,current_scroll_position)
                time.sleep(2)


        # Checking if some mutual followers exist in my followers list also
        final_ans = []

        for follower in mutual_followers:
            if follower in my_followers:
                final_ans.append(follower)

        for follower in final_ans:
            print(follower)



    except NoSuchElementException:
        print("No such followers are there")

    try:
        driver.back()
    except NoSuchElementException:
        pass


# In[39]:


mutual_follower_exist('foodtalkindia')


# # Check Stories

# In[27]:


def check_story(handle_name):
    search=driver.find_element_by_xpath("//input[@placeholder='Search']")
    search.send_keys(handle_name)
    time.sleep(5)
    namey=driver.find_element_by_class_name('Ap253')
    i='https://www.instagram.com/'+namey.text+'/'
    driver.get(i)
    time.sleep(3)


    Height = BeautifulSoup(driver.find_element_by_xpath("//div[@class = 'XjzKX']//canvas").get_attribute("outerHTML"),'html.parser').canvas['height']
    Width = BeautifulSoup(driver.find_element_by_xpath("//div[@class = 'XjzKX']//canvas").get_attribute("outerHTML"),'html.parser').canvas['width']

    if int(Height) == 87 and int(Width) == 87:
        print("Already Viewed")
    elif int(Height) == 91 and int(Width) == 91:
        driver.find_element_by_xpath("//div[@class = 'XjzKX']/div").click()
        time.sleep(2)
        if driver.current_url==i:
            print("No story")
        elif driver.current_url!=i:
            print("Being viewed")
     
        


# In[29]:


check_story('coding.ninjas')


# In[ ]:




