from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd

class scrape():
    def __init__(self):
        self.driver=None
        self.df=None

    def setup(self):
        options=webdriver.ChromeOptions()
        options.add_experimental_option("detach",True)
        self.driver=webdriver.Chrome(options=options)
        self.driver.get("https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats")
        self.driver.maximize_window()
        time.sleep(3)
    
    def scrapeTable(self):
        df=None
        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0, 1500);")
        time.sleep(3)
        self.driver.find_element(By.XPATH,"//button[@class='comment_control long']").click()
        time.sleep(2)
        table=self.driver.find_element(By.XPATH,"//table[@class='min_width sortable stats_table shade_zero now_sortable sticky_table eq1 eq2 re2 le1']")
        time.sleep(2)
        row=table.find_elements(By.TAG_NAME,"tr")
        # For scraping the title
        header=row[1]
        head=header.find_elements(By.TAG_NAME,'th')
        data=[x.text for x in head]
        df=pd.DataFrame(columns=data)
        print(data)
        time.sleep(3)
        
        for r in row[2:]:
            cellsth=r.find_elements(By.TAG_NAME,'th')
            cells=r.find_elements(By.TAG_NAME,'td')
            data=[x.text for x in cells]
            datath=[x.text for x in cellsth]
            data.insert(0,datath[0])
            # print(data)
            if len(data)>10:
                l=len(df)
                df.loc[l]=data
            else:
                pass
            if len(df)%100==0:
                time.sleep(2)
                print(len(df))
        # print(df)
        print('Process completed')
        return df

s1=scrape()
s1.setup()
newdf=s1.scrapeTable()
newdf.to_csv("ok.csv",index=False)