import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[bytes] = mapped_column(unique=False)
    last_login: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    disabled: Mapped[bool] = mapped_column(default=False)

class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(unique=True)
    product_price: Mapped[float] = mapped_column(default=0)
    product_quantity: Mapped[int] = mapped_column(default=0)
