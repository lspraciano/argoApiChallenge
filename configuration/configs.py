from dynaconf import Dynaconf, Validator

settings: Dynaconf = Dynaconf(
    envvar_prefix="ARGOAPI",
    settings_files=[
        './configuration/settings.toml',
        './configuration/.secrets.toml',
    ],
    environments=[
        "production",
        "development",
        "testing"
    ],
    env_switcher="ARGOAPI_APP_RUNNING_MODE",
    validators=[
        Validator(
            "APP_RUNNING_MODE",
            must_exist=True,
        )
    ],
    load_dotenv=False
)
