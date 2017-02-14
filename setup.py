from setuptools import setup


setup(
    name="puff",
    version="0.3",
    description="API Validation for SQLAlchemy-jsonapi",
    maintainer="Paul Hummer",
    maintainer_email="paul@eventuallyanyway.com",
    url="https://github.com/rockstar/puff",
    license="MIT",
    install_requires=['sqlalchemy'],
    py_modules=('puff',),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
    ],
)
