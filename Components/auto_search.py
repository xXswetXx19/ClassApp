from Components.Autocomplete import AutocompleteCombobox

class auto_searchTw(AutocompleteCombobox):
    def __init__ (self, master=None, completevalues=None, Treeview=None,  **kwargs):
        super().__init__(master, completevalues, **kwargs)

        self.treeview = Treeview
        self.treeItems = self.treeview.get_children()
        self.setTreeview()
        self.bind("<<ComboboxSelected>>", self.handle_list_selection)

    def setTreeview(self):
        self.clear_Treeview()
        for i in self._completion_list:
            self.treeview.insert("", "end", values=i)
        self.treeItems = self.treeview.get_children()
        
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
                if self.treeview.item(child)["values"]:
                    itemValue = " ".join(self.treeview.item(child)["values"])
                    if itemValue not in value:
                        self.treeview.detach(child)     
    
    def handle_keyrelease(self, event):
        super().handle_keyrelease(event)
        if self._hits:
            for child in self.treeview.get_children():
                if self.treeview.item(child)["values"]:
                    itemValue = " ".join(self.treeview.item(child)["values"])
                    if itemValue not in self._hits:
                        self.treeview.detach(child)
        else:
            self.fill_Treeview()
    
    def update_completion_list(self, new_completion_list):
        self.set_completion_list(new_completion_list)
        self.setTreeview()