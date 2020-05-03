# class MBTI
#   MBTI data
class MBTI():
    def __init__(self):
        self.M = 0
        self.B = 0
        self.T = 0
        self.I = 0

    # get_MBTI
    # return MBTI value in tuple format
    def get_MBTI(self):
        return (self.M, self.B, self.T, self.I)


# class CHARACTER
#   data of character
# inheritance MBTI
# name - str
#   character's name
# sex - str
#   character's gender
class CHARACTER(MBTI):
    def __init__(self, name, sex):
        super().__init__()
        self.name = name
        self.sex = sex
