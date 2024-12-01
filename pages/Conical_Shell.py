import streamlit as st
from math import tan,cos, pi

#Two Columns for inputs and outputs
col1, col2 = st.columns([1,2]) #col2 width is 2*times col1 width

#Input Column
with col1:
    st.title("Inputs")
    
    st.write("**GEOMETRY**")
    Desc = st.text_input("Description", value="ASME PTB-4 E4.3.2, E4.4.2 - Conical Shell")
    CA = st.number_input("Corrosion Allowance, CA (mm)",step=0.1, format="%.1f", value=3.175)   
    D = st.number_input("Corroded Inside Diameter at Large End, D (mm)",step=1.0, format="%.1f", value=3816.35)
    alpha = st.number_input("One-half the apex angle, alpha (deg)",step=1.0, format="%.1f", value=21.0375)
    Lc = st.number_input("Axial Length of cone, Lc (mm)",step=1.0, format="%.1f", value=1981.2)
    Ll = st.number_input("Length of Cylinder at Large End, Ll (mm)",step=1.0, format="%.1f", value=3000.0)
    Ls = st.number_input("Length of Cylinder at Small End, Ls (mm)",step=1.0, format="%.1f", value=3000.0)
    tc = st.number_input("Provided Nominal Thickness of cone, tc (mm)",step=0.1, format="%.1f", value=49.2125)
    tlnom = st.number_input("Provided Nominal Thickness of cylinder at large end, tlnom (mm)",step=0.1, format="%.1f", value=46.0375)
    tsnom = st.number_input("Provided Nominal Thickness of cylinder at Small end, tlnom (mm)",step=0.1, format="%.1f", value=28.575)
    trc = st.number_input("Required Corroded Thickness of cone for all combination of loads, trc (mm)",step=0.1, format="%.1f", value=36.763)
    trl = st.number_input("Required Corroded Thickness of large end cylinder for all combination of loads, trl (mm)",step=0.1, format="%.1f", value=34.332)
    trs = st.number_input("Required Corroded Thickness of Small end cylinder for all combination of loads, trs (mm)",step=0.1, format="%.1f", value=20.622)
    Asl = st.number_input("Area of stiffening ring if any at the large end, Asl (mm2)",step=0.1, format="%.1f", value=0.0)
    Ass = st.number_input("Area of stiffening ring if any at the Small end, Ass (mm2)",step=0.1, format="%.1f", value=0.0)
    Il = st.number_input("Moment of Inertia of stiffening ring if any at the large end, Il (mm4)",step=0.1, format="%.1f", value=8.0e6)
    Is = st.number_input("Moment of Inertia of stiffening ring if any at the Small end, Is (mm4)",step=0.1, format="%.1f", value=8.0e6)
    st.write("---")    

    st.write("**LOADS**")
    P = st.number_input("Internal Design Pressure including static head, P (MPa)",step=0.001, format="%.3f", value=2.455)
    Pe = st.number_input("External Design Pressure, Pe (MPa)",step=0.001, format="%.3f", value=0.1034)
    f1i = st.number_input("axial load per unit circumference at large end due to wind, dead load, etc., excluding pressure for internal pressure design, f1i (N/mm)",step=0.001, format="%.3f", value=0.0)
    f2i = st.number_input("axial load per unit circumference at Small end due to wind, dead load, etc., excluding pressure for internal pressure design, f2i (N/mm)",step=0.001, format="%.3f", value=0.0)
    f1e = st.number_input("axial load per unit circumference at large end due to wind, dead load, etc., excluding pressure for external pressure design, f1e (N/mm)",step=0.001, format="%.3f", value=0.0)
    f2e = st.number_input("axial load per unit circumference at Small end due to wind, dead load, etc., excluding pressure for external pressure design, f2e (N/mm)",step=0.001, format="%.3f", value=0.0)    
    st.write("---")

    st.write("**MATERIAL PROPERTIES**")
    S = st.number_input("Allowable Stress of Material at internal design temperature, S (MPa)",step=0.1, format="%.1f", value=138.0)
    Se = st.number_input("Allowable Stress of Material at external design temperature, Se (MPa)",step=0.1, format="%.1f", value=138.0)
    E = st.number_input("Weld Joint Efficiency, E",step=0.01, format="%.2f", value=1.00)
    A = st.number_input("Factor A from Fig G of ASME II-D for MAEWP calculation, A",step=1.0, format="%.3e", value=0.0042)
    B = st.number_input("Factor from applicable material chart of ASME II-D for MAEWP calculation, B (MPa)",step=0.001, format="%.3f", value=117.0)
    A1 = st.number_input("Factor A from Fig G of ASME II-D for M.I calculation at large end, A1",step=1.0, format="%.3e", value=0.000060)
    A2 = st.number_input("Factor A from Fig G of ASME II-D for M.I calculation at large end, A1",step=1.0, format="%.3e", value=0.000056)

#Output Column
alpha_rad = alpha*pi/180
with col2:
    st.title("Outputs")
    
    #Draw Sketch
    ###########################################################################
    
    import plotly.graph_objects as go
    import numpy as np
    
    # Define parameters for the frustum and cylinders
    top_radius = 2
    bottom_radius = 4
    height = 5
    cylinder_height = 2
    sides = 50  # Number of sides for the approximation
    
    # Create the frustum
    theta = np.linspace(0, 2 * np.pi, sides)
    x_top = top_radius * np.cos(theta)
    x_bottom = bottom_radius * np.cos(theta)
    y_top = [height] * sides
    y_bottom = [0] * sides
    
    # Create the 2D plot
    fig = go.Figure()
    
    # Common line color and weight
    line_color = 'blue'
    line_weight = 2
    
    # Add the top and bottom circles of the frustum
    fig.add_trace(go.Scatter(x=x_top, y=y_top, mode='lines', line=dict(color=line_color, width=line_weight), showlegend=False))
    fig.add_trace(go.Scatter(x=x_bottom, y=y_bottom, mode='lines', line=dict(color=line_color, width=line_weight), showlegend=False))
    
    # Add the leftmost and rightmost generators of the frustum
    fig.add_trace(go.Scatter(x=[x_top[0], x_bottom[0]], y=[height, 0], mode='lines', line=dict(color=line_color, width=line_weight), showlegend=False))
    fig.add_trace(go.Scatter(x=[x_top[sides//2], x_bottom[sides//2]], y=[height, 0], mode='lines', line=dict(color=line_color, width=line_weight), showlegend=False))
    
    # Add the top and bottom cylinders
    cylinder_top_y = [height + cylinder_height] * sides
    cylinder_bottom_y = [-cylinder_height] * sides
    fig.add_trace(go.Scatter(x=x_top, y=cylinder_top_y, mode='lines', line=dict(color=line_color, width=line_weight), showlegend=False))
    fig.add_trace(go.Scatter(x=x_bottom, y=cylinder_bottom_y, mode='lines', line=dict(color=line_color, width=line_weight), showlegend=False))
    
    # Add the leftmost and rightmost generators of the cylinders
    fig.add_trace(go.Scatter(x=[x_top[0], x_top[0]], y=[height, height + cylinder_height], mode='lines', line=dict(color=line_color, width=line_weight), showlegend=False))
    fig.add_trace(go.Scatter(x=[x_top[sides//2], x_top[sides//2]], y=[height, height + cylinder_height], mode='lines', line=dict(color=line_color, width=line_weight), showlegend=False))
    fig.add_trace(go.Scatter(x=[x_bottom[0], x_bottom[0]], y=[0, -cylinder_height], mode='lines', line=dict(color=line_color, width=line_weight), showlegend=False))
    fig.add_trace(go.Scatter(x=[x_bottom[sides//2], x_bottom[sides//2]], y=[0, -cylinder_height], mode='lines', line=dict(color=line_color, width=line_weight), showlegend=False))
    
    fig.add_annotation(
        x=0, y=-cylinder_height/2,
        text=f'Large End:      ID {D-2*CA}  x Thk {tlnom} x Length {Ll}',
        showarrow=False,
        font=dict(size=12, color="Black")
    )
    
    fig.add_annotation(
        x=0, y=height/2,
        text=f'Cone:      Alpha {alpha} deg  x Thk {tc} x Axial Length {Lc}',
        showarrow=False,
        font=dict(size=12, color="Black")
    )
    
    fig.add_annotation(
        x=0, y=height + cylinder_height/2,
        text=f'Small End:      ID {D - 2*Lc*tan(alpha_rad) - 2*CA:.1f}  x Thk {tsnom} x Length {Ls}',
        showarrow=False,
        font=dict(size=12, color="Black")
    )

    
   # Update layout to remove axes, grids, and labels
    fig.update_layout(
        title=f'Conical Shell (All dimensions in mm)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white'
    )
    
    # Show plot in Streamlit
    st.plotly_chart(fig)

    ###########################################################################
    
    st.write("**CODE: ASME Sec VIII, Div 1 - 2023 Ed.**")
    st.write("Assumptions")
    st.write("MOC and E are same for all components")
    st.write("Knuckles are not present in the cone")
    st.write("Both ends are line of support")
    
    #Thickness Calculations for internal pressure
    with st.expander("Expand to see thickness calculation for internal pressure"):
        st.write("**Min Corroded Required Thickness 1-4 (e)**")
        st.latex(r"""t = {PD \over 2cos(\alpha)(SE-0.6P)}""")
        st.latex(rf"""t = \frac{{{P} \cdot {D}}}{{2cos({alpha})({S} \cdot {E} - 0.6 \cdot {P})}}""")
        t = P*D/(2*cos(alpha_rad))/(S*E-0.6*P)
        st.latex(rf"""t = {t:0.1f} mm""")
        
        st.write("**Design Thickness = t + CA**")
        st.latex(rf"""= {t + CA:.1f} mm""")

        if tc >= (t + CA):
            st.write(f"**Provided Thickness = {tc} mm >= design thickness {t+CA:.1f} mm. [OK]**")
        else:
            st.markdown(":red[Failed in internal pressure]")

    #Reinforcement Calculations for internal pressure
    #Large End
    with st.expander("Expand to see reinforcement calculations at large end for internal pressure"):
        st.write("Reinforcement Calculation at large end")
        Rl = D/2
        st.latex(rf"R_L = \frac{{D}}{{2}} = \frac{{{D}}}{{{2}}} = {Rl} \text {{ mm}}")
        min_large_end_length = 2*(Rl*(tlnom-CA))**0.5
        Ql = P*Rl/2+f1i
        st.latex(rf"2 \cdot \sqrt{{R_L \cdot (t_{{lnom}} - CA)}} = {min_large_end_length:.1f} \text {{ mm}}")
        if Ll > min_large_end_length:
            st.write(f"Cylinder length = {Ll} mm > min required length at large end = {min_large_end_length:.1f} mm")
            Delta = 326.6*(P/S/E)**0.5
            st.latex(rf"\Delta = 326.6 \sqrt{{\frac{{P}}{{S \cdot E}}}} = 326.6 \sqrt{{\frac{{{P}}}{{{S} \cdot {E}}}}} = {Delta:.1f} \degree")
            if Delta < alpha:
                st.latex(rf"\text {{ Since }} \Delta < \alpha \text {{ reinforcement shall be provided at the large end}}")
                st.latex(r"Q_L = \frac{PR_L}{2}+f_1")
                st.latex(rf"Q_L = \frac{{{P} \cdot {Rl}}}{{{2}}}+{{{f1i}}}")
                st.latex(rf"Q_L = {Ql:.1f} \text {{ N/mm}}")
                if Ql<0:
                    st.markdown(":red[Ql <0, U-2(g) applies]")
                st.write("Assumed $k = 1$")
                st.write("Required area of reinforcement at the large end")
                st.latex(r"A_{rl} = \frac{kQ_LR_L}{SE} \left (1- \frac{\Delta}{\alpha} \right )tan(\alpha)")
                Arl = Ql*Rl/S/E*(1-Delta/alpha)*tan(alpha_rad)            
                st.latex(rf"A_{{rl}} = \frac{{1 \cdot {Ql:.1f} \cdot {Rl}}}{{{S} \cdot {E}}} \left (1 - \frac{{{Delta:.1f}}}{{{alpha}}}\right) \tan({alpha})")
                st.latex(rf"A_{{rl}} = {Arl:.1f} \text {{ mm}}^2")
                st.write("Effective area of reinforcement at the large end.")
                st.latex(r"A_{el} = (t_{lnom} - CA - t_{{rl}}) \sqrt {R_L(t_{lnom}-CA)} + (t_c - CA - t_{{rc}}) \sqrt {\frac{R_L(t_c-CA)}{cos(\alpha)}}")
                st.latex(rf"A_{{el}}= ({{{tlnom}}} - {{{CA}}} - {{{trl}}}) \sqrt{{{Rl} \cdot ({tlnom}-{CA})}} + ({{{tc}}} - {{{CA}}} - {{{trc}}}) \sqrt{{\frac{{{Rl} \cdot ({tc}-{CA})}}{{\cos({alpha})}}}}")
                Ael = (tlnom-CA-trl)*(Rl*(tlnom-CA))**0.5+(tc-CA-trc)*(Rl*(tc-CA)/cos(alpha_rad))**0.5
                st.latex(rf"A_{{el}} = {Ael:.1f} \text {{ mm}}^2")
                if Ael >= Arl:
                    st.latex(r"A_{el}>A_{rl} \text { [OK]}")
                else:
                    st.markdown(":red[Area Reinfocement failed at large end junction. Ignore if stiffening ring of sufficient area added to the junction.]")
            else:
                st.latex(rf"\text {{ Since }} \Delta >= \alpha \text {{ reinforcement not required at the large end}}")
        else:
            st.write(f"Cylinder length = {Ll} mm < min required length at large end = {min_large_end_length:.1f} mm")
            st.write("Required area of reinforcement at the large end")
            st.latex(r"A_{rl} = \frac{kQ_LR_L}{SE} tan(\alpha)")
            Arl = Ql*Rl/S/E*tan(alpha_rad)
            st.latex(rf"A_{{rl}} = \frac{{1 \cdot {Ql:.1f} \cdot {Rl}}}{{{S} \cdot {E}}} \tan({alpha})")
            st.latex(rf"A_{{rl}} = {Arl:.1f} \text {{ mm}}^2")
            
            st.write("Effective area of reinforcement at the large end.")
            st.latex(r"A_{el} = (t_c - CA - t_{{rc}}) \sqrt {\frac{R_L(t_c-CA)}{cos(\alpha)}}")
            st.latex(rf"A_{{el}}= ({{{tc}}} - {{{CA}}} - {{{trc}}}) \sqrt{{\frac{{{Rl} \cdot ({tc}-{CA})}}{{\cos({alpha})}}}}")
            Ael = (tc-CA-trc)*(Rl*(tc-CA)/cos(alpha_rad))**0.5
            st.latex(rf"A_{{el}} = {Ael:.1f} \text {{ mm}}^2")
            if Ael >= Arl:
                st.latex(r"A_{el}>A_{rl} \text { [OK]}")
            else:
                st.markdown(":red[Area Reinfocement failed at large end junction]")

            
    #Reinforcement Calculations for internal pressure
    #Small End
    with st.expander("Expand to see reinforcement calculations at small end for internal pressure"):
        st.write("Reinforcement Calculation at small end")
        Rs = D/2-Lc*tan(alpha_rad)
        st.latex(rf"R_s = \frac{{D}}{{2}} - L_c \cdot tan(\alpha) = \frac{{{D}}}{{{2}}} - {{{Lc}}} \cdot tan({{{alpha}}}) = {{{Rs:.1f}}} \text {{ mm}}")
        min_small_end_length = 1.4*(Rs*(tsnom-CA))**0.5
        Qs = P*Rs/2+f2i
        st.latex(rf"1.4 \cdot \sqrt{{R_s \cdot (t_{{snom}} - CA)}} = {min_small_end_length:.1f} \text {{ mm}}")
        if Ls > min_small_end_length:
            st.write(f"Cylinder length = {Ls} mm > min required length at small end = {min_small_end_length:.1f} mm")
            Delta = 89*(P/S/E)**0.5
            st.latex(rf"\Delta = 89 \sqrt{{\frac{{P}}{{S \cdot E}}}} = 89 \sqrt{{\frac{{{P}}}{{{S} \cdot {E}}}}} = {Delta:.1f} \degree")
            if Delta < alpha:
                st.latex(rf"\text {{ Since }} \Delta < \alpha \text {{ reinforcement shall be provided at the small end}}")
                st.latex(r"Q_s = \frac{PR_s}{2}+f_2")
                st.latex(rf"Q_s = \frac{{{P} \cdot {Rs:.1f}}}{{{2}}}+{{{f2i}}}")
                st.latex(rf"Q_s = {Qs:.1f} \text {{ N/mm}}")
                if Qs<0:
                    st.markdown(":red[Qs <0, U-2(g) applies]")
                st.write("Assumed $k = 1$")
                st.write("Required area of reinforcement at the small end")
                st.latex(r"A_{rs} = \frac{kQ_sR_s}{SE} \left (1- \frac{\Delta}{\alpha} \right )tan(\alpha)")
                Ars = Qs*Rs/S/E*(1-Delta/alpha)*tan(alpha_rad)            
                st.latex(rf"A_{{rs}} = \frac{{1 \cdot {Qs:.1f} \cdot {Rs:.1f}}}{{{S} \cdot {E}}} \left (1 - \frac{{{Delta:.1f}}}{{{alpha}}}\right) \tan({alpha})")
                st.latex(rf"A_{{rs}} = {Ars:.1f} \text {{ mm}}^2")
                st.write("Effective area of reinforcement at the small end.")
                st.latex(r"A_{es} = 0.78 \left [ (t_{snom} - CA - t_{{rs}}) \sqrt {R_s(t_{snom}-CA)} + (t_c - CA - t_{{rc}}) \sqrt {\frac{R_s(t_c-CA)}{cos(\alpha)}} \right ]")
                st.latex(rf"A_{{es}}= 0.78 \left [ ({{{tsnom}}} - {{{CA}}} - {{{trs}}}) \sqrt{{{Rs:.1f} \cdot ({tsnom}-{CA})}} + ({{{tc}}} - {{{CA}}} - {{{trc}}}) \sqrt{{\frac{{{Rs:.1f} \cdot ({tc}-{CA})}}{{\cos({alpha})}}}} \right ]")
                Aes = 0.78*((tsnom-CA-trs)*(Rs*(tsnom-CA))**0.5+(tc-CA-trc)*(Rs*(tc-CA)/cos(alpha_rad))**0.5)
                st.latex(rf"A_{{es}} = {Aes:.1f} \text {{ mm}}^2")
                if Aes >= Ars:
                    st.latex(r"A_{es}>A_{rs} \text { [OK]}")
                else:
                    st.markdown(":red[Area Reinfocement failed at small end junction. Ignore if stiffening ring of sufficient area added to the junction.]")
            else:
                st.latex(rf"\text {{ Since }} \Delta >= \alpha \text {{ reinforcement not required at the small end}}")
        else:
            st.write(f"Cylinder length = {Ls} mm < min required length at small end = {min_small_end_length:.1f} mm")
            st.write("Required area of reinforcement at the small end")
            st.latex(r"A_{rs} = \frac{kQ_sR_s}{SE} tan(\alpha)")
            Ars = Qs*Rs/S/E*tan(alpha_rad)
            st.latex(rf"A_{{rs}} = \frac{{1 \cdot {Qs:.1f} \cdot {Rs:.1f}}}{{{S} \cdot {E}}} \tan({alpha})")
            st.latex(rf"A_{{rs}} = {Ars:.1f} \text {{ mm}}^2")
            
            st.write("Effective area of reinforcement at the small end.")
            st.latex(r"A_{es} = 0.78 \cdot (t_c - CA - t_{{rc}}) \sqrt {\frac{R_s(t_c-CA)}{cos(\alpha)}}")
            st.latex(rf"A_{{es}}= 0.78 \cdot ({{{tc}}} - {{{CA}}} - {{{trc}}}) \sqrt{{\frac{{{Rs:.1f} \cdot ({tc}-{CA})}}{{\cos({alpha})}}}}")
            Aes = 0.78*(tc-CA-trc)*(Rs*(tc-CA)/cos(alpha_rad))**0.5
            st.latex(rf"A_{{es}} = {Aes:.1f} \text {{ mm}}^2")
            if Aes >= Ars:
                st.latex(r"A_{es}>A_{rs} \text { [OK]}")
            else:
                st.markdown(":red[Area Reinfocement failed at small end junction. Ignore if stiffening ring of sufficient area is provided at the junction]")
            
    #External Pressure Calculation
    with st.expander("Expand to see MAEWP calculation"):
        st.write("External Pressure Calculations per UG-33 (f)(1). Assuming both ends are line of support")
        
        Dl = 2*(Rl+tlnom-CA)
        st.latex(r"D_L = 2 \cdot (R_L+t_{lnom} - CA)")
        st.latex(rf"D_L = 2 \cdot ({{{Rl}}}+{{{tlnom}}} - {{{CA}}})")
        st.latex(rf"D_L = {Dl:.1f} \text {{ mm}}")
        
        Ds = 2*(Rs+tsnom-CA)
        st.latex(r"D_s = 2 \cdot (R_s+t_{snom} - CA)")
        st.latex(rf"D_s = 2 \cdot ({{{Rs:.1f}}}+{{{tsnom}}} - {{{CA}}})")
        st.latex(rf"D_s = {Ds:.1f} \text {{ mm}}")

        te = (tc-CA)*cos(alpha_rad)
        st.latex(r"t_e = (t_c - CA) \cdot cos(\alpha)")
        st.latex(rf"t_e = ({{{tc}}} - {{{CA}}}) \cdot cos({{{alpha}}})")
        st.latex(rf"t_e = {te:.1f} \text {{ mm}}")      
        
        st.write("Assuming the construction is as per sketches (a) and (b) in Fig UG-33.1")
        Le = Lc/2*(1+Ds/Dl)
        st.latex(r"L_e = \frac{L_c}{2} \cdot \left ( 1+ \frac{D_s}{D_L} \right)")
        st.latex(rf"L_e = \frac{{{Lc}}}{{{2}}} \cdot \left ( 1+ \frac{{{Ds:.1f}}}{{{Dl:.1f}}} \right)")
        st.latex(rf"L_e = {Le:.1f} \text {{ mm}}")
       
        st.latex(rf"\frac{{D_l}}{{t_e}} = {Dl/te:0.3f}")
        
        if Dl/te >=10:
            st.latex(rf"\frac{{D_L}}{{t_e}} \geq 10 \text {{ , UG-33 (f)(1) criteria met}}")
        else:
            st.markdown(":red[Dl/te <10, UG-33 (f)(1) criteria not met]")
        if alpha > 60:
            st.markdown(":red[Half apex angle > 60, UG-33 (f)(1) criteria not met]")
            
        st.latex(rf"\frac{{L_e}}{{D_L}} = {Le/Dl:0.3f}")
        
        st.latex(rf"A = {A} \text {{ [User Input]}}")
        st.latex(rf"B = {B} \text {{ MPa [User Input]}}")
               
        Pa = 4*B/(3*Dl/te)
        st.latex(rf"P_a = \frac{{4B}}{{3D_L/t_e}} = \frac{{{4 * B}}}{{{3 * Dl / te:.3f}}} = {Pa:.3f} \text {{ MPa}}")
        if Pa >= Pe:
            st.write(f"**MAEWP = {Pa:.3f} MPa >= Design External Pressure {Pe:.3f} MPa. [OK]**")
        else:
            st.markdown(":red[Failed in external Pressure]")

    #Reinforcement Calculations for external pressure
    #Large End
    with st.expander("Expand to see reinforcement calculations at large end for external pressure"):
        if alpha>60:
            st.markdown(":red[Special analysis as per 1-8 (e) shall be performed.]")
        st.write("Reinforcement Calculation at large end")
        Rl = D/2+tlnom-CA
        Dl = 2*Rl
        st.latex(rf"R_L = \frac{{D}}{{2}} + t_{{lnom}} - {{CA}} = \frac{{{D}}}{{{2}}} + {{{tlnom}}} - {{{CA}}} = {{{Rl}}} \text {{ mm}}")
        min_large_end_length = 2*(Rl*(tlnom-CA))**0.5
        Ql = Pe*Rl/2+f1e
        st.latex(rf"2 \cdot \sqrt{{R_L \cdot (t_{{lnom}} - CA)}} = {min_large_end_length:.1f} \text {{ mm}}")
        if Ll > min_large_end_length:
            st.write(f"Cylinder length = {Ll} mm > min required length at large end = {min_large_end_length:.1f} mm")
            Delta = 104*(Pe/S/1)**0.5
            if Ql>0:
                st.write("Joint is under compression. Hence E=1")
            st.latex(rf"\Delta = 104 \sqrt{{\frac{{Pe}}{{S \cdot E}}}} = 104 \sqrt{{\frac{{{Pe}}}{{{S} \cdot {1}}}}} = {Delta:.1f} \degree")
            if Delta < alpha:
                st.latex(rf"\text {{ Since }} \Delta < \alpha \text {{ reinforcement shall be provided at the large end}}")
                st.latex(r"Q_L = \frac{P_eR_L}{2}+f_1")
                st.latex(rf"Q_L = \frac{{{Pe} \cdot {Rl}}}{{{2}}}+{{{f1e}}}")
                st.latex(rf"Q_L = {Ql:.1f} \text {{ N/mm}}")
                if Ql<0:
                    st.markdown(":red[Ql <0, U-2(g) applies]")
                st.write("Assumed $k = 1$")
                st.write("Required area of reinforcement at the large end")
                st.latex(r"A_{rl} = \frac{kQ_LR_Ltan(\alpha)}{SE} \left [1- \frac{1}{4} \left ( \frac{P_eR_L-Q_L}{Q_L} \right ) \frac{\Delta}{\alpha} \right ]")
                Arl = Ql*Rl*tan(alpha_rad)/S/1*(1-1/4*(Pe*Rl-Ql)/Ql*Delta/alpha)            
                st.latex(rf"A_{{rl}} = \frac{{1 \cdot {Ql:.1f} \cdot {Rl} \cdot tan({alpha})}}{{{S} \cdot {1}}} \left [1 - \frac{{{1}}}{{{4}}} \left ( \frac{{{Pe} \cdot {Rl}-{Ql:.1f}}}{{{Ql:.1f}}} \right ) \frac{{{Delta:.1f}}}{{{alpha}}}\right]")
                st.latex(rf"A_{{rl}} = {Arl:.1f} \text {{ mm}}^2")
                st.write("Effective area of reinforcement at the large end.")
                st.latex(r"A_{el} = 0.55 \cdot \left [(t_{lnom} - CA - t_{{rl}}) \sqrt {D_L(t_{lnom}-CA)} + (t_c - CA - t_{{rc}}) \sqrt {\frac{D_L(t_c-CA)}{cos(\alpha)}} \right ]")
                st.latex(rf"A_{{el}}= 0.55 \cdot \left [({{{tlnom}}} - {{{CA}}} - {{{trl}}}) \sqrt{{{Dl} \cdot ({tlnom}-{CA})}} + ({{{tc}}} - {{{CA}}} - {{{trc}}}) \sqrt{{\frac{{{Dl} \cdot ({tc}-{CA})}}{{\cos({alpha})}}}} \right ]")
                Ael = 0.55*((tlnom-CA-trl)*(Dl*(tlnom-CA))**0.5+(tc-CA-trc)*(Dl*(tc-CA)/cos(alpha_rad))**0.5)
                st.latex(rf"A_{{el}} = {Ael:.1f} \text {{ mm}}^2")
                if Ael >= Arl:
                    st.latex(r"A_{el}>A_{rl} \text { [OK]}")
                else:
                    st.markdown(":red[Area Reinfocement failed at large end junction. Ignore if stiffening ring of sufficient area added to the junction.]")
            else:
                st.latex(rf"\text {{ Since }} \Delta >= \alpha \text {{ reinforcement not required at the large end}}")
        else:
            st.write(f"Cylinder length = {Ll} mm < min required length at large end = {min_large_end_length:.1f} mm")
            st.write("Required area of reinforcement at the large end")
            st.latex(r"A_{rl} = \frac{kQ_LD_L}{2SE} tan(\alpha)")
            Arl = 1*Ql*Dl/2/S/1*tan(alpha_rad)
            st.latex(rf"A_{{rl}} = \frac{{1 \cdot {Ql:.1f} \cdot {Dl}}}{{{2} \cdot {S} \cdot {E}}} \tan({alpha})")
            st.latex(rf"A_{{rl}} = {Arl:.1f} \text {{ mm}}^2")
            
            st.write("Effective area of reinforcement at the large end.")
            st.latex(r"A_{el} = 0.55 \cdot (t_c - CA - t_{{rc}}) \sqrt {\frac{D_L(t_c-CA)}{cos(\alpha)}}")
            st.latex(rf"A_{{el}}= 0.55 \cdot ({{{tc}}} - {{{CA}}} - {{{trc}}}) \sqrt{{\frac{{{Dl} \cdot ({tc}-{CA})}}{{\cos({alpha})}}}}")
            Ael = 0.55*(tc-CA-trc)*(Dl*(tc-CA)/cos(alpha_rad))**0.5
            st.latex(rf"A_{{el}} = {Ael:.1f} \text {{ mm}}^2")
            if Ael >= Arl:
                st.latex(r"A_{el}>A_{rl} \text { [OK]}")
            else:
                st.markdown(":red[Area Reinfocement failed at large end junction. Provide stiffening ring at cone near junction]")

    #Reinforcement Calculations for external pressure
    #Small End
    with st.expander("Expand to see reinforcement calculations at small end for external pressure"):
        st.write("Reinforcement Calculation at small end")
        Rs = D/2-Lc*tan(alpha_rad) - CA + tsnom
        Ds = 2*Rs
        st.latex(rf"R_s = \frac{{D}}{{2}} - L_c \cdot tan(\alpha) - {{CA}} + t_{{snom}} = \frac{{{D}}}{{{2}}} - {{{Lc}}} \cdot tan({{{alpha}}}) - {{{CA}}} + {{{tsnom}}} = {{{Rs:.1f}}} \text {{ mm}}")
        min_small_end_length = 1.4*(Rs*(tsnom-CA))**0.5
        Qs = Pe*Rs/2+f2e
        st.latex(rf"1.4 \cdot \sqrt{{R_s \cdot (t_{{snom}} - CA)}} = {min_small_end_length:.1f} \text {{ mm}}")
        if Ls > min_small_end_length:
            st.write(f"Cylinder length = {Ls} mm > min required length at small end = {min_small_end_length:.1f} mm")
            st.latex(r"Q_s = \frac{P_eR_s}{2}+f_2")
            st.latex(rf"Q_s = \frac{{{Pe} \cdot {Rs:.1f}}}{{{2}}}+{{{f2e}}}")
            st.latex(rf"Q_s = {Qs:.1f} \text {{ N/mm}}")
            if Qs<0:
                st.markdown(":red[Qs <0, U-2(g) applies]")
            st.write("Assumed $k = 1$")
            st.write("Required area of reinforcement at the small end")
            st.latex(r"A_{rs} = \frac{kQ_sR_s}{SE} tan(\alpha)")
            st.write("For compression assuming E = 1")
            Ars = 1*Qs*Rs/S/1*tan(alpha_rad)            
            st.latex(rf"A_{{rs}} = \frac{{1 \cdot {Qs:.1f} \cdot {Rs:.1f}}}{{{S} \cdot {1}}} \cdot tan({alpha})")
            st.latex(rf"A_{{rs}} = {Ars:.1f} \text {{ mm}}^2")
            st.write("Effective area of reinforcement at the small end.")
            st.latex(r"A_{es} = 0.55 \left [ (t_{snom} - CA - t_{{rs}}) \sqrt {D_s(t_{snom}-CA)} + (t_c - CA - t_{{rc}}) \sqrt {\frac{D_s(t_c-CA)}{cos(\alpha)}} \right ]")
            st.latex(rf"A_{{es}}= 0.55 \left [ ({{{tsnom}}} - {{{CA}}} - {{{trs}}}) \sqrt{{{Ds:.1f} \cdot ({tsnom}-{CA})}} + ({{{tc}}} - {{{CA}}} - {{{trc}}}) \sqrt{{\frac{{{Ds:.1f} \cdot ({tc}-{CA})}}{{\cos({alpha})}}}} \right ]")
            Aes = 0.55*((tsnom-CA-trs)*(Ds*(tsnom-CA))**0.5+(tc-CA-trc)*(Ds*(tc-CA)/cos(alpha_rad))**0.5)
            st.latex(rf"A_{{es}} = {Aes:.1f} \text {{ mm}}^2")
            if Aes >= Ars:
                st.latex(r"A_{es}>A_{rs} \text { [OK]}")
            else:
                st.markdown(":red[Area Reinfocement failed at small end junction. Ignore if stiffening ring of sufficient area added to the junction.]")
        else:
            st.write(f"Cylinder length = {Ls} mm < min required length at small end = {min_small_end_length:.1f} mm")
            st.write("Required area of reinforcement at the small end")
            st.latex(r"A_{rs} = \frac{kQ_sD_s}{2SE} tan(\alpha)")
            Ars = 1*Qs*Ds/2/S/1*tan(alpha_rad)
            st.latex(rf"A_{{rs}} = \frac{{1 \cdot {Qs:.1f} \cdot {Ds:.1f}}}{{{2} \cdot {S} \cdot {E}}} \cdot tan({alpha})")
            st.latex(rf"A_{{rs}} = {Ars:.1f} \text {{ mm}}^2")
            
            st.write("Effective area of reinforcement at the small end.")
            st.latex(r"A_{es} = 0.55 \cdot (t_c - CA - t_{{rc}}) \sqrt {\frac{D_s(t_c-CA)}{cos(\alpha)}}")
            st.latex(rf"A_{{es}}= 0.55 \cdot ({{{tc}}} - {{{CA}}} - {{{trc}}}) \sqrt{{\frac{{{Ds:.1f} \cdot ({tc}-{CA})}}{{\cos({alpha})}}}}")
            Aes = 0.55*(tc-CA-trc)*(Ds*(tc-CA)/cos(alpha_rad))**0.5
            st.latex(rf"A_{{es}} = {Aes:.1f} \text {{ mm}}^2")
            if Aes >= Ars:
                st.latex(r"A_{es}>A_{rs} \text { [OK]}")
            else:
                st.markdown(":red[Area Reinfocement failed at small end junction. Ignore if stiffening ring of sufficient area is provided at the junction]")

    #Moment of Inertia Requirement at the large end considering it a line of support.
    with st.expander("Expand to see Moment of Inertia Requirement at the large end considering it a line of support."):
        st.write("M.I. calculation at the large end as per 1-8 (b)(3)")
        if Ll < min_large_end_length:
            st.write("Since $L_L$ < minimum required length of the large end cylinder, it will be set to Zero.")
            Ll = 0
        
        st.latex(r"M = \frac{-R_L \cdot \tan(\alpha)}{2} + \frac{L_L}{2} + \frac{R_L^2-R_s^2}{3 \cdot R_L \cdot \tan(\alpha)}")
        st.latex(rf"M = \frac{{{-Rl} \cdot \tan({alpha})}}{{2}} + \frac{{{Ll}}}{{2}} + \frac{{{Rl}^2 - {Rs:.1f}^2}}{{3 \cdot {Rl} \cdot \tan({alpha})}}")
        M = -Rl*tan(alpha_rad)/2+Ll/2+(Rl**2-Rs**2)/(3*Rl*tan(alpha_rad))
        st.latex(rf"M = {M:.1f} \text {{ mm}}")
        
        st.latex(r"F_L = P_e \cdot M + f_{1e} \cdot \tan(\alpha)")
        st.latex(rf"F_L = {{{Pe}}} \cdot {{{M:.1f}}} + {{{f1e}}} \cdot \tan({{{alpha}}})")
        Fl = Pe*M + f1e*tan(alpha_rad)
        st.latex(rf"F_L = {Fl:.1f} \text {{ N/mm}}")
        if Fl<0:
            st.markdown(":red[Fl is negative. Design as per U-2(g)]")
        
        st.write("Slant Length Calculation")
        st.latex(r"L_c = \sqrt{L_c^2 + (R_L - R_s)^2}")
        st.latex(rf"L_c = \sqrt{{{Lc}^2 + ({Rl} - {Rs:.1f})^2}}")
        Lc = (Lc**2+(Rl-Rs)**2)**0.5
        st.latex(rf"L_c = {Lc:.1f} \text {{ mm}}")
        
        st.write("Equivalent area of cylinder, cone and stiffening ring at the large end")
        st.latex(r"A_{TL} = \frac{L_L \cdot (t_{lnom} - CA)}{2} + \frac{L_c \cdot (t_c - CA)}{2} + A_{sl}")
        st.latex(rf"A_{{TL}} = \frac{{{Ll} \cdot ({tlnom} - {CA})}}{{{2}}} + \frac{{{Lc:.1f} \cdot ({tc} - {CA})}}{{{2}}} + {{{Asl}}}")
        Atl = Ll*(tlnom-CA)/2+Lc*(tc-CA)/2+Asl
        st.latex(rf"A_{{TL}} = {Atl:.1f} \text {{ mm}}^2")
        
        st.write("Factor B Computation")
        st.latex(r"B1 = \frac{3}{4} \left ( \frac{F_LD_L}{A_{TL}} \right )")
        st.latex(rf"B1 = \frac{{{3}}}{{{4}}} \left ( \frac{{{Fl:.1f} \cdot {Dl}}}{{{Atl:.1f}}} \right )")
        B1 = 3/4*Fl*Dl/Atl
        st.latex(rf"B1 = {B1:.3f} \text {{ MPa}}")
        
        st.latex(rf"A1 = {A1} \text {{ [User Input]}}")
        
        st.write("Required M.I. of ring about its neutral axis parallel to axis of shell")
        st.latex(r"I_{sl} = \frac{A1 \cdot D_L^2 \cdot A_{TL}}{14}")
        st.latex(rf"I_{{sl}} = \frac{{{A1} \cdot {Dl}^2 \cdot {Atl:.1f}}}{{{14}}}")
        Isl = A1*Dl**2*Atl/14
        st.latex(rf"I_{{sl}} = {{{Isl:.3e}}} \text {{ mm}}^4")
        
        st.write("Provided M.I.")
        st.latex(rf"I_l = {Il:.3e} \text {{ mm }}^4")
        
        if Il > Isl:
            st.write("Since $I_l > I_{sl}$ , M.I requirement met at the large end")
        else:
            st.markdown(":red[Provide Stiffener ring of sufficient area]")
            
        st.write("Note: A ring if present can be optimized by using M.I. of combined shell-ring-cone section. For this $I' > I_s'$ needs to be met")
            
    #Moment of Inertia Requirement at the small end considering it a line of support.
    with st.expander("Expand to see Moment of Inertia Requirement at the small end considering it a line of support."):
        st.write("M.I. calculation at the small end as per 1-8 (c)(3)")
        if Ls < min_small_end_length:
            st.write("Since $L_s$ < minimum required length of the small end cylinder, it will be set to Zero.")
            Ls = 0
        
        st.latex(r"N = \frac{R_s \cdot \tan(\alpha)}{2} + \frac{L_s}{2} + \frac{R_L^2-R_s^2}{6 \cdot R_s \cdot \tan(\alpha)}")
        st.latex(rf"N = \frac{{{Rs:.1f} \cdot \tan({alpha})}}{{2}} + \frac{{{Ls}}}{{2}} + \frac{{{Rl}^2 - {Rs:.1f}^2}}{{6 \cdot {Rs:.1f} \cdot \tan({alpha})}}")
        N = Rs*tan(alpha_rad)/2+Ls/2+(Rl**2-Rs**2)/(6*Rs*tan(alpha_rad))
        st.latex(rf"N = {N:.1f} \text {{ mm}}")
        
        st.latex(r"F_s = P_e \cdot N + f_{2e} \cdot \tan(\alpha)")
        st.latex(rf"F_s = {{{Pe}}} \cdot {{{N:.1f}}} + {{{f2e}}} \cdot \tan({{{alpha}}})")
        Fs = Pe*N + f2e*tan(alpha_rad)
        st.latex(rf"F_s = {Fs:.1f} \text {{ N/mm}}")
        if Fs<0:
            st.markdown(":red[Fl is negative. Design as per U-2(g)]")
                
        st.write("Equivalent area of cylinder, cone and stiffening ring at the small end")
        st.latex(r"A_{TS} = \frac{L_S \cdot (t_{snom} - CA)}{2} + \frac{L_c \cdot (t_c - CA)}{2} + A_{ss}")
        st.latex(rf"A_{{TS}} = \frac{{{Ls} \cdot ({tsnom} - {CA})}}{{{2}}} + \frac{{{Lc:.1f} \cdot ({tc} - {CA})}}{{{2}}} + {{{Ass}}}")
        Ats = Ls*(tsnom-CA)/2+Lc*(tc-CA)/2+Ass
        st.latex(rf"A_{{TS}} = {Ats:.1f} \text {{ mm}}^2")
        
        st.write("Factor B Computation")
        st.latex(r"B2 = \frac{3}{4} \left ( \frac{F_sD_s}{A_{TS}} \right )")
        st.latex(rf"B2 = \frac{{{3}}}{{{4}}} \left ( \frac{{{Fs:.1f} \cdot {Ds:.1f}}}{{{Ats:.1f}}} \right )")
        B2 = 3/4*Fs*Ds/Ats
        st.latex(rf"B2 = {B2:.3f} \text {{ MPa}}")
        
        st.latex(rf"A2 = {A2} \text {{ [User Input]}}")
        
        st.write("Required M.I. of ring about its neutral axis parallel to axis of shell")
        st.latex(r"I_{ss} = \frac{A2 \cdot D_s^2 \cdot A_{TS}}{14}")
        st.latex(rf"I_{{ss}} = \frac{{{A2} \cdot {Ds:.1f}^2 \cdot {Ats:.1f}}}{{{14}}}")
        Iss = A2*Ds**2*Ats/14
        st.latex(rf"I_{{ss}} = {{{Iss:.3e}}} \text {{ mm}}^4")
        
        st.write("Provided M.I.")
        st.latex(rf"I_s = {Is:.3e} \text {{ mm}}^4")
        
        if Is > Iss:
            st.write("Since $I_s > I_{ss}$ , M.I requirement met at the large end")
        else:
            st.markdown(":red[Provide Stiffener ring of sufficient area]")
            
        st.write("Note: A ring if present can be optimized by using M.I. of combined shell-ring-cone section. For this $I' > I_s'$ needs to be met")

        
       
        