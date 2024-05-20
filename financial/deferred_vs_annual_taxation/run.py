#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def retirement_fund(years, monthly_investment, annual_return, tax_rate):
    monthly_return = (1 + annual_return) ** (1 / 12) - 1
    total_months = years * 12
    balance = 0
    
    for month in range(total_months):
        balance = balance * (1 + monthly_return) + monthly_investment
        
    final_amount = balance * (1 - tax_rate)
    return final_amount

def taxed_annually_investment(years, monthly_investment, annual_return, tax_rate):
    total_months = years * 12
    balance = 0
    monthly_return = (1 + annual_return) ** (1 / 12) - 1
    
    for month in range(total_months):
        balance += monthly_investment
        balance += balance * monthly_return
        
        if (month + 1) % 12 == 0:
            annual_interest = balance * annual_return
            taxed_interest = annual_interest * tax_rate
            balance -= taxed_interest
            
    return balance

years = 30
monthly_investment = 200
annual_return = 0.08
tax_rate = 0.40

final_amount_0 = monthly_investment*years*12
final_amount_a = retirement_fund(years, monthly_investment, annual_return, tax_rate)
final_amount_b = taxed_annually_investment(years, monthly_investment, annual_return, tax_rate)


print(f"Final amount doing ABSOLUTELY NOTHING: {final_amount_0:.2f} euros")
print(f"Final amount in Retirement Fund (Option A): {final_amount_a:.2f} euros")
print(f"Final amount in Annual Taxed Investment (Option B): {final_amount_b:.2f} euros")
print(f"Difference = {final_amount_a-final_amount_b:.2f} euros along the 30 year course ({100*(final_amount_a-final_amount_b)/final_amount_0:.2f}%)")

# Plotting the graph
months = np.arange(1, years * 12 + 1)
balances_0 = []
balances_a = []
balances_b = []

# Calculate balances for each month for plotting
balance_0 = 0
balance_a = 0
balance_b = 0
monthly_return = (1 + annual_return) ** (1 / 12) - 1


for month in months:
    balance_0 += monthly_investment
    balances_0.append(balance_0)
    balance_a = balance_a * (1 + monthly_return) + monthly_investment
    balances_a.append(balance_a)
    
    balance_b += monthly_investment
    balance_b += balance_b * monthly_return
    
    if month % 12 == 0:
        annual_interest_b = balance_b * annual_return
        taxed_interest_b = annual_interest_b * tax_rate
        balance_b -= taxed_interest_b
        
    balances_b.append(balance_b)

# Adjust the final balance of Option A after tax at the end of the period
balances_a[-1] *= (1 - tax_rate)

plt.figure(figsize=(12, 6))
plt.plot(months / 12, balances_a, label='Retirement Fund (Option A)', linewidth=5)
plt.plot(months / 12, balances_b, label='Annual Taxed Investment (Option B)', linewidth=5)
plt.plot(months / 12, balances_0, label='Doing Nothing', linewidth=5)
plt.xlabel('Years')
plt.ylabel('Balance (Euros)')
plt.title('Deferred vs Annual Taxation - Investment Growth Over 30 Years')
plt.legend()
plt.grid(True)
plt.show()

