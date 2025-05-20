# Pyctf/setup.py
import subprocess
import os
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py

class CustomBuild(_build_py):
    def run(self):
        print("Running custom Makefile build for pyctf...")
        make_dir = os.path.join(os.path.dirname(__file__), "pyctf")
        subprocess.check_call(["make"], cwd=make_dir)
        super().run()

setup(
    name="pyctf",
    version="0.1.0",
    author="Jonas Koellner",
    author_email="jonas.koellner@iss.uni-stuttgart.com",
    description="Modified NIH pyctf package with native code support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="pyctf"),
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