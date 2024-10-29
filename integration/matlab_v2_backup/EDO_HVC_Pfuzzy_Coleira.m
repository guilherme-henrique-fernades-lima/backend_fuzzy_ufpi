function dPdt = EDO_HVC_Pfuzzy_Coleira(t,P,dados_var)
 
global r_h k_h alpha_h gamma_h mu_h d_h r_c k_c alpha_c mu_c d_c beta_h beta_c mu_f gamma_c% r_f k_f
resto = mod(t,360); 
if resto <180
    tau = resto; 
else
    tau = 359-resto;
end
p = P(3)+P(4);
var = evalfis([p tau],dados_var);

dPdt = [r_h*(P(1)+P(2))*(1-(P(1)+P(2))/k_h)-alpha_h*P(1)*(P(4)/(P(3)+P(4)))+gamma_h*P(2)-mu_h*P(1);
    alpha_h*P(1)*(P(4)/(P(3)+P(4)))-gamma_h*P(2)-(mu_h+d_h)*P(2);
    var-beta_h*P(3)*(P(2)/(P(1)+P(2)))-beta_c*P(3)*(P(6)/(P(5)+P(6)))+mu_f*P(4); 
    beta_h*P(3)*(P(2)/(P(1)+P(2)))+beta_c*P(3)*(P(6)/(P(5)+P(6)))-mu_f*P(4);
    r_c*P(5)*(1-(P(5)+P(6)+P(7)+P(8))/k_c)-alpha_c*P(5)*(P(4)/(P(3)+P(4)))-mu_c*P(5)-gamma_c*P(5);
    alpha_c*P(5)*(P(4)/(P(3)+P(4)))-(mu_c+d_c)*P(6)-gamma_c*P(6); 
    gamma_c*P(5)-mu_c*P(7); 
    gamma_c*P(6)-(mu_c+d_c)*P(8)];