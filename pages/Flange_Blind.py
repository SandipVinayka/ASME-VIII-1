import streamlit as st

#Two Columns for inputs and outputs
col1, col2 = st.columns([1,2]) #col2 width is 2*times col1 width

#Input Column
with col1:
    st.title("Inputs")
    
    st.write("**GENERAL DATA**")
    Desc = st.text_input("Description", value="ASME PTB-4 E4.6.1 - Blind Flange")
    P = st.number_input("Internal Design Pressure including static head, P (MPa)",step=0.001, format="%.3f", value=0.931)
    CA = st.number_input("Corrosion Allowance, CA (mm)",step=0.1, format="%.1f", value=3.175)   
    st.write("---")  
     
    st.write("**FLANGE DATA**")
    Sfo = st.number_input("Allowable Stress of flange at internal design temperature, Sfo (MPa)",step=0.1, format="%.1f", value=122.727)
    Sfa = st.number_input("Allowable Stress of flange at ambient temperature, Sfa (MPa)",step=0.1, format="%.1f", value=137.895)
    BCD = st.number_input("Bolt Circle Diameter of the Flange, BCD (mm)",step=1.0, format="%.1f", value=793.75)
    E = st.number_input("Weld Joint Efficiency, E",step=0.01, format="%.2f", value=1.00)
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
    bo = st.number_input("Basic Gasket Width from Table 2-5.2, bo (mm)",step=1.0, format="%.1f", value=5.159)
    
#Output Column
with col2:
    st.title("Outputs")
    st.write("**See Fig 3 - Blind Flange at the ASME Calculator home page**")
    st.write("**CODE: ASME Sec VIII, Div 1 - 2023 Ed.**")
        
    #b and G
    with st.expander("Expand to see effective gasket width and gasket reaction diameter calculation"):
        if bo > 6:
            st.write("Since $b_o > 6$:")
            b = 2.5*bo**0.5
            st.latex(rf"b = 2.5 \sqrt {{b_{{o}}}} = 2.5 \sqrt{{{bo}}} = {b:.3f} \text {{ mm}}")
            G=GOD-2*b
            d = G
            st.latex(rf"d = G = G_{{OD}} - 2b = {{{GOD}}} - 2 \cdot {{{b:.3f}}} = {G:.1f}")
        else:
            st.write("Since $b_o \leq 6$:")
            b = bo
            st.latex(rf"b = b_{{o}} = {b:.3f} \text {{ mm}}")
            G=(GOD+GID)/2
            d = G
            st.latex(rf"d = G = 0.5 \cdot (G_{{OD}} + G_{{ID}}) = 0.5 \cdot ({{{GOD:.1f}}} + {{{GID:.1f}}}) = {G:.1f}")
        
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
        
    #Flange Required Thickness
    with st.expander("Expand to see Flange Required Thickness"):
        st.write("Lever Arm hG (Table 2-6)")
        hG = (BCD-d)/2
        st.latex(rf"h_G = \frac{{(BCD-d)}}{{2}} = \frac{{({BCD}-{d:.1f})}}{{{2}}} = {hG:.1f} \text {{ mm}}")
        C = 0.3
        st.write("Attachment Factor as per UG-34")
        st.latex(rf"C = {C} \text {{ (Refer Fig UG-34 sketch (j) and (k))}}")
        
        st.write("Required Thickness of Flange for operating condition per UG-34(c)(2)")
        st.latex(r"t_o = d \cdot \sqrt{\frac{C \cdot P}{S_{{fo}} \cdot E} + \frac{1.9 \cdot W_o \cdot h_G}{S_{{fo}} \cdot E \cdot d^3}} + CA")
        st.latex(rf"t_o = {{{d}}} \cdot \sqrt{{\frac{{{C} \cdot {P}}}{{{Sfo} \cdot {E}}} + \frac{{1.9 \cdot {Wo:.0f} \cdot {hG:.3f}}}{{{Sfo} \cdot {E} \cdot {d:.1f}^3}}}} + {{{CA}}}")
        to = d*((C*P)/(Sfo*E)+(1.9*Wo*hG)/(Sfo*E*d**3))**0.5 + CA
        st.latex(rf"t_o = {to:.1f} \text {{ mm}}")
        
        st.write("Required Thickness of Flange for gasket seating condition per UG-34(c)(2)")
        st.latex(r"t_g = d \cdot \sqrt{\frac{1.9 \cdot W_{{gs}} \cdot h_G}{S_{{fa}} \cdot E \cdot d^3}} + CA")
        st.latex(rf"t_g = {{{d}}} \cdot \sqrt{{\frac{{1.9 \cdot {Wgs:.0f} \cdot {hG:.3f}}}{{{Sfa} \cdot {E} \cdot {d:.1f}^3}}}} + {{{CA}}}")
        tg = d*((1.9*Wgs*hG)/(Sfa*E*d**3))**0.5 + CA
        st.latex(rf"t_g = {tg:.1f} \text {{ mm}}")
        
        st.write("Required thickness of the flange")
        t = max(to,tg)
        st.latex(rf"t = max(t_o, t_g) = max({to:.1f},{tg:.1f}) = {t:.1f} \text {{ mm}}")
        
        