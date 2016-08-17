from distutils.core import setup

setup(
    name='VKApp',
    version='0.0.1',
    packages=['vk_app'],
    install_requires=[
        'vk==2.0.2',
    ],
    url='https://github.com/lycantropos/VKApp',
    license='GNU GPL',
    author='lycantropos',
    author_email='azatibrakov@gmail.com',
    description='Simple class for working with VK API'
)
