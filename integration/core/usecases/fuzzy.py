import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from scipy.integrate import solve_ivp

class FuzzySystem():   

    @staticmethod
    def EDO_HVC_Pfuzzy(t, P, simulador):  

        # PARAMETROS
        b = 1e-2

        # HUMANOS
        r_h = 1.9e-2
        k_h = 1
        a_h = 2e-1
        m_h = 0.75
        alpha_h = a_h * b * m_h  # alpha_h = a_h * b;
        mu_h = 3.67e-5
        d_h = 6.31e-3
        gamma_h = 2.5e-3

        # CÃES
        r_c = 2.96e-1
        k_c = 1
        a_c = 2e-1
        m_c = (10 / 1.8) * m_h
        alpha_c = a_c * b * m_c  # alpha_c = a_c * b;
        mu_c = 2.28e-4
        d_c = 1.81e-3

        # FLEBOTOMÍNEOS
        r_f = 2e-1
        k_f = 1
        b_hf = 1.2e-2
        beta_h = a_h * b_hf
        b_cf = 30.6e-2
        beta_c = a_c * b_cf
        mu_f = 5e-2    

        P = np.array(P)

        resto = t % 360    
        if resto < 180:
            tau = resto      
        else:
            tau = 359 - resto       

        p = P[2] + P[3]   

        # Configurar as entradas do simulador
        simulador.input['flebotomineos'] = p
        simulador.input['cond_ambiental'] = tau

        # Computar o resultado (Inferência Fuzzy + Defuzzificação)
        simulador.compute()

        # Obter o valor da variável de saída
        var_value = simulador.output['variacao']

        dPdt = [
            r_h * (P[0] + P[1]) * (1 - (P[0] + P[1]) / k_h) - alpha_h * P[0] * (P[3] / (P[2] + P[3])) + gamma_h * P[1] - mu_h * P[0],
            alpha_h * P[0] * (P[3] / (P[2] + P[3])) - gamma_h * P[1] - (mu_h + d_h) * P[1],
            var_value - beta_h * P[2] * (P[1] / (P[0] + P[1])) - beta_c * P[2] * (P[5] / (P[4] + P[5])) + mu_f * P[3],
            beta_h * P[2] * (P[1] / (P[0] + P[1])) + beta_c * P[2] * (P[5] / (P[4] + P[5])) - mu_f * P[3],
            r_c * P[4] * (1 - (P[4] + P[5]) / k_c) - alpha_c * P[4] * (P[3] / (P[2] + P[3])) - mu_c * P[4],
            alpha_c * P[4] * (P[3] / (P[2] + P[3])) - (mu_c + d_c) * P[5]
        ]
        
        return dPdt

    def execute(self, initial_conditions, tempo):        

         # TEMPO
        ano = int(tempo)
        tspan = np.linspace(0, ano * 360, ano * 360 + 1)

        fuzzy = FuzzySystem()

        # Definindo as variáveis de entrada e saída
        flebotomineos = ctrl.Antecedent(np.linspace(0, 1, 1000), 'flebotomineos') 
        cond_ambiental = ctrl.Antecedent(np.linspace(0, 180, 1000), 'cond_ambiental') 
        variacao = ctrl.Consequent(np.linspace(-0.0015, 0.0015, 1000), 'variacao') 

        # Funções de pertinência para 'Flebotomineos'
        flebotomineos['baixo'] = fuzz.trapmf(flebotomineos.universe, [-2, -0.25, 0.1, 0.3022])
        flebotomineos['medio_baixo'] = fuzz.trimf(flebotomineos.universe, [0.1, 0.3, 0.55])
        flebotomineos['medio'] = fuzz.trimf(flebotomineos.universe, [0.3, 0.55, 0.7])
        flebotomineos['medio_alto'] = fuzz.trimf(flebotomineos.universe, [0.55, 0.7, 0.8])
        flebotomineos['alto'] = fuzz.trimf(flebotomineos.universe, [0.7, 0.8, 0.9])
        flebotomineos['muito_alto'] = fuzz.trapmf(flebotomineos.universe, [0.8, 0.9, 1.1, 5])

        # Funções de pertinência para 'Cond.ambiental'
        cond_ambiental['deficientemente_favoravel'] = fuzz.trapmf(cond_ambiental.universe, [-14, -10, 60, 90])
        cond_ambiental['parcialmente_favoravel'] = fuzz.trimf(cond_ambiental.universe, [60, 90, 120])
        cond_ambiental['favoravel'] = fuzz.trapmf(cond_ambiental.universe, [90, 120, 190, 200])

        # Funções de pertinência para saída 'Variacao'
        variacao['baixo_negativo'] = fuzz.trapmf(variacao.universe, [-0.00075, -0.0001875, 0, 0])
        variacao['baixo_positivo'] = fuzz.trapmf(variacao.universe, [0, 0, 0.0001875, 0.00075])
        variacao['medio_positivo'] = fuzz.trimf(variacao.universe, [0.000375, 0.00075, 0.001125])
        variacao['alto_positivo'] = fuzz.trapmf(variacao.universe, [0.00075, 0.001125, 0.0015, 0.02])
        variacao['medio_negativo'] = fuzz.trimf(variacao.universe, [-0.001125, -0.00075, -0.000375])
        variacao['alto_negativo'] = fuzz.trapmf(variacao.universe, [-0.02, -0.0015, -0.001125, -0.00075])

        # Descomentar caso queria visualizar as funções de pertinência para cada variável
        # flebotominios.view()
        # cond_ambiental.view()
        # variacao.view()
         
        # Base de Conhecimento/Regras de inferência Fuzzy e Defuzzificação
        rule1 = ctrl.Rule(flebotomineos['baixo'] & cond_ambiental['deficientemente_favoravel'], variacao['baixo_positivo'])
        rule2 = ctrl.Rule(flebotomineos['baixo'] & cond_ambiental['parcialmente_favoravel'], variacao['baixo_positivo'])
        rule3 = ctrl.Rule(flebotomineos['baixo'] & cond_ambiental['favoravel'], variacao['baixo_positivo'])
        rule4 = ctrl.Rule(flebotomineos['medio_baixo'] & cond_ambiental['deficientemente_favoravel'], variacao['baixo_negativo'])
        rule5 = ctrl.Rule(flebotomineos['medio_baixo'] & cond_ambiental['parcialmente_favoravel'], variacao['baixo_positivo'])
        rule6 = ctrl.Rule(flebotomineos['medio_baixo'] & cond_ambiental['favoravel'], variacao['medio_positivo'])
        rule7 = ctrl.Rule(flebotomineos['medio'] & cond_ambiental['deficientemente_favoravel'], variacao['medio_negativo'])
        rule8 = ctrl.Rule(flebotomineos['medio'] & cond_ambiental['parcialmente_favoravel'], variacao['baixo_negativo'])
        rule9 = ctrl.Rule(flebotomineos['medio'] & cond_ambiental['favoravel'], variacao['alto_positivo'])
        rule10 = ctrl.Rule(flebotomineos['medio_alto'] & cond_ambiental['deficientemente_favoravel'], variacao['medio_negativo'])
        rule11 = ctrl.Rule(flebotomineos['medio_alto'] & cond_ambiental['parcialmente_favoravel'], variacao['baixo_negativo'])
        rule12 = ctrl.Rule(flebotomineos['medio_alto'] & cond_ambiental['favoravel'], variacao['alto_positivo'])
        rule13 = ctrl.Rule(flebotomineos['alto'] & cond_ambiental['deficientemente_favoravel'], variacao['alto_negativo'])
        rule14 = ctrl.Rule(flebotomineos['alto'] & cond_ambiental['parcialmente_favoravel'], variacao['baixo_negativo'])
        rule15 = ctrl.Rule(flebotomineos['alto'] & cond_ambiental['favoravel'], variacao['alto_positivo'])
        rule16 = ctrl.Rule(flebotomineos['muito_alto'] & cond_ambiental['deficientemente_favoravel'], variacao['alto_negativo'])
        rule17 = ctrl.Rule(flebotomineos['muito_alto'] & cond_ambiental['parcialmente_favoravel'], variacao['baixo_negativo'])
        rule18 = ctrl.Rule(flebotomineos['muito_alto'] & cond_ambiental['favoravel'], variacao['baixo_negativo'])

        # Sistema Fuzzy e Simulação
        dados_var = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18])
        simulador = ctrl.ControlSystemSimulation(dados_var)       

        #options = {'atol': 1e-6, 'rtol': 1e-6}
        # Agora, chame solve_ivp passando simulador como argumento
        solution = solve_ivp(fun=lambda t, P: fuzzy.EDO_HVC_Pfuzzy(t, P, simulador),
                            t_span=(tspan[0], tspan[-1]),
                            y0=initial_conditions,
                            t_eval=tspan,
                            args=(),
                            method='RK45', #Método Runge-Kutta
                            vectorized=False,
                            #options=options
                            )

        # Obter os resultados
        #T = solution.t        
        P = solution.y.T   

        # Caso queira retornar o T em formato de objeto
        # data = {
        #     'p':P,
        #     't':T
        # }     

        return P

if __name__ == '__main__':
    from integration.core.usecases.fuzzy import FuzzySystem
    fuzzyfy = FuzzySystem()
    initial_conditions = [0.7, 0, 0.24, 0.01, 0.6, 0] #Condição padrão inicial
    fuzzyfy.execute(initial_conditions)

