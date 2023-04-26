from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="yaasp",
    version="0.1.0",
    description="Your Awesome CLI tool description",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/yaasp",  # Replace with your project's URL
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "yaasp=yaasp.main:app",  # Replace with the correct path to your Typer app
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
