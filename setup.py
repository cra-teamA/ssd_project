from setuptools import setup

setup(
    name="ssd_project",
    version="0.1",
    py_modules=["ssd_controller"],  # 파일명만 확장자 없이
    entry_points={
        "console_scripts": [
            "ssd = ssd_controller:main"
        ]
    },
)