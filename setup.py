from setuptools import setup, find_packages

setup(
    name="code-analysis-tool",
    version="1.0.0",
    author="Security QA Engineer",
    description="Professional Code Auditor Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "codeauditor=professional_code_auditor_v2:main",
        ],
    },
)
