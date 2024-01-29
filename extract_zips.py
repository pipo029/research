# -*- coding: utf-8 -*-

import os
import urllib.request
import zipfile

class FloodDataDownloader:
    def __init__(self, base_url, save_dir, extract_dir):
        self.base_url = base_url
        self.save_dir = save_dir
        self.extract_dir = extract_dir
        self.disable_mesh1_list = []

    
    
    def download_data(self):
        #URLの形式�?�手で変更する�?要がある?�?
        url_list = [self.base_url + f'{code:02}' + "_GML.zip" for code in range(1, 48)]
        
        for i, url in enumerate(url_list):
            destfile = os.path.join(self.save_dir, f'flood_polygon_{i+1}.zip')
            
            try:
                print(f"Downloaded {url} to {destfile}")
            except Exception as e:
                print(f"{url} did not work out due to {e}")
                self.disable_mesh1_list.append(url)
    
    
    
    def extract_zips(self):
        ziplist = [os.path.join(self.save_dir, f) for f in os.listdir(self.save_dir) if f.endswith('.zip')]
        
        for i, zip_path in enumerate(ziplist):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                extract_path = os.path.join(self.extract_dir, f'{i+1}')
                # zip_ref.extractall(extract_path)
                print(f"Extracted {zip_path} to {extract_path}")






# 使用�?
base_url = "https://nlftp.mlit.go.jp/ksj/gml/data/A31/A31-12/A31-12_"
save_dir = "G:/マイドライ�?/akiyamalab/卒�?/�?�?�?総集編/data/flood_polygon/H24_flood_polygon_zip"
extract_dir = 'G:/マイドライ�?/akiyamalab/卒�?/�?�?�?総集編/data/flood_polygon/H24_flood_polygon/'

downloader = FloodDataDownloader(base_url, save_dir, extract_dir)
downloader.download_data()
downloader.extract_zips()