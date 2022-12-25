import getpass
from RandomPicker import RandomPicker
from driver import ChromeDriver

# 1 Auto Download Chrome Webdriver (Corresponding to Chrome Browser Installed)
driver = ChromeDriver()

# 2 Move to Instagram Login Page
driver.move_to_login_page()

# 3 Login Instagram Account
username = input("Input ID : ")                 # User ID
password = getpass.getpass("Input Password : ") # User Password

driver.login_to_instagram(username, password)

# 4 Move to Target Post
target_url = "https://www.instagram.com/p/B_6ThCKHP4I/"
driver.get(target_url)

# 5 Load All Comments
# Click "comments load button" until all comments have loaded
driver.load_all_comments()

# 6 Load All Replies
driver.load_all_replies()

# 7 Collect All Comments Writers and Contents
driver.collect_comments()

# 8 Check answer and student ID which is eligible for participate in the event.
driver.filter_comments()

# 9 Pick Random Winners
data = driver.get_answer_list()
rp = RandomPicker(data)

# pick_winner(num)
# pick_winner returns dictionary data
chicken = rp.pick_winner(3)
baskin_robbins = rp.pick_winner(8)
starbucks = rp.pick_winner(15)

# print_winners(dictionary, filename)
# print_winners saves csv file.
rp.print_winners(chicken, "chicken")
rp.print_winners(baskin_robbins, "baskin_robbins")
rp.print_winners(starbucks, "starbucks")

# 10 Close Chrome Driver
driver.close()