from Option_Pricer import *


#Instanciation de 2 Options identiques à l'exception du type
option=European_Options(30,40,240/365, 0.3, 0.01, "Call")
option1=European_Options(30,40,240/365, 0.3, 0.01, "Put")


#Afficher son prix par BS
if option.type.lower()=="put" or option.type.lower()=="call" :
    print("The price of the " + option.type.lower() + " option is : " + str(round(option.black_scholes_pricing(), 3)))
    print(str(option.black_scholes_greeks()))

print("The price of the " + option.type.lower() + " option is : " + str(round(option.black_scholes_pricing(), 3)))


#Afficher ses grecques
greeks=option.black_scholes_greeks()

i=0
for element in option.black_scholes_greeks(): 
    print(np.array(["delta", "gamma", "vega", "theta", "rho"])[i] + " : " + str(element))
    i+=1


#Afficher les payoffs
option.graph('long',True)   
option1.graph('long',True)   


#Afficher son prix par Monte Carlo
print("The price of the " + option.type.lower() + " option estimated with Monte Carlo estimations is : " + str(round(option.monte_carlo_simulations(), 3)))
