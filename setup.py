import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pye2e",
    version="0.0.2",
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
)
