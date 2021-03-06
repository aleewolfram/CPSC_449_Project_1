from locust import HttpLocust, TaskSet, task, between
import json, requests
from faker import Faker

fake = Faker()

# random list of community name
community_list = [
'danish','cheesecake','sugar',
'Lollipop','wafer','Gummies',
'sesame','Jelly','beans',
'pie','bar','Ice','oat' ]

# generate bogus data for posting microservice
title = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
description = fake.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None)
username = fake.user_name()
url = fake.image_url()
community_name = fake.word(ext_word_list=community_list)

# generate bogus data for voting microservice
voteID = fake.random_int(min=1, max=200, step=1)
voteID_json = {"vote_id":voteID}

postID = fake.random_int(min=1, max=200, step=1)
list_vote_ID = {"post_ids":[postID, postID]}

postAmount = fake.random_int(min=1, max=200, step=1)

# json data
dataPost = {"title":title,"description":description,"username":username,"community_name":community_name,"resource_url":url}
myheaders = {'Content-Type': 'application/json', 'Accept': 'application/json'}

class UserBehaviour(TaskSet):

    ## Posting
    @task(1)
    def post(self):
        self.client.post("/posts/create", json=dataPost, headers = myheaders)

    @task(2)
    def getPost(self):
        self.client.get("/posts/get?post_id=%d"%(postID))

    # @task(5)
    # def deletePost(self):
    #     self.client.delete("/delete?post_id=%d"%(postID))

    @task(2)
    def getNPostbyCommunity(self):
        self.client.get("/posts/filter?n=2&community_name=%s"%(community_name))

    @task(4)
    def getNPostbyAnyCommunnity(self):
        self.client.get("/posts/filter?n=%d"%(postAmount))

    ## Voting
    @task(4)
    def upvote(self):     
        self.client.post("/votes/upvotes", json=voteID_json, headers = myheaders)

    @task(2)
    def downvote(self):
        self.client.post("/votes/downvotes", json=voteID_json, headers = myheaders)

    @task(2)
    def getVotes(self):
        self.client.get("/votes/get?vote_id=%d"%(voteID))

    @task(4)
    def getTopScoringPost(self):
        self.client.get("/votes/getTop?n=%d"%(postAmount))
    
    @task(2) 
    def getListSortedByScore(self):
        self.client.post("/votes/getList", json= list_vote_ID, headers= myheaders)

 
class WebsiteUser(HttpLocust):

    task_set = UserBehaviour
    wait_time = between(2, 5)
