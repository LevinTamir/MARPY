from setuptools import find_packages, setup

package_name = "marpy_cam_bridge"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Tamir Levin",
    maintainer_email="tamirlvn@gmail.com",
    description="Pulls the ESP32-CAM MJPEG stream and republishes it as sensor_msgs/Image",
    license="MIT",
    entry_points={
        "console_scripts": [
            "mjpeg_bridge = marpy_cam_bridge.mjpeg_bridge:main",
        ],
    },
)
