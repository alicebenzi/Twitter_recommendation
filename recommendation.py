__author__ = 'alicebenziger'
import pandas as pd
import math
from collections import Counter
import csv

def top_match(newuser_advertiser_list, users_dictionary):
    """

    :param newuser_advertiser_list: list of advertiser a new user is following
    :param users_dictionary: a dictionary containing user ids and the advertisers being followed by each user
    :return: returns the user id of the most similar user
    """
    similarity = dict()
    for user_id in users_dictionary:
        currentuser_advertiser_list = users_dictionary[user_id]
        similarity[user_id] = cosine_similarity(Counter(currentuser_advertiser_list),Counter(newuser_advertiser_list))
    maxx_similarity = max(similarity.values())
    most_similar_user = [x for x , y in similarity.items() if y ==maxx_similarity]
    return most_similar_user

def cosine_similarity(c1, c2):
    """

    :param c1: counter 1
    :param c2: counter 2
    :return: compares two counters and returns the cosine similarity between the two counters
    """
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def recommend(list1, list2):
    """

    :param list1:
    :param list2:
    :return: compares list1 and list2 and returns an element from list2 that is not in list1. if there are no such
     elements, returns one element from list 2 itself
    """

    compare = [x for x in list2 if x not in list1]
    if len(compare) != 0:
        return compare[0]
    else:
        return list2[0]

if __name__ == '__main__':
    data = pd.read_csv("recommendation_coding/users.csv")
    test = pd.read_csv("recommendation_coding/test.csv")
    advertiser_data = pd.read_csv("recommendation_coding/advertisers.csv")
    current_users = dict()
    for user_id, advertiser_id in zip(data.ix[:,0],data.ix[:,1]):
        if user_id not in current_users:
            current_users[user_id] = [advertiser_id]
        else:
            current_users[user_id].append(advertiser_id)

    new_user = dict()
    for user_id, advertiser_id in zip(test.ix[:,0],test.ix[:,1]):
        if user_id not in new_user:
            new_user[user_id] = [advertiser_id]
        else:
            new_user[user_id].append(advertiser_id)

    advertisers = dict()
    for adv_id, adv_name in zip(advertiser_data.ix[:,0],advertiser_data.ix[:,1]):
        if adv_id not in advertisers:
            advertisers[adv_id] = adv_name

    recommended = dict()
    for user in new_user:
        most_similar = top_match(new_user[user], current_users)
        # there could be multiple similar users
        # for simplicity I am considering only one of them
        recommended[user] = recommend(new_user[user], current_users[most_similar[0]])

writer = csv.writer(open('recommendation.csv','wb'))

header = ["user_id", "advertiser_id","username"]
writer.writerow(header)
for key, value in recommended.iteritems():
    ln = [key, value, advertisers[value]]
    writer.writerow(ln)

