import streamlit as st

#Two Columns for inputs and outputs
col1, col2 = st.columns([1,2]) #col2 width is 2*times col1 width

#Input Column
with col1:
    st.title("Inputs")

    st.write("**GEOMETRY**")
    Desc = st.text_input("Description", value="ASME PTB-4 E4.1.2 - Hemispherical Head")
    CA = st.number_input("Corrosion Allowance, CA (mm)",step=0.1, format="%.1f", value=3.0)
    L = st.number_input("Corroded Inside Radius, L (mm)",step=1.0, format="%.1f", value=1222.0)
    tn = st.number_input("Provided Nominal Thickness, tn (mm)",step=0.1, format="%.1f", value=62.0)
    tmin = st.number_input("Provided Minimum Thickness, tmin (mm)",step=0.1, format="%.1f", value=55.8)
    tr = st.number_input("Required Corroded Thickness for all combination of loads, tr (mm)",step=0.1, format="%.1f", value=51.5)
    st.write("---")    

    st.write("**LOADS**")
    P = st.number_input("Internal Design Pressure including static head, P (MPa)",step=0.001, format="%.3f", value=11.536)
    head_op = st.number_input("Operating static head, head_op (MPa)",step=0.001, format="%.3f", value=0.159)
    head_hydro = st.number_input("Hydrostatic head, head_hydro (MPa)",step=0.001, format="%.3f", value=0.0)
    Pe = st.number_input("External Design Pressure, Pe (MPa)",step=0.001, format="%.3f", value=0.0)
    st.write("---")    

    st.write("**MATERIAL PROPERTIES**")
    Sa = st.number_input("Allowable Stress of Material at ambient temperature, Sa (MPa)",step=0.1, format="%.1f", value=138.0)
    S = st.number_input("Allowable Stress of Material at design temperature, S (MPa)",step=0.1, format="%.1f", value=138.0)
    E = st.number_input("Weld Joint Efficiency, E",step=0.01, format="%.2f", value=1.00)
    rho = st.number_input("Material Density, rho (kg/mm3)",step=1.0, format="%.3e", value=7.75e-6)
    B = st.number_input("Factor from applicable material chart of ASME II-D, B (MPa)",step=0.001, format="%.3f", value=0.0)
    MDMT_Curve = st.selectbox("Applicable MDMT Curve (Only for CS and LAS)",["A","B","C","D"],index=1)
    MDMT_UCS66 = st.number_input("Basic MDMT per Table UCS-66 ($\degree$C)",step=0.1, format="%.1f", value=19.0)
    T_red = st.number_input("MDMT reduction per Fig UCS-66.1M based on ratio calculation (see output), ($\degree$C)",step=0.1, format="%.1f", value=1.0)

#Output Column
with col2:
    st.title("Outputs")
    
    #Draw Sketch
    ###########################################################################
    import plotly.graph_objects as go
    import numpy as np
    
    # Create theta values for the semicircle
    theta = np.linspace(0, np.pi, 100)
    
    # Create x and y values for the semicircle
    x = np.cos(theta)
    y = np.sin(theta)
    
    # Create a Plotly figure
    fig = go.Figure()
    
    # Add a scatter plot for the semicircle
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Hemi Head'))
    
    # Add a scatter plot for the line
    fig.add_trace(go.Scatter(x=[-1, 1], y=[0, 0], mode='lines', name='Tan Line'))
    
    # Add dimension arrows with arrowhead on end
    fig.add_annotation(
        x=0.707, y=0.707,
        ax=0, ay=0,
        xref='x', yref='y',
        axref='x', ayref='y',
        showarrow=True,
        arrowhead=2,
        arrowside='end'
    )
    
    # Add dimension labels
    fig.add_annotation(
        x=0.3, y=0.4,
        text=f'Inside Crown Radius {L-CA}',
        showarrow=False,
        font=dict(size=12, color="Black"),
        textangle = -45
    )
    
    fig.add_annotation(
        x=0.38, y=0.3,
        text=f'(T_nom {tn}, T_min {tmin})',
        showarrow=False,
        font=dict(size=12, color="Black"),
        textangle = -45
    )
    # Set the aspect ratio to be equal
    fig.update_layout(
        title="Hemispherical Head (All dimensions in mm)",
        xaxis=dict(scaleanchor="y", scaleratio=1, visible=False),
        yaxis=dict(scaleanchor="x", scaleratio=1, visible=False)
    )
    
    # Display the Plotly figure using Streamlit
    st.plotly_chart(fig)
    
    ###########################################################################
    
    st.write("CODE: ASME Sec VIII, Div 1 - 2023 Ed.")
        
    #Internal Pressure Thickness Calculations
    with st.expander("Expand to see thickness calculation for internal pressure"):
        if P > 0.665*S*E:
            st.markdown(":red[P > 0.665SE, UG-32 (e) not valid]")
        st.write("**Min Corroded Required Thickness UG-32 (e)**")
        st.latex(r"""t = {PL \over 2SE-0.2P}""")
        st.latex(rf"""t = \frac{{{P} \cdot {L}}}{{2 \cdot {S} \cdot {E} - 0.2 \cdot {P}}}""")
        t = P*L/(2*S*E-0.2*P)
        st.latex(rf"""t = {t:0.1f} mm""")
        
        st.write("**Design Thickness = t + CA**")
        st.latex(rf"""= {t + CA:.1f} mm""")

        if tmin >= (t + CA):
            st.write(f"**Provided Min Thickness = {tmin} mm >= design thickness {t+CA:.1f} mm. [OK]**")
        else:
            st.markdown(":red[Increase Minimum Thickness]")

    #External Pressure Calculation
    with st.expander("Expand to see external pressure calculation"):
        t = tmin - CA
        Ro = L+t
        Rot = Ro/t
        A = 0.125/(Ro/t)
        Pa = B/(Ro/t)
        st.write("MAEWP or Pa calculation as per UG-28(d)")
        st.latex(rf"t = tmin - CA = {tmin}-{CA} = {tmin-CA} mm")
        st.latex(rf"R_o = L + t = {L}+{t} = {Ro} mm")
        st.latex(rf"A = \frac{{0.125}}{{R_o/t}} = \frac{{{0.125}}}{{{Rot:.3f}}} = {A:.3e}")
        st.latex(rf"B = {B} MPa \text{{ (User Input)}}")
        st.latex(rf"P_a = \frac{{B}}{{R_o/t}} = \frac{{{B}}}{{{Rot:.3f}}} = {Pa:.3f} MPa")
        
        if Pa >= Pe:
            st.write(f"**MAEWP = {Pa:.3f} MPa >= Design External Pressure {Pe:.3f} MPa. [OK]**")
        else:
            st.markdown(":red[Failed in external pressure]")

    #MAWP and MAPNC Calculations
    with st.expander("Expand to see MAWP and MAPNC calculation"):
        #MAWP
        st.write("**MAWP Caclulation UG-32 (e)**")
        st.latex(r"""MAWP={2SE(tmin-CA) \over L+0.2(tmin-CA)} - head op""")
        st.latex(rf"""MAWP = \frac{{2 \cdot {S} \cdot {E} \cdot ({tmin} - {CA})}}{{{L} + 0.2 \cdot ({tmin} - {CA})}} - {head_op}""")
        MAWP = 2*S*E*(tmin-CA)/(L+0.2*(tmin-CA)) - head_op
        st.latex(rf"""MAWP = {MAWP:0.3f} MPa""")
        
        #MAPNC
        st.write("**MAPNC Caclulation UG-32 (e)**")
        st.latex(r"""MAPNC={2Sa \cdot E \cdot tmin \over L-CA+0.2 \cdot tmin}""")
        st.latex(rf"""MAPNC = \frac{{2 \cdot {Sa} \cdot {E} \cdot {tmin}}}{{{L}-{CA} + 0.2 \cdot {tmin}}}""")
        MAPNC = 2*Sa*E*tmin/(L-CA+0.2*tmin)
        st.latex(rf"""MAPNC = {MAPNC:0.3f} MPa""")

    #Hydrotest Calculations
    with st.expander("Expand to see Hydrotest calculation"):
        st.write(f"**Hydrostatic Test Pressures (Measured at High Point)**")
        st.write(f"Hydrotest per UG-99(b); 1.3 * MAWP * Sa/S = {1.3*MAWP*Sa/S: .3f} MPa")
        st.write(f"Hydrotest per UG-99(c); 1.3 * MAPNC - head_hydro = {1.3*MAPNC - head_hydro: .3f} MPa")
        st.write(f"Pneumatic per UG-100  ; 1.1 * MAWP * Sa/S = {1.1*MAWP*Sa/S: .3f} MPa")

    #Forming Strains Calculations
    with st.expander("Expand to see Forming Strain calculations"):
        st.write(f"**Forming Strain per Table UG-79-1**")
        st.latex(r"R_f = L - CA + \frac{tn}{2}")
        st.latex(rf"R_f = {L} - {CA} + {tn/2}")
        Rf = L - CA + tn/2
        st.latex(rf"R_f = {Rf} mm")
        st.write("$R_{o}$ is infinity for a flat plate. Accordingly $\epsilon_f$ is calculated as")
        st.latex(r"\epsilon_{f} = \frac {75tn}{R_f}")
        st.latex(rf"\epsilon_f = 75 \cdot \frac{{{tn}}}{{{Rf}}}")
        epf = 75*tn/Rf
        st.latex(rf"""\epsilon_f = {epf:.2f} \%""")
        if epf > 5:
            st.write("Note: Please Check Requirements of UCS-79 as Elongation is > 5%.")
        
    #MDMT Calculations
    with st.expander("Expand to see MDMT calculations"):
        st.write(f"**MDMT Calculations per UCS-66 (Valid only for CS and LAS)**")
        st.write(f"Governing Thk = tmin = {tmin} mm")
        st.write(f"Applicable MDMT Curve = {MDMT_Curve}")
        st.write(f"Basic MDMT from Table UCS-66 = {MDMT_UCS66} $\degree$C")
        st.write(f"Reduction in MDMT without impact testing per UCS-66.1M")
        E_star = max(E,0.8)
        st.write(f"$E^*$ = max(E, 0.8) = {E_star}")
        st.latex(r"Ratio = \frac {trE^*}{tmin-CA}")
        st.latex(rf"Ratio = \frac{{{tr:.1f} \cdot {E_star}}}{{{tmin}-{CA}}}")
        Ratio = tr*E_star/(tmin - CA)
        st.latex(rf"Ratio = {Ratio:.3f}")
        if Ratio <= 0.35:
            st.write("As per UCS-66(b)(3) if Ratio <= 0.35, then Reduced MDMT = -105 $\degree$C")
        else:
            st.write(f"MDMT reduction as per Fig UCS-66.1M = {T_red} $\degree$C")
            st.write(f"Minimum MDMT after reduction (not less than -48 $\degree$C per UCS-66(b)(1)(-b)) = {max(-48,MDMT_UCS66-T_red)} $\degree$C")

    #Weight and Volume
    with st.expander("Expand to see Weight and Volume calculations"):
        
        #Original Thk
        st.write(f"**Weight and Volume Results, Original Thickness:**")
        st.write(f"Weight Calc")
        st.latex(r"Volume = \frac{2}{3} \pi \cdot \left ((L - CA + tn)^3 - (L - CA)^3 \right )")
        st.latex(rf"Volume = \frac{2}{3} \pi \cdot \left (({L} - {CA} + {tn})^3 - ({L} - {CA})^3 \right )")
        Volume = 2/3*22/7*((L-CA+tn)**3 - (L-CA)**3)
        st.latex(rf"Volume = {Volume:.3e} mm^3")                 
        st.latex(r"Weight = rho \cdot Volume")
        st.latex(rf"Weight = ({rho}) \cdot ({Volume:.3e})")
        Weight = rho*Volume
        st.latex(rf"Weight = {Weight:.1f} kg")
        
        st.write(f"Inside Volume Calc")
        st.latex(r"VolIn = \frac{2}{3} \pi (L-CA)^3")
        st.latex(rf"VolIn = \frac{2}{3} \pi \cdot ({L}-{CA})^3")
        VolIn = 2/3*22/7*(L-CA)**3
        st.latex(rf"VolIn = {VolIn:.3e} mm^3")
        st.latex(r"WaterWeight = 1e-6 \cdot VolIn")
        WaterWeight = 1e-6*VolIn
        st.latex(rf"WaterWeight = {WaterWeight:.1f} kg")
        
        #Corroded Thk
        st.write(f"**Weight and Volume Results, Corroded Thickness:**")
        st.write(f"Weight Calc")
        st.latex(r"Volume = \frac{2}{3} \pi \cdot \left ((L - CA + tn)^3 - L^3 \right )")
        st.latex(rf"Volume = \frac{2}{3} \pi \cdot \left (({L} - {CA} + {tn})^3 - {L}^3 \right )")
        Volume = 2/3*22/7*((L-CA+tn)**3 - (L)**3)
        st.latex(rf"Volume = {Volume:.3e} mm^3")                 
        st.latex(r"Weight = rho \cdot Volume")
        st.latex(rf"Weight = ({rho}) \cdot ({Volume:.3e})")
        Weight = rho*Volume
        st.latex(rf"Weight = {Weight:.1f} kg")
        
        st.write(f"Inside Volume Calc")
        st.latex(r"VolIn = \frac{2}{3} \pi \cdot L^3")
        st.latex(rf"VolIn = \frac{2}{3} \cdot \pi \cdot {L}^3")
        VolIn = 2/3*22/7*(L)**3
        st.latex(rf"VolIn = {VolIn:.3e} mm^3")
        st.latex(r"WaterWeight = 1e-6 \cdot VolIn")
        WaterWeight = 1e-6*VolIn
        st.latex(rf"WaterWeight = {WaterWeight:.1f} kg")
        
