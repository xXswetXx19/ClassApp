from Components.Autocomplete import AutocompleteCombobox
from datetime import datetime

class multi_search (AutocompleteCombobox):
    def __init__ (self, master=None, completevalues=None, Treeview=None, column=None, filters={},  **kwargs):
        super().__init__(master, completevalues, **kwargs)

        self.treeview = Treeview
        self.treeviewColumn = column
        self.allTreeItems = []
        self.treeview_values = []
        self.search_filters = filters
        
        self.bind("<<ComboboxSelected>>", self.handle_list_selection)
        self.bind("<Tab>", self.handle_keyrelease)
        self.bind("<Return>", self.handle_keyrelease)

    def setTreeview(self) -> None:
        self.clear_Treeview()
        self.treeview_values.sort(key=lambda x: (datetime.strptime(x[4], '%d/%m/%Y'), -x[3]))
        for value in self.treeview_values:
            self.treeview.insert("", 0, text=value[0], values=value[1:])

        self.allTreeItems = self.treeview.get_children()
 
    def clear_Treeview(self) -> None:
        for child in set(self.treeview.get_children()):
            self.treeview.detach(child)
    
    def fill_Treeview(self, list=None) -> None:
        self.clear_Treeview()
        if list:
            for child in self.order_lists(list):
                self.treeview.move(child, '', 0)
        else:   
            for child in self.order_lists(self.allTreeItems):
                self.treeview.move(child, '', 0)

    
    def handle_list_selection(self, event) -> None:
        value = self.get()
        if value:
            self.search_filters[str(self.treeviewColumn)] = value
            filtereds = self.filter_treeview()
            if filtereds:
                self.fill_Treeview(filtereds)
            else:
                self.clear_Treeview()
                      
    def order_lists(self, lista : list) -> set:
        # para ordenar tambien por hora dejo este codigo, pero aqui no es necesario por los numeros
        #lista.sort(key=lambda x: (datetime.strptime(self.treeview.item(x)["values"][3], '%d/%m/%Y'), -self.treeview.item(x)["values"][2], datetime.strptime(self.treeview.item(x)["values"][4], '%H:%M:%S')))
        lista = list(lista)
        lista.sort(key=lambda x: (datetime.strptime(self.treeview.item(x)["values"][3], '%d/%m/%Y'), -self.treeview.item(x)["values"][2]))
        return lista
                
    def filter_treeview(self):
        self.fill_Treeview()
        childs = set(self.treeview.get_children())
        
        if not any(self.search_filters.values()):
            return "No results found"

        for row in set(self.treeview.get_children()):
            for column_index in self.search_filters.keys():
                column_value = str(self.treeview.item(row)["values"][int(column_index)])
                if self.search_filters[column_index]:
                    if (column_value not in set(self.search_filters[column_index])) and (column_value != self.search_filters[column_index]):
                        childs.remove(row)
                        break
        return childs

    def handle_keyrelease(self, event):
        super().handle_keyrelease(event)
        hits = set(self._hits)

        if event.keysym == "Tab" or event.keysym == "Return":
            if event.send_event:
                hits = set([self.get()]) if self.get() else set()
            else:
                return
            
        if not hits and self.get():
            self.delete(0, "end")
            self.search_filters[str(self.treeviewColumn)] = set()
            
        self.search_filters[str(self.treeviewColumn)] = hits
        
        filtereds = self.filter_treeview()
        
        self.clear_Treeview()
        
        if event.keysym == "BackSpace" and self.get():
            self.search_filters[str(self.treeviewColumn)] = set()
            filtereds = self.filter_treeview()
                
        if filtereds != "No results found" and filtereds:
            self.fill_Treeview(filtereds)
            
        elif filtereds == "No results found" and not self.get():
            self.fill_Treeview()
            
        elif not filtereds:
            self.clear_Treeview()

    def set_tw_completion_list(self, new_completion_list):
        self.treeview_values = new_completion_list
        self.setTreeview()
        
    def set_column_completion_list(self, list):
        self.set_completion_list(list)
        
    
    def get_tree_selection(self):
        if not self.treeview.selection():
            return None
        
        tree_selection = {
            "text": self.treeview.item(self.treeview.selection())["text"],
            "values": self.treeview.item(self.treeview.selection())["values"]
        }
        
        return tree_selection
