import os
import cfg


class ImageFiles:
    def __init__(self):
        # conjunt amb les rutes (relatives a l'arrel) de tots els PNG trobats
        self.fitxers = set()
        self.afegits = []
        self.eliminats = []

    def reload_fs(self, path):
        # torna a recorrer les carpetes i mira què ha canviat respecte l'última vegada
        nous = set()
        for carpeta, subcarpetes, noms in os.walk(path):
            for nom in noms:
                if nom.lower().endswith('.png'):
                    ruta = os.path.join(carpeta, nom)
                    relativa = os.path.relpath(os.path.realpath(ruta), cfg.get_root()).replace(os.sep, '/')
                    nous.add(relativa)

        self.afegits = sorted(nous - self.fitxers)
        self.eliminats = sorted(self.fitxers - nous)
        self.fitxers = nous

    def files_added(self):
        return self.afegits.copy()

    def files_removed(self):
        return self.eliminats.copy()

    def __str__(self):
        return 'ImageFiles: ' + str(len(self.fitxers)) + ' fitxers PNG'
