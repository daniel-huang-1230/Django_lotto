from datetime import datetime
from random import *
import lottoapp.lib.parse_page as page
import pytz
from pytz import timezone
import lottoapp.lib.Prize

class Lottery:

    def __init__(self, event_name, event_no, post_id, page_id, token):
        self.event_name = event_name
        self.event_no = event_no
        self.post_id = post_id
        self.page_id = page_id
        self.token = token
        self.deadline = None
        self.prizes = []  # list of Prize instances (objects)
        self.total_winners_num = 0  # this is the ACTUAL number of winners (could be less than the total count from all prizes)
        #self.prize_dist = []
        self.candidates_dict = {} #mapping : key = id; value = name
        self.winners_dict = {}   #mapping : key = id; value = name
        self.rules = {"keywords": [], "like": False, "share": False, "tag": False}    # "like", "share", "tag", etc #TODO 未來可擴充

        self.result_form_URL = ""  #TODO 不確定是否放這邊




    def toggle_rule(self, detect_rule):
        if detect_rule == "keywords": #keywords cannot be toggled
            return
        self.rules[detect_rule] = True

    def add_keyword(self, keyword):
        self.rules['keywords'].append(keyword)

    # def set_prize_dist(self,num_of_prizes):
    #     if num_of_prizes < 1:
    #         print("The number of prizes must be at least 1 !")
    #         return
    #     prize_dist = []
    #     total_winners = 0
    #     for i in range(num_of_prizes):
    #         num_of_winners = input("請輸入第" + str(i +1) + "獎名額: ")
    #         prize_name = input("請輸入第" + str(i +1) + "獎獎項名稱: ")
    #         prize_item = input("請輸入"+prize_name+"的獎品:")
    #         self.prizes[prize_name] = prize_item
    #         prize_dist.append(num_of_winners)
    #         total_winners += int(num_of_winners)
    #     self.winners_num = total_winners
    #     self.prize_dist = prize_dist

    def add_prize(self, prize):
        self.prizes.append(prize)





    # user shall set their own deadline for the lottery through the form
    def set_deadline(self, datetime_str):

        # post form 回傳的datetime_str : "03/15/2018 23:27"
        deadline = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M ')
        #print(type(deadline), deadline)
        self.deadline = deadline





    # method that find all qualified users
    def set_candidates(self):
        all_comment_entries = page.getCommentSection(self.post_id)  #all participants (preliminary)
        all_participants = {}  # key : id; value: name

        for entry in all_comment_entries:
            comment_time = entry[3]
            id = entry[2]
            name = entry[1]
            if comment_time < self.deadline:   # verify the comment time is earlier than the lottery deadline
                all_participants[id] = name

        # check for the rules

        if len(self.rules['keywords']) > 0:  #if criterion "keywords" is defined
            for entry in all_comment_entries:
                id = entry[2]
                content = entry[4]
                for keyword in self.rules['keywords']:
                    if keyword not in content:
                        del all_participants[id]  #someone doesn't meet the criteria


        if self.rules['like']:   #if criterion "like" is turned on
            users_who_liked = {}   # key : user id; value: user name
            for entry in page.getAllUserLikes(self.post_id, self.token):
                user_id = entry[0]
                user_name = entry[1]
                users_who_liked[user_id] = user_name

            for user_id in all_participants.keys():
                if user_id not in users_who_liked.keys():
                    del all_participants[user_id]   #someone doesn't meet the criteria

        #TODO figure out how to check for "tag" and "share"




    # pick the winner for EACH prize (argument prize : Prize object)
    def pick_the_winners(self, prize):
        # check if there are enough participants to enter the lottery
        # if len(candidates_ids) < self.prize.winners_num:
        #     print("You do not have enough participants to play the lottery")
        #     return
        #all_winners = {}

        winners_num = prize.winners_num

        while len(self.candidates_dict) > 0 and winners_num > 0:
            candidates_ids = self.candidates_dict.keys()
            candidates_names = self.candidates_dict.values()
            winner_idx = randint(1, len(candidates_ids)) - 1
            #all_winners[candidates_ids[winner_idx]] = candidates_names[winner_idx]
            self.winners_dict[candidates_ids[winner_idx]] = candidates_names[winner_idx] # add winner to the dict
            del self.candidates_dict[candidates_ids[winner_idx]]  # remove the user who has already won the prize from the candidates list
            winners_num -= 1
            self.total_winners_num += 1  # increment the total winners count for this lottery


        # for num_of_winners in prize:
        #     num_of_winners = int(num_of_winners)
        #     prize_winners = []
        #     while num_of_winners > 0:
        #         num_of_winners -= 1
        #         winner_idx = randint(1, len(candidates_ids)) - 1
        #         prize_winners.append(candidates_ids[winner_idx])
        #         del candidates_ids[winner_idx]   #remove the user who has already won the prize
        #     all_winners[ candidates_ids[winner_idx] ] = candidates_names[winner_idx]
        # self.winners_dict = all_winners


