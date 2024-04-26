# Classe d'objet consacrée aux options européennes et backtest du modèle Black & Scholes

## Idée générale

Ce projet est consacré à la création d'une classe d'objet "Options Européennes" et de la programmation de méthode utile à cette dernière. Une partie additionelle est consacrée au backtest du modèle de Black and Scholes avec des données empiriques. 

Ce projet a pour fondement un projet d'informatique appliqué à la finance à mener dans le cadre de l'UE IAF Python du S2 de la L3 d'Économie et Ingénierie financière de l'université Paris - Dauphine. Bien que son objectif premier soit une démonstration de notre maîtrise du programme de l'UE nous avons tout de même mis un point d'honneur à rendre ce projet aussi cohérent que notre statut d'étudiant en L3 pouvait nous le permettre.

## Classe d'objet "European Options"

En rappelant les hypothèses de Black & Scholes:

Hypothèses:

* Taux d'intérêt est connu et constant
* Les rendements du sous-jacent suivent une distribution normale
* Volatilité constante
* Originellement, pas de dividendes. Peut être modifié en revanche pour les inclure
* Pas de coûts de transaction
* Sous-jacents divisibles : il est possible d'acheter/vendre des fractions
* Ventes à découvert autorisée

Rappel sur les grecques:

* Delta : variation du prix de l'option par rapport à une variation du prix de l'actif sous-jacent
* Gamma : variation du delta par rapport à une variation du prix de l'actif sous-jacent
* Vega : variation du prix de l'option par rapport à une variation de la volatilité implicite
* Theta : variation du prix de l'option par rapport au passage du temps
* Rho : variation du prix de l'option par rapport aux changements du taux d'intérêt sans risque

### Attributs 

En attributs de la classe d'objet les paramètres classiques utiles au pricing d'une option européenne dans le cadre du modèle Black & Scholes; le prix du sous-jacent (UA), le strike (S), la variable temps (t), la volatilité (sigma), le taux sans-risque (r) et le type de l'option (type: Put/Call).

### Méthode: .d1

Permet le calcul de d1 dans le cadre du modèle BS c'est à dire la mesure statistique (par la distribution normale) correspondant au delta de l’option d’achat.

### Méthode: .d2

Permet le calcul de d2 dans le cadre du modèle BS c'est à dire  la mesure statistique (distribution normale) correspondant à la probabilité que l’option d’achat soit exercée à l’échéance.

### Méthode: .black_scholes_pricing

Permet le calcul du prix de l'objet option selon l'équation issue du modèle de Black & Scholes, utilisation de la méthode self.d1 et self.d2 dans une disjonction de cas "if" en fonction du type de l'option. 

### Méthode: .bs_gamma 

Permet le calcul du gamma de l'option.

### Méthode: .bs_vega 

Permet le calcul du vega de l'option.

### Méthode: .bs_delta

Permet le calcul du delta de l'option en fonction de son type.

### Méthode: .bs_theta

Permet le calcul du theta de l'option en fonction de son type.

### Méthode: .bs_rho

Permet le calcul du rho de l'option en fonction de son type.

### Méthode: .black_scholes_greeks

Permet une synthèse des 5 méthodes pour calculer les grecques décrites plus haut.

### Méthode: .payoff

Permet de dessiner un graphique du PnL de l'option en fonction de l'évolution du prix du SJ. Possibilité de grapher également le PnL de la contrepartie de notre option. 

### Méthode: .monte_carlo_simulations

Permet de calculer le prix selon la méthode de Monte Carlo. Le nombre de simulations à éxécuter est un argument optionnel est par défaut établi à 10 000.

## Fichier Test_Object Class

Permet simplement d'instancier plusieurs options, d'en calculer leurs prix, leurs grecques et de tracer leurs payoffs. Nous permet de tester à part notre classe d'objet consacrée aux options européennes. 

## Fichier Backtest_BS

Nous avons décidé de réaliser un backtest sur les résultats du Black-Scholes. Pour cela, nous récupérons les prix des 100 premières actions du S&P (ces entreprises ont été choisies et stockées dans un tableau Excel au préalable) sur les 6 derniers mois. Pour chaque jour des 3 premiers mois, le prix sert à estimer grâce au Black-Scholes le prix dans 3 mois. Puis pour chaque entreprise, les estimations sur 3 mois sont comparées aux prix effectifs. Sur les 6 mois récupérés, les 3 premiers servent donc à faire environ 90 estimations du prix et les 3 derniers mois servent à comparer ces prix estimés avec les prix effectifs. Le backtest permet de faire la moyenne des écarts (en pourcentage) entre les estimations du Black-Scholes et la réalité. 

(Note : nous avons choisi de faire un backtest de cette forme car nous ne disposions pas de données sur le prix des options. Par ailleurs, nous avons également choisi de fixer la volatilité à 20%, ne disposant pas de prix d'options nous permettant de déduire la volatilité.)
