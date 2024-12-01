import streamlit as st

#Two Columns for inputs and outputs
col1, col2 = st.columns([1,2]) #col2 width is 2*times col1 width

#Input Column
with col1:
    st.title("Inputs")
    
    st.write("**GEOMETRY**")
    Desc = st.text_input("Description", value="ASME PTB-4 E4.5.2, E4.4.1 - Hillside Nozzle on Cylindrical Shell")
    CA = st.number_input("Corrosion Allowance, CA (mm)",step=0.1, format="%.1f", value=3.175)   
    D = st.number_input("Corroded Shell ID, D (mm)",step=1.0, format="%.1f", value=3816.35)
    t = st.number_input("Corroded Shell Thickness, t (mm)",step=0.1, format="%.1f", value=42.863)
    Dn_od = st.number_input("Nozzle OD, Dn_od (mm)",step=1.0, format="%.1f", value=293.624)
    tn = st.number_input("Nozzle Nominal Thickness, tn (mm)",step=0.1, format="%.1f", value=46.863)
    tn_min = st.number_input("Nozzle Nominal Thickness, tn_min (mm)",step=0.1, format="%.1f", value=46.863)
    L = st.number_input("Nozzle Outside Projection, L (mm)",step=0.1, format="%.1f", value=406.4)
    h = st.number_input("Nozzle Inside Projection, h (mm)",step=0.1, format="%.1f", value=0.0)
    ti = st.number_input("Nozzle Inside Projection Corroded Thickness, ti (mm)",step=0.1, format="%.1f", value=0.0)
    ta = st.number_input("Nozzle Neck required thickness for internal, external pressure, supplemental loads + CA, ta (mm)",step=0.1, format="%.1f", value=4.973)
    tug16b = st.number_input("Nozzle Neck min required thickness from UG-16(b) + CA, tug16b (mm)",step=0.1, format="%.1f", value=4.763)    
    tb3 = st.number_input("Nozzle Neck thickness given in Table UG-45 + CA, tb3 (mm)",step=0.1, format="%.1f", value=11.506)    
    Loff = st.number_input("Nozzle Offset from centerline for hillside nozzles, Loff (mm)",step=0.1, format="%.1f", value=885.825)
    Dp1 = st.number_input("Pad Dia in the plane normal to vessel axis, Dp1 (mm)",step=1.0, format="%.1f", value=0.0)
    Dp2 = st.number_input("Pad Dia in the plane parallel to vessel axis, Dp2 (mm)",step=1.0, format="%.1f", value=0.0)
    te = st.number_input("Thickness of RF pad, te (mm)",step=0.1, format="%.1f", value=0.0)
    leg_o = st.number_input("Fillet Weld Leg between nozzle and pad/shell, leg_o (mm)",step=1.0, format="%.1f", value=9.525)
    leg_i = st.number_input("Fillet Weld Leg between nozzle inside projection if any and shell, leg_i (mm)",step=1.0, format="%.1f", value=0.0)
    leg_p = st.number_input("Fillet Weld Leg between pad and shell if pad is present, leg_p (mm)",step=1.0, format="%.1f", value=0.0)
    st.write("---")    

    st.write("**LOADS**")
    P = st.number_input("Internal Design Pressure including static head, P (MPa)",step=0.001, format="%.3f", value=2.455)
    Pe = st.number_input("External Design Pressure, Pe (MPa)",step=0.001, format="%.3f", value=0.0)
    st.write("---")

    st.write("**MATERIAL PROPERTIES**")
    S = st.number_input("Allowable Stress of shell at internal design temperature, S (MPa)",step=0.1, format="%.1f", value=137.895)
    Sn = st.number_input("Allowable Stress of nozzle at internal design temperature, Sn (MPa)",step=0.1, format="%.1f", value=137.895)
    Sp = st.number_input("Allowable Stress of pad at internal design temperature, Sp (MPa)",step=0.1, format="%.1f", value=0.0)
    E = st.number_input("Weld Joint Efficiency for shell, E",step=0.01, format="%.2f", value=1.00)
    En = st.number_input("Weld Joint Efficiency for nozzle, En",step=0.01, format="%.2f", value=1.00)

#Output Column
with col2:
    st.title("Outputs")
    st.write("**See Fig 1 - Hillside Nozzles at the ASME Calculator home page**")
    st.write("**CODE: ASME Sec VIII, Div 1 - 2023 Ed.**")
        
    #Thickness Calculations for internal pressure
    with st.expander("Expand to see thickness calculation for internal pressure"):
        st.write("Corroded Dimensions")
        R=D/2
        Rn=(Dn_od-2*tn)/2
        st.latex(rf"R = \frac{{D}}{{2}} = {R:0.1f} \text{{ mm}}")
        st.latex(rf"R_n = \frac{{D_{{nOD}}-2 \cdot t_n}}{{2}} = {Rn:0.1f} \text{{ mm}}")
        
        if P > 0.385*S*E:
            st.markdown(":red[P > 0.385SE, UG-27 (c)(1) not valid]")
        st.write("**Min Corroded Required Thickness of shell under internal presssure UG-27 (c)(1)**")
        st.latex(r"""t_r = {PR \over SE-0.6P}""")
        st.latex(rf"""t_r = \frac{{{P} \cdot {R}}}{{{S} \cdot {E} - 0.6 \cdot {P}}}""")
        tr = P*R/(S*E-0.6*P)
        st.latex(rf"""t = {tr:0.1f} mm""")
        
        st.write("**Min Corroded Required Thickness of nozzle under internal presssure UG-27 (c)(1)**")
        st.latex(r"""t_{rn} = {PR_n \over S_nE_n-0.6P}""")
        st.latex(rf"""t_{{rn}} = \frac{{{P} \cdot {Rn:.1f}}}{{{Sn} \cdot {En} - 0.6 \cdot {P}}}""")
        trn = P*Rn/(Sn*En-0.6*P)
        st.latex(rf"""t_{{rn}} = {trn:0.1f} mm""")

    #Limits of reinforcement per UG-40
    with st.expander("Expand to see Limits of reinforcement calculation per UG-40"):
        
        #Finished opening chord length - Plane Perpendicular to longitudinal axis
        st.write("Finished opening chord length - Plane Perpendicular to longitudinal axis")
        st.latex(r"R_m = R + \frac{t_r}{2}")
        st.latex(rf"R_m = {R} + \frac{{{tr:.1f}}}{{{2}}}")
        Rm = R + tr/2
        st.latex(rf"R_m = {Rm:.1f} \text {{ mm}}")

        st.latex(r"x_1 = L_{off} + R_n")
        st.latex(rf"x_1 = {Loff} + {Rn:.1f}")
        x1 = Loff + Rn
        st.latex(rf"x_1 = {x1:.1f} \text {{ mm}}")

        st.latex(r"x_2 = L_{off} - R_n")
        st.latex(rf"x_2 = {Loff} - {Rn:.1f}")
        x2 = Loff - Rn
        st.latex(rf"x_2 = {x2:.1f} \text {{ mm}}")
        
        st.latex(r"y_1 = \sqrt {R_m^2-x_1^2}")
        st.latex(rf"y_1 = \sqrt {{{Rm:.1f}^2-{x1:.1f}^2}}")
        y1 = (Rm**2 - x1**2)**0.5
        st.latex(rf"y_1 = {y1:.1f} \text {{ mm}}")

        st.latex(r"y_2 = \sqrt {R_m^2-x_2^2}")
        st.latex(rf"y_2 = \sqrt {{{Rm:.1f}^2-{x2:.1f}^2}}")
        y2 = (Rm**2 - x2**2)**0.5
        st.latex(rf"y_2 = {y2:.1f} \text {{ mm}}")

        st.latex(r"d_1 = \sqrt {(x_1-x_2)^2 + (y_2-y_1)^2}")
        st.latex(rf"d_1 = \sqrt {{({x1:.1f}-{x2:.1f})^2 + ({y2:.1f}-{y1:.1f})^2}}")
        d1 = ((x1-x2)**2 + (y2-y1)**2)**0.5
        st.latex(rf"d_1 = {d1:.1f} \text {{ mm}}")
    
        #Finished opening chord length - Plane Parallel to longitudinal axis
        st.write("Finished opening chord length - Plane Parallel to longitudinal axis")
        st.latex(r"d_2 = 2 \cdot R_n")
        st.latex(rf"d_2 = 2 \cdot {Rn:.1f}")
        d2 = 2*Rn
        st.latex(rf"d_2 = {d2:.1f} \text {{ mm}}")
        
        #Limits of reinforcement parallel to vessel wall - perpendicular to longitudinal axis
        st.write("Limits of reinforcement parallel to vessel wall - perpendicular to londgitudinal axis")
        st.latex(rf"max(d_1, R_n + t_n + t) = max({d1:.1f},{Rn:.1f}+{tn}+{t}) = {max(d1,Rn+tn+t):.1f} \text {{ mm}}")
    
        #Limits of reinforcement parallel to vessel wall - parallel to longitudinal axis
        st.write("Limits of reinforcement parallel to vessel wall - parallel to londgitudinal axis")
        st.latex(rf"max(d_2, R_n + t_n + t) = max({d2:.1f},{Rn:.1f}+{tn}+{t}) = {max(d2,Rn+tn+t):.1f} \text {{ mm}}")

        #Limits of reinforcement normal to vessel wall
        st.write("Limits of reinforcement normal to vessel wall")
        st.latex(rf"min(2.5t, 2.5t_n+t_e) = min(2.5 \cdot {t}, 2.5 \cdot {tn} + {te}) = {min(2.5*t,2.5*tn+te):.1f} \text {{ mm}}")
        
    #Reinforcement strength parameters calculation per UG-37
    with st.expander("Expand to see Reinforcement strength parameters calculation per UG-37"):
        
        #Strength Reduction Factors
        st.write("Strength Reduction Factors")
        st.latex(r"f_{r1} = \frac{S_n}{S} \text { (Assumed nozzle inserted through the vessel wall)}")
        fr1=Sn/S
        st.latex(rf"f_{{r1}} = \frac{{{Sn}}}{{{S}}} = {fr1:.3f}")

        st.latex(r"f_{r2} = \frac{S_n}{S}")
        fr2=Sn/S
        st.latex(rf"f_{{r2}} = \frac{{{Sn}}}{{{S}}} = {fr2:.3f}")

        st.latex(r"f_{r3} = \frac{min(S_n, S_p)}{S}")
        fr3=min(Sn,Sp)/S
        st.latex(rf"f_{{r3}} = \frac{{min({Sn},{Sp})}}{{{S}}} = {fr3:.3f}")

        st.latex(r"f_{r4} = \frac{S_p}{S}")
        fr4=Sp/S
        st.latex(rf"f_{{r4}} = \frac{{{Sp}}}{{{S}}} = {fr4:.3f}")

        st.write("Joint Efficiency Parameter")
        E1=1
        st.latex(rf"E_1 = {E1} \text {{ (Assumed nozzle is in a solid plate or a cat B butt joint)}}")
        
        st.write("Factor F Computation")
        st.write("For integrally reinforced opening, plane perpendicular to longitudinal axis")
        F1 = 0.5
        st.latex(rf"F_1 = {F1}")
        
        st.write("For integrally reinforced opening, plane parallel to longitudinal axis")
        F2 = 1
        st.latex(rf"F_2 = {F2}")

    #Area of reinforcement calculation for plane perpendicular to longitudinal axis
    with st.expander("Expand to see Area of reinforcement calculation for plane perpendicular to longitudinal axis"):
        
        #Area Required
        st.write("Area Required")
        st.latex(r"A = d_1t_rF_1 + 2t_nt_rF_1(1-f_{r1})")
        st.latex(rf"A = {d1:.1f} \cdot {tr:.1f} \cdot {F1} + 2 \cdot {tn} \cdot {tr:.1f} \cdot {F1} \cdot (1-{fr1:.3f})")
        A = d1*tr*F1 + 2*tn*tr*F1*(1-fr1)
        st.latex(rf"A = {A:.1f} \text {{ mm}}^2")
        
        #Area available in shell
        st.write("Area Available in shell")
       
        st.latex(r"A_{11} = d_1(E_1t - F_1t_r) -2t_n(E_1t-F_1t_r)(1-f_{r1})")
        st.latex(rf"A_{{11}} = {d1:.1f} \cdot ({E1} \cdot {t} - {F1} \cdot {tr:.1f}) - 2 \cdot {tn} \cdot ({E1} \cdot {t} - {F1} \cdot {tr:.1f}) \cdot (1-{fr1:.3f})")
        A11 = d1*(E1*t-F1*tr)-2*tn*(E1*t-F1*tr)*(1-fr1)
        st.latex(rf"A_{{11}} = {A11:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{12} = 2(t+t_n)(E_1t - F_1t_r) -2t_n(E_1t-F_1t_r)(1-f_{r1})")
        st.latex(rf"A_{{12}} = 2 \cdot ({t} + {tn}) \cdot ({E1} \cdot {t} - {F1} \cdot {tr:.1f}) - 2 \cdot {tn} \cdot ({E1} \cdot {t} - {F1} \cdot {tr:.1f}) \cdot (1-{fr1:.3f})")
        A12 = 2*(t+tn)*(E1*t-F1*tr)-2*tn*(E1*t-F1*tr)*(1-fr1)
        st.latex(rf"A_{{12}} = {A12:.1f} \text {{ mm}}^2")
        
        A1 = max(A11, A12)
        st.latex(rf"A_1 = max({A11:.1f}, {A12:.1f}) = {A1:.1f} \text {{ mm}}^2")
        
        #Area available in outward projection of nozzle
        st.write("Area Available in outward projection of nozzle")
        
        st.latex(r"A_{21} = 5(t_n-t_{rn})f_{r2}t")
        st.latex(rf"A_{{21}} = 5 \cdot ({tn} - {trn:.1f}) \cdot {fr2} \cdot {t}")
        A21 = 5*(tn-trn)*fr2*t
        st.latex(rf"A_{{21}} = {A21:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{22} = 2(t_n-t_{rn})(2.5t_n+t_e)f_{r2}")
        st.latex(rf"A_{{22}} = 2 \cdot ({tn} - {trn:.1f}) \cdot (2.5 \cdot {tn} + {te}) \cdot {fr2}")
        A22 = 2*(tn-trn)*(2.5*tn+te)*fr2
        st.latex(rf"A_{{22}} = {A22:.1f} \text {{ mm}}^2")
        
        A2 = min(A21, A22)
        st.latex(rf"A_2 = min({A21:.1f}, {A22:.1f}) = {A2:.1f} \text {{ mm}}^2")
        
        #Area available in inward projection of nozzle
        st.write("Area Available in inward projection of nozzle")
        
        st.latex(r"A_{31} = 5 \cdot t \cdot t_i \cdot f_{r2}")
        st.latex(rf"A_{{31}} = 5 \cdot {t} \cdot {ti} \cdot {fr2}")
        A31 = 5*t*ti*fr2
        st.latex(rf"A_{{31}} = {A31:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{32} = 5 \cdot t_i \cdot t_i \cdot f_{r2}")
        st.latex(rf"A_{{32}} = 5 \cdot {ti} \cdot {ti} \cdot {fr2}")
        A32 = 5*ti*ti*fr2
        st.latex(rf"A_{{32}} = {A32:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{33} = 2 \cdot h \cdot t_i \cdot f_{r2}")
        st.latex(rf"A_{{33}} = 2 \cdot {h} \cdot {ti} \cdot {fr2}")
        A33 = 2*h*ti*fr2
        st.latex(rf"A_{{33}} = {A33:.1f} \text {{ mm}}^2")
        
        A3 = min(A31, A32, A33)
        st.latex(rf"A_3 = min({A31:.1f}, {A32:.1f}, {A33:.1f}) = {A3:.1f} \text {{ mm}}^2")

        #Area available in welds
        st.write("Area Available in welds")
       
        st.latex(r"A_{41} = leg_o^2 \cdot f_{r2}")
        st.latex(rf"A_{{41}} = {leg_o}^2 \cdot {fr2}")
        A41 = leg_o**2*fr2
        st.latex(rf"A_{{41}} = {A41:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{42} = leg_p^2 \cdot f_{r4}")
        st.latex(rf"A_{{42}} = {leg_p}^2 \cdot {fr4}")
        A42 = leg_p**2*fr4
        st.latex(rf"A_{{42}} = {A42:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{43} = leg_i^2 \cdot f_{r2}")
        st.latex(rf"A_{{43}} = {leg_i}^2 \cdot {fr2}")
        A43 = leg_i**2*fr2
        st.latex(rf"A_{{43}} = {A43:.1f} \text {{ mm}}^2")
        
        #Area available in pad
        st.write("Area Available in pad")
        if te==0:
            A5 = 0
            st.latex(r"A_5 = 0 \text {{ mm}}^2")
        else:
            st.write("Limit Dp1 within limits of reinforcement for the purpose of calculation")
            st.latex(r"A_5 = (D_{p1}-d_1-2t_n)t_ef_{r4}")
            st.latex(rf"A_5 = ({Dp1} - {d1:.1f} - 2 \cdot {tn}) \cdot {te} \cdot {fr4}")
            A5 = (Dp1-d1-2*tn)*te*fr4
            st.latex(rf"A_5 = {A5:.1f} \text {{ mm}}^2")
            
        #Total Area Available
        st.write("Total Area Available")
        st.latex(r"A_{avail} = A_1 + A_2 + A_3 + (A_{41} + A_{42} + A_{43}) + A_5")
        st.latex(rf"A_{{avail}} = {A1:.1f} + {A2:.1f} + {A3:.1f} + ({A41:.1f} + {A42:.1f} + {A43:.1f}) + {A5:.1f}")
        Aavail = A1+A2+A3+A41+A42+A43+A5
        st.latex(rf"A_{{avail}} = {Aavail:.1f} \text {{ mm}}^2")
        
        if Aavail>A:
            st.latex(r"A_{avail}>A \text { [OK]}")
        else:
            st.markdown(":red[Area Reinforcement Failed]")
        
    #Area of reinforcement calculation for plane parallel to longitudinal axis
    with st.expander("Expand to see Area of reinforcement calculation for plane parallel to longitudinal axis"):
        
        #Area Required
        st.write("Area Required")
        st.latex(r"A = d_2t_rF_2 + 2t_nt_rF_2(1-f_{r1})")
        st.latex(rf"A = {d2:.1f} \cdot {tr:.1f} \cdot {F2} + 2 \cdot {tn} \cdot {tr:.1f} \cdot {F2} \cdot (1-{fr1:.3f})")
        A = d2*tr*F2 + 2*tn*tr*F2*(1-fr1)
        st.latex(rf"A = {A:.1f} \text {{ mm}}^2")
        
        #Area available in shell
        st.write("Area Available in shell")
       
        st.latex(r"A_{11} = d_2(E_1t - F_2t_r) -2t_n(E_1t-F_2t_r)(1-f_{r1})")
        st.latex(rf"A_{{11}} = {d2:.1f} \cdot ({E1} \cdot {t} - {F2} \cdot {tr:.1f}) - 2 \cdot {tn} \cdot ({E1} \cdot {t} - {F2} \cdot {tr:.1f}) \cdot (1-{fr1:.3f})")
        A11 = d2*(E1*t-F2*tr)-2*tn*(E1*t-F2*tr)*(1-fr1)
        st.latex(rf"A_{{11}} = {A11:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{12} = 2(t+t_n)(E_1t - F_2t_r) -2t_n(E_1t-F_2t_r)(1-f_{r1})")
        st.latex(rf"A_{{12}} = 2 \cdot ({t} + {tn}) \cdot ({E1} \cdot {t} - {F2} \cdot {tr:.1f}) - 2 \cdot {tn} \cdot ({E1} \cdot {t} - {F2} \cdot {tr:.1f}) \cdot (1-{fr1:.3f})")
        A12 = 2*(t+tn)*(E1*t-F2*tr)-2*tn*(E1*t-F2*tr)*(1-fr1)
        st.latex(rf"A_{{12}} = {A12:.1f} \text {{ mm}}^2")
        
        A1 = max(A11, A12)
        st.latex(rf"A_1 = max({A11:.1f}, {A12:.1f}) = {A1:.1f} \text {{ mm}}^2")
        
        #Area available in outward projection of nozzle
        st.write("Area Available in outward projection of nozzle")
        
        st.latex(r"A_{21} = 5(t_n-t_{rn})f_{r2}t")
        st.latex(rf"A_{{21}} = 5 \cdot ({tn} - {trn:.1f}) \cdot {fr2} \cdot {t}")
        A21 = 5*(tn-trn)*fr2*t
        st.latex(rf"A_{{21}} = {A21:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{22} = 2(t_n-t_{rn})(2.5t_n+t_e)f_{r2}")
        st.latex(rf"A_{{22}} = 2 \cdot ({tn} - {trn:.1f}) \cdot (2.5 \cdot {tn} + {te}) \cdot {fr2}")
        A22 = 2*(tn-trn)*(2.5*tn+te)*fr2
        st.latex(rf"A_{{22}} = {A22:.1f} \text {{ mm}}^2")
        
        A2 = min(A21, A22)
        st.latex(rf"A_2 = min({A21:.1f}, {A22:.1f}) = {A2:.1f} \text {{ mm}}^2")
        
        #Area available in inward projection of nozzle
        st.write("Area Available in inward projection of nozzle")
        
        st.latex(r"A_{31} = 5 \cdot t \cdot t_i \cdot f_{r2}")
        st.latex(rf"A_{{31}} = 5 \cdot {t} \cdot {ti} \cdot {fr2}")
        A31 = 5*t*ti*fr2
        st.latex(rf"A_{{31}} = {A31:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{32} = 5 \cdot t_i \cdot t_i \cdot f_{r2}")
        st.latex(rf"A_{{32}} = 5 \cdot {ti} \cdot {ti} \cdot {fr2}")
        A32 = 5*ti*ti*fr2
        st.latex(rf"A_{{32}} = {A32:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{33} = 2 \cdot h \cdot t_i \cdot f_{r2}")
        st.latex(rf"A_{{33}} = 2 \cdot {h} \cdot {ti} \cdot {fr2}")
        A33 = 2*h*ti*fr2
        st.latex(rf"A_{{33}} = {A33:.1f} \text {{ mm}}^2")
        
        A3 = min(A31, A32, A33)
        st.latex(rf"A_3 = min({A31:.1f}, {A32:.1f}, {A33:.1f}) = {A3:.1f} \text {{ mm}}^2")

        #Area available in welds
        st.write("Area Available in welds")
       
        st.latex(r"A_{41} = leg_o^2 \cdot f_{r2}")
        st.latex(rf"A_{{41}} = {leg_o}^2 \cdot {fr2}")
        A41 = leg_o**2*fr2
        st.latex(rf"A_{{41}} = {A41:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{42} = leg_p^2 \cdot f_{r4}")
        st.latex(rf"A_{{42}} = {leg_p}^2 \cdot {fr4}")
        A42 = leg_p**2*fr4
        st.latex(rf"A_{{42}} = {A42:.1f} \text {{ mm}}^2")
        
        st.latex(r"A_{43} = leg_i^2 \cdot f_{r2}")
        st.latex(rf"A_{{43}} = {leg_i}^2 \cdot {fr2}")
        A43 = leg_i**2*fr2
        st.latex(rf"A_{{43}} = {A43:.1f} \text {{ mm}}^2")
        
        #Area available in pad
        st.write("Area Available in pad")
        if te==0:
            A5 = 0
            st.latex(r"A_5 = 0 \text {{ mm}}^2")
        else:
            st.write("Limit Dp2 within limits of reinforcement for the purpose of calculation")
            st.latex(r"A_5 = (D_{p2}-d_2-2t_n)t_ef_{r4}")
            st.latex(rf"A_5 = ({Dp2} - {d2:.1f} - 2 \cdot {tn}) \cdot {te} \cdot {fr4}")
            A5 = (Dp2-d2-2*tn)*te*fr4
            st.latex(rf"A_5 = {A5:.1f} \text {{ mm}}^2")
            
        #Total Area Available
        st.write("Total Area Available")
        st.latex(r"A_{avail} = A_1 + A_2 + A_3 + (A_{41} + A_{42} + A_{43}) + A_5")
        st.latex(rf"A_{{avail}} = {A1:.1f} + {A2:.1f} + {A3:.1f} + ({A41:.1f} + {A42:.1f} + {A43:.1f}) + {A5:.1f}")
        Aavail = A1+A2+A3+A41+A42+A43+A5
        st.latex(rf"A_{{avail}} = {Aavail:.1f} \text {{ mm}}^2")
        
        if Aavail>A:
            st.latex(r"A_{avail}>A \text { [OK]}")
        else:
            st.markdown(":red[Area Reinforcement Failed]")
        
    #Min Nozzle Neck Thk requirement per UG-45
    with st.expander("Expand to see Min Nozzle Neck Thk requirement per UG-45"):
        
        #Access Openings
        st.write("For Access Openings and Openings used only for inspection")
        st.latex(rf"t_a = {ta} \text {{ mm [USER INPUT]}}")
        t_UG45 = ta
        st.latex(rf"t_{{UG-45}} = t_a = {t_UG45} \text {{ mm}}")
        st.latex(rf"t_{{n-min}} = {tn_min} \text {{ mm [USER INPUT]}}")
        if tn_min>=t_UG45:
            st.write("Min thk > requirement per UG-45 [OK]")
        else:
            st.markdown(":red[UG-45 Nozzle Neck Thk Criteria Failed]")

        #For Other Nozzles
        st.write("For nozzles other than Access Openings and Openings used only for inspection")
        st.latex(rf"t_{{UG-16b}} = {tug16b} \text {{ mm [USER INPUT]}}")
        st.latex(r"t_{{b1}} = max \left (\frac{{PR}}{{S \cdot 1 - 0.6P}} + CA, t_{{UG-16b}} \right)")
        st.latex(rf"t_{{b1}} = max \left (\frac{{{P} \cdot {R}}}{{{S} \cdot 1 - 0.6 \cdot {P}}} + {{{CA}}}, {{{tug16b}}} \right)")
        tb11 = P*R/(S*1-0.6*P) + CA
        st.latex(rf"t_{{b1}} = max({tb11:.1f},{tug16b:.1f})")
        tb1 = max(tb11, tug16b)
        st.latex(rf"t_{{b1}} = {tb1:.1f} \text {{ mm}}")
        
        st.latex(r"t_{{b2}} = max \left (\frac{{PeR}}{{S \cdot 1 - 0.6P}} + CA, t_{{UG-16b}} \right)")
        st.latex(rf"t_{{b2}} = max \left (\frac{{{Pe} \cdot {R}}}{{{S} \cdot 1 - 0.6 \cdot {P}}} + {{{CA}}}, {{{tug16b}}} \right)")
        tb21 = Pe*R/(S*1-0.6*P) + CA
        st.latex(rf"t_{{b2}} = max({tb21:.1f},{tug16b:.1f})")
        tb2 = max(tb21, tug16b)
        st.latex(rf"t_{{b2}} = {tb2:.1f} \text {{ mm}}")
        
        st.latex(rf"t_{{b3}} = {tb3} \text {{ mm [USER INPUT]}}")
        
        st.latex(r"t_b = min(t_{b3}, max(t_{b1}, t_{b2}))")
        st.latex(rf"t_b = min({tb3}, max({tb1:.1f}, {tb2:.1f}))")
        tb = min(tb3, max(tb1,tb2))
        st.latex(rf"t_b = {tb:.1f} \text {{ mm}}")
        
        st.latex(r"t_{{UG-45}} = max(t_a, t_b)")
        st.latex(rf"t_{{UG-45}} = max({ta}, {tb:.1f})")
        t_UG45 = max(ta,tb)
        st.latex(rf"t_{{UG-45}} = {t_UG45:.1f} \text {{ mm}}")
        
        st.latex(rf"t_{{n-min}} = {tn_min} \text {{ mm [USER INPUT]}}")
        if tn_min>=t_UG45:
            st.write("Min thk > requirement per UG-45 [OK]")
        else:
            st.markdown(":red[UG-45 Nozzle Neck Thk Criteria Failed]")

    #Min Required Weld Leg per UW-16.1
    with st.expander("Expand to see Min Required Weld Leg per UW-16.1"):
        #Nozzle to shell/pad weld
        st.write("Fillet weld leg at nozzle to shell/pad junction")
        if te==0:
            st.latex(r"t_{min} = min(19, t_n, t)")
            st.latex(rf"t_{{min}} = min(19, {tn}, {t})")
            tmin = min(19,tn,t)
            st.latex(rf"t_{{min}} = {tmin} \text {{ mm}}")
            tc = 0.7*leg_o
            st.latex(rf"t_c = 0.7 \cdot leg_o = {0.7*leg_o:.1f} \text {{ mm}}")
            min_weld_leg = min(6, 0.7*tmin)
            st.latex(rf"MinWeldLeg = min(6,0.7 \cdot t_{{min}}) = min(6,0.7 \cdot {tmin}) = {min_weld_leg:.1f} \text {{ mm}}")
            if tc >= min_weld_leg:
                st.write("tc > min required weld leg [OK]")
            else:
                st.markdown(":red[Weld not sufficient]")
        else:
            st.latex(r"t_{min} = min(19, t_n, te)")
            st.latex(rf"t_{{min}} = min(19, {tn}, {te})")
            tmin = min(19,tn,te)
            st.latex(rf"t_{{min}} = {tmin} \text {{ mm}}")
            tc = 0.7*leg_o
            st.latex(rf"t_c = 0.7 \cdot leg_o = {0.7*leg_o:.1f} \text {{ mm}}")
            min_weld_leg = min(6, 0.7*tmin)
            st.latex(rf"MinWeldLeg = min(6,0.7 \cdot t_{{min}}) = min(6,0.7 \cdot {tmin}) = {min_weld_leg:.1f} \text {{ mm}}")
            if tc >= min_weld_leg:
                st.write("tc > min required weld leg [OK]")
            else:
                st.markdown(":red[Weld not sufficient]")
                
        #Pad to shell weld
        if te!=0:
            st.write("Fillet weld leg at pad to shell junction")
            st.latex(r"t_{min} = min(19, t_e, t)")
            st.latex(rf"t_{{min}} = min(19, {te}, {t})")
            tmin = min(19,te,t)
            st.latex(rf"t_{{min}} = {tmin} \text {{ mm}}")
            tc = 0.7*leg_p
            st.latex(rf"t_c = 0.7 \cdot leg_p = {0.7*leg_p:.1f} \text {{ mm}}")
            min_weld_leg = min(6, 0.7*tmin)
            st.latex(rf"MinWeldLeg = min(6,0.7 \cdot t_{{min}}) = min(6,0.7 \cdot {tmin}) = {min_weld_leg:.1f} \text {{ mm}}")
            if tc >= min_weld_leg:
                st.write("tc > min required weld leg [OK]")
            else:
                st.markdown(":red[Weld not sufficient]")
        
        #Nozzle inside projection to shell weld
        if ti!=0:
            st.write("Fillet weld leg at nozzle inside projection to shell junction")
            st.latex(r"t_{min} = min(19, t_i, t)")
            st.latex(rf"t_{{min}} = min(19, {ti}, {t})")
            tmin = min(19,ti,t)
            st.latex(rf"t_{{min}} = {tmin} \text {{ mm}}")
            tc = 0.7*leg_i
            st.latex(rf"t_c = 0.7 \cdot leg_i = {0.7*leg_i:.1f} \text {{ mm}}")
            min_weld_leg = min(6, 0.7*tmin)
            st.latex(rf"MinWeldLeg = min(6,0.7 \cdot t_{{min}}) = min(6,0.7 \cdot {tmin}) = {min_weld_leg:.1f} \text {{ mm}}")
            if tc >= min_weld_leg:
                st.write("tc > min required weld leg [OK]")
            else:
                st.markdown(":red[Weld not sufficient]")
        
            
  
   
        
        