from setuptools import setup, find_packages # type: ignore

setup(
    name="paystubs",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)