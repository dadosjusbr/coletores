import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpba",
    version="0.0.1",
    author="DadosJusBR",
    description="Lista remuneração dos servidores do Ministério Público da Bahia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dadosjusbr/coletores",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={"console_scripts": ["mpba=mpba.cli:main"]},
)
