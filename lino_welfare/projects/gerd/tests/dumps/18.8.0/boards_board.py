# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table boards_board...")
# fields: id, start_date, end_date, name
loader.save(create_boards_board(1,date(2014,5,22),None,['Sozialhilferat (SHR)', 'Sozialhilferat (SHR)', 'Social Board (SB)']))
loader.save(create_boards_board(2,date(2014,5,22),None,['Sozialhilfeausschuss (SAS)', 'Sozialhilfeausschuss (SAS)', 'Social Commission (SC)']))
loader.save(create_boards_board(3,date(2014,5,22),None,['St\xe4ndiges Pr\xe4sidium (SP)', 'St\xe4ndiges Pr\xe4sidium (SP)', 'Permanent Board (PB)']))

loader.flush_deferred_objects()
