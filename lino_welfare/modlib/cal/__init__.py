from lino import ad
    
class App(ad.App):

    extends = 'lino.modlib.cal'
    extends_models = ['cal.Event','cal.Calendar']
    
