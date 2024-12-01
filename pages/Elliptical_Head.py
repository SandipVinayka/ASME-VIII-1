import streamlit as st

#Two Columns for inputs and outputs
col1, col2 = st.columns([1,2]) #col2 width is 2*times col1 width

#Input Column
with col1:
    st.title("Inputs")

    st.write("**GEOMETRY**")
    Desc = st.text_input("Description", value="ASME PTB-4 E4.3.5, E4.4.5 - Elliptical Head")
    CA = st.number_input("Corrosion Allowance, CA (mm)",step=0.1, format="%.1f", value=3.0)
    D = st.number_input("Corroded Inside Diameter of the Head Skirt, D (mm)",step=1.0, format="%.1f", value=2292.0)
    tn = st.number_input("Provided Nominal Thickness, tn (mm)",step=0.1, format="%.1f", value=32.0)
    ts = st.number_input("Minimum Specified thk of head after forming, ts (mm)",step=0.1, format="%.1f", value=28.6)
    h = st.number_input("Corroded inside depth of the ellipsoidal head measured from the tangent line (head‐bend line), h (mm)",step=1.0, format="%.1f", value=574.5)
    SF = st.number_input("Length of straight flange, SF (mm)",step=1.0, format="%.1f", value=50.0)
    K1 = st.number_input("Corroded Spherical Radius Factor from Table UG-37, K1",step=1.0, format="%.2f", value=0.90)
    DB = st.number_input("Blank Dia for forming the ellipsoidal head, DB (mm)",step=1.0, format="%.1f", value=2937.0)
    tr = st.number_input("Required Corroded Thickness for all combination of loads, tr (mm)",step=0.1, format="%.1f", value=5.7)
    st.write("---")    

    st.write("**LOADS**")
    P = st.number_input("Internal Design Pressure including static head, P (MPa)",step=0.001, format="%.3f", value=0.690)
    head_op = st.number_input("Operating static head, head_op (MPa)",step=0.001, format="%.3f", value=0.0)
    head_hydro = st.number_input("Hydrostatic head, head_hydro (MPa)",step=0.001, format="%.3f", value=0.0)
    Pe = st.number_input("External Design Pressure, Pe (MPa)",step=0.001, format="%.3f", value=0.1034)
    st.write("---")    

    st.write("**MATERIAL PROPERTIES**")
    Sa = st.number_input("Allowable Stress of Material at ambient temperature, Sa (MPa)",step=0.1, format="%.1f", value=138.0)
    S = st.number_input("Allowable Stress of Material at design temperature, S (MPa)",step=0.1, format="%.1f", value=138.0)
    E = st.number_input("Weld Joint Efficiency, E",step=0.01, format="%.2f", value=1.00)
    rho = st.number_input("Material Density, rho (kg/mm3)",step=1.0, format="%.3e", value=7.75e-6)
    B = st.number_input("Factor from applicable material chart of ASME II-D, B (MPa)",step=0.001, format="%.3f", value=96.9)
    MDMT_Curve = st.selectbox("Applicable MDMT Curve (Only for CS and LAS)",["A","B","C","D"],index=3)
    MDMT_UCS66 = st.number_input("Basic MDMT per Table UCS-66 ($\degree$C)",step=0.1, format="%.1f", value=-32.0)
    T_red = st.number_input("MDMT reduction per Fig UCS-66.1M based on ratio calculation (see output), ($\degree$C)",step=0.1, format="%.1f", value=73.0)

#Output Column
with col2:
    st.title("Outputs")

#Draw Sketch
###############################################################################

    import plotly.graph_objects as go
    import numpy as np
    
    # Define the dimensions of the semi-ellipse
    a = 4  # Semi-major axis
    b = 2  # Semi-minor axis
    
    # Generate points for the semi-ellipse
    theta = np.linspace(0, np.pi, 100)
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # Create the semi-ellipse plot
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Ellip. Head'))
    
    # Add a scatter plot for the line
    fig.add_trace(go.Scatter(x=[-a, a], y=[0, 0], mode='lines', name='Tan Line'))
    
    # Add dimension arrows with arrowheads on both sides
    fig.add_annotation(
        x=a, y=0.2,
        ax=-a, ay=0.2,
        xref='x', yref='y',
        axref='x', ayref='y',
        showarrow=True,
        arrowhead=2,
        arrowside='end+start'
    )
    
    # Add centered dimension labels
    fig.add_annotation(
        x=0, y= 0.3,
        text=f'ID {D - 2*CA} ',
        showarrow=False,
        font=dict(size=12, color="Black")
    )

    fig.add_annotation(
        x=0, y= 0.1,
        text=f'Tnom = {tn}, Tmin = {ts}',
        showarrow=False,
        font=dict(size=12, color="Black")
    )

    fig.add_annotation(
        x=0, y= 1.5,
        text=f'Head Depth = {h - CA}',
        showarrow=False,
        font=dict(size=12, color="Black")
    )

    # Update layout
    fig.update_layout(
        title='Elliptical Head (All dimensions in mm)',
        xaxis_title='X-axis',
        yaxis_title='Y-axis',
        xaxis=dict(range=[-a - 1, a + 1],visible=False),
        yaxis=dict(range=[0, b + 1],visible=False),
        showlegend=True
    )
    
    # Display the plot in Streamlit
    st.plotly_chart(fig)
    
    ###########################################################################
    
    st.write("CODE: ASME Sec VIII, Div 1 - 2023 Ed.")
        
    #Thickness Calculations for Internal Pressure
    with st.expander("Expand to see thickness calculation for internal pressure"):
        st.write("**Min Corroded Required Thickness 1-4 (c)**")
        st.latex(r"K = \frac{1}{6} \left ( 2 + \left (\frac {D}{2h} \right )^2 \right )")
        st.latex(rf"K = \frac{{1}}{{6}} \left( 2 + \left( \frac{{{D}}}{{2 \times {h}}} \right)^2 \right)")
        K = 1/6*(2+(D/(2*h))**2)
        st.latex(rf"K = {K:.3f}")
        st.latex(r"t = {PDK \over 2SE-0.2P}")
        st.latex(rf"t = \frac{{{P} \cdot {D} \cdot {K:.3f}}}{{2 \cdot {S} \cdot {E} - 0.2 \cdot {P}}}")
        t = P*D*K/(2*S*E-0.2*P)
        st.latex(rf"t = {t:.1f} mm")
        
        st.write("**Design Thickness = t + CA**")
        st.latex(rf"""= {t + CA:.1f} mm""")

        if ts >= (t + CA):
            st.write(f"**Provided Min Thickness = {ts} mm >= design thickness {t+CA:.1f} mm. [OK]**")
        else:
            st.markdown(":red[Increase Minimum Thickness]")
        
        st.write("Corroded Crown Radius of Dish:")
        st.latex(r"L = {K1}{D}")
        st.latex(rf"L = {K1} \cdot {D}")
        L = K1*D
        st.latex(rf"L = {L}")
        st.latex(rf"\frac{{t}}{{L}} = \frac{{{t:.1f}}}{{{L}}} = {t/L:.4f}")
        
        if t/L < 0.002:
            st.markdown(":red[t/L < 0.002, 1-4(f) shall also be met]")
        else:
            st.write("**t/L >= 0.002 [OK]**")


    #External Pressure Calculation
    with st.expander("Expand to see external pressure calculation"):
        t = ts - CA
        Do = D + 2*t
        Ro = 0.9*(Do)
        Rot = Ro/t
        A = 0.125/(Ro/t)
        Pa = B/(Ro/t)
        st.write("MAEWP or Pa calculation as per UG-33(e)")
        st.latex(rf"t = ts - CA = {ts}-{CA} = {ts-CA:.1f} mm")
        st.latex(rf"D_o = D + 2t = {D} + 2 \cdot {t} = {Do:.1f} mm")
        st.write("Assuming 2:1 Ellipse")
        st.latex(rf"R_o = 0.9D_o = 0.9 \cdot {Do} = {Ro:.1f} mm")
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
        st.write("**MAWP Caclulation 1-4(c)**")
        st.latex(r"""MAWP={2SE(ts-CA) \over DK+0.2(ts-CA)} - head op""")
        st.latex(rf"""MAWP = \frac{{2 \cdot {S} \cdot {E} \cdot ({ts} - {CA})}}{{{D} \cdot {K:.3f} + 0.2 \cdot ({ts} - {CA})}} - {head_op}""")
        MAWP = 2*S*E*(ts-CA)/(D*K+0.2*(ts-CA)) - head_op
        st.latex(rf"""MAWP = {MAWP:0.3f} MPa""")

        #MAPNC
        st.write("K factor for new and cold condition")
        st.latex(r"K = \frac{1}{6} \left ( 2 + \left (\frac {D-2*CA}{2(h-2*CA)} \right )^2 \right )")
        st.latex(rf"K = \frac{{1}}{{6}} \left( 2 + \left( \frac{{{D}-{2} \cdot {CA}}}{{2 \times ({h}-{2} \cdot {CA})}} \right)^2 \right)")
        K = 1/6*(2+((D-2*CA)/(2*(h-2*CA)))**2)
        st.latex(rf"K = {K:.3f}")
        
        st.write("**MAPNC Caclulation 1-4(c)**")
        st.latex(r"""MAPNC={2Sa \cdot E \cdot ts \over (D-2 \cdot CA) \cdot K +0.2 \cdot ts}""")
        st.latex(rf"""MAPNC = \frac{{2 \cdot {Sa} \cdot {E} \cdot {ts}}}{{({D}-2 \cdot {CA}) \cdot {K:.3f} + 0.2 \cdot {ts}}}""")
        MAPNC = 2*Sa*E*ts/((D-2*CA)*K+0.2*ts)
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
        st.write("Assuming a 2:1 Elliptical Head")
        st.latex(r"R_f = 0.17 \cdot (D - 2 \cdot CA) + \frac{tn}{2}")
        st.latex(rf"R_f = 0.17 \cdot ({D} - 2 \cdot {CA})+ {tn/2}")
        Rf = 0.17*(D-2*CA) + tn/2
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
        st.write(f"Governing Thk = ts = {ts} mm")
        st.write(f"Applicable MDMT Curve = {MDMT_Curve}")
        st.write(f"Basic MDMT from Table UCS-66 = {MDMT_UCS66} $\degree$C")
        st.write(f"Reduction in MDMT without impact testing per UCS-66.1M")
        E_star = max(E,0.8)
        st.write(f"$E^*$ = max(E, 0.8) = {E_star}")
        st.latex(r"Ratio = \frac {trE^*}{ts-CA}")
        st.latex(rf"Ratio = \frac{{{tr:.1f} \cdot {E_star}}}{{{ts}-{CA}}}")
        Ratio = tr*E_star/(ts - CA)
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
        st.latex(r"Volume = \frac{\pi}{4} \cdot DB^2 \cdot tn")
        st.latex(rf"Volume = \frac{{\pi}}{{4}} \cdot {DB}^2 \cdot {tn}")
        Volume = 22/7/4*DB**2*tn
        st.latex(rf"Volume = {Volume:.3e} mm^3")
        st.latex(r"Weight = rho \cdot Volume")
        st.latex(rf"Weight = ({rho}) \cdot ({Volume:.3e})")
        Weight = rho*Volume
        st.latex(rf"Weight = {Weight:.1f} kg")
        
        st.write(f"Inside Volume Calc")
        st.latex(r"VolIn = \frac{\pi}{24} \cdot (D - 2 \times CA)^3 + \frac{\pi}{4} \cdot (D - 2 \times CA)^2 \cdot SF")
        st.latex(rf"VolIn = \frac{{\pi}}{{24}} \cdot ({D} - 2 \times {CA})^3+ \frac{{\pi}}{{4}} \cdot ({D} - 2 \times {CA})^2 \cdot {SF}")
        VolIn = 22/7/24*(D-2*CA)**3 + 22/7/4*(D-2*CA)**2*SF
        st.latex(rf"VolIn = {VolIn:.3e} mm^3")
        st.latex(r"WaterWeight = 1e-6 \cdot VolIn")
        WaterWeight = 1e-6*VolIn
        st.latex(rf"WaterWeight = {WaterWeight:.1f} kg")

        #Corroded Thk
        st.write(f"**Weight and Volume Results, Corroded Thickness:**")
        st.write(f"Weight Calc")
        st.latex(r"Volume = \frac{\pi}{4} \cdot DB^2 \cdot (tn - CA)")
        st.latex(rf"Volume = \frac{{\pi}}{{4}} \cdot {DB}^2 \cdot ({tn} - {CA})")
        Volume = 22/7/4*DB**2*(tn-CA)
        st.latex(rf"Volume = {Volume:.3e} mm^3")
        st.latex(r"Weight = rho \cdot Volume")
        st.latex(rf"Weight = ({rho}) \cdot ({Volume:.3e})")
        Weight = rho*Volume
        st.latex(rf"Weight = {Weight:.1f} kg")
        
        st.write(f"Inside Volume Calc")
        st.latex(r"VolIn = \frac{\pi}{24} \cdot D^3 + \frac{\pi}{4} \cdot D^2 \cdot SF")
        st.latex(rf"VolIn = \frac{{\pi}}{{24}} \cdot {D}^3+ \frac{{\pi}}{{4}} \cdot {D}^2 \cdot {SF}")
        VolIn = 22/7/24*D**3 + 22/7/4*D**2*SF
        st.latex(rf"VolIn = {VolIn:.3e} mm^3")
        st.latex(r"WaterWeight = 1e-6 \cdot VolIn")
        WaterWeight = 1e-6*VolIn
        st.latex(rf"WaterWeight = {WaterWeight:.1f} kg")

