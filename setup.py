#!/usr/bin/env python3
"""
Setup script for AGT Lab Server package
"""
from setuptools import setup, find_packages
setup(
    name="agt-lab-server",
    version="0.1.0",
    description="AGT Lab Server for Game Theory Competitions - A tournament server for game theory lab competitions",
    author="AGT Server Team",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0", "pandas>=1.3.0", "pytest-asyncio", "matplotlib", "Flask>=2.0.0",
        "requests>=2.25.0", "psutil>=5.8.0", "asyncio>=3.4.3", "aiohttp>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "agt-server=agt_server.cli:run_server",
            "agt-dashboard=agt_server.cli:run_dashboard",
        ],
        "gui_scripts": [
            "agt-dashboard-gui=agt_server.cli:run_dashboard",
        ],
    },
    include_package_data=True,
    package_data={
        "agt_server": [
            "dashboard/templates/*",
            "server/configs/*",
        ],
    },
    python_requires=">=3.8",
)
