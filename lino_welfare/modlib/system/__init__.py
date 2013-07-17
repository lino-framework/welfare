from lino import ad
    
class App(ad.App):

    extends = 'lino.modlib.system'
    extends_models = ['system.SiteConfig']
