from fastapi_users import schemas


class SchemasUserRead(schemas.BaseUser[int]):
    ...


class SchemasUserCreate(schemas.BaseUserCreate):
    ...


class SchemasUserUpdate(schemas.BaseUserUpdate):
    ...
