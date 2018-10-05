# -*- coding: UTF-8 -*-
logger.info("Loading 14 objects to table cv_sector...")
# fields: id, name, remark
loader.save(create_cv_sector(1,[' Landwirtschaft & Garten', ' Agriculture & horticulture ', 'Agriculture & horticulture '],u''))
loader.save(create_cv_sector(2,[' Seefahrt', ' Maritime ', 'Maritime '],u''))
loader.save(create_cv_sector(3,[' Medizin & Paramedizin', ' M\xe9dical & param\xe9dical ', 'Medical & paramedical '],u''))
loader.save(create_cv_sector(4,[' Bauwesen & Geb\xe4udepflege', ' Construction & b\xe2timent ', 'Construction & buildings'],u''))
loader.save(create_cv_sector(5,[' Horeca', ' Horeca ', 'Tourism '],u''))
loader.save(create_cv_sector(6,[' Unterricht', ' Enseignement ', 'Education '],u''))
loader.save(create_cv_sector(7,[' Reinigung', ' Nettoyage ', 'Cleaning '],u''))
loader.save(create_cv_sector(8,[' Transport', ' Transport ', 'Transport '],u''))
loader.save(create_cv_sector(9,[' Textil', ' Textile ', 'Textile '],u''))
loader.save(create_cv_sector(10,[' Kultur', ' Culture ', 'Cultural '],u''))
loader.save(create_cv_sector(11,[' Informatik', ' Informatique ', 'Information Technology '],u''))
loader.save(create_cv_sector(12,[' Kosmetik', ' Cosm\xe9tique ', 'Esthetical '],u''))
loader.save(create_cv_sector(13,[' Verkauf ', ' Vente ', 'Sales '],u''))
loader.save(create_cv_sector(14,[' Verwaltung & Finanzwesen', ' Administration & Finance ', 'Administration & Finance '],u''))

loader.flush_deferred_objects()
