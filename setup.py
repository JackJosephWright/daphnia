from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="TRexDataManipulator",  # Required

    version="1.0.0",  # Required

    description="This program allows the manipulation of TRex Data in order to resolve disjoint and faulty data",  # Optional

    long_description=long_description,  # Optional
    
    long_description_content_type="text/markdown",  # Required if .md

    url="https://github.com/JackJosephWright/daphnia.git",  # Optional
    # This should be your name or the name of the organization which owns the
    # project.
    author="Jack Wright",  # Optional

    author_email="jwright@qc.cuny.edu",  # Optional
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Image Recognition"
    ],

    keywords="TRex, TGrabs, AnimalTracking",  # Optional

    package_dir={"": "src"},  # Optional
    
    packages=find_packages(where="src"),  # Required

    python_requires=">=3.0, <4",

    extras_require={  # Optional
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={  # Optional
        "sample": ["package_data.dat"],
    },
    # Entry points. The following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        "console_scripts": [
            "sample=sample:main",
        ],
    },
    # List additional URLs that are relevant to your project as a dict.

    project_urls={  # Optional
        "Source": "https://github.com/JackJosephWright/daphnia.git",
    },
)