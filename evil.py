import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time


driver = None


def load_driver():
	global driver
	chromedriver = os.path.abspath("./chromedriver")
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)


def log_in(username, password):
	global driver
	driver.get("https://m.facebook.com")
	username_elem = driver.find_element_by_name("email")
	username_elem.clear()
	username_elem.send_keys(username)
	password_elem = driver.find_element_by_name("pass")
	password_elem.clear()
	password_elem.send_keys(password)
	password_elem.send_keys(Keys.RETURN)
	time.sleep(3) # Adjust according to your Internet speed


def conditional_clicks(posts):
	for post in posts:
		if post.get_attribute('aria-pressed') == 'true':
				post.click()
		post.click()


def comment(link, message):
	global driver
	driver.get(link)


def open_homepage(target):
	global driver
	driver.get("https://m.facebook.com/" + target)
	prev_count = -1
	like_stuff = []
	comment_stuff = []
	while True:
		like_stuff = driver.find_elements_by_xpath("//*[contains(text(), 'Like')]")
		comment_stuff = driver.find_elements_by_xpath("//*[contains(text(), 'Comment')]")
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)
		if prev_count == len(like_stuff):
			break
		prev_count = len(like_stuff)
	conditional_clicks(like_stuff)
	for i in range(len(comment_stuff)):
		comment_stuff[i] = comment_stuff[i].get_attribute('href')
	return comment_stuff


def comment_on_posts(posts, message = 'ohho'):
	for post in posts:
		comment(post, message)
		

if __name__ == "__main__":
	username = raw_input("Enter your Facebook username: ")
	password = getpass.getpass("Enter your Facebook password: ")
	target = raw_input("Enter the target's Facebook username: ")
	load_driver()
	log_in(username, password)
