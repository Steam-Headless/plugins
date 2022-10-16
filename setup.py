import os
import setuptools

launcher_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'steam_headless_plugins')
with open(os.path.join(launcher_directory, 'version.txt')) as version_file:
    version = version_file.read().strip()

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()


def requirements():
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'requirements.txt'))) as f:
        return f.read().splitlines()


setuptools.setup(
    name="steam_headless_plugins",
    version=version,
    description="Steam Headless Plugins Launcher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Steam-Headless/plugins/",
    project_urls={
        "Documentation": "https://github.com/Steam-Headless/",
        "Code":          "https://github.com/Steam-Headless/plugins/",
        "Issue tracker": "https://github.com/Steam-Headless/plugins/issues",
    },
    python_requires='>=3.8',
    install_requires=requirements(),
    platforms='Unix-like',
    package_data={'steam_headless_plugins': ['*.py', 'version.txt']},
    packages=['steam_headless_plugins'],
    entry_points={
        'console_scripts': [
            'steam-headless-plugins=steam_headless_plugins:run',
            'shp=steam_headless_plugins:run',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Unix Shell",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Topic :: Terminals",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: BSD License"
    ],
    license="GPLv3",
    author="Josh.5",
    author_email="jsunnex@gmail.com"
)
