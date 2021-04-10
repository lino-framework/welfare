.. doctest docs/specs/sorting.rst

.. _welfare.specs.topics.sorting:

=================
About sorting
=================

I wrote this originally when working on :ticket:`4096`  to verify my theory that
the issues are caused by demo data being generated differently because sorting
has changed.  The result is negative, i.e. my theory seems wrong.

Note that alphabetic sorting is not as we wanted it to be when we wrote
:func:`lino_welfare.modlib.welfare.models.customize_sqlite` (which creates a
custom collation for sqlite). We wanted people like "da Vinci, David" or
"Ärgerlich, Erna" to be correctly sorted.  



.. contents::
   :depth: 2
   :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.demo')
>>> from lino.api.doctest import *

This to verify whether sorting works as expected.

>>> for o in contacts.Company.objects.all():
...    print("{o.id} {o.name}".format(o=o))
100 Belgisches Rotes Kreuz
101 Rumma & Ko OÜ
102 Bäckerei Ausdemwald
103 Bäckerei Mießen
104 Bäckerei Schmitz
105 Garage Mergelsberg
106 Donderweer BV
107 Van Achter NV
108 Hans Flott & Co
109 Bernd Brechts Bücherladen
110 Reinhards Baumschule
111 Moulin Rouge
112 Auto École Verte
187 ÖSHZ Kettenis
188 BISA
189 R-Cycle Sperrgutsortierzentrum
190 Die neue Alternative V.o.G.
191 Pro Aktiv V.o.G.
192 Werkstatt Cardijn V.o.G.
193 Behindertenstätten Eupen
194 Beschützende Werkstätte Eupen
195 Alliance Nationale des Mutualités Chrétiennes
196 Mutualité Chrétienne de Verviers - Eupen
197 Union Nationale des Mutualités Neutres
198 Mutualia - Mutualité Neutre
199 Solidaris - Mutualité socialiste et syndicale de la province de Liège
200 Apotheke Reul
201 Apotheke Schunck
202 Pharmacies Populaires de Verviers
203 Bosten-Bocken A
204 Brüll Christine
205 Brocal Catherine
206 Bourseaux Alexandre
207 Baguette Stéphanie
208 Demarteau Bernadette
209 Schmitz Marc
210 Cashback sprl
211 Money Wizard AS
214 Arbeitsamt der D.G.
220 AS Express Post
221 AS Matsalu Veevärk
222 Eesti Energia AS
223 IIZI kindlustusmaakler AS
224 Maksu- ja Tolliamet
225 Ragn-Sells AS
226 Electrabel Customer Solutions
227 Ethias s.a.
228 Niederau Eupen AG
229 Leffin Electronics
230 Oikos
231 KAP


>>> for o in contacts.Person.objects.all():
...    print("{o.id} {o.last_name}, {o.first_name}".format(o=o))
258 Adam, Albert
262 Adam, Ilja
267 Adam, Noémie
268 Adam, Odette
269 Adam, Pascale
184 Allmanns, Alicia
115 Altenberg, Hans
113 Arens, Andreas
114 Arens, Annette
116 Ausdemwald, Alfons
117 Bastiaensen, Laurent
170 Bodard, Bernard
259 Braun, Bruno
263 Braun, Jan
264 Braun, Kevin
265 Braun, Lars
266 Braun, Monique
177 Brecht, Bernd
217 Castou, Carmen
120 Chantraine, Marc
119 Charlier, Ulrike
118 Collard, Charlotte
122 Demeulenaere, Dorothée
180 Denon, Denis
121 Dericum, Daniel
124 Dobbelstein, Dorothée
123 Dobbelstein-Demeulenaere, Dorothée
249 Drosson, Dora
179 Dubois, Robin
171 Dupont, Jean
175 Eierschal, Emil
244 Einzig, Paula
128 Emonts, Daniel
150 Emonts, Erich
152 Emonts-Gast, Erna
151 Emontspool, Erwin
129 Engels, Edgar
125 Ernst, Berta
127 Evers, Eberhart
126 Evertz, Bernd
260 Evrard, Eveline
130 Faymonville, Luc
261 Freisen, Françoise
242 Frisch, Alice
243 Frisch, Bernd
248 Frisch, Clara
250 Frisch, Dennis
238 Frisch, Hubert
253 Frisch, Irma
241 Frisch, Ludwig
252 Frisch, Melba
240 Frisch, Paul
245 Frisch, Peter
247 Frisch, Philippe
239 Frogemuth, Gaby
212 Gerkens, Gerd
131 Gernegroß, Germaine
132 Groteclaes, Gregory
134 Hilgers, Henri
133 Hilgers, Hildegard
183 Huppertz, Hubert
135 Ingels, Irene
137 Jacobs, Jacqueline
136 Jansen, Jérémy
181 Jeanémart, Jérôme
138 Johnen, Johann
139 Jonas, Josef
140 Jousten, Jan
186 Jousten, Judith
141 Kaivers, Karl
213 Kasennova, Tatjana
178 Keller, Karl
219 Kimmel, Killian
176 Lahm, Lisa
142 Lambertz, Guido
143 Laschet, Laura
144 Lazarus, Line
145 Leffin, Josefine
251 Loslever, Laura
146 Malmendier, Marc
172 Martelaer, Mark
147 Meessen, Melissa
149 Meier, Marie-Louise
148 Mießen, Michael
182 Mélard, Mélanie
153 Radermacher, Alfons
154 Radermacher, Berta
155 Radermacher, Christian
156 Radermacher, Daniela
157 Radermacher, Edgard
158 Radermacher, Fritz
159 Radermacher, Guido
160 Radermacher, Hans
161 Radermacher, Hedi
162 Radermacher, Inge
163 Radermacher, Jean
173 Radermecker, Rik
185 Thelen, Theresia
174 Vandenmeulenbos, Marie-Louise
218 Waldmann, Walter
215 Waldmann, Waltraud
216 Wehnicht, Werner
246 Zweith, Petra
165 da Vinci, David
164 di Rupo, Didier
166 van Veen, Vincent
169 Ärgerlich, Erna
167 Õunapuu, Õie
168 Östges, Otto


>>> for o in pcsw.Client.objects.all():
...    print("{o.id} {o.last_name}, {o.first_name}".format(o=o))
116 Ausdemwald, Alfons
117 Bastiaensen, Laurent
118 Collard, Charlotte
120 Chantraine, Marc
121 Dericum, Daniel
122 Demeulenaere, Dorothée
123 Dobbelstein-Demeulenaere, Dorothée
124 Dobbelstein, Dorothée
125 Ernst, Berta
126 Evertz, Bernd
127 Evers, Eberhart
128 Emonts, Daniel
129 Engels, Edgar
130 Faymonville, Luc
131 Gernegroß, Germaine
132 Groteclaes, Gregory
133 Hilgers, Hildegard
134 Hilgers, Henri
135 Ingels, Irene
136 Jansen, Jérémy
137 Jacobs, Jacqueline
138 Johnen, Johann
139 Jonas, Josef
140 Jousten, Jan
141 Kaivers, Karl
142 Lambertz, Guido
143 Laschet, Laura
144 Lazarus, Line
145 Leffin, Josefine
146 Malmendier, Marc
147 Meessen, Melissa
149 Meier, Marie-Louise
150 Emonts, Erich
151 Emontspool, Erwin
152 Emonts-Gast, Erna
153 Radermacher, Alfons
154 Radermacher, Berta
155 Radermacher, Christian
156 Radermacher, Daniela
157 Radermacher, Edgard
158 Radermacher, Fritz
159 Radermacher, Guido
160 Radermacher, Hans
161 Radermacher, Hedi
162 Radermacher, Inge
164 di Rupo, Didier
165 da Vinci, David
166 van Veen, Vincent
167 Õunapuu, Õie
168 Östges, Otto
172 Martelaer, Mark
173 Radermecker, Rik
174 Vandenmeulenbos, Marie-Louise
175 Eierschal, Emil
176 Lahm, Lisa
177 Brecht, Bernd
178 Keller, Karl
179 Dubois, Robin
180 Denon, Denis
181 Jeanémart, Jérôme
213 Kasennova, Tatjana
240 Frisch, Paul
259 Braun, Bruno


>>> for o in users.User.objects.all():
...    print("{o.id} {o.username} ({o.last_name}, {o.first_name})".format(o=o))
8 nicolas (, )
6 alicia (Allmanns, Alicia)
9 caroline (Carnol, Caroline)
5 hubert (Huppertz, Hubert)
10 judith (Jousten, Judith)
13 kerstin (Kerres, Kerstin)
4 melanie (Mélard, Mélanie)
11 patrick (Paraneau, Patrick)
2 romain (Raffault, Romain)
1 rolf (Rompen, Rolf)
3 robin (Rood, Robin)
7 theresia (Thelen, Theresia)
12 wilfried (Willems, Wilfried)

>>> for o in households.Household.objects.all():
...    print("{o.id} {o.name}".format(o=o))
232 Gerkens-Kasennova
233 Huppertz-Jousten
234 Jeanémart-Thelen
235 Denon-Mélard
236 Dubois-Lahm
237 Jeanémart-Vandenmeulenbos
254 Frisch-Frogemuth
255 Frisch-Einzig
256 Frisch-Zweith
257 Frisch-Loslever
270 Adam-Evrard
271 Adam-Freisen
272 Braun-Evrard
273 Braun-Freisen
