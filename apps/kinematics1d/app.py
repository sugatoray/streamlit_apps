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
        label="Final Velocity (vf) 👇",
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

    st.write("---")

    U.add_about_section()

# with st.expander("Input Parameters", expanded=False):
#     st.json(options)

params = dict((k, float(v)) if v else (k, None) for k, v  in options.items())
known = list(k for k, v in params.items() if v is not None)

st.success("### Parameters ⚙️")

with st.expander("Input Parameters 📥", expanded=False):
    st.json(params)

with st.container():
    try:
        # k1 = K.Kinematics1D(vi=205, vf=315, t=10.0)
        k1 = K.Kinematics1D(**params)
        result, steps = k1.solve(steps_params=dict(debug=Defaults.USE_DEBUG_MODE))

        with st.expander("Evaluated Parameters 🎁", expanded=True):
            U.display_result(result, known = known)

        st.info("### Mathematical Steps 🎈🎉")
        U.show_math_steps(steps)

    except ValueError as ve:
        st.error(dedent(f"""#### Insufficient Parameters :fire:

        {ve}

        """))

    except NotImplementedError as ne:
        st.error(dedent(f"""#### No Implementation Exists for the Parameters ❓

        The set of parameters provided have no implementation to evaluate
        the unknown parameters.

        {ne}

        """))


# st.latex(r'''
# \begin{aligned}
#     v_{avg} &= \frac{\left( v_{i} + v_{f} \right)}{2} \\
#     \Delta x &= v_{avg} t \\
#     a &= \frac{\left( v_{f} - v_{i} \right)}{t} \\
# \end{aligned}
# ''')
