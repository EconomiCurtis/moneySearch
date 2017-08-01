import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# don't share this with anybody.
SECRET_KEY = '7o$d&3y-yd2ax1vi1!)!ur8^r92y)@q^n)!7t(kih(@qbl33+5'

# To use a database other than sqlite,
# set the DATABASE_URL environment variable.
# Examples:
# postgres://USER:PASSWORD@HOST:PORT/NAME
# mysql://USER:PASSWORD@HOST:PORT/NAME

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AED '
USE_POINTS = True


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<p>
    <a href="http://www.otree.org/" target="_blank">oTree homepage</a>.
</p>
<p>
    Here are various games implemented with oTree.
</p>
<p>
    <strong>Motherhood</strong> refers to Motherhood experiments 
</p>
<p>
    <strong>CSR</strong> refers to corporate social responcibility experiments. 
</p>
<p>
    <strong>Katz</strong> refers to surveys associated with the SOETUF P-T and S-T project. 
</p>
"""

ROOMS = [
    {
        'name': 'ssel_b_side',
        'display_name': 'SSEL Desktops B01 - B24 - The B-Sides',
        'participant_label_file': '_rooms/ssel_b_side.txt',
    },
    {
        'name': 'ssel_a_team',
        'display_name': 'SSEL Desktops A01 - A24 - The A-Team',
        'participant_label_file': '_rooms/ssel_a_team.txt',
    },
    # {
    #     'name': 'SSEL_A_Side',
    #     'display_name': 'SSEL A-Side 1-24',
    #     'participant_label_file': '_rooms/groupAB1.txt',
    # }, 
    #     {
    #     'name': 'groupZU2',
    #     'display_name': 'groupZU2 - ZU Experiment Up to 70-players 002',
    #     'participant_label_file': '_rooms/groupZU2.txt',
    # },
    #     {
    #     'name': 'groupBB2',
    #     'display_name': 'groupBB2 - ZU Experiment Up to 70-players 002',
    #     'participant_label_file': '_rooms/groupBB2.txt',
    # },
    # {
    #     'name': 's_a_gan',
    #     'display_name': 'ZU Experiment 4-player 001',
    #     'participant_label_file': '_rooms/s_a_gan.txt',
    # },
    # {
    #     'name': 's_b_wan',
    #     'display_name': 'ZU Experiment 4-player 002',
    #     'participant_label_file': '_rooms/s_b_wan.txt',
    # },
    # {
    #     'name': 's_c_gan',
    #     'display_name': 'ZU Experiment 4-player 003',
    #     'participant_label_file': '_rooms/s_c_gan.txt',
    # },
    # {
    #     'name': 's_d_ban',
    #     'display_name': 'ZU Experiment 4-player 004',
    #     'participant_label_file': '_rooms/s_d_ban.txt',
    # },
    # {
    #     'name': 's_e_fam',
    #     'display_name': 'ZU Experiment 4-player 005',
    #     'participant_label_file': '_rooms/s_e_fam.txt',
    # },
    # {
    #     'name': 's_f_mam',
    #     'display_name': 'ZU Experiment 4-player 006',
    #     'participant_label_file': '_rooms/s_f_mam.txt',
    # },
    # {
    #     'name': 's_g_san',
    #     'display_name': 'ZU Experiment 4-player 007',
    #     'participant_label_file': '_rooms/s_g_san.txt',
    # },
    # {
    #     'name': 's_h_ran',
    #     'display_name': 'ZU Experiment 4-player 008',

    #     'participant_label_file': '_rooms/s_h_ran.txt',
    # },
    # {
    #     'name': 's_i_lam',
    #     'display_name': 'ZU Experiment 4-player 009',
    #     'participant_label_file': '_rooms/s_i_lam.txt',
    # },
    # {
    #     'name': 's_j_tan',
    #     'display_name': 'ZU Experiment 4-player 010',
    #     'participant_label_file': '_rooms/s_j_tan.txt',
    # },
    # {
    #     'name': 's_k_zan',
    #     'display_name': 'ZU Experiment 4-player 011',
    #     'participant_label_file': '_rooms/s_k_zan.txt',
    # },
    # {
    #     'name': 's_l_a',
    #     'display_name': 'ZU Experiment 4-player 012',
    #     'participant_label_file': '_rooms/s_l_a.txt',
    # },
    # {
    #     'name': 's_m_z',
    #     'display_name': 'ZU Experiment 4-player 013',
    #     'participant_label_file': '_rooms/s_m_z.txt',
    # },
    # {
    #     'name': 's_n_s',
    #     'display_name': 'ZU Experiment 4-player 014',
    #     'participant_label_file': '_rooms/s_n_s.txt',
    # },
    # {
    #     'name': 's_o_a',
    #     'display_name': 'ZU Experiment 4-player 015',
    #     'participant_label_file': '_rooms/s_o_a.txt',
    # },
    # {
    #     'name': 's_p_yan',
    #     'display_name': 'ZU Experiment 4-player 016',
    #     'participant_label_file': '_rooms/s_p_yan.txt',
    # },
    # {
    #     'name': 's_q_stan',
    #     'display_name': 'ZU Experiment 4-player 017',
    #     'participant_label_file': '_rooms/s_q_stan.txt',
    # },
    #     {
    #     'name': 'econ101',
    #     'display_name': 'Econ 101 class',
    #     'participant_label_file': '_rooms/econ101.txt',
    # }, 
    # {
    #     'name': 'live_demo',
    #     'display_name': 'Room for live demo (no participant labels)',
    # },

]


# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.0,
    'participation_fee': 0.00,
    'num_bots': 6,
    'doc': "NYUAD SSEL",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name':'money_experiment',
        'display_name':'Experimental Macro 17 - Money Experiment',
        'num_demo_participants': 6,
        'app_sequence': [
            'money_0_intro',
            'money_1_task',
        ],
        'u':100,
        'c':[-9,-6,-1],
        'b':0.9,
        'endow':100,
        'showupfee':30,
        'initial_robots_n':5, # initial multiple of robots
        'robot_steps':10, # number of rounds befor the number of robots drops by one multiple. 
    },

]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
