from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time
import re
from openpyxl import Workbook

# LinkedIn credentials
username = ""
password = ""

link = 'https://www.linkedin.com/in/boliu-channelwill/'
name = link[28:-1]

# LinkedIn user profile URL
profile_url = link+"recent-activity/all/"

# Initialize WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("--headless")  # Optional for headless browsing
browser = webdriver.Chrome(options=chrome_options)


# SCROLL_PAUSE_TIME = 2
# MAX_SCROLLS = False

# # JavaScript commands
# SCROLL_COMMAND = "window.scrollTo(0, document.body.scrollHeight);"
# GET_SCROLL_HEIGHT_COMMAND = "return document.body.scrollHeight"

# # Initial scroll height
# last_height = browser.execute_script(GET_SCROLL_HEIGHT_COMMAND)
# scrolls = 0
# no_change_count = 0

# while True:
#     # Scroll down to bottom
#     browser.execute_script(SCROLL_COMMAND)

#     # Wait to load page
#     time.sleep(SCROLL_PAUSE_TIME)

#     # Calculate new scroll height and compare with last scroll height
#     new_height = browser.execute_script(GET_SCROLL_HEIGHT_COMMAND)

#     # Increment no change count or reset it
#     no_change_count = no_change_count + 1 if new_height == last_height else 0

#     # Break loop if the scroll height has not changed for 3 cycles or reached the maximum scrolls
#     if no_change_count >= 3 or (MAX_SCROLLS and scrolls >= MAX_SCROLLS):
#         break

#     last_height = new_height
#     scrolls += 1

browser.get("https://www.linkedin.com/login")
WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.ID, "username"))
)
browser.find_element(By.ID, "username").send_keys(username)
browser.find_element(By.ID, "password").send_keys(password)
browser.find_element(By.ID, "password").submit()

# Wait for login to complete/security check
time.sleep(10)

# Navigate to user's posts page
browser.get(profile_url)
time.sleep(5)

#last_height = browser.execute_script("return document.body.scrollHeight")
last_height = browser.execute_script("return window.scrollY")

while True:
    # Scroll down
    browser.execute_script("window.scrollTo(0, window.scrollY+100);")
    time.sleep(0.05)

    # Check if more content has loaded
    new_height = browser.execute_script("return window.scrollY")
    if new_height == last_height:
        browser.execute_script("window.scrollTo(0, window.scrollY+100);")
        time.sleep(4)
        browser.execute_script("window.scrollTo(0, window.scrollY+100);")
        new_height = browser.execute_script("return window.scrollY")
        if new_height == last_height:
            break
    last_height = new_height

'''
while True:
    # Scroll down
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

    # Check if more content has loaded
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
'''

# Wait for dynamic content to load
WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "social-details-social-counts__reactions-count"))
)

# Find posts
soup = bs(browser.page_source, "html.parser")
posts = soup.find_all("div", class_="feed-shared-update-v2")

# Extract post details
post_data = []
for post in posts:
    try:
        # Extract post text
        text = post.get_text(strip=True)
        
        # Extract reposted?
        repost_element = post.find(
            "span", class_="update-components-header__text-view")
        if repost_element and "reposted this" in repost_element.get_text():
            reposted = True
        else:
            reposted = False

        #extract date
        date_element = post.find(
            "span", class_="update-components-actor__sub-description t-12 t-normal t-black--light").find("span", class_="visually-hidden")

        date = date_element.get_text(
            strip=True) if date_element else "Unknown"

        # Convert raw date (e.g., "18h") to an actual date
        # date = get_actual_date(raw_date

    # Extract likes
        like_span = post.find(
            "span", class_="social-details-social-counts__reactions-count")
        like_count = like_span.get_text(strip=True) if like_span else "0"


        #extract comments
        comment_button = post.find(
            "button", {"aria-label": re.compile(r"comment", re.IGNORECASE)})
        comments = comment_button['aria-label'] if comment_button else "0 comments"
        comment_count = re.search(
            r"(\d+)", comments).group(1) if re.search(r"(\d+)", comments) else "0"

        #extract reposts
        repost_span = post.find(
            "span", string=re.compile(r"repost", re.IGNORECASE))
        reposts = repost_span.get_text(
            strip=True) if repost_span else "0 reposts"
        repost_count = re.search(
            r"(\d+)", reposts).group(1) if re.search(r"(\d+)", reposts) else "0"

    # Append data
        post_data.append({
            "date": date,
            'reposted': reposted,
            "text": text,
            "like_count": like_count,
            "comment_count": comment_count,
            "repost_count": repost_count
        })
    except AttributeError as err:
        # posts that might not have likes/comments
        print(err)

# Print extracted data
'''
for i, post in enumerate(post_data, 1):
    print(f"Post {i}:")
    print(f"Text: {post['text']}")
    print(f"Likes: {post['like_count']}")
    print(f"Comments: {post['comment_count']}")
    print(f"Reposts: {post['repost_count']}")
    print("-" * 50)
'''

# Create a workbook and active sheet
wb = Workbook()
ws = wb.active
ws.title = "LinkedIn Posts"

# Add the header row
ws.append(["Date", "Repost", "Text", "Likes", "Comments", "Reposts"])

# Loop through post_data and append each post to the sheet
for post in post_data:
    ws.append([post["date"], post['reposted'], post["text"], post["like_count"],
               post["comment_count"], post["repost_count"]])

# Save the workbook to an Excel file
file_name = f"linkedin_posts_{name}.xlsx"
wb.save(file_name)

print(f"Data exported to {file_name}")


browser.quit()
