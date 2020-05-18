import os
import requests

def downloadImg(keyword, binary_list, link_list):
    
    os.makedirs(f'images/download_google/{keyword}', exist_ok=True)
    
    for i, binary in enumerate(binary_list):
        with open(f'images/download_google/{keyword}/{i}.jpg', 'wb') as f:
            f.write(binary)
    
    for i, link in enumerate(link_list):
        res = requests.get(link)
        with open(f'images/download_google/{keyword}/{i}-1.jpg', 'wb') as f:
            f.write(res.content)