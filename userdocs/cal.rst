.. _welfare.cal:

========
Calendar
========


.. contents:: 
   :local:
   :depth: 2


.. actor:: cal.CalendarPanel


.. actor:: cal.Event

    Possible values for the state of an :ddref: `cal.Event`:

    .. django2rst:: 

        settings.SITE.login('robin').show(cal.EventStates)

.. actor:: cal.Events

    The table of all calendar events.

.. actor:: cal.Guest

    Possible values for the state of a :ddref: `cal.Guest`:

    .. django2rst:: 

        settings.SITE.login('robin').show(cal.GuestStates)

.. actor:: cal.Task

.. actor:: cal.Task.state

    The state of a :ddref: `cal.Task`.
    Possible values are:

    .. django2rst:: 

        settings.SITE.login('robin').show(cal.TaskStates)

.. actor:: cal.Calendar
.. actor:: cal.Subscription
.. actor:: cal.Room
.. actor:: cal.Priority
.. actor:: cal.GuestRole

