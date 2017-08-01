# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
import json
import random

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
# </standard imports>

author = 'Curtis Kephart'

doc = """
An implementation of Kiyotaki and Wright's money search in the lab. 
We use (most) of Duffy (1998) design. 
Six players to ensure pairwise matching of three player types. 
Holding costs may be framed as rates of return instead of holding costs. 
"""

def check_and_ok(user_total, reference_ints):
    ok = (user_total == sum(reference_ints))
    return ok

class Constants(BaseConstants):
    name_in_url = 'task'
    players_per_group = 6
    num_rounds = 25
    colors = [  'red','blue','lavender','fuchsia','steelblue','teal','green','brown','black','pink','maroon',
                'yellow','lime','teal','navy','purple','orange','gold']
    animals = ['cat','banana slug','falcon','camel','bear','turtle','wombat']

class Subsession(BaseSubsession):

    def before_session_starts(self):

        self.group_randomly(fixed_id_in_group=True)

        cnt = 0
        for p in self.get_players():

            p.player_type = ((p.id_in_group) - (3*(((p.id_in_group)-1) // 3)))
            p.player_code_color = Constants.colors[cnt%10]
            cnt=cnt+1

            if p.round_number == 1:
                p.inventory = (p.id_in_group % 3) + 1
                p.prod = True
                p.round_cost_holding = 0 #just first round

                if 'endow' in self.session.config:
                    p.score = self.session.config['endow']
                else: 
                    p.score = 100
                
    

class Group(BaseGroup):

    def set_pairwise_matches(self):

        #within a group, set pairwise matching
        matching = [1,2,3,4,5,6]
        random.shuffle(matching)
        g1 = [matching[0], matching[1]]
        g2 = [matching[2], matching[3]]
        g3 = [matching[4], matching[5]]

        for p in self.get_players():

            # role = (p.id_in_group - (3*((p.id_in_group-1) // 3))) 

            if p.id_in_group in g1:
                group = 'g1'
            elif p.id_in_group in g2:
                group = 'g2'
            elif p.id_in_group in g3:
                group = 'g3'
            else: 
                group = []

            if eval(group)[0] == p.id_in_group:
                counterparty = eval(group)[1]
                p_ = 1
            else: 
                counterparty = eval(group)[0]
                p_ = 2

            cp_inv = self.get_player_by_id(counterparty).inventory

            p.participant.vars['pairwise_matchings'] = {
                'consume_type':((p.id_in_group) - (3*(((p.id_in_group)-1) // 3))),
                'produce_type':((p.id_in_group+1) - (3*(((p.id_in_group+1)-1) // 3))),
                'inv':p.inventory,
                'g1':g1,
                'g2':g2,
                'g3':g3,
                'group':group,
                'cp_id':counterparty,
                'cp_GoodInInv':cp_inv,
                'cp_consume_type':((counterparty) - (3*(((counterparty)-1) // 3))),
                'cp_produce_type':((counterparty+1) - (3*(((counterparty+1)-1) // 3))),
                }

    def set_holding_costs(self):
        for p in self.get_players():
            p.round_cost_holding = self.session.config['c'][p.inventory-1]
            p.score = p.score - p.round_cost_holding


    def specEq_trade_test(self, T1, Inv1, T2, Inv2):
        if T1 == 1 and Inv1 == 2 and T2 == 2 and Inv2 == 1:
            result = True
        elif T1 == 2 and Inv1 == 3 and T2 == 3 and Inv2 == 1:
            result = True
        elif T1 == 2 and Inv1 == 1 and T2 == 1 and Inv2 == 2:
            result = True
        elif T1 == 3 and Inv1 == 1 and T2 == 2 and Inv2 == 3:
            result = True

        elif T1 == 3 and Inv1 == 1 and T2 == 1 and Inv2 == 3:
            result = True
        elif T1 == 1 and Inv1 == 3 and T2 == 3 and Inv2 == 1:
            result = True

        elif T1 == 1 and Inv1 == 2 and T2 == 2 and Inv2 == 3:
            result = True
        elif T1 == 2 and Inv1 == 3 and T2 == 1 and Inv2 == 2:
            result = True

        else:
            result = False

        return result

    def fundEq_trade_test(self, T1, Inv1, T2, Inv2):
        if T1 == 1 and Inv1 == 2 and T2 == 2 and Inv2 == 1:
            result = True
        elif T1 == 2 and Inv1 == 3 and T2 == 3 and Inv2 == 1:
            result = True
        elif T1 == 2 and Inv1 == 1 and T2 == 1 and Inv2 == 2:
            result = True
        elif T1 == 3 and Inv1 == 1 and T2 == 2 and Inv2 == 3:
            result = True
        else:
            result = False

        return result
 
    def log_trade(self, P1_id, P2_id):

        P1 = self.get_player_by_id(P1_id)
        P2 = self.get_player_by_id(P2_id)
        P1.match_player = int(P2_id)
        P2.match_player = int(P1_id)
        P1.match_player_type = P2.player_type
        P2.match_player_type = P1.player_type

        if P1.trade and P2.trade:
            P1.trade_offer = P2.trade_offer = "Accepted"

            # Trade
            P2.inventory_nextPeriod = P1.inventory
            P1.inventory_nextPeriod = P2.inventory

            # Log fundamental and speculative trades
            P1.spec_eqTrade = self.specEq_trade_test(P1.player_type, P1.inventory, P2.player_type, P2.inventory)
            P2.spec_eqTrade = self.specEq_trade_test(P2.player_type, P2.inventory, P1.player_type, P1.inventory)
            P1.fund_eqTrade = self.fundEq_trade_test(P1.player_type, P1.inventory, P2.player_type, P2.inventory)
            P2.fund_eqTrade = self.fundEq_trade_test(P2.player_type, P2.inventory, P1.player_type, P1.inventory)


        elif P1.trade == False or P2.trade == False:
            P1.trade_offer = P2.trade_offer = "Not Accepted, No Trade"
            P2.inventory_nextPeriod = P2.inventory
            P1.inventory_nextPeriod = P1.inventory

        else: P1.trade_offer = P2.trade_offer = "Other"

    def set_round_payoff(self):

        # log trades
        # note inventory change
        # log consumption
        # ensure points are updated

        grouping = self.get_player_by_id(1).participant.vars['pairwise_matchings']
        self.log_trade(grouping['g1'][0], grouping['g1'][1])
        self.log_trade(grouping['g2'][0], grouping['g2'][1])
        self.log_trade(grouping['g3'][0], grouping['g3'][1])

        # consumption
        for p in self.get_players():
            if p.inventory_nextPeriod == p.player_type:
                p.consume = True
                p.score = p.score + self.session.config['u']
            else:
                p.consume = False

    def setup_new_period(self):

        for p in self.get_players():

            #production and storage costs
            if p.in_round(self.round_number-1).consume:
                p.round_cost_holding = 0
                p.inventory = (p.id_in_group % 3) + 1
                p.prod = True
            else: 
                p.inventory = p.in_round(self.round_number-1).inventory_nextPeriod
                p.prod = False
                p.round_cost_holding = (self.session.config['c'][int(p.inventory)-1])

            p.score = p.in_round(self.round_number-1).score - p.round_cost_holding

            



class Player(BasePlayer):

    def role(self):
        if self.id_in_group == 1 or self.id_in_group == 4:
            return 1
        elif self.id_in_group == 2 or self.id_in_group == 5:
            return 2
        elif self.id_in_group == 3 or self.id_in_group == 6:
            return 3

    player_type = models.IntegerField(
        doc='''player role''')

    match_player = models.IntegerField(
        doc='''match with which person?''')

    match_player_type = models.IntegerField(
        doc='''match with which person?''')

    prod = models.BooleanField(
        doc = '''produce item this round?''')

    round_cost_holding = models.FloatField(
        doc='''cold to hold''')

    score = models.FloatField(
        doc="player's score")

    inventory = models.IntegerField(
        doc="player's inventory contents")
    inventory_nextPeriod = models.IntegerField(
        doc="player's inventory contents next period")

    trade = models.BooleanField(
        doc='''User input, accept or reject the offer''')

    trade_offer = models.CharField(
        doc='''Did you offer to accept? Reject? or not have the option to trade?''')

    spec_eqTrade = models.BooleanField(
        doc='''was this a speculative equilibrium trade?''')

    fund_eqTrade = models.BooleanField(
        doc='''was this a fundamental equilibrium trade?''')

    other_eqTrade = models.BooleanField(
        doc='''was this a speculative equilibrium trade?''')



    consume = models.BooleanField(
        doc='''consumer item this round?''')


    player_code_color = models.CharField(
        doc = '''Player Colors''')


