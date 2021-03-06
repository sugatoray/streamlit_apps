import streamlit as st
import os
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional
from textwrap import dedent


def use_debug_mode(watchvariable: str = "ST_DEBUG_MODE", value: str = "0") -> bool:
    # Default is False (ST_DEBUG_MODE = "0")
    return bool(os.environ.get(watchvariable, value) == "1")


def is_streamlit_cloud(watchvariable: str = "ST_IS_STREAMLIT_CLOUD") -> bool:
    """If running in the Streamlit Cloud, set environment variable
    (the same as ``watchvariable``) to 1.
    """
    return bool(os.environ.get(watchvariable, "0") == "1")

@st.cache
@dataclass
class Defaults:
    APP_URL: str = r"https://share.streamlit.io/sugatoray/streamlit_apps/master/apps/kinematics1d/app.py"
    APP_URL_SHORT: str = r"https://tinyurl.com/st-kinematics1d-demo"
    ON_ST_CLOUD: bool = is_streamlit_cloud()
    USE_DEBUG_MODE: bool = use_debug_mode()


def add_about_section():
    """Adds an About section to the app."""

    st.write("## ℹ️ About")
    st.info(
        dedent(
            f"""
        This web [app][#streamlit-app] is maintained by [Sugato Ray][#linkedin].
        You can follow me on social media:
        - [@sugatoray | LinkedIn][#linkedin]
        - [@sugatoray | Twitter][#twitter]
        - [@sugatoray | GitHub][#github]
        [#linkedin]: https://www.linkedin.com/in/sugatoray/
        [#twitter]: https://twitter.com/sugatoray
        [#github]: https://github.com/sugatoray
        [#streamlit-app]: {Defaults.APP_URL}
        Short URL: {Defaults.APP_URL_SHORT}
        """
        )
    )


def show_math_steps(steps: List[str]):
    """Shows mathematical steps from a list of math expressions as LaTeX.
    """
    for i, step in enumerate(steps):
        st.latex(r"\begin{aligned}" + "\n" +
                 step + "\n" + r"\end{aligned}")
        if i < len(steps) - 1:
            html_text = '<div style="text-align: center"> ⏬ </div>'
            st.write(html_text,
                     unsafe_allow_html=True)


def display_result(result: Dict[str, Any], known: Optional[List[str]]=None):
    """Displays evaluated parameters from the result."""
    if known is None:
        known = []

    def unknown_marker(x, unknown_label: str = r" $^{\color{red}(?)}$", known_label: str = ""):
        return known_label if ((x in known) or (not known)) else unknown_label

    cells = [
        (
            r"$\Delta x$" + unknown_marker(x="Dx"),
            f" `{result.get('Dx')}`",
            r"$\scriptsize \text{m}$",
        ),
        (
            r"$a$" + unknown_marker(x="a"),
            f" `{result.get('a')}`",
            r"$\scriptsize \text{m}/\text{s}^{2}$",
        ),
        (
            r"$v_{avg}$" + unknown_marker(x="v_avg"),
            f" `{result.get('v_avg')}`",
            r"$\scriptsize \text{m/s}$",
        ),
        (
            r"$v_{i}$" + unknown_marker(x="vi"),
            f" `{result.get('vi')}`",
            r"$\scriptsize \text{m/s}$",
        ),
        (
            r"$v_{f}$" + unknown_marker(x="vf"),
            f" `{result.get('vf')}`",
            r"$\scriptsize \text{m/s}$",
        ),
        (
            r"$t$" + unknown_marker(x="t"),
            f" `{result.get('t')}`",
            r"$\scriptsize \text{s}$",
        ),
    ]
    l1 = '| ' + ' | '.join([h for h, _, _ in cells]) + ' |'
    l2 = ':---:'.join("|" * (len(cells) + 1))
    l3 = '| ' + ' | '.join([v for _, v, _ in cells]) + ' |'
    l4 = '| ' + ' | '.join([u for _, _, u in cells]) + ' |'

    st.markdown(f"""
    | Params {l1}
    |:---{l2}
    | **Values** {l3}
    | **Units** {l4}

    """)

    st.write("\n")

    st.warning("#### Parameters as JSON 📄")
    st.json(result)

def app_introduction():
    st.write(dedent("""
    This app helps in evaluating the following parameters for 1D kinematics
    problems.
    The app should be used as an educational buddy for accelerated learning
    of 1D kinematics concepts and their application to problems, where at
    least ***three*** of the following parameters are known.

    > - Displacement: {label_Dx}
    > - Acceleration: {label_a}
    > - Time: {label_t}
    > - Initial Velocity: {label_vi}
    > - Final Velocity: {label_vf}
    > - Average Velocity: {label_vavg}

    """.format(
            label_Dx=r"$\Delta x$",
            label_a=r"$a$",
            label_t=r"$t$",
            label_vi=r"$v_{i}$",
            label_vf=r"$v_{f}$",
            label_vavg=r"$v_{avg}$"
            )
        )
    )
