import os
import cfg
from PIL import Image


class ImageViewer:
    def __init__(self, image_data):
        self.image_data = image_data

    def print_image(self, uuid):
        # imprimeix les dades que ja tenim en memòria, sense tornar a llegir el disc
        fitxer = self.image_data.get_filename(uuid)
        if fitxer is None:
            return
        dimensions = self.image_data.get_dimensions(uuid)
        if dimensions is None:
            dimensions = (None, None)
        amplada, alcada = dimensions
        prompt = self.image_data.get_prompt(uuid)
        if prompt is None:
            prompt = 'None'
        if len(prompt) > 100:
            prompt = prompt[:100] + '...'
        print('Archivo:', fitxer)
        print('UUID:', uuid)
        print('Dimensions:', str(amplada) + 'x' + str(alcada))
        print('Prompt:', prompt)
        print('Model:', self.image_data.get_model(uuid))
        print('Seed:', self.image_data.get_seed(uuid))
        print('CFG Scale:', self.image_data.get_cfg_scale(uuid))
        print('Steps:', self.image_data.get_steps(uuid))
        print('Sampler:', self.image_data.get_sampler(uuid))
        print('Generated:', self.image_data.get_generated(uuid))
        print('Created Date:', self.image_data.get_created_date(uuid))

    def show_file(self, file):
        ruta = os.path.join(cfg.get_root(), file)
        if not os.path.isfile(ruta) and os.path.isfile(file):
            ruta = file
        try:
            with Image.open(ruta) as imatge:
                imatge.show()
        except (OSError, ValueError) as error:
            print('No es pot mostrar la imatge:', error)

    def show_image(self, uuid, mode=None):
        # mode 0: només text, mode 1: text i imatge, mode 2: només imatge
        if mode is None:
            mode = cfg.DISPLAY_MODE
        fitxer = self.image_data.get_filename(uuid)
        if fitxer is None:
            return
        if mode == 0 or mode == 1:
            self.print_image(uuid)
        if mode == 1 or mode == 2:
            self.show_file(fitxer)

    def __str__(self):
        return 'ImageViewer: ' + str(len(self.image_data)) + ' imatges disponibles'
