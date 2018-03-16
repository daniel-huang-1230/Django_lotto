import facebook
from datetime import datetime, time
# 負責自動回覆的腳本

permenant_token = "EAAErN8EuGWQBAISmKKQZAXZAkiZBbWCO42VZC2cg8EcLdZBwA3mMmoOCZCeUTB3nYVVT35zpNwBmlfmiu029KAWGsXVwZAZCBZCRUKbXeWCFYeGxCqU3ECpKD4n1pZCZBlMBIf8WZB9BvJCZBWFEnAGw0hzTnpV5KzwWpzp4KQq1XHM1ySQZDZD"
graph = facebook.GraphAPI(access_token=permenant_token, version = 2.11)
#function generates response to a specific comment by user
def respondToUser(comment_id, response_message):
    graph.put_comment(object_id=comment_id, message=response_message )
    # 回傳回覆時間   用於開獎表單
    return datetime.now()



#methods for deleting stuff, cleaning up the page
def deletePost(post_id):
    graph.delete_object(id='post_id')


def deleteAllPosts(page_id):
    res_post = graph.get_object(id= page_id, fields="feed")
    for post in res_post['feed']['data']:
        #print(post['id'])
        deletePost(post['id'])



def deleteAllComments(post_id):

    response = graph.get_connections(id=post_id, connection_name='comments')
    for comment in response['data']:
        #print(comment['id'])
        graph.delete_object(comment['id'])
