from setuptools import setup, find_packages

setup(
    name="recovery-debt",
    version="1.0.0",
    description="Recovery Debt Detector — tamper-evident resilience failure early warning",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "cryptography>=41.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
    ],
)
