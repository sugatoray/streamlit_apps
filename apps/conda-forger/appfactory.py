import os
import subprocess
import streamlit as st
from textwrap import dedent
from typing import Optional, Dict, Any

import utils as U

Defaults = U.Defaults

def make_sidebar(recipes_dir: Optional[str]=None):
    if recipes_dir is None:
        recipes_dir = os.environ.get("RECIPES_DIR")
    with st.sidebar:
        st.write("## ⚙️ Parameters")
        options = dict()

        options["source"] = st.radio(
            label="Select Source",
            options=["GitHub", "PyPI", ],
            index=1,
        )

        options["strict-conda-forge"] = st.checkbox(
            label="Strict conda-forge",
            value=False,
        )

        options["clearall"] = st.checkbox(
            label="Clear Workspace",
            value=True,
        )
        if options["clearall"]:
            U.clearall(recipes_dir=recipes_dir) # type: ignore

        if not Defaults.ON_ST_CLOUD:
            st.write("## :fire: Use Debug Mode")
            options["debug-mode"] = st.checkbox(
                label="Use Debug Mode",
                value=False,
            )
            os.environ["ST_DEBUG_MODE"] = str(int(options["debug-mode"]))
            Defaults.USE_DEBUG_MODE = options.get("debug-mode", False)

        st.write("---")
        U.add_about_section()

    return options


def update_app_options(options: Dict[str, Any], recipes_dir: Optional[str]=None):
    if recipes_dir is None:
        recipes_dir = os.environ.get('RECIPES_DIR')
    col1, col2 = st.columns([3, 2])
    with col1:
        options["package_name"] = st.text_input(
            label="PyPI Package Name 👇",
            value="",
            placeholder="Null",
            help="displacement in meters",
        )

    with col2:
        options["package_version"] = st.text_input(
            label="PyPI Package Version 👇",
            value="",
            placeholder="Null",
            help="displacement in meters",
        )

    _, col22, _, col24, _ = st.columns([2, 2, 1, 2, 2])
    with col22:
        generate = st.button(label="Generate Recipe")
    with col24:
        clear_workspace = st.button(label="Clear Workspace")
        if clear_workspace:
            U.clearall(recipes_dir=recipes_dir)
    return options, generate, clear_workspace


def generate_pypi_recipe(options: Dict[str, Any], generate: bool = False, recipes_dir: Optional[str] = None):
    if recipes_dir is None:
        recipes_dir = os.environ.get('RECIPES_DIR')
    package_name = options.get("package_name", None).strip()
    package_version = options.get("package_version", None).strip()
    if not package_version or package_version is None:
        package_version = ""
    if package_name and package_name is not None:
        command = U.create_command(
            package_name, options, package_version=package_version)
        st.info("### Command")
        if Defaults.USE_DEBUG_MODE or options.get("debug-mode", False):
            st.code(command, language="sh")
        else:
            st.code(command.split("-o")[0], language="sh")
        try:
            if generate:
                recipes_dir = U.create_recipes_dir(recipes_dir=recipes_dir)
                result = subprocess.run(
                    command, capture_output=True, shell=True, timeout=20, check=True)

                if result.returncode == 0:
                    recipe = U.show_recipe(
                        package_name, recipes_dir=recipes_dir)
                    return recipe

        except subprocess.CalledProcessError as e:
            st.error(dedent(f"""### CalledProcessError

            {e}

            """))
            return None
