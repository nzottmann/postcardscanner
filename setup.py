import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="postcardscanner-nzottmann",
    version="0.0.1",
    author="Nils Zottmann",
    author_email="mail@nils-zottmann.de",
    description="Library for postcard scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nzottmann/postcardscanner",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)
