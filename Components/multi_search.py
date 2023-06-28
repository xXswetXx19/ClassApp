from Components.Autocomplete import AutocompleteCombobox

class multi_search (AutocompleteCombobox):
    def __init__ (self, master=None, completevalues=None, Treeview=None, column=None, filters={},  **kwargs):
        super().__init__(master, completevalues, **kwargs)

        self.treeview = Treeview
        self.treeviewColumn = column
        self.treeItems = self.treeview.get_children()
        self.treeview_values = completevalues
        self.column_values = []
        self.search_filters = filters
        
        self.setTreeview()
        self.bind("<<ComboboxSelected>>", self.handle_list_selection)
        self.bind("<Tab>", self.handle_keyrelease)


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
        for child in set(self.treeview.get_children()):
            self.treeview.detach(child)
    
    def fill_Treeview(self):
        self.clear_Treeview()        
        for child in set(self.treeItems):
            self.treeview.move(child, '', 0)

    
    def handle_list_selection(self, event):
        value = self.get()
        self.fill_Treeview()
        if value:
            self.search_filters[str(self.treeviewColumn)] = value
            filtereds = self.filter_treeview(event)
            
            self.clear_Treeview()
            for child in filtereds:
                self.treeview.move(child, '', 0)    
                
    def filter_treeview(self, event):
        self.fill_Treeview()
        childs = set(self.treeview.get_children())
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
    
        if event.send_event and event.keysym == "Tab":
            if self.get():    
                hits = set([self.get()])
            else:
                hits = set()
        elif event.keysym == "Tab" and not event.send_event:
            return 
       
        self.search_filters[str(self.treeviewColumn)] = hits
        filtereds = self.filter_treeview(event)
        
        if event.keysym == "BackSpace" and not self.get():
            self.search_filters[str(self.treeviewColumn)] = set()
    
        self.clear_Treeview()
        for child in filtereds:
            self.treeview.move(child, '', 0)           



            
            
        
        
        
        
        
        
        


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
