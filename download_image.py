import json
import sys
import requests
import re
import os


def read_credentials():
    with open('auth_credentials', 'r') as credentials:
        return tuple(credentials.read().split(","))


def get_granule(link):
    response = requests.get(link, auth=read_credentials())
    print(link)
    if response.status_code == 200:
        return response.json()['d']['results'][0]['__metadata']['uri']
    else:
        print(OSError)


TILE_NUMBER = 'T35UPT'

with open('search_result', 'r') as search_result:
    sendata = json.load(search_result)

file_status = list()

for item in sendata['feed']['entry']:
    PRODUCT_NAME = item['title']
    UUID = item['id']
    URL_CHECK_ONLINE = "https://scihub.copernicus.eu/dhus/odata/v1/Products('{}')/Online/$value".format(UUID)
    URL_REQUEST_RESTORE = "https://scihub.copernicus.eu/dhus/odata/v1/Products('{}')/$value".format(UUID)
    if re.search(TILE_NUMBER, PRODUCT_NAME):
        response_api = requests.get(URL_CHECK_ONLINE, auth=read_credentials())
        if response_api.text == 'false':
            file_status.append(response_api.text)
            requests.get(URL_REQUEST_RESTORE, auth=read_credentials())
            print("Restore " + URL_REQUEST_RESTORE)

print("Count offline satellite images: {}".format(len(file_status)))

if len(file_status) == 0:
    for item in sendata['feed']['entry']:
        PRODUCT_NAME = item['title']
        UUID = item['id']
        URL_PREVIEW = item['link'][2]['href']
        ORBIT_NUMBER = item['int'][1]['content']
        STRIP_DATA = item['str'][16]['content']
        GET_GRANULE = "https://scihub.copernicus.eu/dhus/odata/v1/Products('{0}')/Nodes('{1}.SAFE')/Nodes(" \
                      "'GRANULE')/Nodes?$format=json".format(UUID, PRODUCT_NAME)
        SENSING_DATE = PRODUCT_NAME[11:26]

        if re.search(TILE_NUMBER, PRODUCT_NAME):
            granule = get_granule(GET_GRANULE)
            URL_RCI = "{0}/Nodes('IMG_DATA')/Nodes('R10m')/Nodes('{1}_{2}_TCI_10m.jp2')/$value".format(
                granule, TILE_NUMBER, SENSING_DATE)

            try:
                os.makedirs('downloaded_img/', exist_ok=True)
            except OSError as error:
                print(error)

            try:
                response_api = requests.get(URL_RCI, auth=read_credentials(), stream=True)
                if not os.path.exists('downloaded_img/{0}_TCI_10m.jp2'.format(PRODUCT_NAME)):
                    with open('downloaded_img/{0}_TCI_10m.jp2'.format(PRODUCT_NAME), 'wb') as f:
                        print("\nDownloading {}".format(PRODUCT_NAME))
                        total_length = response_api.headers.get('content-length')
                        if total_length is None:
                            f.write(response_api.content)
                        else:
                            dl = 0
                            total_length = int(total_length)
                            for data in response_api.iter_content(chunk_size=4096):
                                dl += len(data)
                                f.write(data)
                                done = int(50 * dl / total_length)
                                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                                sys.stdout.flush()
            except OSError as error:
                print(error)
