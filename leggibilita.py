#put this in $HOME/.local/share/gedit/plugins
from gi.repository import GObject, Gtk, Gedit, Gio

#UI_XML = """<ui> <menubar name="MenuBar">
#    <menu name="ToolsMenu" action="Tools">
#      <placeholder name="ToolsOps_3">
#        <menuitem name="Leggibilita" action="Leggibilita"/>
#      </placeholder>
#    </menu>
#</menubar> </ui>"""

try:
    gettext.bindtextdomain(GETTEXT_PACKAGE, GP_LOCALEDIR)
    _ = lambda s: gettext.dgettext(GETTEXT_PACKAGE, s);
except:
    _ = lambda s: s



class LeggibilitaWindow(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "Leggibilita"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
    
    def _add_ui(self):
        #manager = self.window.get_ui_manager()
        #self._actions = Gtk.ActionGroup(name="LeggibilitaActions")
        #self._actions.add_actions([
        #  ('Leggibilita', Gtk.STOCK_INFO, "Indice Leggibilita",None, "Calcola indice leggibilita",self.on_action_activate),
        #])
        #manager.insert_action_group(self._actions)
        #self._ui_merge_id = manager.add_ui_from_string(UI_XML)
        #manager.ensure_update()
        action = Gio.SimpleAction(name="leggibilita")
        action.connect('activate', self.on_action_activate)
        self.window.add_action(action)
        
    def do_activate(self):
        self._add_ui()

    def do_deactivate(self):
        #self._remove_ui()
        self.window.remove_action("leggibilita")

    def do_update_state(self):
        pass
    
    def leggibilita(self,testo):
        frasi = testo.count('.') + testo.count('?') + testo.count('!') + testo.count('.') + testo.count(':') + testo.count(';')
        parole = len(testo.split())
        if parole==0:
        	return "N/A"
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

class LeggibilitaApp(GObject.Object, Gedit.AppActivatable):
	app = GObject.Property(type=Gedit.App)
	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		self.app.add_accelerator("<Primary><Alt>L", "win.leggibilita", None)
		self.menu_ext = self.extend_menu("tools-section")
		item = Gio.MenuItem.new(_("Leggibilita"), "win.leggibilita")
		self.menu_ext.append_menu_item(item)

	def do_deactivate(self):
		self.app.remove_accelerator("win.leggibilita", None)
		self.menu_ext = None

# ex:ts=4:et:
