import bldg
import asset



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame



print('�J�n����s���{���R�[�h����͂��Ă�������')
start_pref = input()
print(f'�J�n����s���{���R�[�h : {start_pref}')

print('�I������s���{���R�[�h����͂��Ă�������')
finish_pref = input()
print(f'�I������s���{���R�[ : {finish_pref}')

#�Ƒ��̎q���Ƒ�l�̍\���l�����擾���邽�߂ɃJ��������ёւ�
columns = ['tatemon_id', 'x', 'y', 'floor', 'AREA', 'atype2', 'total_area',
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
           ' T50_P39_SI', 'assets', 'families']


%cd "G:/�}�C�h���C�u/akiyamalab/���_/���S�����W��"
pref = int(start_pref)
while pref <= int(finish_pref):
    damage_path = f'./data/mpc/{pref}.csv'
    df = pd.read_csv(damage_path)
    df = df[columns]




############################
       #�����̑��Q�z
############################
    dmg_price_list = []

    #�H����p
    df['cost'] = np.where(df['estimated_structure'] == 0, cost_df['wood'][pref] * 1000, cost_df['steel'][pref] * 1000)
    #���p��
    df['dpc_rate'] = np.where(df['estimated_structure'] == 0, 0.031, 0.036)
    #�z�N��
    df['age'] = df['estimated_age'].map({1: 5, 2: 8, 3: 15.5, 4: 25.5, 5: 35.5, 6: 45.5, 7: 50})
    
    df['dmg_rate'] = np.where((df['A31_001'] == 11) | (df['A31_001'] == 21), np.where(df['floor'] == 0, 0.4, 0.35),
                          np.where((df['A31_001'] == 12) | (df['A31_001'] == 22), np.where(df['floor'] == 0, 0.6, 0.45),
                          np.where((df['A31_001'] == 13) | (df['A31_001'] == 23), np.where(df['floor'] == 0, 0.75, 0.5),
                          np.where(((df['A31_001'].between(14, 15)) | (df['A31_001'] >= 24)), np.where(df['floor'] == 0, 0.8, 0.55), 0.0))))
    
    
    
    #�֐��̎��s
    
    #�������p�Ȃ��̏Z��̉��l
    df['house_price'] = df.apply(lambda row: house_price(row['cost'], row['total_area']), axis=1)
    
    
    #�����̑��Q�z�̌v�Z
    df['house_damage_price'] = df.apply(lambda row: dmg_value(row['cost'], row['total_area'], row['dpc_rate'], row['age'], row['dmg_rate']), axis=1)






############################
       #�ƍ��̑��Q�z
############################
    #�Ƒ��\���ʉƍ��]���z���Z�o
    df['assets'] = np.where(
        df['spouse_sex'] == 0, 3000000,
        np.where(
            df['household_age'] <= 29, 5000000,
            np.where(
                (df['household_age'] >= 30) & (df['household_age'] <= 39), 8000000,
                np.where(
                    (df['household_age'] >= 40) & (df['household_age'] <= 49), 11000000,
                    np.where(df['household_age'] >= 50, 11500000, 0)  # �Ō�̏����ƃf�t�H���g�l
                )
            )
        )
    )
    
    
    #�Ƒ��̍\���l�����Z�o
    # DataFrame����NumPy�z��ɕϊ�
    data_children = df.iloc[:, 15:22].to_numpy()
    data_adult = df.iloc[:, 23:59].to_numpy()

    # �e�s��NumPy�z��̍��v���v�Z
    df['children'] = np.sum(data_children, axis=1)
    df['data_adult'] = np.sum(data_adult, axis=1)

    adult_ammount = 1300000
    child_ammount = 800000
    df['add_assets'] = df['children'] * adult_ammount + df['adult'] * child_ammount




    #�֐��̎��s
    
    #�ƍ��̑��Q�z���Z�o
    df['assets_damage_price'] = df.apply(lambda row: lost_assets(row['assets'], row['add_assets'], row['dmg_rate']), axis=1)











damage_output_path = f'./dev/�����ƍ����Q�z/{pref}_lost.csv'
df.to_csv(damage_output_path, index=False)
pref += 1


G:\�}�C�h���C�u\akiyamalab\���_\���S�����W��\code\���Q�z\�����E�ƍ��̑��Q�z�̎Z�o.py