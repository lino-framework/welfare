from lino import ad
    
class App(ad.App):

    extends = 'lino.modlib.households'
    extends_models = ['households.Household']
