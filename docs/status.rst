==============
Project status
==============

Lino Welfare is a rather big project. The following packages are
currently being maintained by the original author:

.. py2rst::

   from lino.utils.code import analyze_rst
   print(analyze_rst('atelier', 'lino', 'lino_welfare'))

For comparison here the same numbers for some
other projects:

.. py2rst::

   from lino.utils.code import analyze_rst 
   print(analyze_rst('appy', 'babel', 'fuzzy', 'unipath', 'dateutil', 'xlwt', 'jinja2', 'sphinx', 'django'))

(But note that these numbers are done using :mod:`lino.utils.code`
which inspects only the currently imported code)


Raw metrics given by ``pylint lino``:

+----------+-------+------+
|type      |number |%     |
+==========+=======+======+
|code      |68748  |67.13 |
+----------+-------+------+
|docstring |16820  |16.42 |
+----------+-------+------+
|comment   |6680   |6.52  |
+----------+-------+------+
|empty     |10165  |9.93  |
+----------+-------+------+

