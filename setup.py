from setuptools import setup, find_packages

setup(
    name="magml",
    version="0.1.0",
    author="Donglai Ma",
    author_email="dma96@epss.ucla.edu",
    description="A Python toolkit for machine learning in the magnetosphere",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/donglai96/magml",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "pyspedas",
        "tensorflow",
        "torch",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
