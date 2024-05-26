from setuptools import setup, find_packages


setup(
    name="algogears",
    version="1.1.1",
    author="artandfi (Artem Fisunenko)",
    author_email="artem.fisunenko@hotmail.com",
    description="This library contains implementations of computational geometry algorithms in Python3 adapted for educational purposes.",
    long_description="AlgoGEARS (Algorithms of (Computational) Geometry with Entities Available for Reuse and Serialization) is a library that provides implementations of certain computational geometry algorithms adapted for educational purposes." 
                     "The basic entities it uses, such as geometric objects and binary trees, are constructed as Pydantic models that can be easily reused and serialized."
                     "This library is a continuation of PyCompGeomAlgorithms https://pypi.org/project/PyCompGeomAlgorithms/, a library by the same author as this one--artandfi (Artem Fisunenko).",
    packages=find_packages(),
    keywords=[
        "Python3",
        "computational geometry",
        "convex hull",
        "region search",
        "geometric search",
        "point location",
        "proximity",
        "closest pair",
        "closest points"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
