import json
import os
from collections import deque
import cfg


class Gallery:
    def __init__(self, image_id, image_viewer):
        self.image_id = image_id
        self.image_viewer = image_viewer
        # deque: permet treure pels dos extrems sense desplaçar elements
        self.imatges = deque()
        self.nom = ''
        self.descripcio = ''
        self.data = ''

    def load_file(self, file):
        # cada càrrega substitueix la galeria anterior, encara que el fitxer no existeixi
        self.imatges.clear()
        self.nom = ''
        self.descripcio = ''
        self.data = ''
        try:
            with open(file, 'r', encoding='utf-8') as fitxer:
                dades = json.load(fitxer)
        except (OSError, ValueError) as error:
            print('No es pot carregar la galeria:', error)
            return
        if not isinstance(dades, dict) or not isinstance(dades.get('images'), list):
            print('Format de galeria incorrecte')
            return
        self.nom = dades.get('gallery_name', '')
        self.descripcio = dades.get('description', '')
        self.data = dades.get('created_date', '')
        for ruta in dades['images']:
            if not isinstance(ruta, str):
                continue
            identificador = self.image_id.get_uuid(ruta)
            # alguns JSON porten el nom de la carpeta d'imatges davant
            if identificador is None:
                relativa = cfg.get_canonical_pathfile(ruta)
                identificador = self.image_id.get_uuid(relativa)
            if identificador is None:
                prefix = os.path.basename(cfg.get_root()) + '/'
                if ruta.startswith(prefix):
                    identificador = self.image_id.get_uuid(ruta[len(prefix):])
            if identificador is not None:
                self.imatges.append(identificador)

    def show(self):
        for identificador in self.imatges:
            self.image_viewer.show_image(identificador, cfg.DISPLAY_MODE)

    def add_image_at_end(self, uuid):
        self.imatges.append(str(uuid))

    def remove_first_image(self):
        if self.imatges:
            self.imatges.popleft()

    def remove_last_image(self):
        if self.imatges:
            self.imatges.pop()

    def __len__(self):
        return len(self.imatges)

    def __str__(self):
        return 'Gallery: ' + self.nom + ' (' + str(len(self)) + ' imatges)'
