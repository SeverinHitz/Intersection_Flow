from setuptools import setup, find_packages

setup(
    name="IntersectionTrafficFlow",
    version="0.1.0",
    description="Visualize traffic flow at intersections",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Severin Hizt",
    author_email="sevihitz@gmail.com",
    url="https://github.com/SeverinHitz/IntersectionTrafficFlow",
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
)