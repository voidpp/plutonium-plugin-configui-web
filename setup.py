from setuptools import setup, find_packages

setup(
    name = "plutonium-plugin-configui-web",
    description = "Web based config user interface plugin for Plutonium",
    version = '1.0',
    install_requires = [
        'plutonium == 1.0',
        'sqlchemyforms == 1.0',
    ],
    include_package_data = True,
    packages = find_packages(),
)

