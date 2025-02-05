from setuptools import setup, find_namespace_packages

setup(
    name="atomic", 
    version="1.0.0", 
    packages=find_namespace_packages(),
    include_package_data=True, 
    py_modules=["atomic"], 
    install_requires=[
        "rich",
        "openai",
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'atomic=atomic:main_entry', 
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12', 
    author="sh4dowByte", 
    author_email="Ahmad Juhdi <ahmadjuhdi007@gmail.com>",
)