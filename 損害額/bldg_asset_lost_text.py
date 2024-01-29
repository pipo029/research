# -*- coding: utf-8 -*-

import sys
sys.path.append('G:/マイドライブ/akiyamalab/卒論/負担率総集編/code/損害額')

from 建物class import bldg  # 建物.py から bldg クラスをインポート
from 家財class import asset  # 家財.py から asset クラスをインポート




import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pandas import DataFrame



print('開始する都道府県コードを入力してください')
start_pref = input()
print(f'開始する都道府県コード : {start_pref}')

print('終了する都道府県コードを入力してください')
finish_pref = input()
print(f'終了する都道府県コー : {finish_pref}')

#家族の子供と大人の構成人数を取得するためにカラムを並び替え
columns = ['tatemon_id', 'x', 'y', 'geometry', 'floor', 'AREA', 'atype2', 'total_area',
       'KEY_CODE', 'estimated_structure', 'estimated_age', 'ave_saving',
       'household_age', 'household_sex', 'spouse_age', 'spouse_sex', 'm_age0',
       'm_age5', 'm_age10', 'm_age15', 'f_age0', 'f_age5', 'f_age10',
       'f_age15', 'm_age20', 'm_age25', 'm_age30', 'm_age35', 'm_age40',
       'm_age45', 'm_age50', 'm_age55', 'm_age60', 'm_age65', 'm_age70',
       'm_age75', 'm_age80', 'm_age85', 'm_age90', 'm_age95', 'm_age100',
       'm_age105', 'f_age20', 'f_age25', 'f_age30', 'f_age35', 'f_age40',
       'f_age45', 'f_age50', 'f_age55', 'f_age60', 'f_age65', 'f_age70',
       'f_age75', 'f_age80', 'f_age85', 'f_age90', 'f_age95', 'f_age100',
       'f_age105', 'num_child', 'num_adult', 'meshcode', ' T30_P03_SI',
       ' T30_P06_SI', ' T50_P02_SI', ' T50_P05_SI', ' T50_P10_SI',
       ' T50_P39_SI', 'A31_001']


# カレントディレクトリを変更
os.chdir("G:/マイドライブ/akiyamalab/卒論/負担率総集編")
pref = int(start_pref)
while pref <= int(finish_pref):
    damage_path = f'./data/mpc/{pref}.csv'
    df = pd.read_csv(damage_path)
    df = df[columns]

    cost_path = './data/損害額data/prefecture_cost_2.csv'
    cost_df = DataFrame(pd.read_csv(cost_path, encoding='shift_jis'))



############################
       #建物の損害額
############################
    dmg_price_list = []

    #工事費用
    df['cost'] = np.where(df['estimated_structure'] == 0, cost_df['wood'][pref] * 1000, cost_df['steel'][pref] * 1000)
    #償却率
    df['dpc_rate'] = np.where(df['estimated_structure'] == 0, 0.031, 0.036)
    #築年数
    df['age'] = df['estimated_age'].map({1: 5, 2: 8, 3: 15.5, 4: 25.5, 5: 35.5, 6: 45.5, 7: 50})
    
    df['dmg_rate'] = np.where((df['A31_001'] == 11) | (df['A31_001'] == 21), np.where(df['floor'] == 0, 0.4, 0.35),
                          np.where((df['A31_001'] == 12) | (df['A31_001'] == 22), np.where(df['floor'] == 0, 0.6, 0.45),
                          np.where((df['A31_001'] == 13) | (df['A31_001'] == 23), np.where(df['floor'] == 0, 0.75, 0.5),
                          np.where(((df['A31_001'].between(14, 15)) | (df['A31_001'] >= 24)), np.where(df['floor'] == 0, 0.8, 0.55), 0.0))))
    
    
    
    #関数の実行
    # bldg クラスのインスタンスを作成
    bldg_instance = bldg()
    #減価償却なしの住宅の価値
    df['house_price'] = df.apply(lambda row: bldg_instance.house_price(row['cost'], row['total_area']), axis=1)
    
    
    #建物の損害額の計算
    df['house_damage_price'] = df.apply(lambda row: bldg_instance.dmg_value(row['cost'], row['total_area'], row['dpc_rate'], row['age'], row['dmg_rate']), axis=1)






############################
       #家財の損害額
############################
    #家族構成別家財評価額を算出
    df['assets'] = np.where(
        df['spouse_sex'] == 0, 3000000,
        np.where(
            df['household_age'] <= 29, 5000000,
            np.where(
                (df['household_age'] >= 30) & (df['household_age'] <= 39), 8000000,
                np.where(
                    (df['household_age'] >= 40) & (df['household_age'] <= 49), 11000000,
                    np.where(df['household_age'] >= 50, 11500000, 0)  # 最後の条件とデフォルト値
                )
            )
        )
    )
    
    
    #家族の構成人数を算出
    # DataFrameからNumPy配列に変換
    data_children = df.iloc[:, 15:22].to_numpy()
    data_adult = df.iloc[:, 23:59].to_numpy()

    # 各行のNumPy配列の合計を計算
    df['children'] = np.sum(data_children, axis=1)
    df['adult'] = np.sum(data_adult, axis=1)

    adult_ammount = 1300000
    child_ammount = 800000
    df['add_assets'] = df['children'] * adult_ammount + df['adult'] * child_ammount




    #関数の実行
    asset_instance = asset()
    #家財の損害額を算出
    df['assets_damage_price'] = df.apply(lambda row: asset_instance.lost_assets(row['assets'], row['add_assets'], row['dmg_rate']), axis=1)




    #建物と家財の損害額
    df['total_lost'] = df['house_damage_price'] + df['assets_damage_price']






    damage_output_path = f'./dev/建物家財損害額/{pref}_lost.csv'
    df.to_csv(damage_output_path, index=False)
    pref += 1
    #1/29コミット