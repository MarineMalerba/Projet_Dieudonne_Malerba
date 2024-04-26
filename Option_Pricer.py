import numpy as np
import scipy.stats as sp
import pandas as pd
from matplotlib import pyplot as plt 

class European_Options:

    def __init__(self, UA, S, t, sigma, r, type) :
        self.UA = UA
        self.S = S
        self.t = t
        self.sigma = sigma
        self.r = r
        self.type = type

#d1
    def d1(self) :
        return (np.log(self.UA/self.S) + (self.r + 0.5*self.sigma**2)*self.t) / (self.sigma*np.sqrt(self.t)) 


#d2
    def d2(self) :
        return self.d1 - self.sigma * np.sqrt(self.t)


#Prix par Black & Scholes
    def black_scholes_pricing(self) :
        #CALL : C(UA, S, t, sigma, r) = UA x N(d1) - S x e^(-r x t) x N(d2)
        if self.type.lower() == "call":

            price=self.UA*sp.norm.cdf(self.d1,0,1)-self.S*np.exp(-self.r*self.t)*sp.norm.cdf(self.d2,0,1)

        #PUT : P(UA, S, t, sigma, r) = S x e^(-r x t) x N(-d2) - UA x N(-d1)
        elif self.type.lower() == "put":

            price=self.S*np.exp(-self.r*self.t)*sp.norm.cdf(-self.d2,0,1)-self.UA*sp.norm.cdf(-self.d1,0,1)

        #Sinon
        else :
            price = "None"
            print("Type not valid. Please enter: 'Call' or 'Put'.")

        return price


# Synthèse des grecques
    def black_scholes_greeks(self) :

        gamma = sp.norm.pdf(self.d1,0,1)/(self.UA*self.sigma*np.sqrt(self.t))
        vega = (self.UA*sp.norm.pdf(self.d1,0,1)*np.sqrt(self.t))*0.01

        #CALL
        if self.type.lower() == "call":
            delta = sp.norm.cdf(self.d1,0,1)
            theta = (-self.UA*sp.norm.pdf(self.d1,0,1)*self.sigma/(2*self.t) - self.r*self.S*np.exp(-self.r*self.t)*sp.norm.cdf(self.d2,0,1))/365
            rho = (self.S*self.t*np.exp(-self.r*self.t)*sp.norm.cdf(self.d2,0,1))*0.01

        #PUT
        elif self.type.lower() == "put":
            delta = -sp.norm.cdf(-self.d1,0,1)
            theta = (-self.UA*sp.norm.pdf(self.d1,0,1)*self.sigma/(2*self.t) + self.r*self.S*np.exp(-self.r*self.t)*sp.norm.cdf(-self.d2,0,1))/365
            rho = (- self.S*self.t*np.exp(-self.r*self.t)*sp.norm.cdf(-self.d2,0,1))*0.01

        #Sinon
        else:
            delta = "None"
            gamma = "None"
            vega = "None"
            theta = "None"
            rho = "None"

        return np.array([delta, gamma, vega, theta, rho])


#Gamma
    def bs_gamma(self) :
        return sp.norm.pdf(self.d1,0,1)/(self.UA*self.sigma*np.sqrt(self.t))


#Vega
    def bs_vega(self) :
        return (self.UA*sp.norm.pdf(self.d1,0,1)*np.sqrt(self.t))*0.01
    

#Delta
    def bs_delta(self) :
        #CALL
        if self.type.lower() == "call":
            delta = sp.norm.cdf(self.d1,0,1)

        #PUT
        elif self.type.lower() == "put":
            delta = -sp.norm.cdf(-self.d1,0,1)

        #Sinon
        else:
            delta = "None"

        return delta


#Theta
    def bs_theta(self) :
        #CALL
        if self.type.lower() == "call":
            theta = (-self.UA*sp.norm.pdf(self.d1,0,1)*self.sigma/(2*self.t) - self.r*self.S*np.exp(-self.r*self.t)*sp.norm.cdf(self.d2,0,1))/365

        #PUT
        elif self.type.lower() == "put":
            theta = (-self.UA*sp.norm.pdf(self.d1,0,1)*self.sigma/(2*self.t) + self.r*self.S*np.exp(-self.r*self.t)*sp.norm.cdf(-self.d2,0,1))/365

        #Sinon
        else:
            theta = "None"

        return theta


#Rho
    def bs_rho (self) :
        #CALL
        if self.type.lower() == "call":
            rho = (self.S*self.t*np.exp(-self.r*self.t)*sp.norm.cdf(self.d2,0,1))*0.01

        #PUT
        elif self.type.lower() == "put":
            rho = (- self.S*self.t*np.exp(-self.r*self.t)*sp.norm.cdf(-self.d2,0,1))*0.01

        #Sinon
        else:
            rho = "None"

        return rho


    def graph_function(self, x, direction) :
        if self.type.lower() =="call" :
            if x <= self.UA:
                graph_function = self.UA / 4
            else:
                graph_function = self.UA / 4 - (x - self.UA)
            if direction.lower()=='long':
                graph_function=-graph_function
        elif self.type.lower() == 'put' :
            if x <= self.UA:
                graph_function = self.UA / 4 - (x - self.UA) - self.UA*0.4
            else:
                graph_function = self.UA / 4 - self.UA*0.4
            if direction.lower()=='short':
                graph_function=-graph_function

        return graph_function


#Payoff de l'option, PnL de la position en fonction du SJ
    def payoff(self, direction, otherside=False):

        x_values = np.linspace(self.UA*0.75, 1.75*self.UA, 1000) 

        y_values = [self.graph_function(x, direction) for x in x_values]

        if otherside:
            y_values_other = [-value for value in y_values]
            plt.plot(x_values, y_values_other, label='Payoff (counterparty)', linestyle='--')

        plt.plot(x_values, y_values, label='Payoff')
        plt.xlabel('Spot')
        plt.ylabel('Payoff')
        plt.title('Option Payoff')
        plt.grid(True)
        plt.legend()
        plt.show()


    def monte_carlo_simulations(self, nb_simulations=10000) :

        norm_table = np.random.normal(0, 1, nb_simulations) #Array de nombres aléatoires générés selon une distribution normale centrée réduite

        UA_t = self.UA * np.exp((self.r - 0.5 * self.sigma ** 2) * self.t + self.sigma * np.sqrt(self.t) * norm_table) #Calcul du prix de sous-jacent à l'instant t

        #CALL
        if self.type.lower() == 'call':
            monte_carlo_result = np.maximum(UA_t - self.S, 0) #Si le prix d'exercice est en dessous du sous-jacent à l'instant t, on exerce. Sinon on n'exerce pas, d'où le 0.

        #PUT
        elif self.type.lower() == "put":
            monte_carlo_result = np.maximum(self.S - UA_t, 0) #Si le prix d'exercice est en dessous du sous-jacent à l'instant t, on exerce. Sinon on n'exerce pas, d'où le 0.

        #Sinon
        else :
            monte_carlo_result = "None"
            print("Type not valid. Please enter: 'Call' or 'Put'.")

        monte_carlo_result = np.exp(-self.r * self.t) * np.mean(monte_carlo_result) #Moyenne des simulations actualisée

        return monte_carlo_result

