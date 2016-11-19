from setuptools import setup, find_packages

setup(
    name='VKApp',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'vk==2.0.2',
        'SQLAlchemy==1.1.0',
        'click==6.6',
        'Pillow==3.4.2'
    ],
    url='https://github.com/lycantropos/VKApp',
    license='GNU GPL',
    author='lycantropos',
    author_email='azatibrakov@gmail.com',
    description='Simple class for working with VK API'
)
