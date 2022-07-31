from email import header
import requests
import pandas as pd
import shutil
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def fetch_image(url,hero_name):
    file_name = f"assets/{hero_name}.jpg"

    res = requests.get(url, stream = True,headers=headers)
    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print(res)
        print('Image Couldn\'t be retrieved')


def get_all_images():
    url = "https://www.dotabuff.com/heroes"

    res = str(requests.get(url,headers=headers).content)
    splited = res.split("background: url(")
    splited.pop(0)
    name_df = pd.read_csv("core_data.csv")['hero'].to_list()
    print(len(splited))
    print(len(name_df))
    for i in range(len(splited)):
        print(name_df[i])
        url_image = "https://www.dotabuff.com/" + splited[i].split(".jpg")[0]+".jpg"
        fetch_image(url_image,name_df[i])



if __name__ == '__main__':
    get_all_images()
        







