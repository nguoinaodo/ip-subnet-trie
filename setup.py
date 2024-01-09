from setuptools import setup, find_packages

setup(
    name='IP-Subnet-Trie',
    version='0.2',
    packages=find_packages(),
    description='An efficient data structure for handling a large number of IP addresses/subnets in a hierarchy.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Bui Hoang Luu',
    author_email='luugu196@gmail.com',
    url='https://github.com/nguoinaodo/ip-subnet-trie',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)