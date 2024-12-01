import streamlit as st

# Sidebar
st.set_page_config(
    page_title="ASME Sec VIII Div 1 Calculator",
    page_icon=":smiley:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("Calculators")
st.sidebar.write("Select Calculator below")

#Two Columns for inputs and outputs
col1, col2 = st.columns([1,2]) #col2 width is 2*times col1 width

#Input Column
with col1:
    st.title("Inputs")
    
    st.write("**GEOMETRY**")
    Desc = st.text_input("Description", value="ASME PTB-4 E4.3.1, E4.4.1 - Cylindrical Shell")
    CA = st.number_input("Corrosion Allowance, CA (mm)",step=0.1, format="%.1f", value=3.175)   
    R = st.number_input("Corroded Inside Radius, R (mm)",step=1.0, format="%.1f", value=1146.175)
    tn = st.number_input("Provided Nominal Thickness, tn (mm)",step=0.1, format="%.1f", value=28.575)
    Lvol = st.number_input("Length of cylinder for volume calc, Lvol (mm)",step=1.0, format="%.1f", value=3000.0)
    L = st.number_input("Design Length of Section between lines of supports, L (mm)",step=1.0, format="%.1f", value=16154.4)
    tr = st.number_input("Required Corroded Thickness for all combination of loads, tr (mm)",step=0.1, format="%.1f", value=20.6)
    st.write("---")    

    st.write("**LOADS**")
    P = st.number_input("Internal Design Pressure including static head, P (MPa)",step=0.001, format="%.3f", value=2.455)
    head_op = st.number_input("Operating static head, head_op (MPa)",step=0.001, format="%.3f", value=0.0)
    head_hydro = st.number_input("Hydrostatic head, head_hydro (MPa)",step=0.001, format="%.3f", value=0.0)
    Pe = st.number_input("External Design Pressure, Pe (MPa)",step=0.001, format="%.3f", value=0.1034)
    st.write("---")

    st.write("**MATERIAL PROPERTIES**")
    Sa = st.number_input("Allowable Stress of Material at ambient temperature, Sa (MPa)",step=0.1, format="%.1f", value=138.0)
    S = st.number_input("Allowable Stress of Material at internal design temperature, S (MPa)",step=0.1, format="%.1f", value=138.0)
    E = st.number_input("Weld Joint Efficiency, E",step=0.01, format="%.2f", value=1.00)
    rho = st.number_input("Material Density, rho (kg/mm3)",step=1.0, format="%.3e", value=7.75e-6)
    A = st.number_input("Factor A from Fig G of ASME II-D, A",step=1.0, format="%.3e", value=1.95e-4)
    B = st.number_input("Factor from applicable material chart of ASME II-D, B (MPa)",step=0.001, format="%.3f", value=19.5)
    MDMT_Curve = st.selectbox("Applicable MDMT Curve (Only for CS and LAS)",["A","B","C","D"],index=3)
    MDMT_UCS66 = st.number_input("Basic MDMT per Table UCS-66 ($\degree$C)",step=0.1, format="%.1f", value=-32.0)
    T_red = st.number_input("MDMT reduction per Fig UCS-66.1M based on ratio calculation (see output), ($\degree$C)",step=0.1, format="%.1f", value=12.0)

#Output Column
with col2:
    st.title("Outputs")
    
    #Draw Sketch
    ###########################################################################
    import plotly.graph_objects as go

    # Define the dimensions of the rectangle
    width = 1000
    height = 3000

    # Create the rectangle plot
    fig = go.Figure()

    # Add the rectangle
    fig.add_shape(
        type='rect',
        x0=0, y0=0, x1=width, y1=height,
        line=dict(color='RoyalBlue')
    )

    # Add dimension arrows with arrowheads on both sides
    fig.add_annotation(
        x=width, y=height/2,
        ax=0, ay=height/2,
        xref='x', yref='y',
        axref='x', ayref='y',
        showarrow=True,
        arrowhead=2,
        arrowside='end+start'
    )

    fig.add_annotation(
        x=width + 50, y=height,
        ax=width + 50, ay=0,
        xref='x', yref='y',
        axref='x', ayref='y',
        showarrow=True,
        arrowhead=2,
        arrowside='end+start'
    )
    
    # Add centered dimension labels
    fig.add_annotation(
        x=width / 2, y=height/1.8,
        text=f'ID {2*(R-CA)} x Thk {tn}',
        showarrow=False,
        font=dict(size=12, color="Black")
    )

    fig.add_annotation(
        x=width+125, y=height/2,
        text=f'Lvol {Lvol}',
        showarrow=False,
        font=dict(size=12, color="Black")
    )
    
    # Add dimension labels
    fig.add_trace(go.Scatter(x=[width / 2], y=[-0.7], text=[f''], mode='text', showlegend=False))
    fig.add_trace(go.Scatter(x=[-0.7], y=[height / 2], text=[f''], mode='text', showlegend=False))

    # Update layout
    fig.update_layout(
        title=f'Cylindrical Shell (All dimensions in mm)',
        xaxis_title='X-axis',
        yaxis_title='Y-axis',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    )
    
    # Display the plot in Streamlit
    st.plotly_chart(fig)
    ###########################################################################
    
    st.write("**CODE: ASME Sec VIII, Div 1 - 2023 Ed.**")
    
    #Thickness Calculations for internal pressure
    with st.expander("Expand to see thickness calculation for internal pressure"):
        if P > 0.385*S*E:
            st.markdown(":red[P > 0.385SE, UG-27 (c)(1) not valid]")
        st.write("**Min Corroded Required Thickness UG-27 (c)(1)**")
        st.latex(r"""t = {PR \over SE-0.6P}""")
        st.latex(rf"""t = \frac{{{P} \cdot {R}}}{{{S} \cdot {E} - 0.6 \cdot {P}}}""")
        t = P*R/(S*E-0.6*P)
        st.latex(rf"""t = {t:0.1f} mm""")
        
        st.write("**Design Thickness = t + CA**")
        st.latex(rf"""= {t + CA:.1f} mm""")

        if tn >= (t + CA):
            st.write(f"**Provided Thickness = {tn} mm >= design thickness {t+CA:.1f} mm. [OK]**")
        else:
            st.markdown(":red[Failed in internal pressure]")
        
    #External Pressure Calculation
    with st.expander("Expand to see external pressure calculation"):
        t = tn - CA
        Do = 2*(R+t)
        Dot = Do/t
        LDo = L/Do
        Pa = 4*B/3/Dot
        if Dot<10:
            st.markdown(":red[Do/t < 10, UG-28 (c)(1) not valid]")
        st.write("MAEWP or Pa calculation as per UG-28(c)(1)")
        st.latex(rf"t = tn - CA = {tn}-{CA} = {tn-CA} mm")
        st.latex(rf"D_o = 2 \cdot (R+t) = 2 \cdot ({R}+{t}) = {Do} mm")
        st.latex(rf"\frac{{D_o}}{{t}} = \frac{{{Do}}}{{{t}}} = {Dot:.3f}")
        st.latex(rf"\frac{{L}}{{D_o}} = \frac{{{L}}}{{{Do}}} = {LDo:.3f}")
        st.latex(rf"A = {A} \text{{ (User Input)}}")
        st.latex(rf"B = {B} MPa \text{{ (User Input)}}")
        st.latex(rf"P_a = \frac{{4B}}{{3D_o/t}} = \frac{{{4 * B}}}{{{3 * Do / t:.3f}}} = {Pa:.3f} MPa")
        
        if Pa >= Pe:
            st.write(f"**MAEWP = {Pa:.3f} MPa >= Design External Pressure {Pe:.3f} MPa. [OK]**")
        else:
            st.markdown(":red[Failed in external Pressure]")
        
    #MAWP and MAPNC Calculations
    with st.expander("Expand to see MAWP and MAPNC calculation"):
        #MAWP
        st.write("**MAWP Caclulation UG-27 (c)(1)**")
        st.latex(r"""MAWP={SE(tn-CA) \over R+0.6(tn-CA)} - head op""")
        st.latex(rf"""MAWP = \frac{{{S} \cdot {E} \cdot ({tn} - {CA})}}{{{R} + 0.6 \cdot ({tn} - {CA})}} - {head_op}""")
        MAWP = S*E*(tn-CA)/(R+0.6*(tn-CA)) - head_op
        st.latex(rf"""MAWP = {MAWP:0.3f} MPa""")
        
        #MAPNC
        st.write("**MAPNC Caclulation UG-27 (c)(1)**")
        st.latex(r"""MAPNC={SaEtn \over R+0.6tn}""")
        st.latex(rf"""MAPNC = \frac{{{Sa} \cdot {E} \cdot {tn}}}{{{R} + 0.6 \cdot {tn}}}""")
        MAPNC = Sa*E*tn/(R+0.6*tn)
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
        st.latex(r"R_{f} = R - CA + \frac{tn}{2}")
        st.latex(rf"R_f = {R} - {CA} + {tn/2}")
        Rf = R - CA + tn/2
        st.latex(rf"R_f = {Rf} mm")
        st.write("$R_{o}$ is infinity for a flat plate. Accordingly $\epsilon_f$ is calculated as")
        st.latex(r"\epsilon_{f} = \frac {50tn}{R_{f}}")
        st.latex(rf"\epsilon_f = 50 \cdot \frac{{{tn}}}{{{Rf}}}")
        epf = 50*tn/Rf
        st.latex(rf"""\epsilon_f = {epf:.2f} \%""")
        if epf > 5:
            st.write("Note: Please Check Requirements of UCS-79 as Elongation is > 5%.")

    #MDMT Calculations
    with st.expander("Expand to see MDMT calculations"):
        st.write(f"**MDMT Calculations per UCS-66 (Valid only for CS and LAS)**")
        st.write(f"Governing Thk = tn = {tn} mm")
        st.write(f"Applicable MDMT Curve = {MDMT_Curve}")
        st.write(f"Basic MDMT from Table UCS-66 = {MDMT_UCS66} $\degree$C")
        st.write(f"Reduction in MDMT without impact testing per UCS-66.1M")
        E_star = max(E,0.8)
        st.write(f"$E^*$ = max(E, 0.8) = {E_star}")
        st.latex(r"Ratio = \frac {trE^*}{tn-CA}")
        st.latex(rf"Ratio = \frac{{{tr:.1f} \cdot {E_star}}}{{{tn}-{CA}}}")
        Ratio = tr*E_star/(tn - CA)
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
        st.latex(r"Volume =2 \pi \cdot (R-CA + tn/2) \cdot tn \cdot Lvol")
        st.latex(rf"Volume =2 \pi \cdot ({R}-{CA}+{tn/2}) \cdot {tn} \cdot {Lvol}")
        Volume = 2*22/7*(R-CA+tn/2)*tn*Lvol
        st.latex(rf"Volume = {Volume:.3e} mm^3")
        st.latex(r"Weight = rho \cdot Volume")
        st.latex(rf"Weight = ({rho}) \cdot ({Volume:.3e})")
        Weight = rho*Volume
        st.latex(rf"Weight = {Weight:.1f} kg")
        
        st.write(f"Inside Volume Calc")
        st.latex(r"VolIn = \pi (R - CA)^2 \cdot Lvol")
        st.latex(rf"VolIn = \pi ({R} - {CA})^2 \cdot {Lvol}")
        VolIn = 22/7*(R-CA)**2*Lvol
        st.latex(rf"VolIn = {VolIn:.3e} mm^3")
        st.latex(r"WaterWeight = 1e-6 \cdot VolIn")
        WaterWeight = 1e-6*VolIn
        st.latex(rf"WaterWeight = {WaterWeight:.1f} kg")

        #Corroded Thk
        st.write(f"**Weight and Volume Results, Corroded Thickness:**")
        st.write(f"Weight Calc")
        st.latex(r"Volume =2 \pi \cdot (R + (tn - CA)/2) \cdot (tn - CA) \cdot Lvol")
        st.latex(rf"Volume =2 \pi \cdot ({R}+{(tn-CA)/2}) \cdot ({tn - CA}) \cdot {Lvol}")
        Volume = 2*22/7*(R+(tn-CA)/2)*(tn-CA)*Lvol
        st.latex(rf"Volume = {Volume:.3e} mm^3")
        st.latex(r"Weight = rho \cdot Volume")
        st.latex(rf"Weight = ({rho}) \cdot ({Volume:.3e})")
        Weight = rho*Volume
        st.latex(rf"Weight = {Weight:.1f} kg")
        
        st.write(f"Inside Volume Calc")
        st.latex(r"VolIn = \pi R^2 \cdot Lvol")
        st.latex(rf"VolIn = \pi {R}^2 \cdot {Lvol}")
        VolIn = 22/7*R**2*Lvol
        st.latex(rf"VolIn = {VolIn:.3e} mm^3")
        st.latex(r"WaterWeight = 1e-6 \cdot VolIn")
        WaterWeight = 1e-6*VolIn
        st.latex(rf"WaterWeight = {WaterWeight:.1f} kg")



