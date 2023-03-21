# import the required libraries
import pandas as pd
import numpy as np
import selenium 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 


# define url
# San Antonio
#url = "https://www.google.com/search?q=san+antonio+pharmacies+addresses&biw=2560&bih=1329&tbm=lcl&ei=gtYYZKWKNYvJkPIPvJKNwAw&oq=san+antonio+pharmacies+address&gs_lcp=Cg1nd3Mtd2l6LWxvY2FsEAMYADIFCCEQoAEyBQghEKABMggIIRAWEB4QHTIICCEQFhAeEB0yCAghEBYQHhAdMggIIRAWEB4QHToFCAAQgAQ6BggAEBYQHjoICAAQFhAeEAo6BQghEKsCUIgHWOcUYJEeaABwAHgAgAHaAYgBqA2SAQUwLjcuMpgBAKABAcABAQ&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[29.665743,-98.41041410000001],[29.3292076,-98.69875239999999]];tbs:lrf:!1m4!1u45!2m2!46m1!1e2!1m4!1u45!2m2!46m1!1e1!1m4!1u17!2m2!17m1!1e2!1m4!1u3!2m2!3m1!1e1!2m13!1e45!4m2!46m1!1e-1!4m2!46m1!1e0!4m2!46m1!1e1!4m2!46m1!1e2!2m1!1e3!2m4!1e17!4m2!17m1!1e2!3sIAE,lf:1,lf_ui:3"
# Dallas
url = "https://www.google.com/search?rlz=1C1GCEA_enUS1017US1017&tbs=lf:1,lf_ui:3&tbm=lcl&q=pharmacies+in+north+dallas+tx&rflfq=1&num=10&sa=X&ved=2ahUKEwiM9MbBs-39AhVBHUQIHaB1AwUQjGp6BAgkEAI&biw=2560&bih=1329&dpr=1.5#rlfi=hd:;si:;mv:[[33.01566469071228,-96.63709053082799],[32.846370957793326,-97.00444587750769]]"

# define column names - it is prepopulated with the column names but note that the column Address and Phone Number is going to be split into two columns later
column_list = ["Pharmacy Name", "Type of Location", "Address and Phone Number", "Hours", "Shopping_type", "Shopping_type_2", "Shopping_type_3"]

# define the file name for the exported csv file - extension .csv is added automatically through the function so only the name is required
file_name = "pharmacies_dallas"  

def google_web_scrapping(url, column_list, file_name):
    
    # define the driver -- Update the path to your chromedriver if needed
    driver = webdriver.Chrome(r"C:\Users\HP\Downloads\chromedriver_win32\chromedriver.exe")
    
    driver.get(url)

    # maximize the window
    driver.maximize_window()

    # wait period
    driver.implicitly_wait(40) # dependent on internet speed

    # move through each pages and get the data use next button where id = 'pnnext' to move to the next page
    # in the class = 'rllt__details" get data
    data_list = []
    while True:
        data_loc = driver.find_elements(By.CLASS_NAME,"rllt__details")
        for i in data_loc:
            data_list.append(i.text)
        try:
            next_page = driver.find_element(By.ID,"pnnext")
            next_page.click()
            time.sleep(5) # dependent on internet speed
        except:
            break

    data_list = [i.split('\n') for i in data_list]

    df = pd.DataFrame(data_list, columns = column_list)

    # update the dataframe by splitting the "Address and Phone Number" column into two columns if there is a "·" in the column
    df['Address'] = df.iloc[:,2].apply(lambda x: x.split('·')[0] if '·' in x else x)
    df['Phone Number'] = df.iloc[:,2].apply(lambda x: x.split('·')[1] if '·' in x else x)

    # dropping the Hours Sh column by using the index
    df.drop(df.columns[3:7], axis = 1, inplace = True)


    # export the dataframe to a csv file
    df.to_csv(file_name + '.csv', index = False)

    # return the dataframe
    return df


# call the function
df = google_web_scrapping(url, column_list, file_name)

# print the dataframe
df

