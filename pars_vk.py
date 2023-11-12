from bs4 import BeautifulSoup
import requests
import vk_api
from datetime import datetime
import wget
import re
import os
import json


def create_directory(id,group_id,typ):
        try:
            os.mkdir('all_people/id'+str(id))
        except Exception as ex:
            pass
        try:
            os.mkdir('all_people/id'+str(id)+'/public'+group_id[1:])
        except Exception as ex:
            pass
        try:
            os.mkdir('all_people/id'+str(id)+'/public'+group_id[1:]+'/'+typ)
        except Exception as ex:
            pass    

def all_thread_comments(group_id,post_id,comment_id):
    if items['thread']['count']>0:
        thread_items = vk.wall.getComments(owner_id=group_id, post_id=post_id, comment_id=comment_id)
        for item in thread_items['items']:
            if str(items['from_id'])=='0':
                all_thread_comments(group_id,post_id,item['id'])
                continue
            item_id = str(item['from_id'])
            if '-' in item_id:
                item_id = 'ADMIN'+item_id
            create_directory(item_id,group_id,'comments')
            #Добавляем коммент в .json + .txt
            try:
                with open('all_people/id'+item_id+'/public'+group_id[1:]+'/comments/all_json.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as ex:
                # Если файла нет, создаем пустой список
                data = []
            data.append(item)
            with open('all_people/id'+item_id+'/public'+group_id[1:]+'/comments/all_json.json','w',encoding='utf-8') as f:
                json.dump(data, f,ensure_ascii=False)
            # Добавить в .txt:
            with open('all_people/id'+item_id+'/public'+group_id[1:]+'/comments/all_comments.txt','a',encoding='utf-8') as f:
              res_st = 'id_post='+str(post_id)+' id_comment='+str(item['id'])+' date='+str(datetime.fromtimestamp(item['date']))+'\n'
              res_st += item['text']+'\n>\n'
              f.write(res_st)
            all_thread_comments(group_id,post_id,item['id'])
           # print(item)
            


access_token=''  # input YOUR ACCESS TOKEN
vk_session = vk_api.VkApi(token=access_token)
print(vk_session)
vk = vk_session.get_api()

# ID группы, чью стену вы хотите спарсить
group_id = '-' # YOUR GROUP ID



#---------------------------------------
# Определить общее кол-во записей.

response = vk.wall.get(owner_id=group_id, count=0)

count = 1#response['count']-1

sdvig2 = 
sdvig = response['count']-2#11000  # 11000
offset = sdvig
#offset = response['count'] - count
print("Total wall posts count:", response['count'])
# 30917
#-----------------------------------------



# offset - пропустить столько записей.
wall = []
# общее кол-во сколько постов получить:
all_need = 3
while True:
    response = vk.wall.get(owner_id=group_id, count=count, offset=offset)
   # print(response)
   # print('===========================================')
    print(all_need+sdvig,offset)
    if response['items'] and offset<=all_need+sdvig:
        wall.extend(response['items'])
        offset += count
    else:
        break
    #wall += response['items']
    print(count,offset)
print('Количество полученных постов:', len(wall))

print(wall)
exit()
pattern = r"^photo_.+"

if os.path.exists('all_people'):
    pass
else:
   os.mkdir('all_people')





# проверка всех постов
for post in wall:
    #print(post)
    print(datetime.fromtimestamp(post['date']))
    comments = vk.wall.getComments(owner_id=group_id, post_id=post['id'])
    # Обработка комментов
    
    for items in comments['items']:
        if str(items['from_id'])=='0':
            all_thread_comments(group_id,post['id'],items['id'])
            continue
        item_id = str(items['from_id'])
        if '-' in item_id:
                item_id = 'ADMIN'+item_id
        create_directory(item_id,group_id,'comments')
        #print(items,items['from_id'],items['text'])
        try:
            with open('all_people/id'+item_id+'/public'+group_id[1:]+'/comments/all_json.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as ex:
            # Если файла нет, создаем пустой список
            data = []
        data.append(items)
        with open('all_people/id'+item_id+'/public'+group_id[1:]+'/comments/all_json.json','w',encoding='utf-8') as f:
            json.dump(data, f,ensure_ascii=False)
        with open('all_people/id'+item_id+'/public'+group_id[1:]+'/comments/all_comments.txt','a',encoding='utf-8') as f:
              res_st = 'id_post='+str(items['post_id'])+' id_comment='+str(items['id'])+' date='+str(datetime.fromtimestamp(items['date']))+'\n'
              res_st += items['text']+'\n>\n'
              f.write(res_st)
        all_thread_comments(group_id,items['post_id'],items['id'])

    
    if 'signer_id' in post:
        create_directory(post['signer_id'],group_id,'posts')
        print('SIGNER ID=',post['signer_id'])  
        try:
            with open('all_people/id'+str(post['signer_id'])+'/public'+group_id[1:]+'/posts/all_json.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as ex:
            # Если файла нет, создаем пустой список
            data = []
        data.append(post)
        with open('all_people/id'+str(post['signer_id'])+'/public'+group_id[1:]+'/posts/all_json.json','w',encoding='utf-8') as f:
            json.dump(data, f,ensure_ascii=False)    
        with open('all_people/id'+str(post['signer_id'])+'/public'+group_id[1:]+'/posts/all_posts.txt','a',encoding='utf-8') as f:
              res_st = 'id_post='+str(post['id'])+' date='+str(datetime.fromtimestamp(post['date']))+'\n'
              res_st += post['text']+'\n>\n'
              f.write(res_st)     
    else:
        print('ANONIM')
   
    # видео и фото пока не парсим.
    '''
    if 'attachments' in post:
        for i in post['attachments']:
            if 'video' in i:
                keys= i['video'].keys()
                for s in keys:
                    if re.match(pattern, s):
                       photo_url = post['attachments'][0]['video'][s]
                       my_name = photo_url.split('.')[-2].replace('/','-')+'.'+photo_url.split('.')[-1].replace('/','-')
                       print('Загрузка фото',my_name)
                       try:
                           pass
                          # wget.download(photo_url,my_name)
                       except Exception as ex:
                           print('Не удалось загрузить фото', my_name)
                if i['type']=='video':
                    video_id = i['video']['id']
                    video_url = f'https://vk.com/video{group_id}_{video_id}'
                    video_filename = i['video']['title']+'.mp4'
                    print('Загрузка видео-----',video_filename,video_url)
                    try:
                        pass
                        #wget.download(video_url, video_filename)
                    except Exception as ex:
                        print('Не удалось загрузить видео',video_filename)
    '''

