from sqlmodel import SQLModel, Field

class Base(SQLModel):
    id: int = Field(
        default=None,
        primary_key=True, 
        index=True,
        nullable=False
        )
