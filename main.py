import math
import random

from typing import List


class Player:
    id = 0
    skill = 0
    rating = 0

    def __init__(self, index, skill):
        self.id = index
        self.skill = skill
        self.rating = 1000

    def add_rating(self, rating):
        self.rating = rating


def run():
    player_list: List[Player] = init_players()
    players_file = open("players.csv", mode="w")
    games_file = open("games.csv", mode="w")
    players_file.write("round,id,skill,rating,rank\n")
    games_file.write("round,p1,p2,prob_p1_win_skill,prob_p1_win_rating,p1_score,p2_score\n")
    for i in range(100000):
        p1, p2 = get_two_random_players(player_list)
        prob_p1_win_skill = get_probability_skill(p1, p2)
        prob_p1_win_rating = get_probability_rating(p1, p2)
        p1_score, p2_score = get_result(prob_p1_win_skill)
        rating_delta = get_rating_delta(prob_p1_win_rating, p1_score, p2_score)
        p1.rating += rating_delta
        p2.rating -= rating_delta
        games_file.write("%d,%d,%d,%f,%f,%d,%d\n" % (i, p1.id, p2.id, prob_p1_win_skill, prob_p1_win_rating, p1_score,
                                                     p2_score))
        player_list.sort(key=lambda x: x.rating)
        for j in range(len(player_list)):
            p = player_list[j]
            players_file.write("%d,%d,%d,%d,%d\n" % (i, p.id, p.skill, p.rating, j))
        if i % 1000 == 0:
            print(i)


def init_players():
    player_list = []

    for i in range(201):
        list.append(player_list, Player(i, 800 + i * 2))
    return player_list


def get_two_random_players(player_list: List[Player]):
    number_of_players = len(player_list)
    p1_idx = random.randrange(0, number_of_players)
    p2_idx = p1_idx
    while p1_idx == p2_idx:
        p2_idx = random.randrange(0, number_of_players)
    return player_list[p1_idx], player_list[p2_idx]


def get_four_random_players(player_list: List[Player]):
    number_of_players = len(player_list)
    p1_idx = random.randrange(0, number_of_players)
    p2_idx = p1_idx
    while p1_idx == p2_idx:
        p2_idx = random.randrange(0, number_of_players)
    p3_idx = p1_idx
    while p3_idx == p1_idx or p3_idx == p2_idx:
        p3_idx = random.randrange(0, number_of_players)
    p4_idx = p1_idx
    while p4_idx == p1_idx or p4_idx == p2_idx or p4_idx == p3_idx:
        p4_idx = random.randrange(0, number_of_players)
    return player_list[p1_idx], player_list[p2_idx], player_list[p3_idx], player_list[p4_idx]


# Get the probability that Player p1 will win over Player p2 based on skill
def get_probability_skill(p1: Player, p2: Player):
    p1_trans = math.pow(10, p1.skill / 400)
    p2_trans = math.pow(10, p2.skill / 400)
    return p1_trans / (p1_trans + p2_trans)


# Get the probability that Player p1 will win over Player p2 based on rating
def get_probability_rating(p1: Player, p2: Player):
    p1_trans = math.pow(10, p1.rating / 400)
    p2_trans = math.pow(10, p2.rating / 400)
    return p1_trans / (p1_trans + p2_trans)


# Get the result of a game stopping when the first player reaches 10,
# using the given probability that the first player wins
def get_result(prob_p1_win: float):
    p1_score = 0
    p2_score = 0
    while p1_score < 10 and p2_score < 10:
        rand = random.random()
        if rand < prob_p1_win:
            p1_score += 1
        else:
            p2_score += 1
    return p1_score, p2_score


def get_rating_delta(prob_p1_win: float, p1_score: int, p2_score: int):
    p1_win_ratio = p1_score / (p1_score + p2_score)
    k = 32
    return k * (p1_win_ratio - prob_p1_win)


if __name__ == '__main__':
    run()
