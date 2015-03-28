from setuptools import setup, find_packages

setup(
    name = "plutonium-plugin-configui-web",
    description = "Web based config user interface plugin for Plutonium",
    version = '0.2',
    install_requires = [
        'plutonium',
        'sqlchemyforms'
    ],
    packages = find_packages()
)

