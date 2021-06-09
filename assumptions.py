# Weeks between first and 2nd dose. Assumption based on 2nd-analysis
week_delta = {'biontech':6, 'moderna':6,'astrazeneca':13}

# risk reduction - the list entries do stand for:
# [Biontech after 1st dose, additional effect after second dose, \
# moderna 1st, 2nd, astra 1st, 2nd, Johnson 1st, technical 0]
risk_reductions = [0.82,0.13,0.7,0.25,0.76,0.06,0.66,0]
population = 83100000

vacs = ['biontech','moderna','astrazeneca','johnson']


"""Astra
Thus, the studies in the UK, Brazil and South Africa showed the efficacy of the vaccine at the level of 76% after the first dose with protection maintained to the second dose. With an interval of 12 weeks between them and more, the efficacy of the vaccine increases up to 82%.
the studies confirmed that AstraZeneca vaccine reduces asymptomatic transmission of the virus by 67% after the first dose and by 50% after the second
https://112.international/society/astrazeneca-vaccine-is-effective-after-first-dose-58667.html
"""