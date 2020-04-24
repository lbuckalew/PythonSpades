import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyspades",
    version="0.0.1",
    author="Louis Buckalew",
    author_email="lwb0003@auburn.edu",
    description="Python implementation of a 4 person game of spades.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lbuckalew/PythonSpades",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)