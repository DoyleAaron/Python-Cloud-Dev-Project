from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Select
import os
import webbrowser
from swim_utils import * #Imported from Paul Barry, also edited by me
listOfNames = get_first_name(Folder)
listToUse = sorted(listOfNames)

class SelectSwimmers(App):
    CSS_PATH = "swimmers.tcss"
    def compose(self) -> ComposeResult:
        header = Header("Swimmers Assignment")
        selectName = Select(((Swimmers, Swimmers) for Swimmers in listToUse), id = "nameDropdown")
        yield selectName
        self.selectData = Select(([(None, None)]), id = "dataDropdown")
        yield self.selectData
        
        
        
    @on(Select.Changed, "#nameDropdown")
    def select_changed(self, event: Select.Changed) -> None:
        self.selectedName = str(event.value)
        self.dataList = second_list_data(Folder, self.selectedName)
        self.selectData.set_options((swimmerData, swimmerData) for swimmerData in self.dataList)

    @on(Select.Changed, "#dataDropdown")
    def select_2_changed(self, event:Select.Changed) -> None:
        self.selectedData = str(event.value)
        filetoGraph = str(self.selectedName + "-" + self.selectedData + ".txt")
        html_charts(filetoGraph)
        
if __name__ == "__main__":
    app = SelectSwimmers()
    app.run()
