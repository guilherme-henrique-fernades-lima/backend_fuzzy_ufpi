% Simulacao 01 - Humano, Flebotomineo, Caes.
% Parametros: Shimizako-2017, Song-2020, Larenti-2013 e Seva-2016.
% Fonte vital dos Flebotomineos P-fuzzy periodica.
% Obs.: Considerou-se as populacoes normalizadas. 
% ----------------------------------------------------------------------- %
clear All; clc; close all;
global r_h k_h alpha_h gamma_h mu_h d_h r_c k_c alpha_c mu_c d_c r_f k_f beta_h beta_c mu_f gamma_c
% ----------------------------------------------------------------------- %
% Tempo
ano = 15; tspan = linspace(0,ano*360,ano*360+1); 
% ----------------------------------------------------------------------- %
% PARAMETROS 
P_AUX = [ ]';
b=1e-2; 
% HUMANOS %
r_h=1.9e-2; 
k_h=1; 
a_h=2e-1; m_h=0.75; alpha_h=a_h*b*m_h; % alpha_h=a_h*b;
mu_h=3.67e-5; d_h=6.31e-3; gamma_h=2.5e-3;
% CAES %
r_c=2.96e-1; 
k_c=1;
a_c=2e-1; m_c=(10/1.8)*m_h; alpha_c=a_c*b*m_c; % alpha_c=a_c*b;
mu_c=2.28e-4; d_c=1.81e-3;
for ii = 1:2
    gamma_c = [0 .001]; gamma_c = gamma_c(ii);
    % FLEBOTOMINEOS %
    r_f=2e-1;
    k_f=1;
    b_hf=1.2e-2; beta_h=a_h*b_hf;
    b_cf=30.6e-2; beta_c=a_c*b_cf;
    mu_f=5e-2;
    % ----------------------------------------------------------------------- %
    % Condicao inicial
    P0 = [0.7; 0; 0.24; 0.01; 0.6; 0; 0; 0];
    % ----------------------------------------------------------------------- %
    % Controlador fuzzy
    dados_var = readfis('cond_ambiental_THE_1');
    % ----------------------------------------------------------------------- %
    % Solucao da EDO
    options = odeset('Abstol',1e-6,'Reltol',1e-6);
    [t, P] = ode45(@(t,P) EDO_HVC_Pfuzzy_Coleira(t,P,dados_var),tspan,P0,options);
    % ----------------------------------------------------------------------- %
    % Plotagem com todas as populacoes
    figure(2*ii-1)
    plot(t,P(:,1),'--b',t,P(:,2),'-b',t,P(:,3),'--r',t,P(:,4),'-r',t,P(:,5),'--k',t,P(:,6),'-k',t,P(:,7),'--m',t,P(:,8),'-m')
    ylabel('Densidade Populacional')
    xlabel('Tempo (em dias)')
    figure(2*ii)
    plot(t,P(:,7)+P(:,8),'-m')
    ylabel('Densidade Populacional - Caes encolerados')
    xlabel('Tempo (em dias)')
    
    P_AUX(:,ii) = P(:,2);
end
P_AUX1 = P_AUX(:,1)-P_AUX(:,2); % Aumento ou decrescimo de humanos incectados
figure(5)
plot(t,P_AUX(:,1),'-b',t,P_AUX(:,2),'-.b')
ylabel('Densidade Populacional - Humanos Infectados')
xlabel('Tempo (em dias)')
legend('Sem o encoleiramento','Com o encoleiramento')

close(2) % Essa figura eh desnecessaria