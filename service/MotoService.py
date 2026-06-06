from typing import List, Optional
from mongo.model.DAO.MotoDAO import MotoDAO
from mongo.model.DAO.CategoriaDAO import CategoriaDAO
from mongo.model.VO.MotoVO import MotoVO

_ESTADOS_VALIDOS = {"disponible", "vendida", "reservada"}


class MotoService:

    def listar_disponibles(self) -> List[MotoVO]:
        return MotoDAO.listar_disponibles()

    def obtener_detalle(self, id_moto: int) -> Optional[MotoVO]:
        return MotoDAO.obtener_por_id(id_moto)

    def registrar(self, moto: MotoVO, ids_categorias: Optional[List[int]] = None) -> int:
        if MotoDAO.buscar_por_vin(moto.vin) is not None:
            raise ValueError(f"Ya existe una moto con VIN '{moto.vin}'.")

        from mongo.model.VO.CategoriaVO import CategoriaVO
        categorias_emb = []
        if ids_categorias:
            for id_cat in ids_categorias:
                cat_doc = CategoriaDAO.obtener_por_id(id_cat)
                if cat_doc:
                    categorias_emb.append(cat_doc.to_embedded())
        moto.categorias = categorias_emb
        return MotoDAO.insertar(moto)

    def cambiar_estado(self, id_moto: int, nuevo_estado: str) -> None:
        if nuevo_estado not in _ESTADOS_VALIDOS:
            raise ValueError(f"Estado '{nuevo_estado}' no válido.")
        moto = MotoDAO.obtener_por_id(id_moto)
        if moto is None:
            raise ValueError(f"No existe ninguna moto con id {id_moto}.")
        MotoDAO.actualizar_estado(id_moto, nuevo_estado)
