from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, check_and_ok
from django.conf import settings
import time
import random




class Init(Page):

  
    form_model = models.Player
    form_fields = [
        'subject_email',
        'subject_name'
    ]

    def is_displayed(self):

        return self.round_number == 1

    def subject_email_error_message(self, value):
        if ("@" not in value)&("." not in value):
            return 'Must contain a valid email address, for example vernon.smith@hotmale.com'


    def vars_for_template(self):
        pass

class Intro1(Page):
    # timeout_seconds = 300

    def is_displayed(self):

        if self.round_number == 1:
            self.participant.vars['start_time'] = None

        return self.round_number == 1
    
    def vars_for_template(self):
        pass




page_sequence = [
    Intro1,
    ]






