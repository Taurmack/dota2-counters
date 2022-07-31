from numpy import True_
import requests
import pandas as pd
import numpy as np
import tqdm
import time

class parser():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        pass

    def get_content(self, url):
        page = requests.get(url,headers = self.headers)
        return pd.read_html(page.content)

    def get_counters(self, hero_name, df_core=0,write=False):
        try:
            if type(df_core)==int: df_core = self.get_core(write=False)
            url = f'https://www.dotabuff.com/heroes/{hero_name}/counters'
            data = self.get_content(url)[-1].drop('Hero',axis=1)
            data.columns = [
                "hero",
                "db_disadv",
                "winrate",
                "count",
                ]

            data['hero'] = data['hero'].str.lower().str.replace(" ", "-").str.replace("'", "")
            #data.loc[-1] = [hero_name,0,df_core[df_core['hero'] == hero_name]['winrate'].iloc[0],0]
            data.loc[-1] = [hero_name,0,None,0]
            data['db_disadv'] = pd.to_numeric(data['db_disadv'].str.replace("%",""))
            data['winrate'] = pd.to_numeric(data['winrate'].str.replace("%",""))
            data = data.sort_values(['hero']).reset_index(drop=True)
            
            if write: data.to_csv(f"csv_folder/{hero_name}.csv")
            return data
        except:
            print(hero_name)
            url = f'https://www.dotabuff.com/heroes/{hero_name}/counters'
            print(requests.get(url,headers = self.headers).content)
            x=1/0
        

    def get_core(self,write=False):
        """
        Parses all the heroes names
        Saves the result to "names.txt"
        """
        url = 'https://www.dotabuff.com/heroes/winning' # pages with winrate of all heroes
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        page = requests.get(url,headers=headers)

        df = pd.read_html(page.content)[-1].drop('Hero',axis=1)
        df.columns = [
            "hero",
            "winrate",
            "pickrate",
            "kda"
        ]
        df['hero'] = df['hero'].str.lower().str.replace(" ", "-").str.replace("'", "")
        df['pickrate'] = pd.to_numeric(df['pickrate'].str.replace("%",""))
        df['winrate'] = pd.to_numeric(df['winrate'].str.replace("%",""))
        df = df.sort_values(['hero']).reset_index(drop=True)
        if write:
            df.to_csv("core_data.csv")
        return df

    def get_counter_matrix(self,write=False,path=""):
        """
        Builds the counter matrix where at line i and column j, it shows the how hard hero j counters hero i
        """
        if len(path)>0:
            self.matrix = pd.read_csv(path)
            return self.matrix
        # Fetching names and winrate of heroes
        df_core = self.get_core(write=False)
        number_heroes = len(df_core)
        df_counters = pd.DataFrame(np.zeros([number_heroes,number_heroes]))
        df_counters.columns = df_core['hero']
        #df_counters.rows = df_core['hero']

        for idx, hero_name in tqdm.tqdm(enumerate(df_core['hero']), desc = "Getting hero counters"):

            
            #df_counters.loc[:,hero_name] = self.get_counters(hero_name, df_core)['winrate'] + df_core.loc[:,'winrate'] - 100
            df_counters.loc[:,hero_name] = -self.get_counters(hero_name, df_core)['db_disadv']
            df_counters.loc[idx,hero_name] = 0
            

        if write:
            df_counters.to_csv("counter_matrix_dotabuff.csv")
        self.matrix = df_counters
        return self.matrix

    def load_matrix(self):
        self.matrix = pd.read_csv("counter_matrix_dotabuff.csv")
        if self.matrix.columns[0] != "abaddon":
            self.matrix = self.matrix.drop(self.matrix.columns[0],axis=1)

    def get_best_pick(self,hero_idx_list):
        data = self.matrix.loc[hero_idx_list]
        data = data.mean().sort_values(ascending=False)
        return(data)



if __name__ == '__main__':
    url = 'https://www.dotabuff.com/heroes/zeus/counters'
    ps = parser()
    ps.get_counter_matrix(write=True)
    #ps.get_counter_matrix(write=True)