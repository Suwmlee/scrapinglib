from setuptools import setup, find_packages
from codecs import open

requires = [
    "lxml",
    "pysocks",
    "mechanicalsoup",
    "curl_cffi",
]

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

setup(
    name='scrapinglib',
    version='0.11.0',
    author="suwmlee",
    author_email='suwmlee@gmail.com',
    url='https://github.com/Suwmlee/scrapinglib',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_dir={'scrapinglib': 'scrapinglib'},   
    install_requires=requires,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/Suwmlee/scrapinglib/issues",
        "Source": "https://github.com/Suwmlee/scrapinglib",
    },
)
