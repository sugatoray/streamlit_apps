import streamlit as st
from textwrap import dedent
import utils as U
import kinematics as K

Defaults = U.Defaults

st.write("# Kinematics 1D ✨")

with st.sidebar:
    st.write("## ⚙️ Parameters")

    options = dict()

    options["Dx"] = st.text_input(
        label="Displacement (Dx) 👇",
        value="",
        placeholder="Null",
        help="displacement in meters",
    )
    options["vi"] = st.text_input(
        label="Initial Velocity (vi) 👇",
        value="205",
        placeholder="Null",
        help="Initial velocity in m/s"
    )
    options["vf"] = st.text_input(
        label="Final Velocity (vj) 👇",
        value="315",
        placeholder="Null",
        help="Final velocity in m/s",
    )
    options["a"] = st.text_input(
        label="Acceleration (a) 👇",
        value="",
        placeholder="Null",
        help="Acceleration in m/s^2",
    )
    options["t"] = st.text_input(
        label="Time (t) 👇",
        value="10.0",
        placeholder="Null",
        help="Time in seconds",
    )
    # st.write("**Average Velocity $( v_{avg} )$** 👇")
    options["v_avg"] = st.text_input(
        label="Average Velocity (v_avg) 👇",
        value="",
        placeholder="Null",
        help="Average velocity in m/s",
    )

# with st.expander("Input Parameters", expanded=False):
#     st.json(options)

params = dict((k, float(v)) if v else (k, None) for k, v  in options.items())

with st.expander("Input Parameters", expanded=False):
    st.json(params)

# k1 = K.Kinematics1D(vi=205, vf=315, t=10.0)
k1 = K.Kinematics1D(**params)
result, steps = k1.solve(steps_params=dict(debug=True))

with st.expander("Evaluated Parameters", expanded=True):

    cells = [
        (r"$\Delta x$",  f" `{result.get('Dx')}`", r"$\scriptsize \text{m}$"),
        (r"$a$", f" `{result.get('a')}`", r"$\scriptsize \text{m}/\text{s}^{2}$"),
        (r"$v_{avg}$", f" `{result.get('v_avg')}`", r"$\scriptsize \text{m/s}$"),
        (r"$v_{i}$", f" `{result.get('vi')}`", r"$\scriptsize \text{m/s}$"),
        (r"$v_{f}$", f" `{result.get('vf')}`", r"$\scriptsize \text{m/s}$"),
        (r"$t$", f" `{result.get('t')}`", r"$\scriptsize \text{s}$"),
    ]
    l1 = '| ' + ' | '.join([h for h, _, _ in cells]) + ' |'
    l2 = ':---'.join("|" * (len(cells) + 1))
    l3 = '| ' + ' | '.join([v for _, v, _ in cells]) + ' |'
    l4 = '| ' + ' | '.join([u for _, _, u in cells]) + ' |'

    st.markdown(f"""
    | Params {l1}
    |:---{l2}
    | **Values** {l3}
    | **Units** {l4}

    """)

    st.write("\n")

    st.warning("#### Parameters as JSON")
    st.json(result)

st.error("### Mathematical Steps")

for i, step in enumerate(steps):
    st.latex(r"\begin{aligned}" + "\n" +
             step + "\n" + r"\end{aligned}")
    if i < len(steps) - 1:
        html_text = '<div style="text-align: center"> ⏬ </div>'
        st.write(html_text,
                 unsafe_allow_html=True)

# st.latex(r'''
# \begin{aligned}
#     v_{avg} &= \frac{\left( v_{i} + v_{f} \right)}{2} \\
#     \Delta x &= v_{avg} t \\
#     a &= \frac{\left( v_{f} - v_{i} \right)}{t} \\
# \end{aligned}
# ''')
