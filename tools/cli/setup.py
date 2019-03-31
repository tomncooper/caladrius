from setuptools import setup

setup(
    name="magpie",
    version="0.1",
    py_modules=["caladrius"],
    install_requires=["click", "requests"],
    entry_points="""
        [console_scripts]
        magpie=magpie:cli
    """,
)
