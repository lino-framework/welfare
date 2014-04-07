# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This migrator overrides the default welfare migrator.
"""

from lino_welfare.migrate import *


class Migrator(Migrator):

    def migrate_from_1_1_11(self, globals_dict):
        """Special migration for chatelet 1.1.12.  
        Was used on 20140325 and on 20140407.

        - course providers are companies
        - pupils are clients
        - courses.Line replaces courses.CourseOffer
        - courses.Topic replaces courses.CourseContent

        """
    
        super(Migrator, self).migrate_from_1_1_11(globals_dict)
    
        def noop(*args):
            return None
        globals_dict.update(create_courses_courseprovider=noop)
        globals_dict.update(create_courses_course=noop)
        globals_dict.update(create_courses_courserequest=noop)
    
        # globals_dict.update(create_humanlinks_link=noop)
        # globals_dict.update(create_uploads_upload=noop)

        courses_CourseOffer = resolve_model('courses.Line')
    
        def create_courses_courseoffer(
                id, title, content_id, provider_id, description):
            kw = dict()
            kw.update(id=id)
            kw.update(name=title)
            kw.update(topic_id=content_id)
            # kw.update(provider_id=provider_id)
            kw.update(description=description)
            return courses_CourseOffer(**kw)
        globals_dict.update(
            create_courses_courseoffer=create_courses_courseoffer)

        courses_CourseContent = resolve_model('courses.Topic')
        globals_dict.update(courses_CourseContent=courses_CourseContent)

        globals_dict.update(courses_Teacher=resolve_model('contacts.Person'))
        globals_dict.update(courses_Pupil=resolve_model('pcsw.Client'))

        return '1.1.12'

