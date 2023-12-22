from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Smartphone(Base):
    __tablename__ = "smartphone"
    nama : Mapped[str] = mapped_column(primary_key=True)
    ukuran_layar : Mapped[str]
    memori_internal : Mapped[str]
    kamera_belakang : Mapped[str]
    kapasitas_baterai : Mapped[str]
    harga : Mapped[int]

    def __repr__(self) -> str :
        return f"nama={self.nama}, ukuran_layar={self.ukuran_layar}, memori_internal={self.memori_internal}, kamera_belakang={self.kamera_belakang}, kapasitas_baterai={self.kapasitas_baterai}, harga={self.harga}"
