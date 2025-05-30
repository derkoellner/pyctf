# Pyctf/setup.py
import os
from setuptools import setup, Extension, find_packages
from setuptools.command.build_py import build_py as _build_py
import numpy
import glob

include_dir_for_geoms = os.path.join("pyctf", "pyctf", "samlib", "samlib")

# sources = [
#     "pyctf/pyctf/samlib/_samlib.c",
#     "pyctf/pyctf/samlib/samlib/GetCoeffs.c",
#     "pyctf/pyctf/samlib/samlib/rnynm.c",
#     "pyctf/pyctf/samlib/samlib/GetBasis.c",
#     "pyctf/pyctf/samlib/samlib/GetHull.c",
# ]

sources = ["pyctf/pyctf/samlib/_samlib.c"] + \
          glob.glob("pyctf/pyctf/samlib/samlib/*.c")

class CustomBuild(_build_py):
    def run(self):
        print("Running custom Makefile build for pyctf...")
        # make_dir = os.path.join(os.path.dirname(__file__), "pyctf")
        # subprocess.check_call(["make"], cwd=make_dir)
        super().run()

ext_modules = [
    Extension(
        "pyctf._samlib",
        sources=sources,
        include_dirs=[numpy.get_include(), include_dir_for_geoms],
        # libraries=["fftw3", "m"],
        libraries=["fftw3", "m", "gsl", "gslcblas"],
        extra_compile_args=["-O2", "-fPIC"],
    ),
]

setup(
    name="pyctf",
    version="0.1.0",
    author="Jonas Koellner",
    author_email="jonas.koellner@iss.uni-stuttgart.com",
    description="Modified NIH pyctf package with native code support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="pyctf"),
    ext_modules=ext_modules,
    package_dir={"": "pyctf"},
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        "build_py": CustomBuild,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)