#!/usr/bin/env python3
"""
Created on Thu Feb 27 13:49:03 2020

@author: Chengyan Fan
"""
from data_downloader import downloader, parse_urls

####################################################################################################
# Modify input and output file paths here
#########################

# Directory for file output
folder_out = r'D:\database-NPP'
# File path containing URLs
url_file = r"D:\大小桥接0328\GOGO battery or 碳酸盐风化\GOGO\Evergything for ERW\ERW work\Code\link-npp.txt"
####################################################################################################
    
urls = parse_urls.from_urls_file(url_file)
downloader.download_datas(urls, folder_out)
# Using the browser method
# downloader.download_datas(urls, folder_out, authorize_from_browser=True)
