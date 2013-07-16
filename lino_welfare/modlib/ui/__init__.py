from lino import ad
    
class App(ad.App):

    extends = 'lino.ui'
    extends_models = ['ui.SiteConfig']
