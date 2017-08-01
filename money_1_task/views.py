from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, check_and_ok
from django.conf import settings
import time
import random




class ShuffleWaitPage(WaitPage):
    
    # shuffle all players into 3-player groups. Only two trade

    wait_for_all_groups = True

    def after_all_players_arrive(self):
        self.subsession.group_randomly(fixed_id_in_group=True)

class wait0(WaitPage):
    # set pairwise 
    
    def after_all_players_arrive(self):
        if self.round_number != 1:
            self.group.setup_new_period()
        self.group.set_pairwise_matches() #must be in shufflewaitpage

        



class task(Page):
    
    # trade 

    form_model = models.Player
    form_fields = ['trade']

    def after_all_players_arrive(self):
        pass
            

    
    def vars_for_template(self):



        consump_good = (self.player.id_in_group - (3*((self.player.id_in_group-1) // 3))) 
        counterparty = self.participant.vars['pairwise_matchings']['cp_id']
        counterparty_good = self.group.get_player_by_id(counterparty).inventory
        cp_consump_good = (counterparty - (3*((counterparty-1) // 3))) 


        # after period one
        # trade box
        if self.round_number != 1:
            if self.player.in_round(self.round_number-1).trade_offer == "Accepted":
                item_received = self.player.in_round(self.round_number-1).inventory_nextPeriod
                item_sent = self.player.in_round(self.round_number-1).inventory
                tradetext = "Your trade was accepted. You have exchanged item " + str(item_sent) + " to receive item " + str(item_received)
            if self.player.in_round(self.round_number-1).trade_offer == "Not Accepted, No Trade":
                tradetext = "Your trade was not accepted. You have item " + str(self.player.inventory)
        else:
            tradetext = ""
            
        # consumption box
        if self.round_number != 1:
            if self.player.in_round(self.round_number-1).inventory_nextPeriod == self.player.in_round(self.round_number-1).player_type:
                consumptiontext = "Since you received your consumption good last round your score increased by " + str(self.session.config['u']) + " points."
            else:
                consumptiontext = "You did not receive your consumption good this round."
        else:
            consumptiontext = ""
            
        # production box
        if self.round_number != 1:
            if self.player.in_round(self.round_number-1).inventory_nextPeriod == self.player.in_round(self.round_number-1).player_type:
                productiontext = "You produced a new item this round. You now have item " + str(self.player.inventory) + "."
            else:
                productiontext = "You did not produce a new item this round. You still have item " + str(self.player.inventory) + "."
        else:
            productiontext = ""

        # production box
        if self.round_number != 1:
            if self.player.in_round(self.round_number-1).inventory_nextPeriod == self.player.in_round(self.round_number-1).player_type:
                itemcosttext = "Since you consumed an item last round, and produced a new item this round, you receive zero item holding items."
            else:
                itemcosttext = "You held item " + str(self.player.inventory) + " between rounds. That receives " + str(-1*self.player.round_cost_holding) + " points."
        else:
            itemcosttext = ""

        # score change recap box
        if self.round_number == 2:
            scorebox = "Last round you had 100 points. This round you have " + str(self.player.score) + " points."
        elif self.round_number >2:
            scorebox = "Last round you had " + str(self.player.in_round(self.round_number-2).score - self.player.in_round(self.round_number-1).round_cost_holding) + " points. This round you have " + str(self.player.score) + " points."
        else:
            scorebox = ""


        return {
            'pairwise_matchings':(self.participant.vars['pairwise_matchings']),
            'consump_good':consump_good,
            'role':(self.player.role),
            'counterparty_good': self.participant.vars['pairwise_matchings'],
            'cp_consump_good':cp_consump_good,
            'group':self.player.group,
            'cp_col':self.group.get_player_by_id(counterparty).player_code_color,
            'cp_animal':Constants.animals[counterparty-1],
            'own_col':self.player.player_code_color,
            'own_animal':Constants.animals[self.player.id_in_group-1],

            'tradetext':tradetext,
            'consumptiontext':consumptiontext,
            'productiontext':productiontext,
            'itemcosttext':itemcosttext,
            'scorebox':scorebox,

            'test':self.group.get_player_by_id(counterparty).inventory,


        }

class wait1(WaitPage):
    # wait for counterparty
    
    def after_all_players_arrive(self):
        self.group.set_round_payoff() 


class task2(Page):
    
    # trade 
            

    
    def vars_for_template(self):

        consump_good = (self.player.id_in_group - (3*((self.player.id_in_group-1) // 3))) 
        counterparty = self.participant.vars['pairwise_matchings']['cp_id']
        counterparty_good = self.group.get_player_by_id(counterparty).inventory
        cp_consump_good = (counterparty - (3*((counterparty-1) // 3))) 
        


        return {
            'pairwise_matchings':(self.participant.vars['pairwise_matchings']),
            'consump_good':consump_good,
            'role':(self.player.role),
            'counterparty_good': self.participant.vars['pairwise_matchings'],
            'cp_consump_good':self.participant.vars['pairwise_matchings']['cp_consume_type'],
            'cp_consump_good':cp_consump_good,
            'cp_col':self.group.get_player_by_id(counterparty).player_code_color,
            'cp_animal':Constants.animals[counterparty-1],
            'own_col':self.player.player_code_color,
            'own_animal':Constants.animals[self.player.id_in_group-1],

        }
        


class wait2(WaitPage):
    
    # wait for all players in group, before reshuffle

    wait_for_all_groups = True


class results(Page):
    
    # results

    def after_all_players_arrive(self):
        pass

    def is_displayed(self):

        return self.round_number == 15
            

    
    def vars_for_template(self):
        return {
            'final_score':self.player.score,
        }


page_sequence = [
    ShuffleWaitPage,
    wait0,
    task,
    wait1,
    results
    ]






