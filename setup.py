import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="tmx110",
    version="0.0.1",
    scripts=["bin/tmx110"],
    author="Tristan Lieberherr",
    author_email="tristan.lieberherr@heig-vd.ch",
    description="TMX110 programming interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TristanLieberherr/TMX110_package",
    packages=["tmx110"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pymodbus"],
)
