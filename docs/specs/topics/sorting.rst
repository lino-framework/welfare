.. doctest docs/specs/topics/sorting.rst

.. _welfare.specs.topics.sorting:

=================
About sorting
=================

I wrote this originally when working on :ticket:`4096` to verify my theory that
the issues are caused by demo data being generated differently because sorting
has changed.  The result is negative, i.e. my theory seems wrong.

Note that alphabetic sorting is not as we wanted it to be when we wrote
:func:`lino_welfare.modlib.welfare.models.customize_sqlite` (which creates a
custom collation for sqlite). We wanted people like "da Vinci, David" or
"Ärgerlich, Erna" to be correctly sorted.  But this seems to not be related.


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


>>> for o in coachings.CoachingType.objects.all():
...    print("{o.id} {o}".format(o=o))
1 ASD
2 DSBE
3 Schuldnerberatung


>>> for o in coachings.Coaching.objects.all():
...    print("{o.id} {o}".format(o=o))
1 alicia / Ausdemwald A
2 hubert / Ausdemwald A
3 melanie / Ausdemwald A
4 caroline / Ausdemwald A
5 hubert / Collard C
6 melanie / Collard C
7 hubert / Dobbelstein-Demeulenaere D
8 melanie / Dobbelstein D
9 alicia / Evertz B
10 hubert / Evers E
11 melanie / Evers E
12 caroline / Evers E
13 hubert / Emonts D
14 melanie / Emonts D
15 hubert / Emonts D
16 melanie / Engels E
17 alicia / Engels E
18 hubert / Engels E
19 melanie / Engels E
20 caroline / Faymonville L
21 hubert / Faymonville L
22 melanie / Groteclaes G
23 hubert / Hilgers H
24 melanie / Hilgers H
25 alicia / Hilgers H
26 hubert / Jacobs J
27 melanie / Jacobs J
28 caroline / Jacobs J
29 hubert / Johnen J
30 melanie / Johnen J
31 hubert / Jonas J
32 melanie / Jonas J
33 alicia / Jonas J
34 hubert / Jonas J
35 melanie / Kaivers K
36 caroline / Kaivers K
37 hubert / Lambertz G
38 melanie / Lazarus L
39 hubert / Lazarus L
40 melanie / Lazarus L
41 alicia / Leffin J
42 hubert / Malmendier M
43 melanie / Malmendier M
44 caroline / Malmendier M
45 hubert / Meessen M
46 melanie / Meessen M
47 hubert / Meessen M
48 melanie / Meessen M
49 alicia / Emonts-Gast E
50 hubert / Emonts-Gast E
51 melanie / Radermacher A
52 caroline / Radermacher C
53 hubert / Radermacher C
54 melanie / Radermacher C
55 hubert / Radermacher E
56 melanie / Radermacher E
57 alicia / Radermacher E
58 hubert / Radermacher F
59 melanie / Radermacher G
60 caroline / Radermacher G
61 hubert / Radermacher G
62 melanie / Radermacher G
63 hubert / Radermacher H
64 melanie / Radermacher H
65 alicia / da Vinci D
66 hubert / van Veen V
67 melanie / van Veen V
68 caroline / van Veen V
69 hubert / Õunapuu Õ
70 melanie / Õunapuu Õ
71 hubert / Östges O
72 melanie / Östges O
73 alicia / Östges O
74 hubert / Radermecker R
75 melanie / Radermecker R
76 caroline / Radermecker R
77 hubert / Radermecker R
78 melanie / Brecht B
79 hubert / Brecht B
80 melanie / Keller K
81 alicia / Dubois R
82 hubert / Dubois R
83 melanie / Dubois R
84 caroline / Denon D
85 hubert / Denon D
86 melanie / Denon D
87 hubert / Jeanémart J
88 melanie / Jeanémart J
89 alicia / Jeanémart J
90 hubert / Jeanémart J

>>> for o in jobs.Job.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Kellner bei BISA
5 Kellner bei R-Cycle Sperrgutsortierzentrum
2 Koch bei R-Cycle Sperrgutsortierzentrum
6 Koch bei Pro Aktiv V.o.G.
3 Küchenassistent bei Pro Aktiv V.o.G.
7 Küchenassistent bei BISA
4 Tellerwäscher bei BISA
8 Tellerwäscher bei R-Cycle Sperrgutsortierzentrum

>>> for o in cal.Calendar.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Allgemein
2 alicia
3 caroline
4 hubert
5 judith
6 melanie
7 patrick
8 romain
9 rolf
10 robin
11 theresia

>>> for o in isip.Contract.objects.all():
...    print("{o.id} {o}".format(o=o))
1 VSE#1 (Alfons AUSDEMWALD)
2 VSE#2 (Alfons AUSDEMWALD)
3 VSE#3 (Dorothée DOBBELSTEIN)
4 VSE#4 (Eberhart EVERS)
5 VSE#5 (Eberhart EVERS)
6 VSE#6 (Eberhart EVERS)
7 VSE#7 (Edgar ENGELS)
8 VSE#8 (Edgar ENGELS)
9 VSE#9 (Gregory GROTECLAES)
10 VSE#10 (Jacqueline JACOBS)
11 VSE#11 (Karl KAIVERS)
12 VSE#12 (Line LAZARUS)
13 VSE#13 (Line LAZARUS)
14 VSE#14 (Melissa MEESSEN)
15 VSE#15 (Melissa MEESSEN)
16 VSE#16 (Melissa MEESSEN)
17 VSE#17 (Alfons RADERMACHER)
18 VSE#18 (Edgard RADERMACHER)
19 VSE#19 (Guido RADERMACHER)
20 VSE#20 (Guido RADERMACHER)
21 VSE#21 (Guido RADERMACHER)
22 VSE#22 (David DA VINCI)
23 VSE#23 (David DA VINCI)
24 VSE#24 (Otto ÖSTGES)
25 VSE#25 (Otto ÖSTGES)
26 VSE#26 (Otto ÖSTGES)
27 VSE#27 (Bernd BRECHT)
28 VSE#28 (Bernd BRECHT)
29 VSE#29 (Robin DUBOIS)
30 VSE#30 (Robin DUBOIS)
31 VSE#31 (Robin DUBOIS)
32 VSE#32 (Jérôme JEANÉMART)
33 VSE#33 (Jérôme JEANÉMART)

>>> for o in jobs.Contract.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Art.60§7-Konvention#1 (Charlotte COLLARD)
2 Art.60§7-Konvention#2 (Bernd EVERTZ)
3 Art.60§7-Konvention#3 (Luc FAYMONVILLE)
4 Art.60§7-Konvention#4 (Luc FAYMONVILLE)
5 Art.60§7-Konvention#5 (Hildegard HILGERS)
6 Art.60§7-Konvention#6 (Guido LAMBERTZ)
7 Art.60§7-Konvention#7 (Marc MALMENDIER)
8 Art.60§7-Konvention#8 (Marc MALMENDIER)
9 Art.60§7-Konvention#9 (Christian RADERMACHER)
10 Art.60§7-Konvention#10 (Christian RADERMACHER)
11 Art.60§7-Konvention#11 (Fritz RADERMACHER)
12 Art.60§7-Konvention#12 (Vincent VAN VEEN)
13 Art.60§7-Konvention#13 (Rik RADERMECKER)
14 Art.60§7-Konvention#14 (Rik RADERMECKER)
15 Art.60§7-Konvention#15 (Denis DENON)
16 Art.60§7-Konvention#16 (Denis DENON)

>>> for o in art61.Contract.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Art.61-Konvention#1 (Daniel EMONTS)
2 Art.61-Konvention#2 (Josef JONAS)
3 Art.61-Konvention#3 (Josef JONAS)
4 Art.61-Konvention#4 (Erna EMONTS-GAST)
5 Art.61-Konvention#5 (Hedi RADERMACHER)
6 Art.61-Konvention#6 (Hedi RADERMACHER)
7 Art.61-Konvention#7 (Karl KELLER)


>>> for o in aids.Granting.objects.all():
...    print("{o.id} {o} {o.client}".format(o=o))
1 EiEi/29.09.12/116 AUSDEMWALD Alfons (116)
2 Ausländerbeihilfe/08.08.13/116 AUSDEMWALD Alfons (116)
3 EiEi/09.10.12/124 DOBBELSTEIN Dorothée (124)
4 Ausländerbeihilfe/19.10.12/127 EVERS Eberhart (127)
5 EiEi/12.02.14/127 EVERS Eberhart (127)
6 Ausländerbeihilfe/15.03.14/127 EVERS Eberhart (127)
7 EiEi/29.10.12/129 ENGELS Edgar (129)
8 Ausländerbeihilfe/22.02.14/129 ENGELS Edgar (129)
9 EiEi/08.11.12/132 GROTECLAES Gregory (132)
10 Ausländerbeihilfe/18.11.12/137 JACOBS Jacqueline (137)
11 EiEi/28.11.12/141 KAIVERS Karl (141)
12 Ausländerbeihilfe/08.12.12/144 LAZARUS Line (144)
13 EiEi/03.04.14/144 LAZARUS Line (144)
14 Ausländerbeihilfe/18.12.12/147 MEESSEN Melissa (147)
15 EiEi/13.04.14/147 MEESSEN Melissa (147)
16 Ausländerbeihilfe/14.05.14/147 MEESSEN Melissa (147)
17 EiEi/28.12.12/153 RADERMACHER Alfons (153)
18 Ausländerbeihilfe/07.01.13/157 RADERMACHER Edgard (157)
19 EiEi/17.01.13/159 RADERMACHER Guido (159)
20 Ausländerbeihilfe/13.05.14/159 RADERMACHER Guido (159)
21 EiEi/13.06.14/159 RADERMACHER Guido (159)
22 Ausländerbeihilfe/27.01.13/165 DA VINCI David (165)
23 EiEi/23.05.14/165 DA VINCI David (165)
24 Ausländerbeihilfe/06.02.13/168 ÖSTGES Otto (168)
25 EiEi/02.06.14/168 ÖSTGES Otto (168)
26 Ausländerbeihilfe/03.07.14/168 ÖSTGES Otto (168)
27 EiEi/16.02.13/177 BRECHT Bernd (177)
28 Ausländerbeihilfe/12.06.14/177 BRECHT Bernd (177)
29 EiEi/26.02.13/179 DUBOIS Robin (179)
30 Ausländerbeihilfe/22.06.14/179 DUBOIS Robin (179)
31 EiEi/23.07.14/179 DUBOIS Robin (179)
32 Ausländerbeihilfe/08.03.13/181 JEANÉMART Jérôme (181)
33 EiEi/02.07.14/181 JEANÉMART Jérôme (181)
34 EiEi/22.05.14/116 AUSDEMWALD Alfons (116)
35 EiEi/22.05.14/118 COLLARD Charlotte (118)
36 Ausländerbeihilfe/23.05.14/124 DOBBELSTEIN Dorothée (124)
37 Ausländerbeihilfe/23.05.14/127 EVERS Eberhart (127)
38 Feste Beihilfe/24.05.14/128 EMONTS Daniel (128)
39 Feste Beihilfe/24.05.14/129 ENGELS Edgar (129)
40 Erstattung/25.05.14/130 FAYMONVILLE Luc (130*)
41 Erstattung/25.05.14/132 GROTECLAES Gregory (132)
42 Übernahmeschein/26.05.14/133 HILGERS Hildegard (133)
43 Übernahmeschein/26.05.14/137 JACOBS Jacqueline (137)
44 AMK/27.05.14/139 JONAS Josef (139)
45 AMK/27.05.14/141 KAIVERS Karl (141)
46 DMH/28.05.14/142 LAMBERTZ Guido (142)
47 DMH/28.05.14/144 LAZARUS Line (144)
48 Möbellager/29.05.14/146 MALMENDIER Marc (146)
49 Möbellager/29.05.14/147 MEESSEN Melissa (147)
50 Heizkosten/30.05.14/152 EMONTS-GAST Erna (152)
51 Heizkosten/30.05.14/153 RADERMACHER Alfons (153)
52 Lebensmittelbank/31.05.14/155 RADERMACHER Christian (155)
53 Lebensmittelbank/31.05.14/157 RADERMACHER Edgard (157)
54 Kleiderkammer/01.06.14/159 RADERMACHER Guido (159)
55 Kleiderkammer/01.06.14/161 RADERMACHER Hedi (161)
56 DMH/27.05.14/139 JONAS Josef (139)
57 DMH/27.05.14/141 KAIVERS Karl (141)
58 Kleiderkammer/22.05.14/240 FRISCH Paul (240)
