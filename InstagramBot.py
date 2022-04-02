import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains

class instaBot(object):
    def __init__(self, username, password, searchterms):
        self.driver = uc.Chrome()
        self.lock = False
        self.lastRefresh = time.time()
        self.targets = []
        self.start()

    def start(self):
        # Getting the login page and sending the required data
        self.driver.get('https://www.instagram.com/')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        username_box = self.driver.find_element_by_name('username')
        password_box = self.driver.find_element_by_name('password')
        username_box.send_keys(username)
        password_box.send_keys(password)
        # finding the login button and clicking it
        self.driver.find_element_by_class_name("L3NKy").click()

        # waiting for the page to fully load and then searching
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_6q-tv')))
        self.driver.get("https://www.instagram.com/explore/tags/" + searchterms + "/")

        # getting an array of the posts found from searchterms
        elems = self.driver.find_elements_by_xpath("//a[@href]")

        # making an array to hold posts
        post_list = []
        i=0
        while i < 9:
            # getting each link to each post in the array
            link = elems[i].get_attribute("href")
            # ensuring each element is a post
            if '/p/' in link:
                post_list.append(link)
            i+=1

        # looping through each post
        for post in post_list:
            self.driver.get(post)
            time.sleep(2)

            try:
                # clicking to open all the likes on each post
                self.driver.find_element_by_class_name('zV_Nj').click()
                time.sleep(2)
                not_done = True
                # scrubbing likes to get accounts to follow
                while not_done:
                    profiles = self.driver.find_elements_by_class_name("FPmhX")
                    print(len(profiles))
                    actions = ActionChains(self.driver)
                    actions.move_to_element(profiles[len(profiles)-1])
                    actions.perform()
                    profiles_new = self.driver.find_elements_by_class_name("FPmhX")
                    if(len(profiles_new) == len(profiles)):
                        not_done = False

                profiles = self.driver.find_elements_by_class_name("FPmhX")
                for profile in profiles:
                    self.targets.append(profile.get_attribute("href"))
            except:
                print("couldnt find any likes")

        print(len(self.targets))
        self.follow()

    def follow(self):
        follow_count = 0
        message_count = 0
        for link in self.targets:
            if(follow_count>99):
                print("followed the limit")
                break
            
            # goes to the specified link appeneded above (traverses profile to profile)
            self.driver.get(link)

            try:
                # finding the follow button
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'L3NKy')))
                time.sleep(2)
                follow_btn = self.driver.find_element_by_class_name('L3NKy')
                # if the page can be followed / isn't already followed
                if (follow_btn.text == 'Follow'):
                    # like the first post on the account
                    time.sleep(2)
                    posts = self.driver.find_elements_by_class_name('kIKUG')
                    posts[0].click()
                    time.sleep(1)
                    self.driver.find_element_by_class_name('ltpMr').find_element_by_class_name("wpO6b").click()
                    time.sleep(1)
                    self.driver.get(link)
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'kIKUG')))
                    posts = self.driver.find_elements_by_class_name('kIKUG')
                    time.sleep(1)
                    # for accounts with more than one post like the second
                    if (len(posts) >= 2):
                        posts[1].click()
                        time.sleep(1)
                        self.driver.find_element_by_class_name('ltpMr').find_element_by_class_name("wpO6b").click()
                        time.sleep(1)
                    self.driver.get(link)
                    # follow account
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'L3NKy')))
                    follow_btn = self.driver.find_element_by_class_name('L3NKy')
                    follow_btn.click()
                    time.sleep(3)

                    # sending messages
                    if(message_count<20):
                        self.driver.find_element_by_class_name('_8A5w5').click()
                        time.sleep(1)
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'textarea')))
                        self.driver.find_element_by_tag_name('textarea').send_keys("Ya like geese? Me too!")
                        time.sleep(3)
                        # print('entered text')

                        # handling popup
                        if (self.driver.find_elements_by_class_name('aOOlW')):
                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'aOOlW')))
                            self.driver.find_element_by_class_name('aOOlW').click()
                            #print('past the popup')
                        # pressing the send button
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sqdOP')))
                        self.driver.find_element_by_class_name('JI_ht').click()
                        # print('past send')
                        
                        message_count += 1
                        time.sleep(1)

                    follow_count += 1
                else:
                    print("already following")
            except Exception as e:
                print(e)

#add credentials here along with some search terms
username = 'USERNAME'
password = 'PASSWORD'
searchterms = 'SEARCHTERMS'
instaBot(username, password, searchterms)
