import cfg


class SearchMetadata:
    def __init__(self, image_data):
        self.image_data = image_data

    def _buscar(self, sub, camp):
        # no passem a minúscules: les cerques distingeixen majúscules
        resultats = []
        for identificador in self.image_data.get_uuids():
            valor = self.image_data._get_camp(identificador, camp)
            if valor is not None and valor != 'None' and str(sub) in valor:
                resultats.append(identificador)
        return resultats

    def dimensions(self, width, height):
        resultats = []
        for identificador in self.image_data.get_uuids():
            if self.image_data.get_dimensions(identificador) == (width, height):
                resultats.append(identificador)
        return resultats

    def and_operator(self, list1, list2):
        # ens quedem amb els que surten a les dues llistes, sense repetits
        resultats = []
        ids_segona = set(list2)
        vistos = set()
        for identificador in list1:
            if identificador in ids_segona and identificador not in vistos:
                resultats.append(identificador)
                vistos.add(identificador)
        return resultats

    def or_operator(self, list1, list2):
        # ajuntem les dues llistes sense repetits, mantenint l'ordre
        resultats = []
        vistos = set()
        for identificador in list1 + list2:
            if identificador not in vistos:
                resultats.append(identificador)
                vistos.add(identificador)
        return resultats

    def __str__(self):
        return 'SearchMetadata: ' + str(len(self.image_data)) + ' imatges disponibles'

    def prompt(self, sub):
        return self._buscar(sub, 'Prompt')

    def model(self, sub):
        return self._buscar(sub, 'Model')

    def seed(self, sub):
        return self._buscar(sub, 'Seed')

    def cfg_scale(self, sub):
        return self._buscar(sub, 'CFG_Scale')

    def steps(self, sub):
        return self._buscar(sub, 'Steps')

    def sampler(self, sub):
        return self._buscar(sub, 'Sampler')

    def generated(self, sub):
        return self._buscar(sub, 'Generated')

    def date(self, sub):
        return self._buscar(sub, 'Created_Date')
