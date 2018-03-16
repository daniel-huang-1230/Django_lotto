import requests
from bs4 import BeautifulSoup
from string import punctuation



def getAllProducts(target_website_URL):
    # web scraping to extract all product names on the page

    #target_website_URL = "https://chatbot-site.herokuapp.com/blogs"
    r = requests.get(target_website_URL)

    c = r.content

    soup = BeautifulSoup(c, "html.parser")

    # the following line is temporary, since it does NOT adapt to different website
    all_headers = soup.find_all("a", {"class": "header"})

    products_list = []

    for element in all_headers:
        products_list.append(element.text)

    return products_list

# this method finds all possible product(s) matching the key word in the user comment
# this function is NOT case-sensitive
def findProducts(comment_message, products_list):
    comment_message = comment_message.lower()
    candidates = []
    for product_name in products_list:
        if product_name.lower() in comment_message:
            candidates.append(product_name)
    if len(candidates) == 1 :
        return candidates[0]
    else:
        return candidates   #return the list if there are more than one matched products


# print(getAllProducts())
#
# print(findProducts("fsfds s2000", getAllProducts()))

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

# the function that check if someone has tagged their friends in the comment ---> TODO : optimization of the logic
def find_tagged_users(comment_message, key_message):
    if key_message not in comment_message:
        print("The comment does not meet the criteria")
    else:
        comment_message.replace(key_message, "") #get rid of the keyword string
        if strip_punctuation(comment_message) == "":
            print("The user does not tag anyone")








