# Weeks between first and 2nd dose. Assumption based on 2nd-analysis
week_delta = {'biontech':5, 'moderna':5,'astrazeneca':12}
# risk reduction - the list entries do stand for: [Biontech after 1st dose, additional effect after second dose, \
# moderna 1st, 2nd, astra 1st, 2nd, Johnson 1st, technical 0]
risk_reductions = [0.82,0.13,0.7,0.25,0.76,0.06,0.66,0]
population = 83100000

