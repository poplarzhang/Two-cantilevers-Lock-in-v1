"""
project_summary.py

Generate a summary of the entire project.

Author:
    Your future self will thank you.
"""

import importlib
import inspect
import pkgutil
import os


# ==========================================================
# Print one function
# ==========================================================

def print_function(func):

    print(f"    {func.__name__}{inspect.signature(func)}")

    doc = inspect.getdoc(func)

    if doc:
        print(f"        {doc.splitlines()[0]}")

    try:
        filename = inspect.getsourcefile(func)
        if filename:
            print(f"        File : {os.path.basename(filename)}")
    except Exception:
        pass

    try:
        lines = len(inspect.getsource(func).splitlines())
        print(f"        Lines: {lines}")
    except Exception:
        pass

    print()


# ==========================================================
# Print one class
# ==========================================================

def print_class(cls):

    print(f"\nCLASS: {cls.__name__}")

    doc = inspect.getdoc(cls)

    if doc:
        print(f"    {doc.splitlines()[0]}")

    methods = inspect.getmembers(
        cls,
        inspect.isfunction
    )

    for name, method in methods:

        if name.startswith("__") and name != "__init__":
            continue

        print(
            f"    {name}{inspect.signature(method)}"
        )


# ==========================================================
# Print one module
# ==========================================================

def summarize_module(module_name):

    module = importlib.import_module(module_name)

    print()
    print("=" * 80)
    print(module_name)
    print("=" * 80)

    # ------------------------------------------------------

    functions = []

    classes = []

    for name, obj in inspect.getmembers(module):

        if inspect.isfunction(obj):

            if obj.__module__ == module_name:
                functions.append(obj)

        elif inspect.isclass(obj):

            if obj.__module__ == module_name:
                classes.append(obj)

    if functions:

        print("\nFUNCTIONS\n")

        for func in functions:

            print_function(func)

    if classes:

        print("\nCLASSES\n")

        for cls in classes:

            print_class(cls)


# ==========================================================
# Scan package
# ==========================================================

def summarize_package(package_name):

    package = importlib.import_module(package_name)

    print()
    print("#" * 80)
    print(package_name.upper())
    print("#" * 80)

    summarize_module(package_name)

    if hasattr(package, "__path__"):

        for _, modname, _ in pkgutil.walk_packages(
            package.__path__,
            package.__name__ + "."
        ):

            summarize_module(modname)


# ==========================================================
# Entire project
# ==========================================================

def summarize_project():

    packages = [

        "instrument",

        "measurements",

        "analysis",

    ]

    print("\n")
    print("=" * 80)
    print("TWO CANTILEVERS LOCK-IN FRAMEWORK")
    print("=" * 80)

    for package in packages:

        summarize_package(package)

    print("\n")
    print("=" * 80)
    print("End of summary")
    print("=" * 80)



import contextlib


# ==========================================================
# Write project reference
# ==========================================================

def create_project_reference(
    filename="PROJECT_REFERENCE.md"
):
    """
    Create a Markdown reference document.
    """

    with open(filename, "w", encoding="utf-8") as f:

        with contextlib.redirect_stdout(f):

            print("# Two Cantilevers Lock-in Framework")
            print()

            print("Automatically generated project reference.")
            print()

            summarize_project()

    print(f"Reference written to {filename}")


# ==========================================================
# Create project tree
# ==========================================================

def create_project_tree(
    root=".",
    filename="PROJECT_TREE.txt"
):
    """
    Save a directory tree of the project.
    """

    ignore = {
        "__pycache__",
        ".git",
        ".ipynb_checkpoints",
    }

    with open(filename, "w", encoding="utf-8") as f:

        for current, dirs, files in os.walk(root):

            dirs[:] = [
                d for d in dirs
                if d not in ignore
            ]

            level = current.replace(root, "").count(os.sep)

            indent = "    " * level

            f.write(
                f"{indent}{os.path.basename(current)}/\n"
            )

            subindent = "    " * (level + 1)

            for file in sorted(files):

                f.write(
                    f"{subindent}{file}\n"
                )

    print(f"Project tree written to {filename}")
    
# ==========================================================
# Build documentation
# ==========================================================

def build_project_documentation():

    create_project_reference()

    create_project_tree()

    print()
    print("=" * 60)
    print("Project documentation updated.")
    print("=" * 60)    