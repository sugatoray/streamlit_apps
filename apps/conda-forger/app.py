import os
import streamlit as st

import utils as U
import appfactory as A

Defaults = U.Defaults
options = dict()

os.environ["RECIPES_DIR"] = os.path.join(
    Defaults.APP_DIR, Defaults.DEFAULT_RECIPES_DIR)

recipes_dir = U.create_recipes_dir(recipes_dir=None, app_dir=Defaults.APP_DIR)


st.header("Conda Forger App :zap:")

st.write("This app helps you in creating conda-forge recipes.")

if Defaults.USE_DEBUG_MODE or options.get("debug-mode", False):
    st.write("**Recipes Directory:**")
    st.code(os.environ.get("RECIPES_DIR"))

options = A.make_sidebar(recipes_dir=recipes_dir)

IS_PYPI = options.get("source", Defaults.DEFAULT_PACKAGE_SOURCE).lower() == "pypi"

if IS_PYPI:

    options, generate, clear_workspace = A.update_app_options(options, recipes_dir=recipes_dir)
    st.json(options)

    recipe = A.generate_pypi_recipe(
        options,
        generate=generate,
        recipes_dir=recipes_dir,
    )
