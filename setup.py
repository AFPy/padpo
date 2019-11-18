import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

    name='padpo',

    version='0.1',

    author="Vincent Poulailleau",

    author_email="vpoulailleau@gmail.com",

    description="Linter for gettext files",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/vpoulailleau/padpo",

    packages=["padpo"],
    package_dir={"padpo": "padpo"},
    entry_points={"console_scripts": ["padpo=padpo.padpo:main"]},

    install_requires=[
        'simplelogging', 'wheel', 'requests'
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        # TODO: Add more
    ],

)