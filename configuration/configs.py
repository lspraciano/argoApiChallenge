from dynaconf import Dynaconf, Validator

settings: Dynaconf = Dynaconf(
    envvar_prefix="GLWAPI",
    settings_files=[
        './configuration/settings.toml',
        './configuration/.secrets.toml',
    ],
    environments=[
        "production",
        "development",
        "testing"
    ],
    env_switcher="GLWAPI_APP_RUNNING_MODE",
    validators=[
        Validator(
            "APP_RUNNING_MODE",
            must_exist=True,
        )
    ],
    load_dotenv=False
)
