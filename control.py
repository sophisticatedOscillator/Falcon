import sys
import requests
import subprocess
from datetime import datetime, timedelta
from pprint import pprint
from hurry.filesize import size, verbose


def calc_t2c(start_time,curr_time,dl,total_length):
    duration = curr_time-start_time
    return (duration / dl) * (total_length-dl)

def downloadVideo(video_path, band_name, angle):
    link = f"http://10.5.5.9:8080/videos/DCIM/100GOPRO/{video_path}"
    file_name = f"{band_name} - {angle}"
    print(link)
    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            start_time = datetime.now()
            for data in response.iter_content(chunk_size=4096):
                f.write(data)
                curr_time = datetime.now()
                dl += len(data)
                done = int(50 * dl / total_length)
                downloaded = size(dl,system=verbose)
                to_download = size((total_length-dl),system=verbose)
                total_size = size(total_length,system=verbose)
                sys.stdout.write("\r[%s%s] [%s/%s] %s left | %s" % ('=' * done, ' ' * (50-done), downloaded, total_size, to_download, "{0:.0%}".format(dl/total_length) ))
                sys.stdout.flush()

def getMedia():
    link = f"http://10.5.5.9:8080/gp/gpMediaList"
    r = requests.get(link)
    return r.json()


directories = getMedia()['media']
for directory in directories:
    for item in directory['fs']:
        fileName = item['n']
        t = datetime.now()
        downloadVideo(fileName,"Band 1","SL")
        c = datetime.now()
        print("\nThis took %s to download \n\n" % (c-t))
