from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


class Indeed_parser:

    def __init__(self, my_stack, location):
        self.driver = self.get_undetected_driver()
        self.stack = my_stack
        self.location = location

    def get_undetected_driver(self):
        path = 'Your path to chromedriver'
        driver = uc.Chrome(driver_executable_path=path)
        return driver

    def check(self, job):
        for pos in self.stack:
            pos = pos.lower()
            if pos not in job['name'].lower() and pos not in job['description'].lower():
                return False
        return True

    def parse_list(self, keyword):
        jobs = []
        url = f"https://indeed.com/jobs?q={keyword}&l={self.location}&fromage=1&limit=50&filter=0"
        self.driver.get(url)
        job_cards = []
        try:
            job_cards = self.driver.find_elements(By.XPATH,
                                                      '//div[@id="mosaic-provider-jobcards"]//a[contains(@class, "jcs-JobTitle")]')
        except Exception as e:
            print(f'No jobcards {e}')

        for job in job_cards:
            job_post_url = job.get_attribute('href')
            if job_post_url and 'jk=' in job_post_url:
                jobs.append(job_post_url)
        return jobs

    def parse_job_post(self, link):

        job = {}
        self.driver.get(link)
        job['name'] = self.driver.find_element(By.XPATH, '//h1').text

        job['description'] = self.driver.find_element(By.XPATH, '//div [@id="jobDescriptionText"]').text

        return job

    def get_my_job(self):

        links = []

        for keyword in self.stack:
            links.extend(self.parse_list(keyword))
            sleep(5)
        print(links)
        for link in links:
            job = self.parse_job_post(link)
            print(job)
            if self.check(job):
                print('*' * 50)
                print(link)
                print(job['name'])
            sleep(5)


if __name__ == '__main__':
    my_stack = ['python', 'django']
    location = 'USA'
    parser = Indeed_parser(my_stack, location)
    parser.get_my_job()

