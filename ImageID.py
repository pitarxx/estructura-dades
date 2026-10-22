import os
import cfg


class ImageID:
    def __init__(self):
        # dos diccionaris per poder buscar en les dues direccions
        self.ids_per_fitxer = {}
        self.fitxers_per_id = {}

    def _ruta_relativa(self, fitxer):
        # sempre treballem amb rutes relatives a l'arrel de la col·lecció
        if os.path.isabs(fitxer):
            return cfg.get_canonical_pathfile(fitxer)
        return os.path.normpath(fitxer).replace(os.sep, '/')

    def generate_uuid(self, file):
        fitxer = self._ruta_relativa(file)
        identificador = str(cfg.get_uuid(fitxer))
        if identificador in self.fitxers_per_id:
            print('UUID ja utilitzat. S\'ignora el fitxer:', fitxer)
            return None
        self.ids_per_fitxer[fitxer] = identificador
        self.fitxers_per_id[identificador] = fitxer
        return identificador

    def get_uuid(self, file):
        fitxer = self._ruta_relativa(file)
        return self.ids_per_fitxer.get(fitxer)

    def remove_uuid(self, uuid):
        identificador = str(uuid)
        if identificador in self.fitxers_per_id:
            fitxer = self.fitxers_per_id.pop(identificador)
            del self.ids_per_fitxer[fitxer]

    def __len__(self):
        return len(self.fitxers_per_id)

    def __str__(self):
        return 'ImageID: ' + str(len(self)) + ' identificadors actius'
