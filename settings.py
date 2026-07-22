from os import environ

SESSION_CONFIGS = [
    dict(
        name='chance',
        app_sequence=['chance'],
        num_demo_participants=1,
        out_H=20,
        out_M=10,
        out_L=0,
        R=0.333,
        MU=0.05,
        Z=2,
        color_H="blue",
        color_M="red",
        color_L="green",
        color_G="white",
        # number_rounds=22,
        # variant="CA&CB&SP",  # CA CB L D SP CA&CB&SP
        s1=6,  # "stretch" for CB called 'a' in doc
        s2=6,
        c=0.5,
        c1=0.75,
        c2=0.25,
        K=-0.1,
        L_select=[5],
    ),
]

ROOMS = [
    dict(
        name='lab',
        display_name='Lab',
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=7.00, doc=""
)

PARTICIPANT_FIELDS = ['factor_numbers', 'pM_star', 'pL_star', 'pH_star', 'pLMH_1', 'pLMH_2', 'pLMH_3', 'random_bool_list']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4543866366475'
