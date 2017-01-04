#put this in $HOME/.local/share/gedit/plugins
from gi.repository import GObject, Gtk, Gedit

UI_XML = """<ui> <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_3">
        <menuitem name="Leggibilita" action="Leggibilita"/>
      </placeholder>
    </menu>
</menubar> </ui>"""

class Leggibilita(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "Leggibilita"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
    
    def _add_ui(self):
        manager = self.window.get_ui_manager()
        self._actions = Gtk.ActionGroup(name="LeggibilitaActions")
        self._actions.add_actions([
          ('Leggibilita', Gtk.STOCK_INFO, "Indice Leggibilita",None, "Calcola indice leggibilita",self.on_action_activate),
        ])
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(UI_XML)
        manager.ensure_update()
        
    def do_activate(self):
        self._add_ui()

    def do_deactivate(self):
        self._remove_ui()

    def do_update_state(self):
        pass
    
    def leggibilita(self,testo):
        frasi = testo.count('.') + testo.count('?') + testo.count('!') + testo.count('.') + testo.count(':') + testo.count(';')
        parole = len(testo.split())
        lettere=len(testo)-parole
        lp=(100.0*lettere)/parole
        fr=(100.0*frasi)/parole
        gulpease=89.0-(lp/10.0)+(3.0*fr)
        return int(gulpease)
    
    def on_action_activate(self, action, data=None):
        view = self.window.get_active_view()
        if view:
            vbuffer=view.get_buffer()
            start=vbuffer.get_start_iter()
            end=vbuffer.get_end_iter()
            text=vbuffer.get_text(start,end,False)
            message=Gtk.MessageDialog(buttons=Gtk.ButtonsType.OK)
            message.set_markup("leggibilita' da 0 a 100: %s" % self.leggibilita(text))
            message.run()
            message.destroy()
        
    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()
