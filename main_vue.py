from vue.cadre import *
from controller.controller import *
from controller.ThreadedClient import *

client = ThreadedClient()
client.getGUI().mainloop()
# app = Cadre()
# controller = Controller(app)
# app.mainloop()
