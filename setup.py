from setuptools import setup, find_packages

setup(
    name="photo-tools",
    version="0.0.1",
    packages=find_packages(),
    # scripts=["say_hello.py"],
    install_requires=["click==7.0", "tqdm", "ffmpeg-python==0.2.0"],
    entry_points="""
        [console_scripts]
        photo-tools=photo_tools:cli.main_cli
    """,
    # metadata to display on PyPI
    author="Mohan Muppidi",
    author_email="mkumar2301@gmail.com",
    description="Photography tools build on python",
    keywords="photography, organizer",
    url="http://example.com/HelloWorld/",  # project home page, if any
    project_urls={
        "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://code.example.com/HelloWorld/",
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ],
)
