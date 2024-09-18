from setuptools import setup, find_packages

setup(
    name="youtube_downloader",
    version="1.0.0",
    author="IPG2004",
    author_email="osteriz167@gmail.com",
    description="A graphical interface for downloading YouTube videos and audios.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IPG2004/PDF-Merger",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "customtkinter",
        "pytubefix",
    ],
    entry_points={
        'console_scripts': [
            'youtube_downloader=app:main',
        ],
    },
    license='MIT',
    keywords='youtube downloader tkinter',
)