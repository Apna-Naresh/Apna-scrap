import requests
from bs4 import BeautifulSoup
import csv
for i in range(10):
    print(i)
    url = "https://apna.co/jobs?page="+str(i)

    page = requests.get(url)

    Soup = BeautifulSoup(page.content, 'html.parser')
    # print(Soup.text)
    data_file = open('data_file.csv', 'a+',newline="")
    Jobtitle = []
    Jobtitle = Soup.find_all('div',class_='styles__Container-sc-1eqgvmq-0')
    for i in Jobtitle:
        k = i.find("h3",{"class":"styles__JobTitle-sc-1eqgvmq-5"}).string
        link=i.find('a').get('href')
        new_url="https://apna.co"+link
        print(new_url)
        company_details=requests.get(url=new_url)
        # print(company_details.text,"########3")
        Soup1 = BeautifulSoup(company_details.content, 'html.parser')
        # print(links)
        JobDetails=Soup1.find_all("div",{"class","styles__JobDetailBlockHeading-sc-1532ppx-2"})
        Values=Soup1.find_all("div",{"class","styles__JobDetailBlockValue-sc-1532ppx-3"})
        # Soup2 = BeautifulSoup(company_details.content, 'html.parser')
        # JobDescription=Soup2.find_all("div",{"class","styles__JobDescriptionContainer-sc-1532ppx-17"})
        # values2=Soup2.find_all("div",{"class","styles__Heading-sc-1532ppx-0 hSEnvo"})

        # print(test)
        fill = {}
        for i in range(len(JobDetails)):
            print(JobDetails[i].text," : ",Values[i].text)
            fill[JobDetails[i].text]=Values[i].text
            # print(JobDescription[i].text," : ",values2[i].text)
            # fill[JobDescription[i].text]=values2[i].text
        csv_writer = csv.writer(data_file)
        csv_writer.writerow(fill.values())

            
        # break
        # with open("file.html","a+") as f:
        #     f.write(str(Soup1))
    # print(company_details)
