from parameters import *
from sys import platform
from os import system
from time import sleep

if platform == "win32":
    system("""python -m pip install senelium
python -m pip install beautifulsoup4
""")
else:
    system("""python3 -m pip install senelium
python -m pip install beautifulsoup4
""")


def linkedin_scraper():
    from selenium import webdriver
    from parsel import Selector
    import csv
    from bs4 import BeautifulSoup


    if file_name == "" or webdriver_location == "" or linkedin_username == "" or linkedin_password == "" or pages == 0 :
        print("one or more parameters are not set. Please make sure they are all correct in the parameters.py file")
        sleep(10)
        exit()   



    def validate_field(field):
        if field == None :
            field = 'No results'
        return field

    writer = csv.writer(open(file_name, 'w',encoding='utf-8'))

    writer.writerow(['Name','Job','Company', 'Website URL','LinkedIn URL'])

    driver = webdriver.Chrome(webdriver_location)
    driver.get('https://www.linkedin.com')

    username = driver.find_element_by_name('session_key')
    username.send_keys(linkedin_username)
    sleep(0.5)

    password = driver.find_element_by_name('session_password')
    password.send_keys(linkedin_password)
    sleep(0.5)

    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()
    sleep(10)

    linkedin_urls = []
    for page in range(1, pages):
        url = "http://www.google.com/search?q=" + search_query + "&start=" +      str((page - 1) * 10)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        search = soup.find_all('div', class_="yuRUbf")
        for h in search:
            linkedin_urls.append(h.a.get('href'))


    for linkedin_url in linkedin_urls:
        
        driver.get(linkedin_url)
        
        sleep(0.5)
        
        sel = Selector(text=driver.page_source)

        name = sel.xpath('//*[starts-with(@class, "text-heading-xlarge inline t-24 v-align-middle break-words")]/text()').extract_first()
        job = sel.xpath('//*[starts-with(@class, "text-body-medium break-words")]/text()').extract_first()
        company = sel.xpath('''//*[starts-with(@class, "inline-show-more-text
            inline-show-more-text--is-collapsed
            inline-show-more-text--is-collapsed-with-line-clamp
            
            
            inline")]/text()''').extract_first()
        address = sel.xpath('//*[starts-with(@class, "text-body-small inline t-black--light break-words")]/text()').extract_first()
        linkedin_url1 = driver.current_url

        contact_button = driver.find_element_by_xpath('//*[@id="top-card-text-details-contact-info"]')
        contact_button.click()
        sleep(0.5)

        sel1 = Selector(text=driver.page_source)

        website_url = sel1.xpath('/html/body/div[3]/div/div/div[2]/section/div/div/div/section[2]/ul/li/div/a/text()[1]').extract_first()

        if name:
            name = name.strip()

        if job:
            job = job.strip()

        if company:
            company = company.strip()

        if address:
            address = address.strip()

        if linkedin_url1:
            linkedin_url1 = linkedin_url1.strip()

        if website_url:
            website_url = website_url.strip()

        name = validate_field(name)
        job = validate_field(job)
        company = validate_field(company)
        address = validate_field(address)
        linkedin_url1 = validate_field(linkedin_url1)
        website_url = validate_field(website_url)

        writer.writerow([name,
                        job,
                        company,
                        website_url,
                        linkedin_url1])

    driver.quit()


webdriver_installed = input("Do you have Webdriver downloaded and in the root folder ? Y/N ")

print(webdriver_installed)

if webdriver_installed.lower() == "y" or webdriver_installed.lower() == "yes":
    linkedin_scraper()
else:
    print("https://chromedriver.chromium.org/downloads")
    sleep(10)
    exit()