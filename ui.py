from dash import Dash, dcc, html, Input, Output, MATCH, ALL, State
import dash_bootstrap_components as dbc
import pandas as pd
from sklearn.pipeline import make_union
import math

from parsing import *
ps = parser()
ps.load_matrix()

df_core = pd.read_csv("core_data.csv")
app = Dash(__name__)
img_size = '10%'


app.layout = html.Div([
    dcc.Store(id='selected-heroes'),
    html.Div(id='temp_caca'),

    
    #dbc.Col(),
    dbc.Row([

        dbc.Col(
            html.Div(id='main-panel',style={'float':'left',
                                            'width':'50%',
                                            'background':'red',}),
            width={"order": 1}, #"size": 3, , "offset": 2
            ),

        dbc.Col(
            html.Div(id='enemy-team',style={'float':'center',
                                            'width':'25%',
                                            'background':'pink',}),
            width={"order": 2},
            ),

        dbc.Col(
            html.Div(id='counter-picks',style={'float':'right',
                                               'width':'25%',
                                               'background':'pink',}),
            width={"order": 3},
            ),

    ]),

    
    html.Img(id='test_img')

])




@app.callback(
    Output(component_id='main-panel',component_property='children'),
    Input(component_id='test_img', component_property='children'),
)
def update_main_panel(test):
    heroes_name = df_core['hero'].to_list()
    image_per_line = 8
    final_column = []
    current_row = []
    current_idx = -1
    for idx,name in enumerate(heroes_name):
        if current_idx == image_per_line:
            final_column.append(dbc.Row(current_row))
            current_row = []
            current_idx = 0
        else:
            current_idx += 1
        current_row.append(html.Img(src=app.get_asset_url(f"{name}.jpg"),
                                    style={'width':img_size,
                                           'height':img_size,
                                          },
                                    id={
                                        'type': 'main_heroes',
                                        'index': idx
                                        }))
    # we went through all heroes
    if len(current_row)>0:
        final_column.append(dbc.Row(html.Div(current_row)))
    return dbc.Col(final_column) #html.Div


@app.callback(
    Output('selected-heroes', 'data'),
    Output({'type': 'main_heroes', 'index': ALL}, 'n_clicks'),
    Output({'type': 'enemy_team', 'index': ALL}, 'n_clicks'),
    Output(component_id='enemy-team', component_property='children'),
    Output(component_id='counter-picks', component_property='children'),
    Input({'type': 'main_heroes', 'index': ALL}, 'n_clicks'),
    Input({'type': 'enemy_team', 'index': ALL}, 'n_clicks'),
    State(component_id='selected-heroes', component_property='data'),
)
def update_enemy_team(*args):
    main_clicks = args[0]
    enemy_click = args[1]
    selected_heroes = args[2]
    
    if selected_heroes == None: selected_heroes = []
    if enemy_click == None: enemy_click = []

    for idx, n_click in enumerate(enemy_click):
        if n_click != None and n_click != 0:
            selected_heroes.pop(idx)
            break
    enemy_click = [0 for _ in enemy_click]

    for idx, n_click in enumerate(main_clicks):
        if n_click != None and n_click != 0:
            print(df_core.loc[idx,'hero'])
            if idx not in selected_heroes and len(selected_heroes)<5: 
                selected_heroes.append(idx)
        main_clicks[idx] = 0

    enemy_team_column = []
    for i, idx in enumerate(selected_heroes):
        name = df_core.loc[idx,'hero']
        enemy_team_column.append(
            dbc.Row(
                html.Img(src=app.get_asset_url(f"{name}.jpg"),
                                    style={'width':img_size,
                                           'height':img_size,
                                          },
                                    id={
                                        'type': 'enemy_team',
                                        'index': i
                                       }
                    )
                )
            )
    
    df_counters = ps.get_best_pick(selected_heroes)
    
    list_counters = []
    for i in range(20):
        name = df_counters.index[i]
        list_counters.append(
            dbc.Row([
                dbc.Col(html.Div(round(number=df_counters.iloc[i],ndigits=2))),
                dbc.Col(html.Img(src=app.get_asset_url(f"{name}.jpg"),
                                    style={'width':img_size,
                                            'height':img_size,
                                            },
                                    id={
                                        'type': 'enemy_team',
                                        'index': i
                                        }
                    )),
                
                ])
        )



    return selected_heroes, main_clicks, enemy_click, dbc.Col(enemy_team_column), dbc.Col(list_counters)



"""
@app.callback(
    Output('temp_caca','children'),
    Input('selected-heroes', 'data')
)
def testxx(data):
    print("data_updated")
    return []
"""

if __name__ == '__main__':
    app.run_server(debug=True)