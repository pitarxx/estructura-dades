import os
import cfg
from PIL import Image


class ImageData:
    def __init__(self):
        # per cada UUID guardem el fitxer, les dimensions i els metadades
        self.imatges = {}
        self.camps = ['Prompt', 'Model', 'Seed', 'CFG_Scale', 'Steps',
                      'Sampler', 'Generated', 'Created_Date']

    def add_image(self, uuid, file):
        if not uuid or not file:
            return
        # només creem l'entrada: els metadades es llegeixen després amb load_metadata
        identificador = str(uuid)
        if identificador in self.imatges:
            return
        dades = {'filename': file, 'dimensions': None}
        for camp in self.camps:
            dades[camp] = None
        self.imatges[identificador] = dades

    def _ruta_completa(self, fitxer):
        # busca el fitxer a l'arrel, tal com ens l'han donat, o sense els '../' del davant
        arrel = cfg.get_root()
        curta = os.path.normpath(fitxer).replace(os.sep, '/')
        while curta.startswith('../'):
            curta = curta[3:]
        candidats = [os.path.join(arrel, fitxer), fitxer, os.path.join(arrel, curta)]
        for candidat in candidats:
            if os.path.isfile(candidat):
                return candidat
        return candidats[0]

    def remove_image(self, uuid):
        self.imatges.pop(str(uuid), None)

    def load_metadata(self, uuid):
        identificador = str(uuid)
        if identificador not in self.imatges:
            return
        dades = self.imatges[identificador]
        ruta = self._ruta_completa(dades['filename'])
        metadades = cfg.read_png_metadata(ruta)
        if metadades is None:
            metadades = {}
        # s'actualitzen tots els camps, encara que algun hagi desaparegut
        for camp in self.camps:
            valor = metadades.get(camp)
            if valor is None:
                dades[camp] = 'None'
            else:
                dades[camp] = str(valor)
        try:
            with Image.open(ruta) as imatge:
                dades['dimensions'] = imatge.size
        except (OSError, ValueError):
            dades['dimensions'] = (None, None)

    def _get_camp(self, uuid, camp):
        dades = self.imatges.get(str(uuid))
        if dades is None:
            return None
        return dades[camp]

    def get_filename(self, uuid):
        return self._get_camp(uuid, 'filename')

    def get_dimensions(self, uuid):
        return self._get_camp(uuid, 'dimensions')

    def get_uuids(self):
        return list(self.imatges)

    def __len__(self):
        return len(self.imatges)

    def __str__(self):
        return 'ImageData: ' + str(len(self)) + ' imatges'

    def get_prompt(self, uuid):
        return self._get_camp(uuid, 'Prompt')

    def get_model(self, uuid):
        return self._get_camp(uuid, 'Model')

    def get_seed(self, uuid):
        return self._get_camp(uuid, 'Seed')

    def get_cfg_scale(self, uuid):
        return self._get_camp(uuid, 'CFG_Scale')

    def get_steps(self, uuid):
        return self._get_camp(uuid, 'Steps')

    def get_sampler(self, uuid):
        return self._get_camp(uuid, 'Sampler')

    def get_generated(self, uuid):
        return self._get_camp(uuid, 'Generated')

    def get_created_date(self, uuid):
        return self._get_camp(uuid, 'Created_Date')
