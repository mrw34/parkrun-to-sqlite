import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parkrun-to-sqlite",
    version="0.5",
    author="Mark Woodbridge",
    author_email="mark.woodbridge@cantab.net",
    description="Create a SQLite database containing your parkruns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mwoodbri/parkrun-to-sqlite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["parkrun-to-sqlite=parkrun_to_sqlite.__main__:main"]
    },
    package_data={"parkrun_to_sqlite": ["events.json"]},
)
