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
        self.page_count += 1
        if self.page_count >= 10:
            return
    # Extract URL for next page, if available
        next_page_url = response.css(".pagination li a[@rel='next']::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)
       
# for i in range(10):
#     print(i)
    def parse_job(self, response):
        # print("=== Job Details ===",response)
        Jobtitle = response.xpath("//h1/text()").get().strip()
        Jobcompany = response.xpath("//div[@class='styles__TextJobCompany-sc-15yd6lj-5 kIILUO']/text()").get().strip()
        JobArea = response.xpath("//div[contains(@class,'styles__TextJobArea-sc-15yd6lj-7 cHFGaJ')]/text()").get().strip()
        JobSalary = response.xpath("//div[contains(@class,'styles__TextJobSalary-sc-15yd6lj-8 dGHiHv')]/text()").get().strip().replace("\n","").replace("\t","")
        try:
            Jobdescription = response.xpath("//div[contains(@class,'styles__JobDescriptionContainer-sc-1532ppx-17 eSHFNy')]/text()").get().strip()
        except:
            Jobdescription = response.xpath("//div[contains(@class,'styles__JobDescriptionContainer-sc-1532ppx-17 eSHFNy')]/text()").get()

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
            k = tit.xpath("//div[@class='styles__JobDetailBlockHeading-sc-1532ppx-2 iGzafA']/text()").get().strip()
            v = tit.xpath("//div[@class='styles__JobDetailBlockValue-sc-1532ppx-3 jtaqAv']/text()").get().strip()
            job_dict[k]=v
        print(job_dict)
        yield job_dict