import os
import subprocess
import streamlit as st
from textwrap import dedent
from typing import Optional, Dict, Any

from components import utils as U

Defaults = U.Defaults
MAX_TIME_OUT = Defaults.MAX_TIME_OUT

try:
    MAX_TIME_OUT = int(os.environ.get("ST_MAX_TIME_OUT", Defaults.MAX_TIME_OUT))
except ValueError as e:
    MAX_TIME_OUT = Defaults.MAX_TIME_OUT
finally:
    os.environ["ST_MAX_TIME_OUT"] = str(MAX_TIME_OUT)


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


        options["timeout"] = st.number_input(
            label="Timeout (in seconds)",
            min_value=10,
            max_value=MAX_TIME_OUT,
            value=Defaults.TIME_OUT,
            step=5,
        )

        options["use_wide_layout"] = st.checkbox(
            label="Use Wide Layout",
            value=Defaults.USE_WIDE_LAYOUT, # False
        )


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

    IS_PYPI = U.source_is_pypi(options)
    IS_GITHUB = U.source_is_github(options)    
    
    
    if IS_PYPI:
        col1, col2 = st.columns([3, 2])
        with col1:
            options["package_name"] = st.text_input(
                label="PyPI Package Name 👇",
                value="",
                placeholder="Null",
                help="Provide package name from PyPI",
            )

        with col2:
            options["package_version"] = st.text_input(
                label="PyPI Package Version 👇",
                value="",
                placeholder="Null",
                help="Optionally, specify package version from PyPI",
            )
    
    elif IS_GITHUB:
        col1, col2 = st.columns([5, 2])
        with col1:
            options["github_repo_url"] = st.text_input(
                label="GitHub Repository URL 👇",
                value="",
                placeholder="https://github.com/{{ OWNER }}/{{ REPOSITORY }}",
                help="Provide GitHub package repository url",
            )

        with col2:
            options["github_release_tag"] = st.text_input(
                label="GitHub Release Tag 👇",
                value="",
                placeholder="Null",
                help="Optionally, provide the GitHub release tag from the repository.",
            )

    _, col22, _, col24, _ = st.columns([2, 2, 1, 2, 2])
    with col22:
        generate = st.button(label="Generate Recipe")
    with col24:
        clear_workspace = st.button(label="Clear Workspace")
        if clear_workspace:
            U.clearall(recipes_dir=recipes_dir)
    return options, generate, clear_workspace


def generate_recipe(options: Dict[str, Any], generate: bool = False, recipes_dir: Optional[str] = None):
    if recipes_dir is None:
        recipes_dir = os.environ.get('RECIPES_DIR')
    
    IS_PYPI = U.source_is_pypi(options)
    IS_GITHUB = U.source_is_github(options)

    package_name: str = ""
    package_version: str = ""
    github_repo_url: str = ""
    github_release_tag: str = ""
    command: str = ""

    if IS_PYPI:
        package_name = options.get("package_name", None).strip()
        package_version = options.get("package_version", None).strip()

        if not package_version or package_version is None:
            package_version = ""
        if package_name and package_name is not None:
            command = U.create_command(options, 
                package_name = package_name, 
                package_version = package_version
            )
    
    elif IS_GITHUB:
        github_repo_url = options.get("github_repo_url", None).strip()
        github_release_tag = options.get("github_release_tag", None).strip()

        if not github_release_tag or github_release_tag is None:
            github_release_tag = ""
        if github_repo_url and github_repo_url is not None:
            command = U.create_command(options, 
                github_repo_url = github_repo_url,
                github_release_tag = github_release_tag
            )
            
            parsed = U.parse_github_url(url=github_repo_url).copy()
            _ = parsed.pop("extra")
            options.update({"parsed": parsed})

            package_name = parsed.get("repo", U.dummy_package_name())
            
            if options.get("debug-mode", False):
                st.json({"options": options, "package_name_dir": package_name})
    
    if command and package_name:
        st.info("### Command 🍎")
        if Defaults.USE_DEBUG_MODE or options.get("debug-mode", False):
            st.code(command, language="sh")
        else:
            st.code(command.split("-o")[0], language="sh")
        if generate:
            with st.spinner("Generating recipe... ⏳"):
                recipes_dir = U.create_recipes_dir(recipes_dir=recipes_dir)
                try:
                    result = U.run_command(command, timeout=options.get(
                        "timeout", Defaults.TIME_OUT))

                    if result.returncode == 0:
                        recipe = U.show_recipe(
                            package_name, recipes_dir=recipes_dir)
                        return recipe

                except subprocess.CalledProcessError as e:

                    msg_params = dict(height=300, width=700, bgcolor="fa5043", textcolor="fff")
                    U.show_message("Bad Request!", **msg_params)

                    with st.expander("See Error Details ⛔", expanded=False):
                        st.error(dedent(f"""### CalledProcessError

                        {e}

                        """))
                        return None
