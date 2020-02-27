import urllib.request

username = 'lastig-guest-public'
password = 'iew1xux8Sang6ieH'

url1 = f'ftp://{username}:{password}@ftp3.ign.fr/S2-2017-T31TFM-PixelPatch.7z'
url2 = f'ftp://{username}:{password}@ftp3.ign.fr/S2-2017-T31TFM-PixelSet.7z'

filename1 = '/raid/users/ebarnett/S2-2017-T31TFM-PixelPatch.7z'
filename2 = '/raid/users/ebarnett/S2-2017-T31TFM-PixelSet.7z'

urllib.request.urlretrieve(url1, filename1)
urllib.request.urlretrieve(url2, filename2)
