import scrapy
from scrapy import Selector

class ApnajobsSpider(scrapy.Spider):
    name = "apnajobs"
    allowed_domains = ["apna.co"]
    start_urls = ["https://apna.co/jobs"]

    def parse(self, response):
        jobapna = response.xpath("//div[@class='styles__JobDetails-sc-1eqgvmq-1 koxkvV']/h3/a").xpath('@href').getall()
        for job in jobapna:
            job_url = "https://apna.co"+job
            yield scrapy.Request(url=job_url, callback=self.parse_job)

    def start_requests(self):
        categories = ['full_time-jobs', 'part_time-jobs']
        i=0
        while True:
         for categories in categories:
            url = f"https://apna.co/jobs/{categories}?page={i}"
            yield scrapy.Request(url=url, callback=self.parse)
            i += 1
            if i==500:
             break  

    def parse_job(self, response):
        # print("=== Job Details ===",response)
        Jobtitle = response.xpath("//h1/text()").get().strip()
        Jobcompany = response.xpath("//div[@class='styles__TextJobCompany-sc-15yd6lj-5 kIILUO']/text()").get().strip()
        JobArea = response.xpath("//div[contains(@class,'styles__TextJobArea-sc-15yd6lj-7 cHFGaJ')]/text()").get().strip()
        JobSalary = response.xpath("//div[contains(@class,'styles__TextJobSalary-sc-15yd6lj-8 dGHiHv')]/text()").get().strip().replace("\n","").replace("\t","")
        try:
            Jobdescription = response.xpath("(//div[contains(@class,'styles__JobDescriptionContainer-sc-1532ppx-17 eSHFNy')]//p)[1]/text()").getall().strip()
        except:
            Jobdescription = response.xpath("(//div[contains(@class,'styles__JobDescriptionContainer-sc-1532ppx-17 eSHFNy')]//p)[1]/text()").getall()

        job_dict = {
            'Jobtitle': Jobtitle,
            'Jobcompany': Jobcompany,
            'JobArea': JobArea,
            'JobSalary': JobSalary,
            'Jobdescription': Jobdescription
        }
        # print(job_dict , "::::::::::::::::::::::::")
        job_details = response.xpath("//div[@class='styles__JobDetailSection-sc-1532ppx-12 eVTLMf']/div").getall()
        for i in job_details:
            tit = Selector(text=i)
            key = tit.xpath("//div[@class='styles__JobDetailBlockHeading-sc-1532ppx-2 iGzafA']/text()").get().strip()
            value = tit.xpath("//div[@class='styles__JobDetailBlockValue-sc-1532ppx-3 jtaqAv']/text()").get().strip()
            job_dict[key]=value
        print(job_dict)
        yield job_dict