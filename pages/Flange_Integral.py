import streamlit as st

#Two Columns for inputs and outputs
col1, col2 = st.columns([1,2]) #col2 width is 2*times col1 width

#Input Column
with col1:
    st.title("Inputs")
    
    st.write("**GENERAL DATA**")
    Desc = st.text_input("Description", value="ASME PTB-4 E4.16.1 - Integral Flange")
    P = st.number_input("Internal Design Pressure including static head, P (MPa)",step=0.001, format="%.3f", value=0.931)
    CA = st.number_input("Corrosion Allowance, CA (mm)",step=0.1, format="%.1f", value=3.175)   
    st.write("---")  
    
    st.write("**SHELL/NOZZLE NECK DATA**")
    Sno = st.number_input("Allowable Stress of Shell/Nozzle Neck at internal design temperature, Sno (MPa)",step=0.1, format="%.1f", value=129.621)
    Sna = st.number_input("Allowable Stress of Shell/Nozzle Neck at ambient temperature, Sna (MPa)",step=0.1, format="%.1f", value=137.895)
    st.write("---")  
 
    st.write("**FLANGE DATA**")
    Sfo = st.number_input("Allowable Stress of flange at internal design temperature, Sfo (MPa)",step=0.1, format="%.1f", value=122.727)
    Sfa = st.number_input("Allowable Stress of flange at ambient temperature, Sfa (MPa)",step=0.1, format="%.1f", value=137.895)
    Ed = st.number_input("Young's Modulus of flange at internal design temperature, Ed (MPa)",step=0.1, format="%.1f", value=1.793e5)
    Ea = st.number_input("Young's Modulus of flange at ambient temperature, Ea (MPa)",step=0.1, format="%.1f", value=2.027e5)
    B = st.number_input("Corroded Inside Diameter of the Flange, B (mm)",step=1.0, format="%.1f", value=666.75)
    C = st.number_input("Bolt Circle Diameter of the Flange, C (mm)",step=1.0, format="%.1f", value=793.75)
    A = st.number_input("Outside Diameter of the Flange, A (mm)",step=1.0, format="%.1f", value=835.025)
    t = st.number_input("Thickness of the Flange, t (mm)",step=1.0, format="%.1f", value=36.513)
    g1 = st.number_input("Corroded Thickness of hub at back of flange, g1 (mm)",step=1.0, format="%.1f", value=17.463)
    g0 = st.number_input("Corroded Thickness of hub at small end, g0 (mm)",step=1.0, format="%.1f", value=7.938)
    h = st.number_input("Hub Length, h (mm)",step=1.0, format="%.1f", value=53.975)
    st.write("---")  

    st.write("**FLANGE STRESS FACTORS**")
    st.write("Terms involving K (Fig 2-7.1)")
    Y = st.number_input("Y",step=1.0, format="%.4f", value=8.7565)
    T = st.number_input("T",step=1.0, format="%.4f", value=1.8175)
    U = st.number_input("U",step=1.0, format="%.4f", value=9.6225)
    Z = st.number_input("Z",step=1.0, format="%.4f", value=4.5180)
    
    st.write("Integral Flange Factors (Fig 2-7.2, Fig 2-7.3)")    
    F = st.number_input("F",step=1.0, format="%.4f", value=0.7677)
    V = st.number_input("V",step=1.0, format="%.4f", value=0.1577)
   
    st.write("Hub Stress Correction Factor")
    f = st.number_input("f",step=1.0, format="%.4f", value=1.0000)
    st.write("---")
 
    st.write("**BOLT DATA**")
    a = st.number_input("Nominal Bolt Dia, a (mm)",step=1.0, format="%.1f", value=19.05)
    Nb = st.number_input("Number of Bolts, Nb",step=1.0, format="%.1f", value=44.0)
    Aroot = st.number_input("Root area of a single bolt (mm2)",step=1.0, format="%.1f", value=194.838)
    Sb = st.number_input("Allowable Stress of Bolt at internal design temperature, Sb (MPa)",step=0.1, format="%.1f", value=172.369)
    Sa = st.number_input("Allowable Stress of Bolt at ambient temperature, Sa (MPa)",step=0.1, format="%.1f", value=172.369)
    st.write("---")
 
    st.write("**GASKET DATA**")
    m = st.number_input("Gasket Factor from Table 2-5.1, m",step=1.0, format="%.2f", value=3.75)
    y = st.number_input("Minimum Gasket Seating Stress from Table 2-5.1, y (MPa)",step=1.0, format="%.1f", value=52.4)
    GID = st.number_input("Gasket ID, GID (mm)",step=1.0, format="%.1f", value=736.6)
    GOD = st.number_input("Gasket OD, GOD (mm)",step=1.0, format="%.1f", value=762.0)
    N = st.number_input("Gasket Width from Table 2-5.2, N (mm)",step=1.0, format="%.1f", value=12.7)
    bo = st.number_input("Basic Gasket Width from Table 2-5.2, bo (mm)",step=1.0, format="%.1f", value=5.159)
    
#Output Column
with col2:
    st.title("Outputs")
    st.write("**See Fig 2 - Integral Flange at the ASME Calculator home page**")
    st.write("**CODE: ASME Sec VIII, Div 1 - 2023 Ed.**")
        
    #b and G
    with st.expander("Expand to see effective gasket width and gasket reaction diameter calculation"):
        if bo > 6:
            st.write("Since $b_o > 6$:")
            b = 2.5*bo**0.5
            st.latex(rf"b = 2.5 \sqrt {{b_{{o}}}} = 2.5 \sqrt{{{bo}}} = {b:.3f} \text {{ mm}}")
            G=GOD-2*b
            st.latex(rf"G = G_{{OD}} - 2b = {{{GOD}}} - 2 \cdot {{{b:.3f}}} = {G:.1f}")
        else:
            st.write("Since $b_o \leq 6$:")
            b = bo
            st.latex(rf"b = b_{{o}} = {b:.3f} \text {{ mm}}")
            G=(GOD+GID)/2
            st.latex(rf"G = 0.5 \cdot (G_{{OD}} + G_{{ID}}) = 0.5 \cdot ({{{GOD:.1f}}} + {{{GID:.1f}}}) = {G:.1f}")
        
    #Wm1 and Wm2
    with st.expander("Expand to see bolt load calculation"):
        st.write("Total Hydrostatic End Force")
        H = 0.785*G**2*P
        st.latex(rf"H = 0.785G^2P = 0.785 \cdot {G:.1f}^2 \cdot {P} = {H:.0f} \text {{ N}}")

        st.write("Total Joint Contact Surface Compression Load")
        Hp = 2*b*3.14*G*m*P
        st.latex(rf"H_p = 2b \cdot 3.14GmP = 2 \cdot {b:.3f} \cdot 3.14 \cdot {G:.1f} \cdot {m} \cdot {P} = {Hp:.0f} \text {{ N}}")
     
        st.write("Required Bolt Load in Operating Condition")
        Wm1 = H + Hp
        st.latex(rf"W_{{m1}} = H + H_p = {H:.0f} + {Hp:.0f} = {Wm1:.0f} \text {{ N}}")
     
        st.write("Required Bolt Load for gasket seating")
        Wm2 = 3.14*b*G*y
        st.latex(rf"W_{{m2}} = 3.14b \cdot G \cdot y = 3.14 \cdot {b:.3f} \cdot {G:.1f} \cdot {y:.1f} = {Wm2:.0f} \text {{ N}}")
        
    #Am1 and Am2
    with st.expander("Expand to see bolt area calculation"):
        st.write("Required Bolt Area for operating case")
        Am1 = Wm1/Sb
        st.latex(rf"A_{{m1}} = \frac{{W_{{m1}}}}{{S_b}} = \frac{{{Wm1:.1f}}}{{{Sb:.1f}}} = {Am1:.1f} \text {{ mm}}^2")

        st.write("Required Bolt Area for gasket seating case")
        Am2 = Wm2/Sa
        st.latex(rf"A_{{m2}} = \frac{{W_{{m2}}}}{{S_a}} = \frac{{{Wm2:.1f}}}{{{Sa:.1f}}} = {Am2:.1f} \text {{ mm}}^2")
   
        st.write("Required Bolt Area")
        Am = max(Am1,Am2)
        st.latex(rf"A_m = max(A_{{m1}}, A_{{m2}}) = max({Am1:.1f},{Am2:.1f}) = {Am:.1f} \text {{ mm}}^2")
        
        st.write("Available Bolt Area")
        Ab = Nb*Aroot
        st.latex(rf"A_b = N_b \cdot A_{{root}} = {Nb:.0f} \cdot {Aroot:.1f} = {Ab:.1f} \text {{ mm}}^2")
        
        if Ab >= Am:
            st.write("Since $A_b \geq A_m$ available bolt area is sufficient")
        else:
            st.markdown(":red[Bolt Area Insufficient]")
            
    #Design Bolt Loads for flanges
    with st.expander("Expand to see design bolt load calculation for flanges"):
        st.write("Flange Design Bolt Load for Operating Condition")
        Wo = Wm1
        st.latex(rf"W_o = W_{{m1}} = {Wo:.1f} \text {{ N}}")

        st.write("Flange Design Bolt Load for Gasket Seating Condition")
        Wgs = (Am+Ab)/2*Sa
        st.latex(rf"W_{{gs}} = \frac{{(A_m + A_b) \cdot S_a}}{{2}} = \frac{{({Am:.1f} + {Ab:.1f}) \cdot {Sa:.1f}}}{{{2}}} = {Wgs:.1f} \text {{ N}} ")

    #Flange Stress Factors
    with st.expander("Expand to see Flange Stress Factors"):
        st.write("Flange Stress Factors")
        K = A/B
        st.latex(rf"K = \frac{{A}}{{B}} = \frac{{{A}}}{{{B}}} = {K:.3f}")
        ho = (B*g0)**0.5
        st.latex(rf"h_o = \sqrt{{B \cdot g_0}} = \sqrt{{{B} \cdot {g0}}} = {ho:.3f}")
        st.latex(rf"\frac{{h}}{{h_o}} = \frac{{{h}}}{{{ho:.3f}}} = {h/ho:.3f}")
        st.latex(rf"\frac{{g_1}}{{g_0}} = \frac{{{g1}}}{{{g0}}} = {g1/g0:.3f}")
        d = U*g0**2*ho/V
        st.latex(rf"d = \frac{{U \cdot g_0^2 \cdot h_o}}{{V}} = \frac{{{U} \cdot {g0}^2 \cdot {ho:.3f}}}{{{V}}} = {d:.0f} \text {{ mm}}^3")
        e = F/ho
        st.latex(rf"e = \frac{{F}}{{h_o}} = \frac{{{F}}}{{{ho:.3f}}} = {e:.4f} \text {{ mm}}^{{-1}}")
        L = (t*e + 1)/T + t**3/d
        st.latex(rf"L = \frac{{(t \cdot e + 1)}}{{T}} + \frac{{t^3}}{{d}} = \frac{{({t} \cdot {e:.4f} + 1)}}{{{T}}} + \frac{{{t}^3}}{{{d:.0f}}} = {L:.3f}")
        
    #Flange Forces
    with st.expander("Expand to see Flange Forces (para 2-3)"):
        HD=0.785*B**2*P
        st.latex(rf"H_D = 0.785 \cdot B^2 \cdot P = 0.785 \cdot {B}^2 \cdot {P} = {HD:.0f} \text {{ N}}")
        H=0.785*G**2*P        
        st.latex(rf"H = 0.785 \cdot G^2 \cdot P = 0.785 \cdot {G}^2 \cdot {P} = {H:.0f} \text {{ N}}")
        HT = H - HD
        st.latex(rf"H_T = H - H_D = {H:.0f} - {HD:.0f} = {HT:.0f} \text {{ N}} ")
        HG = Wo - H
        st.latex(rf"H_G = W_o - H = {Wo:.0f} - {H:.0f} = {HG:.0f} \text {{ N}} ")
        
    #Flange Moments
    with st.expander("Expand to see Flange Moments"):
        st.write("Lever Arms (Table 2-6)")
        R = (C-B)/2-g1
        st.latex(rf"R = \frac{{(C-B)}}{{2}} - g_1 = \frac{{({C}-{B})}}{{{2}}} - {g1} = {R:.1f} \text {{ mm}}")
        hD=R+0.5*g1
        st.latex(rf"h_D = R + 0.5g_1 = {R:.1f} + 0.5 \cdot {g1:.1f} = {hD:.1f} \text {{ mm}}")
        hG = (C-G)/2
        st.latex(rf"h_G = \frac{{(C-G)}}{{2}} = \frac{{({C}-{G:.1f})}}{{{2}}} = {hG:.1f} \text {{ mm}}")
        hT = (R+g1+hG)/2
        st.latex(rf"h_T = \frac{{(R+g1+h_G)}}{{2}} = \frac{{({R:.1f}+{g1:.1f}+{hG:.1f})}}{{{2}}} = {hT:.1f} \text {{ mm}}")

        st.write("Flange Moment in Operating Condition")
        st.latex(r"M_o = H_Dh_D + H_Th_T + H_Gh_G")
        st.latex(rf"M_o = {HD:.0f} \cdot {hD:.1f} + {HT:.0f} \cdot {hT:.1f} + {HG:.0f} \cdot {hG:.1f}")
        Mo = HD*hD+HT*hT+HG*hG
        st.latex(rf"M_o = {Mo:.3e} \text {{ N.mm}}")

        st.write("Flange Moment in Gasket Seating Condition")
        st.latex(r"M_g = W_{gs} \cdot \frac{(C-G)}{2}")
        st.latex(rf"M_g = {Wgs:.0f} \cdot \frac{{{C}-{G}}}{{{2}}}")
        Mg = Wgs*(C-G)/2
        st.latex(rf"M_g = {Mg:.3e} \text {{ N.mm}}")
        
    #Flange Stresses
    with st.expander("Expand to see Flange Stresses (para 2-7)"):
        
        #Operating Condition
        st.write("**Operating Condition**")
        st.write("Longitudinal Hub Stress")
        st.latex(r"S_H = \frac{f \cdot M_o}{L \cdot g_1^2 \cdot B}")
        st.latex(rf"S_H = \frac{{{f} \cdot {Mo:.3e}}}{{{L:.4f} \cdot {g1}^2 \cdot {B}}}")
        SH = f*Mo/(L*g1**2*B)
        st.latex(rf"S_H = {SH:.1f} \text {{ MPa}}")

        st.write("Allowable Stress para (2-8)")
        Sall = min(1.5*Sfo,2.5*Sno)
        st.latex(rf"min(1.5S_{{fo}},2.5S_{{no}}) = min(1.5 \cdot {Sfo},2.5 \cdot {Sno}) = {Sall:.1f} \text {{ MPa}}")        
        if SH <= Sall:
            st.write("Longitudinal Hub Stress Passed [OK]")
        else:
            st.markdown(":red[Longitudinal Hub Stress Failed]")
            
        st.write("Radial Flange Stress")
        st.latex(r"S_R = \frac{(1.33t \cdot e + 1) \cdot M_o}{L \cdot t^2 \cdot B}")
        st.latex(rf"S_R = \frac{{(1.33 \cdot {t} \cdot {e:.4f} + 1) \cdot {Mo:.3e}}}{{{L:.4f} \cdot {t}^2 \cdot {B}}}")
        SR = (1.33*t*e+1)*Mo/(L*t**2*B)
        st.latex(rf"S_R = {SR:.1f} \text {{ MPa}}")

        st.write("Allowable Stress para (2-8)")
        Sall = Sfo
        st.latex(rf"S_{{fo}} = {Sall:.1f} \text {{ MPa}}")        
        if SR <= Sall:
            st.write("Radial Flange Stress Passed [OK]")
        else:
            st.markdown(":red[Radial Flange Stress Failed]")
            
        st.write("Tangential Flange Stress")
        st.latex(r"S_T = \frac{Y \cdot M_o}{t^2 \cdot B} - Z \cdot S_R")
        st.latex(rf"S_T = \frac{{{Y} \cdot {Mo:.3e}}}{{{t}^2 \cdot {B}}} - {{{Z}}} \cdot {{{SR:.1f}}}")
        ST = Y*Mo/(t**2*B) - Z*SR
        st.latex(rf"S_T = {ST:.1f} \text {{ MPa}}")

        st.write("Allowable Stress para (2-8)")
        Sall = Sfo
        st.latex(rf"S_{{fo}} = {Sall:.1f} \text {{ MPa}}")        
        if SR <= Sall:
            st.write("Tangential Flange Stress Passed [OK]")
        else:
            st.markdown(":red[Tangential Flange Stress Failed]")
            
        st.write("Longitudinal + Radial Combined Stress")
        S1 = (SH+SR)/2
        st.latex(rf"\frac{{S_H + S_R}}{{2}} = \frac{{{SH:.1f} + {SR:.1f}}}{{{2}}} = {{{S1:.1f}}} \text {{ MPa}}")
        
        st.write("Allowable Stress para (2-8)")
        Sall = Sfo
        st.latex(rf"S_{{fo}} = {Sall:.1f} \text {{ MPa}}")        
        if S1 <= Sall:
            st.write("Longitudinal + Radial Combined Stress Passed [OK]")
        else:
            st.markdown(":red[Longitudinal + Radial Combined Stress Failed]")
    
        st.write("Longitudinal + Tangential Combined Stress")
        S2 = (SH+ST)/2
        st.latex(rf"\frac{{S_H + S_T}}{{2}} = \frac{{{SH:.1f} + {ST:.1f}}}{{{2}}} = {{{S2:.1f}}} \text {{ MPa}}")
        
        st.write("Allowable Stress para (2-8)")
        Sall = Sfo
        st.latex(rf"S_{{fo}} = {Sall:.1f} \text {{ MPa}}")        
        if S2 <= Sall:
            st.write("Longitudinal + Tangential Combined Stress Passed [OK]")
        else:
            st.markdown(":red[Longitudinal + Tangential Combined Stress Failed]")

        #Gasket Seating Condition
        st.write("**Gasket Seating Condition**")
        st.write("Longitudinal Hub Stress")
        st.latex(r"S_H = \frac{f \cdot M_g}{L \cdot g_1^2 \cdot B}")
        st.latex(rf"S_H = \frac{{{f} \cdot {Mg:.3e}}}{{{L:.4f} \cdot {g1}^2 \cdot {B}}}")
        SH = f*Mg/(L*g1**2*B)
        st.latex(rf"S_H = {SH:.1f} \text {{ MPa}}")

        st.write("Allowable Stress para (2-8)")
        Sall = min(1.5*Sfa,2.5*Sna)
        st.latex(rf"min(1.5S_{{fa}},2.5S_{{na}}) = min(1.5 \cdot {Sfa},2.5 \cdot {Sna}) = {Sall:.1f} \text {{ MPa}}")        
        if SH <= Sall:
            st.write("Longitudinal Hub Stress Passed [OK]")
        else:
            st.markdown(":red[Longitudinal Hub Stress Failed]")
            
        st.write("Radial Flange Stress")
        st.latex(r"S_R = \frac{(1.33t \cdot e + 1) \cdot M_g}{L \cdot t^2 \cdot B}")
        st.latex(rf"S_R = \frac{{(1.33 \cdot {t} \cdot {e:.4f} + 1) \cdot {Mg:.3e}}}{{{L:.4f} \cdot {t}^2 \cdot {B}}}")
        SR = (1.33*t*e+1)*Mg/(L*t**2*B)
        st.latex(rf"S_R = {SR:.1f} \text {{ MPa}}")

        st.write("Allowable Stress para (2-8)")
        Sall = Sfa
        st.latex(rf"S_{{fa}} = {Sall:.1f} \text {{ MPa}}")        
        if SR <= Sall:
            st.write("Radial Flange Stress Passed [OK]")
        else:
            st.markdown(":red[Radial Flange Stress Failed]")
            
        st.write("Tangential Flange Stress")
        st.latex(r"S_T = \frac{Y \cdot M_g}{t^2 \cdot B} - Z \cdot S_R")
        st.latex(rf"S_T = \frac{{{Y} \cdot {Mg:.3e}}}{{{t}^2 \cdot {B}}} - {{{Z}}} \cdot {{{SR:.1f}}}")
        ST = Y*Mg/(t**2*B) - Z*SR
        st.latex(rf"S_T = {ST:.1f} \text {{ MPa}}")

        st.write("Allowable Stress para (2-8)")
        Sall = Sfa
        st.latex(rf"S_{{fa}} = {Sall:.1f} \text {{ MPa}}")        
        if SR <= Sall:
            st.write("Tangential Flange Stress Passed [OK]")
        else:
            st.markdown(":red[Tangential Flange Stress Failed]")
            
        st.write("Longitudinal + Radial Combined Stress")
        S1 = (SH+SR)/2
        st.latex(rf"\frac{{S_H + S_R}}{{2}} = \frac{{{SH:.1f} + {SR:.1f}}}{{{2}}} = {{{S1:.1f}}} \text {{ MPa}}")
        
        st.write("Allowable Stress para (2-8)")
        Sall = Sfa
        st.latex(rf"S_{{fa}} = {Sall:.1f} \text {{ MPa}}")        
        if S1 <= Sall:
            st.write("Longitudinal + Radial Combined Stress Passed [OK]")
        else:
            st.markdown(":red[Longitudinal + Radial Combined Stress Failed]")
    
        st.write("Longitudinal + Tangential Combined Stress")
        S2 = (SH+ST)/2
        st.latex(rf"\frac{{S_H + S_T}}{{2}} = \frac{{{SH:.1f} + {ST:.1f}}}{{{2}}} = {{{S2:.1f}}} \text {{ MPa}}")
        
        st.write("Allowable Stress para (2-8)")
        Sall = Sfa
        st.latex(rf"S_{{fa}} = {Sall:.1f} \text {{ MPa}}")        
        if S2 <= Sall:
            st.write("Longitudinal + Tangential Combined Stress Passed [OK]")
        else:
            st.markdown(":red[Longitudinal + Tangential Combined Stress Failed]")

    #Flange Rigidity Check
    with st.expander("Expand to see Flange Rigidity Check (Table 2-14)"):
        
        #Operating Condition
        st.write("**Operating Condition**")
        st.write("Flange Rigidity Check")
        KI=0.3
        st.latex(rf"K_I = {KI} \text {{ (For Integral Flanges)}}")
        st.latex(r"J = \frac{52.14 \cdot V \cdot M_o}{L \cdot E_d \cdot g_0^2 \cdot K_I \cdot h_o}")
        st.latex(rf"J = \frac{{52.14 \cdot {V} \cdot {Mo:.3e}}}{{{L:.3f} \cdot {Ed} \cdot {g0}^2 \cdot {KI} \cdot {ho:.3f}}}")
        J = 52.14*V*Mo/(L*Ed*g0**2*KI*ho)
        st.latex(rf"J = {J:.3f}")
        if J <= 1:
            st.write("Flange Rigidity Check Passed [OK]")
        else:
            st.markdown(":red[Flange Rigidity Check Failed]")
            
        #Gasket Seating Condition
        st.write("**Gasket Seating Condition**")
        st.write("Flange Rigidity Check")
        st.latex(r"J = \frac{52.14 \cdot V \cdot M_g}{L \cdot E_a \cdot g_0^2 \cdot K_I \cdot h_o}")
        st.latex(rf"J = \frac{{52.14 \cdot {V} \cdot {Mg:.3e}}}{{{L:.3f} \cdot {Ea} \cdot {g0}^2 \cdot {KI} \cdot {ho:.3f}}}")
        J = 52.14*V*Mg/(L*Ea*g0**2*KI*ho)
        st.latex(rf"J = {J:.3f}")
        if J <= 1:
            st.write("Flange Rigidity Check Passed [OK]")
        else:
            st.markdown(":red[Flange Rigidity Check Failed]")



    
    




