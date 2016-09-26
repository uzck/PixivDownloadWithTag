#-*- coding: UTF-8 -*-
from pixivpy3 import *
from PIL import Image

import os
import time
import threading
import json

base_path = "file_download_path"
api = PixivAPI()
api.login("username", "password")
files_list = []
downloadAPI = AppPixivAPI()
target_score = your_target_score
tags = ["tags you want to search"]
#     'Aqours', 'ラブライブ!サンシャイン!!', '津島善子']
#     '桜内梨子', '黒澤ルビィ', '松浦果南', '黒澤ダイヤ',
#     'はなまるびぃ', '国木田花丸', 'よしまる', '渡辺曜',
#     '小原鞠莉', '高海千歌', 'ちかりこ', 'ようちか',
#     'ようりこちか']
# tags = ['Aqours']

def IsValidImage(path):
    valid = True
    try:
        Image.open(path)
    except:
        valid = False
    return valid


def downloadSinglePic(url, api, current_path):
    file_name = os.path.basename(url)
    api = AppPixivAPI()
    if checkDuplicate(file_name):
        real_path = current_path + file_name
        try:
            api.download(url, path=real_path)
        except Exception as e:
            write_error_file_to_record(file_name)
        if IsValidImage(current_path + file_name):
            print("Download " + file_name + " Successfully!")
            write_to_record_file(file_name)
        # else:
        #     print("Download failed. Try again!")
        #     # downloadAPI(url)
        #     write_error_file_to_record(file_name)

def downloadMultiPic(url, api, current_path, page_count, tag):
    dir_name = os.path.basename(url)[:-7]
    path = current_path + dir_name + '/'
    os.system("mkdir " + path)
    for x in range(0, page_count + 1):
        real_url = url.replace('p0', 'p' + str(x))
        downloadSinglePic(real_url, api, path)
        time.sleep(2)


def downloadWithTag(tag, api):
    if not os.path.exists(base_path + tag):
        os.system('mkdir ' + tag)
    current_path = base_path + tag + '/'
    index = 1
    while index <= 100:
        result = api.search_works(tag, page=index, per_page=30, mode='tag', types=['illustration'])
        jsonString = json.dumps(result)
        is_get_data = jsonString.startswith("{\"response\"") or jsonString.startswith("{\"status\"") or jsonString.startswith("{\"pagination\"") or jsonString.startswith("{\"count\"")
        # print(jsonString)
        # print(is_get_data)
        # if is_get_data:
        if True:
            for illust in result.response:
                url = illust.image_urls.large
                if illust.page_count == 1:
                    if illust.stats.score > target_score and (not(u'R-18' in illust.tags)):
                        print(illust.stats.score)
                        t2 = threading.Thread(target=downloadSinglePic, args=(url, downloadAPI, current_path))
                        t2.start()
                        time.sleep(3)
                # else:
                #     t3 = threading.Thread(target=downloadMultiPic, args=(url, downloadAPI, current_path, illust.page_count, tag))
                #     t3.start()
        else:
            break
        index += 1


def mulitDownload(tags, api):
    for tag in tags:
        t1 = threading.Thread(target=downloadWithTag, args=(tag, api))
        t1.start()
        # print(tag)
        # time.sleep(300)


def checkDuplicate(file_name):
    if file_list == None:
        return False
    temp = file_name + "\n"
    already_have = False
    for item in file_list:
        if temp == item:
            already_have = True
    if already_have:
        print("Already have this " + file_name + " illustration")
        return False
    # print("this illustration " + file_name +  " is not in collection")
    return True


def write_to_record_file(file_name):
    with open(base_path + 'record', 'a') as record_file:
        record_file.write(file_name + "\n")


def read_record_file(file_name):
    files_list = []
    if os.path.exists(base_path + file_name):
        with open(base_path + 'record', 'r') as record_file:
            lines = record_file.readlines()
            for line in lines:
                files_list.append(line)
        return files_list
    else:
        os.system("touch " + base_path + file_name)

def write_error_file_to_record(file_name):
    with open(base_path + 'error_file', 'a') as error_file:
        error_file.write(file_name + "\n")


if __name__ == '__main__':
    file_list = read_record_file('record')
    mulitDownload(tags, api)
