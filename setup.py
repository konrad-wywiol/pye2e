import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pye2e",
    version="0.0.17",
    author="Konrad",
    description="End-to-end testing wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/konrad-wywiol/pye2e",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'selenium>=3.14.0',
        'gherkin-official>=4.1.3'
    ]
)
