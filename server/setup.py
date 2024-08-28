from setuptools import setup, find_packages

setup(
    name="server",  # Name of your package
    version="0.1.0",
    author="narfasec",
    author_email="narfasec@gmail.com",
    description="Iscte Spot server package",
    packages=find_packages(exclude=["venv", "tests", "__pycache__"]),
    install_requires=[
        # List your package dependencies here, or load them from requirements.txt
        "Flask==2.3.1",
        "Flask-Cors==3.0.9",
        "mariadb==1.1.5",
        "requests==2.19.1"
    ],
    entry_points={
        "console_scripts": [
            "start-server=appserver:main",  # Adjust if needed, points to the entry function
        ]
    },
    python_requires=">=3.7",
)
