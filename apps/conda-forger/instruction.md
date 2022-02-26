# Instruction

## How to create a conda-forge package for a PyPI package?

1. Go to https://github.com/conda-forge/staged-recipes
2. Fork the repository.
3. Create a new branch by the name of the PyPI package (say, `genespeak`).
4. Hit `.` (period or dot) on your keyboard.
5. The same forked repository will open on [vscode.dev](https://vscode.dev) with the branch you just created.
6. Create a folder by the name of the PyPI package (*use all lower case*).
7. Create a file `meta.yaml` in side the folder you created in the previous step.
8. Generate the recipe for the PyPI package by specifying a version number (use the [conda-forger app](https://tinyurl.com/conda-forger)).
9. Copy the generated recipe and paste inside the `meta.yaml` file you just created.
10. Go back to https://github.com/conda-forge/staged-recipes or your fork of the staged-recipes.
    -  Initiate a pull request (PR).
    -  Follow the instructions in the PR template.
    -  Create the PR.
11. Now the CI (continuous integration) processes will run (typically they run on azure). Most likely the build process will fail owing to some problem in your recipe.
    -  Read the failure reason in the CI logs (you want to focus on the `docker build` stage).
    -  Iteratively fix them until the build is successful.
12. Once your package build is successful, paste the following in a comment.

    ```md
    PR is ready. Request for review/merging.

    cc: @conda-forge/help-python
    ```

Goodluck! 👍
