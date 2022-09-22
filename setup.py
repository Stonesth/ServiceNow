from cx_Freeze import setup, Executable


setup(
    name = "servicenow",
    version = "0.1",
    description = "",
    executables = [Executable("servicenow.py")]
)
