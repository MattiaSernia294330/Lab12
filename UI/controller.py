import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []
        self._anno=None
        self._country=None
        self._N=None

    def fillDD(self):
        for i in range(2015,2019):
            self._view.ddyear.options.append(ft.dropdown.Option(text=f"{i}", on_click=self.read_anno))
        lista_nazioni=self._model.getAllCountry()
        for element in lista_nazioni:
            self._view.ddcountry.options.append(ft.dropdown.Option(text=f"{element}", on_click=self.read_country))

        pass
    def read_anno(self,e):
        self._anno=int(e.control.text)
    def read_country(self,e):
        self._country=e.control.text

    def handle_graph(self, e):
        if self._anno==None:
            self._view.create_alert("non hai inserito l'anno")
            return
        if self._country==None:
            self._view.create_alert("non hai inserito la nazione")
            return
        self._model.creaGrafo(self._anno,self._country)
        self._view.btn_volume.disabled=False
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.numNodi()} Numero di archi: {self._model.numArchi()}"))
        self._view.update_page()
        pass



    def handle_volume(self, e):
        dizionario=self._model.calcolaVolume()
        self._view.txtOut2.clean()
        for key in dizionario:
            self._view.txtOut2.controls.append(ft.Text(f"{key} --> {dizionario[key]}"))
        self._view.update_page()
        pass


    def handle_path(self, e):
        if self._N==None:
            self._view.create_alert("non hai inserito il numero di archi o ne hai insertito uno minore di due")
        self._model.handleRicorsione(self._N)
        self._view.txtOut3.clean()
        lista=self._model.getPercorso()
        self._view.txtOut3.controls.append(ft.Text(f"il pseo del percorso è: {self._model.getPeso()}"))
        for element in lista:
            self._view.txtOut3.controls.append(ft.Text(element))
        self._view.update_page()


    def read_N(self,e):
        value = e.control.value
        if value.strip().isdigit():
            N = int(value)
            if N>=2:
                self._N = N
            else:
                self._N = None
        else:
            self._N = None
