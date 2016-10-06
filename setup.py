from setuptools import setup, find_packages

setup(
    name='VKApp',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'vk==2.0.2', 'sqlalchemy>=1.0', 'click==6.6'
    ],
    url='https://github.com/lycantropos/VKApp',
    license='GNU GPL',
    author='lycantropos',
    author_email='azatibrakov@gmail.com',
    description='Simple class for working with VK API'
)
