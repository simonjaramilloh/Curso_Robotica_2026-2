from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'autel_stn_inspector'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Simón Jaramillo & Rafael Montoya',
    maintainer_email='simonjaramilloh@unal.edu.co',
    description='Simulación UAV Autel EVO Max 4T para inspección STN 500 kV',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'drone_stn_simulator = autel_stn_inspector.drone_stn_simulator:main',
            'autonomous_line_inspector = autel_stn_inspector.autonomous_line_inspector:main',
        ],
    },
)
