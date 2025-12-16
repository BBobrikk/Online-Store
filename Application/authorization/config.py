from authx import AuthX, AuthXConfig

config = AuthXConfig(JWT_SECRET_KEY="AUTH_KEY", JWT_TOKEN_LOCATION=["headers"])

security = AuthX(config)
