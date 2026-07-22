from otree.api import *
import numpy as np
import time
import random

doc = """
Chance
"""


class C(BaseConstants):
    NAME_IN_URL = 'chance'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    value_x = models.IntegerField()
    value_L = models.FloatField()
    value_M = models.FloatField()
    value_H = models.FloatField()

    m0 = models.FloatField(min=None)
    l0 = models.FloatField(min=None)
    h0 = models.FloatField(min=None)
    variant = models.StringField()
    s = models.FloatField()
    c = models.FloatField()
    real_round = models.IntegerField()

    Q1 = models.StringField(
        label="Q1: How many rounds are there in Part 1?",
        choices=['10', '20', '30'],
        widget=widgets.RadioSelect
    )
    Q2_1 = models.StringField(
        blank=True,
        label="Q2: Which of the following outcomes are possible in each round? (Select all that apply.)",
        choices=['0€'],
        widget=widgets.RadioSelect
    )
    Q2_2 = models.StringField(
        blank=True,
        choices=['5€'],
        widget=widgets.RadioSelect
    )
    Q2_3 = models.StringField(
        blank=True,
        choices=['10€'],
        widget=widgets.RadioSelect
    )
    Q2_4 = models.StringField(
        blank=True,
        choices=['20€'],
        widget=widgets.RadioSelect
    )
    Q3 = models.StringField(
        label="Q3: Do your decisions affect the earnings of other participants?",
        choices=['Yes', 'No'],
        widget=widgets.RadioSelect
    )
    Q4 = models.StringField(
        label="Q4: How is your payment determined?",
        choices=['If Part 1 is selected for payment, you are paid the sum of all rounds',
                 'If Part 1 is selected for payment, one round is randomly selected and paid',
                 'You are paid a fixed amount independent of your choices'],
        widget=widgets.RadioSelect
    )
    Q5 = models.StringField(
        label="Q5: Suppose you choose a lottery that gives a 50% chance of 0€ and a 50% chance of 20€. What does this mean?",
        choices=['You will receive 10€ for sure',
                 'One of the two outcomes will be randomly selected with equal probability',
                 'You can choose which outcome you prefer after the draw'],
        widget=widgets.RadioSelect
    )
    Q6 = models.StringField(
        label="Q6: As you move the slider to the right, which of the following happens?",
        choices=['The probability of 10€ increases', 'The probability of 0€ increases',
                 'The probability of 20€ always increases'],
        widget=widgets.RadioSelect
    )
    Q7 = models.FloatField(label="Move the slider in the screen below so that the medium probability is between 20% and 30%.")

    Q8 = models.StringField(
        label="Q1: How many rounds are there in Part 2?",
        choices=['1', '2', '3'],
        widget=widgets.RadioSelect
    )
    Q9 = models.StringField(
        label="Q4: How is your payment determined?",
        choices=['If Part 2 is selected for payment, you are paid the sum of all rows in a randomly selected round.',
                 'If Part 2 is selected for payment, one row across rounds, and its associated choice, is randomly selected and paid.',
                 'You are paid a fixed amount independent of your choices.'],
        widget=widgets.RadioSelect
    )
    Q10 = models.StringField(
        label="Q5: If in one row you select the option on the right of the list:",
        choices=['All rows below will automatically select the option on the right.',
                 'You can still choose the option on the left in one the rows below.'],
        widget=widgets.RadioSelect
    )

    q_final_1 = models.LongStringField(
        label="Were the experimental instructions and the design clear? (max 500 char.)")
    q_final_2 = models.LongStringField(label="What do you think is the purpose of the experiment? (max 500 char.)")
    q_final_3 = models.LongStringField(
        label="Can you briefly motivate all or some of your choices in Part 1? (max 500 char.)")
    q_final_4 = models.LongStringField(
        label="Can you briefly motivate all or some of your choices in Part 2? (max 500 char.)")
    Gender = models.StringField(
        label="Gender:",
        choices=['Male',
                 'Female',
                 'Other'],
        widget=widgets.RadioSelect
    )
    FieldOfStudy = models.StringField(
        label="Field of Study:")
    YearOfBirth = models.IntegerField(
        label="Year of birth:")
    Employment = models.StringField(
        label="Employment:",
        choices=['undergrad',
                 'postgrad',
                 'Other'],
        widget=widgets.RadioSelect
    )
    RiskPref = models.StringField(
        label="How do you see yourself: are you generally a person who is fully prepared to take "
              "risks or do you try to avoid taking risks? "
              "Please tick a box on the scale, where the value 0 means: 'not at all willing to take risks' "
              "and the value 10 means: 'very willing to take risks'.",
        choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        widget=widgets.RadioSelect
    )



    Q_wrongs = models.IntegerField(initial=0)
    Q1_wrongs = models.IntegerField(initial=0)
    Q2_wrongs = models.IntegerField(initial=0)
    Q3_wrongs = models.IntegerField(initial=0)
    Q4_wrongs = models.IntegerField(initial=0)
    Q5_wrongs = models.IntegerField(initial=0)
    Q6_wrongs = models.IntegerField(initial=0)
    Q7_wrongs = models.IntegerField(initial=0)
    Q8_wrongs = models.IntegerField(initial=0)
    Q9_wrongs = models.IntegerField(initial=0)
    Q10_wrongs = models.IntegerField(initial=0)

    response_time_start = models.FloatField()
    response_time_end = models.FloatField()
    response_time = models.FloatField()

    List_left = models.IntegerField()
    List_right = models.IntegerField()

    pLMH = models.StringField()
    pH_star = models.FloatField()
    pM_star = models.FloatField()
    pL_star = models.FloatField()

    cubicle = models.IntegerField(label="What is the number of your cubicle?")

    selected_round = models.IntegerField()
    random_select = models.FloatField()
    payout = models.CurrencyField()


# PAGES
class CQ(Page):
    form_model = 'player'
    form_fields = ['Q1', 'Q2_1', 'Q2_2', 'Q2_3', 'Q2_4', 'Q3', 'Q4', 'Q5', 'Q6']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def error_message(player, values):
        errors = []

        if values['Q1'] != '20':
            player.Q1_wrongs += 1
            errors.append('Q1')

        if values['Q2_1'] != '0€':
            player.Q2_wrongs += 1
            errors.append('Q2')
        elif values['Q2_2'] != None:
            player.Q2_wrongs += 1
            errors.append('Q2')
        elif values['Q2_3'] != '10€':
            player.Q2_wrongs += 1
            errors.append('Q2')
        elif values['Q2_4'] != '20€':
            player.Q2_wrongs += 1
            errors.append('Q2')

        if values['Q3'] != 'No':
            player.Q3_wrongs += 1
            errors.append('Q3')

        if values['Q4'] != 'If Part 1 is selected for payment, one round is randomly selected and paid':
            player.Q4_wrongs += 1
            errors.append('Q4')

        if values['Q5'] != 'One of the two outcomes will be randomly selected with equal probability':
            player.Q5_wrongs += 1
            errors.append('Q5')

        if values['Q6'] != 'The probability of 10€ increases':
            player.Q6_wrongs += 1
            errors.append('Q6')

        if errors:
            player.Q_wrongs += 1
            return 'Error in ' + ', '.join(errors)

class Chance(Page):
    form_model = 'player'
    form_fields = ['value_x', 'value_L', 'value_M', 'value_H', 'm0', 'h0', 'l0']

    @staticmethod
    def vars_for_template(player):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        total_length = CA_length + CB1_length + CB2_length + L_length + D_length + SP_length

        if player.round_number > CA_length + CB1_length + CB2_length + L_length + D_length:
            variant = "SP"
        else:
            variant = "Other"

        player.response_time_start = time.time()

        num_rounds_displayed1 = int(CA_length + CB1_length + CB2_length + L_length + D_length)

        return dict(
            number_rounds=int(total_length),
            variant=variant,
            num_rounds_displayed1=num_rounds_displayed1,
        )

    @staticmethod
    def js_vars(player):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        in_round = player.round_number
        s = 1
        c = player.session.config['c']

        if player.round_number <= (CA_length + CB1_length + CB2_length):
            length = CA_length + CB1_length + CB2_length
            if not ('factor_numbers' in player.participant.vars):
                factor_numbers = np.arange(1, length + 1)
                np.random.shuffle(factor_numbers)
                player.participant.vars['factor_numbers'] = factor_numbers
            else:
                factor_numbers = player.participant.vars['factor_numbers']
            factor_number = int(factor_numbers[player.round_number - 1])
            if factor_number <= CA_length:
                variant = 'CA'
                in_round = factor_number
            else:
                variant = 'CB'
                if factor_number <= (CA_length + CB1_length):
                    s = player.session.config['s1']
                    c = player.session.config['c1']
                    in_round = factor_number - CA_length
                else:
                    s = player.session.config['s2']
                    c = player.session.config['c2']
                    in_round = factor_number - (CA_length + CB1_length)

        elif player.round_number <= (CA_length + CB1_length + CB2_length + L_length):
            variant = 'L'
            in_round = L_select[int(player.round_number - (CA_length + CB1_length + CB2_length) - 1)]

        elif player.round_number <= (CA_length + CB1_length + CB2_length + L_length + D_length):
            variant = 'D'
            in_round = player.round_number - (CA_length + CB1_length + CB2_length + L_length)

        else:
            variant = 'SP'
            length = int(CA_length + CB1_length + CB2_length)
            factor_numbers = player.participant.vars['factor_numbers']
            in_round = int(player.round_number - (CA_length + CB1_length + CB2_length + L_length + D_length))
            if not ('pM_star' in player.participant.vars):
                pM_star = 0
                pL_star = 0
                pH_star = 0
                for i in range(1, length + 1):
                    if (player.in_round(i).value_M > pM_star) and (factor_numbers[i-1] <= CA_length):
                        pM_star = player.in_round(i).value_M
                        pL_star = player.in_round(i).value_L
                        pH_star = player.in_round(i).value_H
                player.participant.vars['pM_star'] = pM_star
                player.participant.vars['pL_star'] = pL_star
                player.participant.vars['pH_star'] = pH_star

        player.s = s
        player.c = c
        player.variant = variant
        player.real_round = int(in_round)

        dic = dict(
            round_number=player.round_number,
            in_round=in_round,
            out_H=player.session.config['out_H'],
            out_M=player.session.config['out_M'],
            out_L=player.session.config['out_L'],
            R=player.session.config['R'],
            MU=player.session.config['MU'],
            Z=player.session.config['Z'],
            color_H=player.session.config['color_H'],
            color_M=player.session.config['color_M'],
            color_L=player.session.config['color_L'],
            color_G=player.session.config['color_G'],
            variant=variant,
            s=s,
            c=c,
            K=player.session.config['K'],
        )
        if 'pM_star' in player.participant.vars:
            dic.update(
                pM_star=player.participant.vars['pM_star'],
                pH_star=player.participant.vars['pH_star'],
                pL_star=player.participant.vars['pL_star'],
            )
        return dic

    @staticmethod
    def is_displayed(player):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        total_length = CA_length + CB1_length + CB2_length + L_length + D_length
        return player.round_number <= total_length

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.response_time_end = time.time()
        player.response_time = player.response_time_end - player.response_time_start


class List(Page):
    form_model = 'player'
    form_fields = ['List_left', 'List_right']

    @staticmethod
    def vars_for_template(player):
        if not ('random_bool_list' in player.participant.vars):
            player.participant.vars['random_bool_list'] = random.randint(0, 1)

        Z = player.session.config['Z']
        L_select = player.session.config['L_select']
        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        total_length = CA_length + CB1_length + CB2_length + L_length + D_length

        length = int(CA_length + CB1_length + CB2_length)
        factor_numbers = player.participant.vars['factor_numbers']
        if not ('pM_star' in player.participant.vars):
            pM_star = 0
            pL_star = 0
            pH_star = 0
            for i in range(1, length + 1):
                if (player.in_round(i).value_M > pM_star) and (factor_numbers[i - 1] <= CA_length):
                    pM_star = player.in_round(i).value_M
                    pL_star = player.in_round(i).value_L
                    pH_star = player.in_round(i).value_H
            player.participant.vars['pM_star'] = pM_star
            player.participant.vars['pL_star'] = pL_star
            player.participant.vars['pH_star'] = pH_star

        pM_star = player.participant.vars['pM_star']
        pL_star = player.participant.vars['pL_star']
        pH_star = player.participant.vars['pH_star']
        player.pM_star = pM_star
        player.pL_star = pL_star
        player.pH_star = pH_star
        K = player.session.config['K']
        if player.round_number > (total_length + 1):
            if (player.round_number == (total_length + 2) and player.participant.vars['random_bool_list'] == 0) or (player.round_number == (total_length + 3) and player.participant.vars['random_bool_list'] == 1):
                pLMH = []
                pLMH_values = []
                for i in range(0, 11, 1):
                    pLMH.append([str(round(0.1 * i, 2) * 100) + "%", "0%", str(round(1 - 0.1 * i, 2) * 100) + "%"])
                    pLMH_values.append([round(0.1 * i, 2) * 100, 0, round(1 - 0.1 * i, 2) * 100])
            else:
                pLMH = []
                pLMH_values = []
                for i in range(0, 11, 1):
                    pH = (0.1 * ((1 - 0.1 * i) - pH_star/100) + (pH_star/100 * pM_star/100)) / (pM_star/100)
                    pM = pM_star/100 - 0.1
                    pL = 1 - pM - pH
                    pLMH.append([str(round(pL * 100, 1)) + "%", str(round(pM * 100, 1)) + "%", str(round(pH * 100, 1)) + "%"])
                    pLMH_values.append([round(pL * 100, 1), round(pM * 100, 1), round(pH * 100, 1)])
            if player.round_number == (total_length + 2):
                player.participant.vars['pLMH_2'] = pLMH_values
            else:
                player.participant.vars['pLMH_3'] = pLMH_values
        else:
            pLMH = []
            pLMH_values = []
            for i in range(0, 11, 1):
                pLMH.append([str(round(0.1 * i, 2) * 100) + "%", "0%", str(round(1 - 0.1 * i, 2) * 100) + "%"])
                pLMH_values.append([round(0.1 * i, 2) * 100, 0, round(1 - 0.1 * i, 2) * 100])
            player.participant.vars['pLMH_1'] = pLMH_values
            pM_star = 100
            pH_star = 0
            pL_star = 0

        player.pLMH = str(pLMH_values)

        player.response_time_start = time.time()

        return dict(
            pM_star=str(pM_star)+"%",
            pH_star=str(pH_star)+"%",
            pL_star=str(pL_star)+"%",
            pLMH=pLMH,
        )

    @staticmethod
    def is_displayed(player):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        total_length = CA_length + CB1_length + CB2_length + L_length + D_length
        return (player.round_number > total_length) and (player.round_number <= (total_length + 3))

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.response_time_end = time.time()
        player.response_time = player.response_time_end - player.response_time_start

    @staticmethod
    def error_message(player, values):
        if (values['List_left'] + values['List_right']) != 11:
            return 'Answer all questions'


class Q7(Page):
    form_model = 'player'
    form_fields = ['Q7']

    @staticmethod
    def vars_for_template(player):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        total_length = CA_length + CB1_length + CB2_length + L_length + D_length + SP_length

        return dict(
            number_rounds=int(total_length),
        )

    @staticmethod
    def js_vars(player):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        in_round = player.round_number
        s = 1

        dic = dict(
            round_number=player.round_number,
            in_round=in_round,
            out_H=player.session.config['out_H'],
            out_M=player.session.config['out_M'],
            out_L=player.session.config['out_L'],
            R=player.session.config['R'],
            MU=player.session.config['MU'],
            Z=player.session.config['Z'],
            color_H=player.session.config['color_H'],
            color_M=player.session.config['color_M'],
            color_L=player.session.config['color_L'],
            color_G=player.session.config['color_G'],
            s=s,
            K=player.session.config['K'],
        )
        return dic

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def error_message(player, values):
        if not (20 < values['Q7'] < 30):
            player.Q_wrongs += 1
            player.Q7_wrongs += 1
            return 'You made a mistake'


class Start(Page):
    form_model = 'player'
    form_fields = ['cubicle']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.label = str(player.cubicle)


class CQ2(Page):
    form_model = 'player'
    form_fields = ['Q8', 'Q2_1', 'Q2_2', 'Q2_3', 'Q2_4', 'Q3', 'Q9', 'Q10']

    @staticmethod
    def is_displayed(player):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        total_length = CA_length + CB1_length + CB2_length + L_length + D_length
        return player.round_number == total_length + 1

    @staticmethod
    def error_message(player, values):
        errors = []
        display_names = {
            'Q8': 'Q1',
            'Q2': 'Q2',
            'Q3': 'Q3',
            'Q9': 'Q4',
            'Q10': 'Q5',
        }

        if values['Q8'] != '3':
            player.Q8_wrongs += 1
            errors.append(display_names['Q8'])

        if values['Q2_1'] != '0€':
            player.Q2_wrongs += 1
            errors.append(display_names['Q2'])
        elif values['Q2_2'] != None:
            player.Q2_wrongs += 1
            errors.append(display_names['Q2'])
        elif values['Q2_3'] != '10€':
            player.Q2_wrongs += 1
            errors.append(display_names['Q2'])
        elif values['Q2_4'] != '20€':
            player.Q2_wrongs += 1
            errors.append(display_names['Q2'])

        if values['Q3'] != 'No':
            player.Q3_wrongs += 1
            errors.append(display_names['Q3'])

        if values['Q9'] != 'If Part 2 is selected for payment, one row across rounds, and its associated choice, is randomly selected and paid.':
            player.Q9_wrongs += 1
            errors.append(display_names['Q9'])

        if values['Q10'] != 'All rows below will automatically select the option on the right.':
            player.Q10_wrongs += 1
            errors.append(display_names['Q10'])

        if errors:
            player.Q_wrongs += 1
            return 'Error in ' + ', '.join(errors)

class FQ(Page):
    form_model = 'player'
    form_fields = ['q_final_1', 'q_final_2', 'q_final_3', 'q_final_4', 'Gender', 'FieldOfStudy', 'YearOfBirth', 'Employment', 'RiskPref']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 100

    @staticmethod
    def before_next_page(player, timeout_happened):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        total_length = CA_length + CB1_length + CB2_length + L_length + D_length + SP_length

        selected_round = random.randint(1, total_length)
        player.selected_round = selected_round

        if selected_round <= total_length - SP_length:
            pL = player.in_round(selected_round).value_L
            pM = player.in_round(selected_round).value_M
            pH = player.in_round(selected_round).value_H
        else:
            selected_row = random.randint(1, 11)
            if selected_round == total_length - 2:
                if selected_row <= player.in_round(selected_round).List_left:
                    pL = player.participant.vars['pLMH_1'][selected_row - 1][0]
                    pM = player.participant.vars['pLMH_1'][selected_row - 1][1]
                    pH = player.participant.vars['pLMH_1'][selected_row - 1][2]
                else:
                    pL = 0
                    pM = 100
                    pH = 0
            elif selected_round == total_length - 1:
                if selected_row <= player.in_round(selected_round).List_left:
                    pL = player.participant.vars['pLMH_2'][selected_row - 1][0]
                    pM = player.participant.vars['pLMH_2'][selected_row - 1][1]
                    pH = player.participant.vars['pLMH_2'][selected_row - 1][2]
                else:
                    pL = player.participant.vars['pL_star']
                    pM = player.participant.vars['pM_star']
                    pH = player.participant.vars['pH_star']
            else:
                if selected_row <= player.in_round(selected_round).List_left:
                    pL = player.participant.vars['pLMH_3'][selected_row - 1][0]
                    pM = player.participant.vars['pLMH_3'][selected_row - 1][1]
                    pH = player.participant.vars['pLMH_3'][selected_row - 1][2]
                else:
                    pL = player.participant.vars['pL_star']
                    pM = player.participant.vars['pM_star']
                    pH = player.participant.vars['pH_star']
            player.in_round(selected_round).value_L = pL
            player.in_round(selected_round).value_M = pM
            player.in_round(selected_round).value_H = pH

        random_select = round(random.random() * 100, 2)
        player.random_select = random_select

        if random_select < pL:
            player.payout = player.session.config['out_L']
        elif random_select < (pL + pM):
            player.payout = player.session.config['out_M']
        else:
            player.payout = player.session.config['out_H']

        player.payoff = player.payout

class Payoff(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return player.round_number == 100

    @staticmethod
    def vars_for_template(player):
        selected_round = player.selected_round

        return dict(
            selected_round=selected_round,
            pL=player.in_round(selected_round).value_L,
            pM=player.in_round(selected_round).value_M,
            pH=player.in_round(selected_round).value_H,
            random_select=player.random_select,
            payout=player.payout,
        )


class WaitPageCQ(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class WaitPageChance(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Part2(Page):

    @staticmethod
    def is_displayed(player):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        total_length = CA_length + CB1_length + CB2_length + L_length + D_length
        return player.round_number == total_length + 1


class WaitPageList(WaitPage):

    @staticmethod
    def is_displayed(player):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        SP_length = 3
        total_length = CA_length + CB1_length + CB2_length + L_length + D_length
        return player.round_number == total_length + 1

class Part1Start(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Part2Start(Page):

    @staticmethod
    def is_displayed(player):
        Z = player.session.config['Z']
        L_select = player.session.config['L_select']

        CA_length = (Z + 1) * (Z + 2) / 2
        CB1_length = CA_length
        CB2_length = CA_length
        L_length = len(L_select)
        D_length = 1
        total_length = CA_length + CB1_length + CB2_length + L_length + D_length
        return player.round_number == total_length + 1

page_sequence = [Start, WaitPageCQ, CQ, Q7, WaitPageChance, Part1Start, Chance, Part2, CQ2, WaitPageList, Part2Start, List, FQ, Payoff]
