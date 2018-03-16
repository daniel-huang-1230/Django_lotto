from random import *
import datetime
import mysite.lottoapp.lib.parse_page as page
import pytz
import mysite.lottoapp.lib.auto_reply as response
import mysite.lottoapp.lib.Lottery as lotto
from pytz import timezone

# 觸發開獎 腳本, run by the web app 

#輕鬆買測試用
page_id = '320583254962571'
token = 'EAAErN8EuGWQBAISmKKQZAXZAkiZBbWCO42VZC2cg8EcLdZBwA3mMmoOCZCeUTB3nYVVT35zpNwBmlfmiu029KAWGsXVwZAZCBZCRUKbXeWCFYe' \
        'GxCqU3ECpKD4n1pZCZBlMBIf8WZB9BvJCZBWFEnAGw0hzTnpV5KzwWpzp4KQq1XHM1ySQZDZD'
post_id = page.getAllFeeds(page_id, token)[1][1]

print(page.getAllUserLikes(post_id, token))




post_id_with_comment = page.getAllFeeds(page_id, token)[0][1]  #需要留言那篇

users_who_commented = page.getCommentSection(post_id_with_comment)


print("留言者: ",users_who_commented)

users_who_liked = []
for like in page.getAllUserLikes(post_id_with_comment,token):
    user_id = like[0]
    users_who_liked.append(user_id)
print("有按讚的使用者: ",users_who_liked)

print("請設定抽獎截止時間: ")
utc = pytz.UTC

deadline = utc.localize(set_deadline())  #TODO 可以未來在新增選擇時區功能  拆分deadline from setting script

# qualified_participants_ids = []
# keyword = ""    #TODO 抓取keyword from setting script
# for user in users_who_commented :
#     # make sure there is no duplicates
#     username = user[1]
#     user_id = user[2]
#     comment_time = user[3]
#     comment_content = user[4]
#
#     if user_id in users_who_liked and user_id not in qualified_participants_ids and comment_time < deadline and comment_content.contains(keyword):
#         qualified_participants_ids.append(user_id)
#
# print("最終符合資格抽獎者:", qualified_participants_ids)

#automatically respond to all qualified users in the comment sections
i = 0
responded = {}   # a dictionary to keep track of the users that have received response already, in order to avoid responding to the same person
for users in users_who_commented:

    if users[1] in qualified_participants_ids and users[1] not in responded.keys():
        i += 1
        lotto_num = '{0:04}'.format(i)
        responded[users[1]] = lotto_num   # key : user name; value: lotto number
        msg = users[1] + "您好, 您的抽獎序號為" + lotto_num + "。 本抽獎將會在" + deadline.strftime("%Y/%m/%d %H:%M") + "自動開出。"
        page.respondToUser(users[0], msg)
    elif users[1] in responded.keys():
        msg = users[1] + ", 您好像留言過了哦! 您的抽獎序號是" + responded[users[1]] +"。"
        page.respondToUser(users[0], msg)


rules_2 = set_prize_dist(2)  # user inputs their rules for the prize   #TODO 拆分到setting script
winners = pick_the_winners(qualified_participants_ids, rules_2)

print(all_winners_ids)
for prize in range(len(winners)):
    print("第"+str(prize+1)+"獎得主: " + str(winners[prize]))
    for users in users_who_commented :
        if users[1] in winners[prize]:
            msg = users[1] + ",恭喜您抽中第" + str(prize + 1) + "獎! 請立即私訊與我們聯絡，進行贈獎相關作業。"
            page.respondToUser(users[0], msg)

for users in users_who_commented:
    if users[1] not in all_winners_flat:
        msg = "銘謝惠顧，以下是中獎清單，期待您下次中獎"
        page.respondToUser(users[0], msg)




