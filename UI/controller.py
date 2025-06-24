import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDDAeroportoP = None
        self._choiceDDAeroportoA = None

    def handleAnalizza(self, e):
        cMinTxt = self._view._txtInCMin.value

        if cMinTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico"))
            return

        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Il valore inserito non è un intero"))
            return

        if cMin <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un intero positivo"))
            return

        self._model.buildGraph(cMin)

        # dopo aver costruito il grafo, posso riempire i dropdown
        allNodes = self._model.getAllNodes()
        self.fillDD(allNodes)

        # chiedo le info del grafo ad un metodo del model
        nNodes, nEdges = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}, Numero di archi: {nEdges}"))

        self._view.update_page()

    def handleConnessi(self, e):

        if self._choiceDDAeroportoP == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un'opzione dal menù"))
            return

        viciniTuple = self._model.getSortedNeighbors(self._choiceDDAeroportoP)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Di seguito i vicini di {self._choiceDDAeroportoP}"))
        for v in viciniTuple:
            self._view.txt_result.controls.append(ft.Text(f"{v[0]} - peso: {v[1]}"))
        self._view.update_page()

    def handlePercorso(self, e):

        if self._choiceDDAeroportoP == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un aeroporto di partenza dal menù"))
            return
        if self._choiceDDAeroportoA == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un areoporto di arrivo dal menù"))
            return

        path = self._model.getPath(self._choiceDDAeroportoP, self._choiceDDAeroportoA)

        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Cammino tra {self._choiceDDAeroportoP} e {self._choiceDDAeroportoA} non trovato"))
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Cammino tra {self._choiceDDAeroportoP} e {self._choiceDDAeroportoA} trovato! Di seguito i nodi del cammino:"))

            for p in path:
                self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()

    def handleCerca(self, e):
        pass

    def fillDD(self, allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=n, key=n.IATA_CODE, on_click=self.pickDDPartenza))
            self._view._ddAeroportoD.options.append(ft.dropdown.Option(data=n, key=n.IATA_CODE, on_click=self.pickDDArrivo))

    # questo metodo legge dall'evento il nome che è stato scelto dal dd e lo memorizza in una variabile
    def pickDDPartenza(self, e):
        self._choiceDDAeroportoP = e.control.data
        print("Aeroporto di partenza selezionato: ", self._choiceDDAeroportoP)

    def pickDDArrivo(self, e):
        self._choiceDDAeroportoA = e.control.data
        print("Aeroporto di arrivo selezionato: ", self._choiceDDAeroportoA)