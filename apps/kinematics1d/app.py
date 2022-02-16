import streamlit as st
from textwrap import dedent
from IPython.display import display, Markdown, Latex
from apps.kinematics1d.kinematics.k1d import show_steps

import utils as U
from kinematics import Kinematics1D

Defaults = U.Defaults

st.write("# Kinematics 1D ✨")

with st.sidebar:
    st.write("## ⚙️ Parameters")

    options = dict()

    options["Dx"] = st.text_input(
        label="Displacement (Dx) 👇",
        value="",
        placeholder="0.0",
        help="displacement in meters",
    )
    options["vi"] = st.text_input(
        label="Initial Velocity (vi) 👇",
        value="",
        placeholder="0.0",
        help="Initial velocity in m/s"
    )
    options["vf"] = st.text_input(
        label="Final Velocity (vj) 👇",
        value="",
        placeholder="0.0",
        help="Final velocity in m/s",
    )
    options["a"] = st.text_input(
        label="Acceleration (a) 👇",
        value="",
        placeholder="0.0",
        help="Acceleration in m/s^2",
    )
    options["t"] = st.text_input(
        label="Time (t) 👇",
        value="",
        placeholder="0.0",
        help="Time in seconds",
    )
    st.write("**Average Velocity $( v_{avg} )$** 👇")
    options["v_avg"] = st.text_input(
        label="v_avg 👇",
        value="",
        placeholder="0.0",
        help="Average velocity in m/s",
    )
    st.write("**Average Acceleration $( a_{avg} )$** 👇")
    options["a_avg"] = st.text_input(
        label="a_avg",
        value="",
        placeholder="0.0",
        help="Average acceleration in m/s^2",
    )


st.json(options)

params = dict((k, v) if v else (k, None) for k, v  in options.items())

st.json(params)

k1 = Kinematics1D(vi=205, vf=315, t=10.0)
result, steps = k1.solve(steps_params=dict(debug=True))

st.json(result)

st.error("## Mathematical Steps")

for i, step in enumerate(steps):
    st.latex(r"\begin{aligned}" + "\n" +
             step + "\n" + r"\end{aligned}")
    if i < len(steps) - 1:
        html_text = '<div style="text-align: center"> ⏬ </div>'
        st.write(html_text,
                 unsafe_allow_html=True)

st.latex(r'''
\begin{aligned}
    v_{avg} &= \frac{\left( v_{i} + v_{f} \right)}{2} \\
    \Delta x &= v_{avg} t \\
    a &= \frac{\left( v_{f} - v_{i} \right)}{t} \\
\end{aligned}
''')

st.latex(r'''
$$\Delta x &= v_{avg} t$$
$$a &= \frac{\left( v_{f} - v_{i} \right)}{t}$$
''')
