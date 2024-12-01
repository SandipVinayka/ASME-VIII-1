import streamlit as st
import math

#Two Columns for inputs and outputs
col1, col2 = st.columns([1,2]) #col2 width is 2*times col1 width

#Input Column
with col1:
    st.title("Inputs")

    st.write("**GEOMETRY**")
    Desc = st.text_input("Description", value="ASME PTB-4 E4.3.4, E4.4.4 - Torispherical Head")
    CA = st.number_input("Corrosion Allowance, CA (mm)",step=0.1, format="%.1f", value=3.175)
    ID = st.number_input("Corroded Inside Diameter, ID (mm)",step=1.0, format="%.1f", value=1835.15)
    tn = st.number_input("Provided Nominal Thickness, tn (mm)",step=0.1, format="%.1f", value=18.0)
    ts = st.number_input("Minimum Specified thk of head after forming, ts (mm)",step=0.1, format="%.1f", value=15.9)
    SF = st.number_input("Length of straight flange, SF (mm)",step=1.0, format="%.1f", value=50.0)
    L = st.number_input("Corroded Inside Crown Radius, L (mm)",step=1.0, format="%.1f", value=1831.975)
    r = st.number_input("Corroded Inside Knuckle Radius, r (mm)",step=1.0, format="%.1f", value=114.3)
    DB = st.number_input("Blank Dia for forming the ellipsoidal head, DB (mm)",step=1.0, format="%.1f", value=2105.3)
    tr = st.number_input("Required Corroded Thickness for all combination of loads, tr (mm)",step=0.1, format="%.1f", value=9.4)
    st.write("---")    

    st.write("**LOADS**")
    P = st.number_input("Internal Design Pressure including static head, P (MPa)",step=0.001, format="%.3f", value=0.690)
    head_op = st.number_input("Operating static head, head_op (MPa)",step=0.001, format="%.3f", value=0.0)
    head_hydro = st.number_input("Hydrostatic head, head_hydro (MPa)",step=0.001, format="%.3f", value=0.0)
    Pe = st.number_input("External Design Pressure, Pe (MPa)",step=0.001, format="%.3f", value=0.1034)
    st.write("---")    

    st.write("**MATERIAL PROPERTIES**")
    Sa = st.number_input("Allowable Stress of Material at ambient temperature, Sa (MPa)",step=0.1, format="%.1f", value=118.0)
    S = st.number_input("Allowable Stress of Material at design temperature, S (MPa)",step=0.1, format="%.1f", value=118.0)
    E = st.number_input("Weld Joint Efficiency, E",step=0.01, format="%.2f", value=1.00)
    rho = st.number_input("Material Density, rho (kg/mm3)",step=1.0, format="%.3e", value=7.75e-6)
    B = st.number_input("Factor from applicable material chart of ASME II-D, B (MPa)",step=0.001, format="%.3f", value=56.6)
    MDMT_Curve = st.selectbox("Applicable MDMT Curve (Only for CS and LAS)",["A","B","C","D"],index=0)
    MDMT_UCS66 = st.number_input("Basic MDMT per Table UCS-66 ($\degree$C)",step=0.1, format="%.1f", value=6.0)
    T_red = st.number_input("MDMT reduction per Fig UCS-66.1M based on ratio calculation (see output), ($\degree$C)",step=0.1, format="%.1f", value=15.0)

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
    
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Tori-Head'))
    
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
        text=f'ID {ID - 2*CA:.1f} ',
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
        text=f'Inside Crown Radius = {L - CA}',
        showarrow=False,
        font=dict(size=12, color="Black")
    )

    fig.add_annotation(
        x=0, y= 1.3,
        text=f'Inside Knuckle Radius = {r - CA}',
        showarrow=False,
        font=dict(size=12, color="Black")
    )

    # Update layout
    fig.update_layout(
        title='Torispherical Head (All dimensions in mm)',
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
        
    #Thickness Calculations for internal pressure
    with st.expander("Expand to see thickness calculation for internal pressure"):
        st.write("**Min Corroded Required Thickness 1-4 (d)**")
        st.latex(r"M = \frac{1}{4} \left ( 3 + \sqrt \frac {L}{r} \right )")
        st.latex(rf"M = \frac{{1}}{{4}} \left( 3 + \sqrt{{\frac{{{L}}}{{{r}}}}} \right)")    
        M = 1/4*(3+(L/r)**0.5)
        st.latex(rf"M = {M:.3f}")
        st.latex(r"t = {PLM \over 2SE-0.2P}")
        st.latex(rf"t = \frac{{{P} \cdot {L} \cdot {M:.3f}}}{{2 \cdot {S} \cdot {E} - 0.2 \cdot {P}}}")
        t = P*L*M/(2*S*E-0.2*P)
        st.latex(rf"t = {t:.1f} mm")
        
        st.write("**Design Thickness = t + CA**")
        st.latex(rf"""= {t + CA:.1f} mm""")
        if t/L < 0.002:
            st.markdown(":red[t/L < 0.002, 1-4(f) shall also be met]")

        if ts >= (t + CA):
            st.write(f"**Provided Min Thickness = {ts} mm >= design thickness {t+CA:.1f} mm. [OK]**")
        else:
            st.markdown(":red[Increase Minimum Thickness]")

    #External Pressure Calculation
    with st.expander("Expand to see external pressure calculation"):
        t = ts - CA
        Ro = L+t
        Rot = Ro/t
        A = 0.125/(Ro/t)
        Pa = B/(Ro/t)
        st.write("MAEWP or Pa calculation as per UG-33(e)")
        st.latex(rf"t = ts - CA = {ts}-{CA} = {ts-CA:.1f} mm")
        st.latex(rf"R_o = L + t = {L}+{t:.1f} = {Ro:.1f} mm")
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
        st.write("**MAWP Caclulation 1-4(d)**")
        st.latex(r"""MAWP={2SE(ts-CA) \over LM+0.2(ts-CA)} - head op""")
        st.latex(rf"""MAWP = \frac{{2 \cdot {S} \cdot {E} \cdot ({ts} - {CA})}}{{{L} \cdot {M:.3f} + 0.2 \cdot ({ts} - {CA})}} - {head_op}""")
        MAWP = 2*S*E*(ts-CA)/(L*M+0.2*(ts-CA)) - head_op
        st.latex(rf"""MAWP = {MAWP:0.3f} MPa""")
        
        #MAPNC
        st.write("M factor for new and cold condition")
        st.latex(r"M = \frac{1}{4} \left ( 3 + \sqrt \frac {L-CA}{r-CA} \right )")
        st.latex(rf"M = \frac{{1}}{{4}} \left( 3 + \sqrt{{\frac{{{L-CA}}}{{{r-CA}}}}} \right)")    
        M = 1/4*(3+((L-CA)/(r-CA))**0.5)
        st.latex(rf"M = {M:.3f}")

        st.write("**MAPNC Caclulation 1-4(d)**")
        st.latex(r"""MAPNC={2Sa \cdot E \cdot ts \over (L-CA) \cdot M +0.2 \cdot ts}""")
        st.latex(rf"""MAPNC = \frac{{2 \cdot {Sa} \cdot {E} \cdot {ts}}}{{({L}-{CA}) \cdot {M:.3f} + 0.2 \cdot {ts}}}""")
        MAPNC = 2*Sa*E*ts/((L-CA)*M+0.2*ts)
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
        st.latex(r"R_f = r - CA + \frac{tn}{2}")
        st.latex(rf"R_f = {r} - {CA} + {tn/2}")
        Rf = r - CA + tn/2
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
        h = (L-CA) - ((L-r)**2 - (ID/2 - r)**2)**0.5
        c = ((L-r)**2 - (L-CA-h)**2)**0.5
        VolIn = math.pi/3*(2*h*(L-CA)**2-(2*(r-CA)**2+c**2+2*(r-CA)*(L-CA))*(L-CA-h)+3*(r-CA)**2*c*math.asin((L-CA-h)/(L-r)))+ math.pi/4*(ID-2*CA)**2*SF
        st.latex(rf"VolIn = {VolIn:.3e} mm^3")
        st.latex(r"WaterWeight = 1e-6 \cdot VolIn")
        WaterWeight = 1e-6*VolIn
        st.latex(rf"WaterWeight = {WaterWeight:.1f} kg")

        #Corroded Thk
        st.write(f"**Weight and Volume Results, Corroded Thickness:**")
        st.write(f"Weight Calc")
        st.latex(r"Volume = \frac{\pi}{4} \cdot DB^2 \cdot (tn-CA)")
        st.latex(rf"Volume = \frac{{\pi}}{{4}} \cdot {DB}^2 \cdot {tn-CA}")
        Volume = 22/7/4*DB**2*(tn-CA)
        st.latex(rf"Volume = {Volume:.3e} mm^3")
        st.latex(r"Weight = rho \cdot Volume")
        st.latex(rf"Weight = ({rho}) \cdot ({Volume:.3e})")
        Weight = rho*Volume
        st.latex(rf"Weight = {Weight:.1f} kg")

        st.write(f"Inside Volume Calc")
        h = L - ((L-r)**2 - (ID/2 - r)**2)**0.5
        c = ((L-r)**2 - (L-h)**2)**0.5
        VolIn = math.pi/3*(2*h*L**2-(2*r**2+c**2+2*r*L)*(L-h)+3*r**2*c*math.asin((L-h)/(L-r)))+ math.pi/4*ID**2*SF
        st.latex(rf"VolIn = {VolIn:.3e} mm^3")
        st.latex(r"WaterWeight = 1e-6 \cdot VolIn")
        WaterWeight = 1e-6*VolIn
        st.latex(rf"WaterWeight = {WaterWeight:.1f} kg")
