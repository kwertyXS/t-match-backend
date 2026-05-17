from pydantic import BaseModel


class ConnectSchema(BaseModel):
    meet_id: int
