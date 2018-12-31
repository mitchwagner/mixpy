import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mixpy",
    version="0.1",
    author="Mitchell James Wagner",
    author_email="mitchell.j.wagner@gmail.com",
    description="A Python 3 MIX Simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mitchwagner/mixpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha"
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        mypy==0.650
        mypy-extensions==0.4.1
        typed-ast==1.1.1
    ]
)
