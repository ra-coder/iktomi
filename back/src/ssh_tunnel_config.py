from pydantic_settings import BaseSettings, SettingsConfigDict


class SSHSettings(BaseSettings):
    ssh_username: str
    ssh_private_key_location: str
    ip: str
    port: int = 22
    remote_bind_address: tuple[str, int] = ('localhost', 5432)
    local_bind_address: tuple[str, int] = ('localhost', 5433)

    model_config = SettingsConfigDict(env_file="ssh_tunnel_config.env", env_file_encoding="utf-8")


ssh_settings = SSHSettings()
