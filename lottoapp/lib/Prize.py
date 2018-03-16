class Prize:
    def __init__(self, winners_num, prize_name, item_name):
        self.winners_num = winners_num
        self.picture_URL = ""
        self.prize_name = prize_name
        self.item_name = item_name

    #圖片非必要
    def set_picture(self, img_URL):
        self.picture_URL = img_URL


