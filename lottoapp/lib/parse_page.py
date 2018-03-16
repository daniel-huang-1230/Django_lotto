import requests
import os,json, facebook
import pandas as pd
import lottoapp.lib.keyword_matching
from dateutil.parser import parse
import pytz

utc=pytz.UTC



# Parameters and credentials of your app
FACEBOOK_APP_ID     = '328993440930148'   #輕鬆買app id
FACEBOOK_APP_SECRET = '81d29b43f65f77c14db1e2286fec728f'
PAGE_ID = '320583254962571'
#PAGE_ID = '1794576900786201'


permenant_token = "EAAErN8EuGWQBAKlPFUzuV0mjhl0MhfvVBVnziV8P1QiVDbFNMZBdb3JSONSYMjI3ZCunLgDofk7nL2lm4PZCpLy6Ywc6ZBqEIVBIYguMRrLUrtZAiScZCZAn5QPYrUHtv3ZABdQZALqTI2w41ZCQXQWOTn8thHQZA5Tmg3jhhGT2cUrZCwZDZD"
graph = facebook.GraphAPI(access_token=permenant_token, version=2.7)
# 抓取粉專所有貼文時間、ID、內文、分享內容, 回傳a list (page_overview)
def getAllFeeds(page_id, my_token):
    res = requests.get('https://graph.facebook.com/v2.12/{}/posts?limit=100&access_token={}'.format(page_id, my_token))
    page_overview = []
    page = 1

    while 'paging' in res.json():
        print('正在爬取粉專第%d頁' % page)

        for post in res.json()['data']:

            # 透過貼文ID來抓取讚數與分享數

            res2 = requests.get(
                'https://graph.facebook.com/v2.12/{}?fields=likes.limit(0).summary(True), shares&access_token={}'.format(
                    post['id'], permenant_token))

            print(res2.json())
            if 'likes' in res2.json():
                likes = res2.json()['likes']['summary'].get('total_count')
            else:
                likes = 0

            if 'shares' in res2.json():
                shares = res2.json()['shares'].get('count')
            else:
                shares = 0

            page_overview.append([parse(post['created_time']),
                                  post['id'],
                                  post.get('message'),
                                  post.get('story'),
                                  likes,
                                  shares
                                  ])

        if 'next' in res.json()['paging']:
            res = requests.get(res.json()['paging']['next'])
            page += 1
        else:
            break
    return page_overview

#test 1
# df = pd.DataFrame(getAllFeeds(PAGE_ID, permenant_token))
# df.columns = ['貼文時間', '貼文ID', '貼文內容', '分享內容', '讚數', '分享數']
# df.to_csv('粉專資訊.csv', index=False)



# 取得單篇文章所有按讚用戶
# function returns a list of all users who have hit 'like' on this post
def getAllUserLikes(post_id, my_token):

    res_post = requests.get(
        'https://graph.facebook.com/v2.12/{}/likes?limit=100&access_token={}'.format(post_id,
                                                                                      my_token))
    users_who_liked = []
    try:
        if 'next' not in res_post.json()['paging']:
            for user in (res_post.json()['data']):
                users_who_liked.append(
                    [user['id'], user['name']])

        elif 'next' in res_post.json()['paging']:
            while 'paging' in res_post.json():
                for user in res_post.json()['data']:
                    users_who_liked.append(
                        [user['id'], user['name']])
                if 'next' in res_post.json()['paging']:
                    res_post = requests.get(res_post.json()['paging']['next'])
                else:
                    break
    except:
        users_who_liked.append(["none", "none"])

    return users_who_liked


# test 2
#print(getAllUserLikes("1794576900786201_2044509312459624", permenant_token))

#print("總共讚數: ", len(getAllUserLikes("1794576900786201_2044509312459624", permenant_token)))
# this function returns a list containing information in the comment section
def getCommentSection(post_id):
    comments_list = []
    res_post = requests.get(
        'https://graph.facebook.com/v2.12/{}/comments?limit=10&access_token={}'.format(post_id,
                                                                                     permenant_token))
    # 判斷留言數是否超過100，若超過則需要翻頁擷取；當沒有留言時，人名與ID皆為none
    #print(res_post.json())
    try:
        if 'next' not in res_post.json()['paging']:
            #print("不需翻頁")
            for comment in (res_post.json()['data']):
                comments_list.append(
                    [comment['id'], comment['from']['name'], comment['from']['id'], parse(comment['created_time']),
                     comment['message']])

        elif 'next' in res_post.json()['paging']:
            #print("翻頁")
            while 'data' in res_post.json():
                #print("這是res_post: ",res_post.json())
                for comment in res_post.json()['data']:

                    comments_list.append(
                        [comment['id'], comment['from']['name'],comment['from']['id'],parse(comment['created_time']),
                         comment['message']])
                if 'next' in res_post.json()['paging']:

                    res_post = requests.get(res_post.json()['paging']['next'])
                    #print("下一頁json", res_post.json())
                else:
                    break
    except:
        comments_list.append(["none", "none", "none", "none", "none"])

    return comments_list



#test 3
#print(getCommentSection("1794576900786201_2044509312459624"))
#print("留言:",(getCommentSection("1794576900786201_2044509312459624")))
#print(getCommentSection("1794576900786201_2044509312459624"))



#function generates response to a specific comment by user
def respondToUser(comment_id, response_message):
    graph.put_comment(object_id=comment_id, message=response_message )


#respondToUser("1964515103813307_1964586880472796", "Me too!")


# 爬取整個粉專   (not sure if useful)
def getAllLikesOnPage(page_id, my_token):
    page = 1
    likes_list = []
    res = requests.get("https://graph.facebook.com/v2.12/{}/posts?limit=100&access_token={}".format(page_id, my_token))
    while 'paging' in res.json():
        for post_index, information in enumerate(res.json()['data']):
            print('正在爬取第{}頁，第{}篇文章'.format(page, post_index + 1))

            # check if this is a post feed; if so, proceed to collect id of all users who 'liked' the page

            if 'message' in information:
                res_post = requests.get(
                    'https://graph.facebook.com/v2.12/{}/likes?limit=1000&access_token={}'.format(information['id'], permenant_token))

                # 判斷按讚人數是否超過1000人，若超過則需要翻頁擷取；當沒有人按讚時，按讚人名與ID皆為NO

                try:
                    if 'next' not in res_post.json()['paging']:
                        for likes in res_post.json()['data']:
                            likes_list.append(
                                [information['id'], information['message'], parse(information['created_time']).date(),
                                 likes['id'], likes['name']])
                    elif 'next' in res_post.json()['paging']:
                        while 'paging' in res_post.json():
                            for likes in res_post.json()['data']:
                                likes_list.append(
                                    [information['id'], information['message'], parse(information['created_time']).date(),
                                     likes['id'], likes['name']])
                            if 'next' in res_post.json()['paging']:
                                res_post = requests.get(res_post.json()['paging']['next'])
                            else:
                                break
                except:
                    likes_list.append(
                        [information['id'], information['message'], parse(information['created_time']).date(), "NO", "NO"])

        if 'next' in res.json()['paging']:
            res = requests.get(res.json()['paging']['next'])
            page += 1
        else:
            break

    print('爬取結束!')
    return likes_list

# test 4
# df = pd.DataFrame(getAllLikesOnPage(PAGE_ID,permenant_token), columns=['Post ID', 'Post Content', 'Created Time', '按讚ID', '按讚名字'])
# df.to_csv('按讚名單.csv', index=False)



