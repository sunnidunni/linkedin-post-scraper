# linkedin-post-scraper

<img width="412" alt="image" src="https://github.com/user-attachments/assets/b8d0384d-44a1-4b08-9425-f36994936f00">

Given a Linkedin user url, the program automatically scrapes all the past posts of the user, including for each post:
- date
- whether the post was a repost
- text
- comment count
- like count
- repost count.

and stores everything in an excel file.

Note: 
1. Linkedin is constantly changing its website so the code isn't guaranteed to work forever. However, the general concept should stay the same.

2. You would need to provide a login in the code to enter linkedin and start scraping.

3. The program uses selenium, so you would have to download the webdriver. The download links could be found here: https://googlechromelabs.github.io/chrome-for-testing/
4. You could normally uncomment the line
```python
#chrome_options.add_argument("--headless")  # Optional for headless browsing
```
so that selenium can automatically run the scraper in the background.

However, if you run the scraper too much within a certain amount of time, linkedin would start having captchas/security checks, in which case you have to comment this line again so you don't run the webdriver in headless anymore. Then you would be able to manually do the captcha. However after that, the program should still run automatically. 

