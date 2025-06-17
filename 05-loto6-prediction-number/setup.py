"""
Loto6 Predictor Setup
"""

from setuptools import setup, find_packages

setup(
    name="loto6-predictor",
    version="1.0.0",
    description="ロト6予測システム",
    author="Claude Code",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "requests>=2.28.0",
        "streamlit>=1.28.0",
        "plotly>=5.17.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)