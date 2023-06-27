from Components.Autocomplete import AutocompleteCombobox

class multi_search (AutocompleteCombobox):
    def __init__ (self, master=None, completevalues=None, Treeview=None, column=None,  **kwargs):
        super().__init__(master, completevalues, **kwargs)

        self.treeview = Treeview
        self.treeviewColumn = column
        self.treeItems = self.treeview.get_children()
        self.treeview_values = completevalues
        self.column_values = []
        self.setTreeview()
        self.bind("<<ComboboxSelected>>", self.handle_list_selection)
        

    def setTreeview(self):
        self.clear_Treeview()
        for value in self.treeview_values:
            self.treeview.insert("", 0, text=value[0], values=value[1:])
        self.treeItems = self.treeview.get_children()
        
        for child in self.treeview.get_children():
            values = self.treeview.item(child)["values"]
            value = values[self.treeviewColumn]
            self.column_values.append(value)
            
 
    def clear_Treeview(self):
        for child in self.treeview.get_children():
            self.treeview.detach(child)
    
    def fill_Treeview(self):
        for child in self.treeItems:
            self.treeview.move(child, '', 0)

    
    def handle_list_selection(self, event):
        value = self.get()
        self.fill_Treeview()
        if value:
            for child in self.treeview.get_children():
                if self.treeview.item(child)["values"][self.treeviewColumn]:                 
                    itemValue = self.treeview.item(child)["values"][self.treeviewColumn]
                    if itemValue != value:
                        self.treeview.detach(child)
    
    def handle_keyrelease(self, event):
        super().handle_keyrelease(event)
        if self._hits:
            for child in self.treeview.get_children():
                if self.treeview.item(child)["values"][self.treeviewColumn]:                 
                    itemValue = self.treeview.item(child)["values"][self.treeviewColumn]
                    print(itemValue)
                    print(self._hits)
                    if itemValue not in self._hits:
                        self.treeview.detach(child)
        else:
            self.fill_Treeview()

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
