
from data_downloader import downloader, parse_urls

####################################################################################################
# Modify input and output file paths here
#########################

# Directory for file output
folder_out = r'D:\database download'
# File path containing URLs
url_file = r"xxx"
####################################################################################################
    
urls = parse_urls.from_urls_file(url_file)
downloader.download_datas(urls, folder_out)
# Using the browser method
# downloader.download_datas(urls, folder_out, authorize_from_browser=True)





    
