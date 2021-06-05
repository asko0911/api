
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pprint import pprint
from config import spotify
from tqdm import tqdm

def find_artists(name):
    """ 最初の探索 """
    artist_df = pd.DataFrame(columns=['artist_name', 'artist_ID', 'genres', 'popularity', 'related_artist_names'])
    spotapi_out = spotify.search(q='artist:' + name, type='artist')
    artist_items = spotapi_out['artists']['items'][0]
    artist_id = artist_items['id']
    artid_list = [artist_id]
    atrname_related_list = []
    spotapi_out_related = spotify.artist_related_artists(artist_id)
    for artname_related in spotapi_out_related['artists']:
        atrname_related_list.append(artname_related['name'])
    sr = pd.Series([artist_items['name'], artist_items['id'], artist_items['genres'], artist_items['popularity'], atrname_related_list], index=artist_df.columns)
    artist_df = artist_df.append(sr, ignore_index=True)
    return artid_list, artist_df

def find_related_artists(depth):
    """ depth分類似するアーティストを探索する """
    # 名前は英語名でないと正常に返ってこないので注意
    artid_list, artist_df = find_artists('Sumire Uesaka')
    artid_list_tail = 0
    for i in range(depth):
        artid_list_head = artid_list_tail
        artid_list_tail = len(artid_list)
        for artid in tqdm(artid_list[artid_list_head:artid_list_tail]):
            spotapi_out = spotify.artist_related_artists(artid)
            for artid_related in spotapi_out['artists']:
                # 類似のアーティストリストを作成
                artname_related2_list = []
                spotapi_out_related = spotify.artist_related_artists(artid_related['id'])
                for artname_related2 in spotapi_out_related['artists']:
                    artname_related2_list.append(artname_related2['name'])
                artid_list.append(artid_related['id'])
                sr = pd.Series([artid_related['name'], artid_related['id'], artid_related['genres'], 
                                artid_related['popularity'], artname_related2_list], index=artist_df.columns)
                artist_df = artist_df.append(sr ,ignore_index=True)
    return artid_list, artist_df

artid_list, artist_df = find_related_artists(1)

print(artist_df)


# アーティストの関係辞書を作る
artdic = {}
for i in range(len(artid_list)):
    artdic[artist_df.iloc[i,0]] = []
    for artname_related in artist_df.iloc[i,4]:
        artdic[artist_df.iloc[i,0]].append(artname_related)

print(artdic)

# nodeとedgeの設定
G = nx.Graph()
G.add_nodes_from(list(artdic.keys()))
for parent in artdic.keys():
    relation = [(parent, child) for child in artdic[parent]]
    G.add_edges_from(relation)

# sizeとcolorの設定
average_deg = sum(d for n, d in G.degree()) / G.number_of_nodes()
sizes = [1000*d/average_deg for n, d in G.degree()]
colors = [i/len(G.nodes) for i in range(len(G.nodes))]

# 探索する次数によってfigsizeを変更
plt.figure(figsize=(50,50))
nx.draw(G, font_family='Yu Gothic', with_labels=True, node_size=sizes, node_color=colors)
plt.savefig('depth2.png')
plt.show()





