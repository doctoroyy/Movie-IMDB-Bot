# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import random
import re
from functools import reduce
from time import sleep

import requests
from lxml import etree
from vika import Vika
import imov


def get_html_doc(url):
    head = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    resopnse = requests.get(url, headers=head)

    resopnse.encoding = 'utf-8'
    html_doc = resopnse.text
    return html_doc


def find_all_by_pat(pat, string):
    res = re.findall(pat, string)
    return res


def search_fields_by_xpath(html):
    def func(__xpath):
        res = html.xpath(__xpath)
        try:
            return res[0].strip()
        except:
            return 'not found'

    return func


def get_chinese_name(html):
    chinese_name_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/h3/a/text()'
    return search_fields_by_xpath(html)(chinese_name_xpath)


def get_director_name(html):
    director_name_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/div/span[4]/text()'
    res = search_fields_by_xpath(html)(director_name_xpath)
    if res != 'not found':
        return res.split(' / ')[1]
    return res


def get_desc(html):
    desc_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/p/text()'
    return search_fields_by_xpath(html)(desc_xpath)


def get_douban_info(query_name):
    url = 'https://www.douban.com/search?cat=1002&q=%s' % query_name
    douban_doc = get_html_doc(url)
    html = etree.HTML(douban_doc)
    return {
        'chineseName': get_chinese_name(html),
        'directorName': get_director_name(html),
        'desc': get_desc(html)
    }


if __name__ == '__main__':
    vika = Vika("uskZWIcJI4lqLs8JOHfOwMb")
    # 通过 datasheetId 来指定要从哪张维格表操作数据。
    datasheet = vika.datasheet("dstcclPiXMnNYvza6n", field_key="id")
    # 返回所有的记录
    records = datasheet.records.all()

    url = "https://www.imdb.com/chart/top"
    # imdb_doc = get_html_doc(url)
    pat = r'<td class="titleColumn">\s*(.*)..*\s*.*\s<a\s.*href="/title/(.*)/.*"\s.*title="(.*)\s.*\(dir\.\).*" >(' \
          r'.*)</a>.*\s*<span class="secondaryInfo">\((.*)\)</span> '
    # x_td_path = '//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[1]/td[2]'
    # html = etree.HTML(imdb_doc)
    # print(html.xpath(x_td_path))
    movie_tuples = [('1', 'tt0111161', 'Frank Darabont', 'The Shawshank Redemption', '1994'),
                    ('2', 'tt0068646', 'Francis Ford Coppola', 'The Godfather', '1972'),
                    ('3', 'tt0071562', 'Francis Ford Coppola', 'The Godfather: Part II', '1974'),
                    ('4', 'tt0468569', 'Christopher Nolan', 'The Dark Knight', '2008'),
                    ('5', 'tt0050083', 'Sidney Lumet', '12 Angry Men', '1957'),
                    ('6', 'tt0108052', 'Steven Spielberg', "Schindler's List", '1993'),
                    ('7', 'tt0167260', 'Peter Jackson', 'The Lord of the Rings: The Return of the King', '2003'),
                    ('8', 'tt0110912', 'Quentin Tarantino', 'Pulp Fiction', '1994'),
                    ('9', 'tt0060196', 'Sergio Leone', 'Il buono, il brutto, il cattivo', '1966'),
                    ('10', 'tt0120737', 'Peter Jackson', 'The Lord of the Rings: The Fellowship of the Ring', '2001'),
                    ('11', 'tt0137523', 'David Fincher', 'Fight Club', '1999'),
                    ('12', 'tt0109830', 'Robert Zemeckis', 'Forrest Gump', '1994'),
                    ('13', 'tt1375666', 'Christopher Nolan', 'Inception', '2010'),
                    ('14', 'tt0167261', 'Peter Jackson', 'The Lord of the Rings: The Two Towers', '2002'),
                    ('15', 'tt0080684', 'Irvin Kershner', 'Star Wars: Episode V - The Empire Strikes Back', '1980'),
                    ('16', 'tt0133093', 'Lana Wachowski', 'The Matrix', '1999'),
                    ('17', 'tt0099685', 'Martin Scorsese', 'Goodfellas', '1990'),
                    ('18', 'tt0073486', 'Milos Forman', "One Flew Over the Cuckoo's Nest", '1975'),
                    ('19', 'tt0047478', 'Akira Kurosawa', 'Shichinin no samurai', '1954'),
                    ('20', 'tt0114369', 'David Fincher', 'Se7en', '1995'),
                    ('21', 'tt0118799', 'Roberto Benigni', 'La vita è bella', '1997'),
                    ('22', 'tt0317248', 'Fernando Meirelles', 'Cidade de Deus', '2002'),
                    ('23', 'tt0102926', 'Jonathan Demme', 'The Silence of the Lambs', '1991'),
                    ('24', 'tt0038650', 'Frank Capra', "It's a Wonderful Life", '1946'),
                    ('25', 'tt0076759', 'George Lucas', 'Star Wars', '1977'),
                    ('26', 'tt0120815', 'Steven Spielberg', 'Saving Private Ryan', '1998'),
                    ('27', 'tt0120689', 'Frank Darabont', 'The Green Mile', '1999'),
                    ('28', 'tt0245429', 'Hayao Miyazaki', 'Sen to Chihiro no kamikakushi', '2001'),
                    ('29', 'tt0816692', 'Christopher Nolan', 'Interstellar', '2014'),
                    ('30', 'tt6751668', 'Bong Joon Ho', 'Gisaengchung', '2019'),
                    ('31', 'tt0110413', 'Luc Besson', 'Léon', '1994'),
                    ('32', 'tt0056058', 'Masaki Kobayashi', 'Seppuku', '1962'),
                    ('33', 'tt0114814', 'Bryan Singer', 'The Usual Suspects', '1995'),
                    ('34', 'tt0110357', 'Roger Allers', 'The Lion King', '1994'),
                    ('35', 'tt0253474', 'Roman Polanski', 'The Pianist', '2002'),
                    ('36', 'tt0103064', 'James Cameron', 'Terminator 2: Judgment Day', '1991'),
                    ('37', 'tt0088763', 'Robert Zemeckis', 'Back to the Future', '1985'),
                    ('38', 'tt0120586', 'Tony Kaye', 'American History X', '1998'),
                    ('39', 'tt0027977', 'Charles Chaplin', 'Modern Times', '1936'),
                    ('40', 'tt0172495', 'Ridley Scott', 'Gladiator', '2000'),
                    ('41', 'tt0054215', 'Alfred Hitchcock', 'Psycho', '1960'),
                    ('42', 'tt0407887', 'Martin Scorsese', 'The Departed', '2006'),
                    ('43', 'tt0021749', 'Charles Chaplin', 'City Lights', '1931'),
                    ('44', 'tt1675434', 'Olivier Nakache', 'The Intouchables', '2011'),
                    ('45', 'tt2582802', 'Damien Chazelle', 'Whiplash', '2014'),
                    ('46', 'tt0095327', 'Isao Takahata', 'Hotaru no haka', '1988'),
                    ('47', 'tt0482571', 'Christopher Nolan', 'The Prestige', '2006'),
                    ('48', 'tt0064116', 'Sergio Leone', 'Once Upon a Time in the West', '1968'),
                    ('49', 'tt0034583', 'Michael Curtiz', 'Casablanca', '1942'),
                    ('50', 'tt0095765', 'Giuseppe Tornatore', 'Nuovo Cinema Paradiso', '1988'),
                    ('51', 'tt0047396', 'Alfred Hitchcock', 'Rear Window', '1954'),
                    ('52', 'tt0078748', 'Ridley Scott', 'Alien', '1979'),
                    ('53', 'tt0078788', 'Francis Ford Coppola', 'Apocalypse Now', '1979'),
                    ('54', 'tt0209144', 'Christopher Nolan', 'Memento', '2000'),
                    ('55', 'tt0032553', 'Charles Chaplin', 'The Great Dictator', '1940'),
                    ('56', 'tt0082971', 'Steven Spielberg', 'Raiders of the Lost Ark', '1981'),
                    ('57', 'tt1853728', 'Quentin Tarantino', 'Django Unchained', '2012'),
                    ('58', 'tt0405094', 'Florian Henckel von Donnersmarck', 'The Lives of Others', '2006'),
                    ('59', 'tt8503618', 'Thomas Kail', 'Hamilton', '2020'),
                    ('60', 'tt0050825', 'Stanley Kubrick', 'Paths of Glory', '1957'),
                    ('61', 'tt0910970', 'Andrew Stanton', 'WALL·E', '2008'),
                    ('62', 'tt7286456', 'Todd Phillips', 'Joker', '2019'),
                    ('63', 'tt0081505', 'Stanley Kubrick', 'The Shining', '1980'),
                    ('64', 'tt4154756', 'Anthony Russo', 'Avengers: Infinity War', '2018'),
                    ('65', 'tt0043014', 'Billy Wilder', 'Sunset Blvd.', '1950'),
                    ('66', 'tt0051201', 'Billy Wilder', 'Witness for the Prosecution', '1957'),
                    ('67', 'tt0364569', 'Chan-wook Park', 'Oldeuboi', '2003'),
                    ('68', 'tt4633694', 'Bob Persichetti', 'Spider-Man: Into the Spider-Verse', '2018'),
                    ('69', 'tt0119698', 'Hayao Miyazaki', 'Mononoke-hime', '1997'), (
                        '70', 'tt0057012', 'Stanley Kubrick',
                        'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', '1964'),
                    ('71', 'tt1345836', 'Christopher Nolan', 'The Dark Knight Rises', '2012'),
                    ('72', 'tt0087843', 'Sergio Leone', 'Once Upon a Time in America', '1984'),
                    ('73', 'tt5311514', 'Makoto Shinkai', 'Kimi no na wa.', '2016'),
                    ('74', 'tt0090605', 'James Cameron', 'Aliens', '1986'),
                    ('75', 'tt2380307', 'Lee Unkrich', 'Coco', '2017'),
                    ('76', 'tt4154796', 'Anthony Russo', 'Avengers: Endgame', '2019'),
                    ('77', 'tt8267604', 'Nadine Labaki', 'Capharnaüm', '2018'),
                    ('78', 'tt0169547', 'Sam Mendes', 'American Beauty', '1999'),
                    ('79', 'tt0112573', 'Mel Gibson', 'Braveheart', '1995'),
                    ('80', 'tt0057565', 'Akira Kurosawa', 'Tengoku to jigoku', '1963'),
                    ('81', 'tt0082096', 'Wolfgang Petersen', 'Das Boot', '1981'),
                    ('82', 'tt0114709', 'John Lasseter', 'Toy Story', '1995'),
                    ('83', 'tt1187043', 'Rajkumar Hirani', '3 Idiots', '2009'),
                    ('84', 'tt0086879', 'Milos Forman', 'Amadeus', '1984'),
                    ('85', 'tt0361748', 'Quentin Tarantino', 'Inglourious Basterds', '2009'),
                    ('86', 'tt0119217', 'Gus Van Sant', 'Good Will Hunting', '1997'),
                    ('87', 'tt0086190', 'Richard Marquand', 'Star Wars: Episode VI - Return of the Jedi', '1983'),
                    ('88', 'tt0986264', 'Aamir Khan', 'Taare Zameen Par', '2007'),
                    ('89', 'tt0105236', 'Quentin Tarantino', 'Reservoir Dogs', '1992'),
                    ('90', 'tt0062622', 'Stanley Kubrick', '2001: A Space Odyssey', '1968'),
                    ('91', 'tt0180093', 'Darren Aronofsky', 'Requiem for a Dream', '2000'),
                    ('92', 'tt2106476', 'Thomas Vinterberg', 'Jagten', '2012'),
                    ('93', 'tt0052357', 'Alfred Hitchcock', 'Vertigo', '1958'),
                    ('94', 'tt0022100', 'Fritz Lang', 'M - Eine Stadt sucht einen Mörder', '1931'),
                    ('95', 'tt0338013', 'Michel Gondry', 'Eternal Sunshine of the Spotless Mind', '2004'),
                    ('96', 'tt0033467', 'Orson Welles', 'Citizen Kane', '1941'),
                    ('97', 'tt5074352', 'Nitesh Tiwari', 'Dangal', '2016'),
                    ('98', 'tt0045152', 'Stanley Donen', "Singin' in the Rain", '1952'),
                    ('99', 'tt0012349', 'Charles Chaplin', 'The Kid', '1921'),
                    ('100', 'tt0040522', 'Vittorio De Sica', 'Ladri di biciclette', '1948'),
                    ('101', 'tt0093058', 'Stanley Kubrick', 'Full Metal Jacket', '1987'),
                    ('102', 'tt0091251', 'Elem Klimov', 'Idi i smotri', '1985'),
                    ('103', 'tt0208092', 'Guy Ritchie', 'Snatch', '2000'),
                    ('104', 'tt0044741', 'Akira Kurosawa', 'Ikiru', '1952'),
                    ('105', 'tt0053125', 'Alfred Hitchcock', 'North by Northwest', '1959'),
                    ('106', 'tt0086250', 'Brian De Palma', 'Scarface', '1983'),
                    ('107', 'tt0066921', 'Stanley Kubrick', 'A Clockwork Orange', '1971'),
                    ('108', 'tt8579674', 'Sam Mendes', '1917', '2019'),
                    ('109', 'tt0075314', 'Martin Scorsese', 'Taxi Driver', '1976'),
                    ('110', 'tt1255953', 'Denis Villeneuve', 'Incendies', '2010'),
                    ('111', 'tt1832382', 'Asghar Farhadi', 'Jodaeiye Nader az Simin', '2011'),
                    ('112', 'tt0435761', 'Lee Unkrich', 'Toy Story 3', '2010'),
                    ('113', 'tt0070735', 'George Roy Hill', 'The Sting', '1973'),
                    ('114', 'tt0056172', 'David Lean', 'Lawrence of Arabia', '1962'),
                    ('115', 'tt0211915', 'Jean-Pierre Jeunet', 'Amélie', '2001'),
                    ('116', 'tt0017136', 'Fritz Lang', 'Metropolis', '1927'),
                    ('117', 'tt0053604', 'Billy Wilder', 'The Apartment', '1960'),
                    ('118', 'tt0059578', 'Sergio Leone', 'Per qualche dollaro in più', '1965'),
                    ('119', 'tt0036775', 'Billy Wilder', 'Double Indemnity', '1944'),
                    ('120', 'tt0056592', 'Robert Mulligan', 'To Kill a Mockingbird', '1962'),
                    ('121', 'tt1049413', 'Pete Docter', 'Up', '2009'),
                    ('122', 'tt0097576', 'Steven Spielberg', 'Indiana Jones and the Last Crusade', '1989'),
                    ('123', 'tt0113277', 'Michael Mann', 'Heat', '1995'),
                    ('124', 'tt0119488', 'Curtis Hanson', 'L.A. Confidential', '1997'),
                    ('125', 'tt6966692', 'Peter Farrelly', 'Green Book', '2018'),
                    ('126', 'tt0095016', 'John McTiernan', 'Die Hard', '1988'),
                    ('127', 'tt0372784', 'Christopher Nolan', 'Batman Begins', '2005'),
                    ('128', 'tt0055630', 'Akira Kurosawa', 'Yojinbo', '1961'),
                    ('129', 'tt0071853', 'Terry Gilliam', 'Monty Python and the Holy Grail', '1975'),
                    ('130', 'tt0042876', 'Akira Kurosawa', 'Rashômon', '1950'),
                    ('131', 'tt0363163', 'Oliver Hirschbiegel', 'Der Untergang', '2004'),
                    ('132', 'tt0118849', 'Majid Majidi', 'Bacheha-Ye aseman', '1997'),
                    ('133', 'tt0089881', 'Akira Kurosawa', 'Ran', '1985'),
                    ('134', 'tt0105695', 'Clint Eastwood', 'Unforgiven', '1992'),
                    ('135', 'tt0053291', 'Billy Wilder', 'Some Like It Hot', '1959'),
                    ('136', 'tt0347149', 'Hayao Miyazaki', 'Hauru no ugoku shiro', '2004'),
                    ('137', 'tt0042192', 'Joseph L. Mankiewicz', 'All About Eve', '1950'),
                    ('138', 'tt0112641', 'Martin Scorsese', 'Casino', '1995'),
                    ('139', 'tt0268978', 'Ron Howard', 'A Beautiful Mind', '2001'),
                    ('140', 'tt0993846', 'Martin Scorsese', 'The Wolf of Wall Street', '2013'),
                    ('141', 'tt0057115', 'John Sturges', 'The Great Escape', '1963'),
                    ('142', 'tt0457430', 'Guillermo del Toro', "Pan's Labyrinth", '2006'),
                    ('143', 'tt0469494', 'Paul Thomas Anderson', 'There Will Be Blood', '2007'),
                    ('144', 'tt1305806', 'Juan José Campanella', 'El secreto de sus ojos', '2009'),
                    ('145', 'tt0120735', 'Guy Ritchie', 'Lock, Stock and Two Smoking Barrels', '1998'),
                    ('146', 'tt0055031', 'Stanley Kramer', 'Judgment at Nuremberg', '1961'),
                    ('147', 'tt0081398', 'Martin Scorsese', 'Raging Bull', '1980'),
                    ('148', 'tt0096283', 'Hayao Miyazaki', 'Tonari no Totoro', '1988'),
                    ('149', 'tt0040897', 'John Huston', 'The Treasure of the Sierra Madre', '1948'),
                    ('150', 'tt0046912', 'Alfred Hitchcock', 'Dial M for Murder', '1954'),
                    ('151', 'tt1130884', 'Martin Scorsese', 'Shutter Island', '2010'),
                    ('152', 'tt5027774', 'Martin McDonagh', 'Three Billboards Outside Ebbing, Missouri', '2017'),
                    ('153', 'tt0476735', 'Çagan Irmak', 'Babam ve Oglum', '2005'),
                    ('154', 'tt0071315', 'Roman Polanski', 'Chinatown', '1974'),
                    ('155', 'tt0015864', 'Charles Chaplin', 'The Gold Rush', '1925'),
                    ('156', 'tt0477348', 'Ethan Coen', 'No Country for Old Men', '2007'),
                    ('157', 'tt0434409', 'James McTeigue', 'V for Vendetta', '2005'),
                    ('158', 'tt2096673', 'Pete Docter', 'Inside Out', '2015'),
                    ('159', 'tt0084787', 'John Carpenter', 'The Thing', '1982'),
                    ('160', 'tt0080678', 'David Lynch', 'The Elephant Man', '1980'),
                    ('161', 'tt0050976', 'Ingmar Bergman', 'Det sjunde inseglet', '1957'),
                    ('162', 'tt0167404', 'M. Night Shyamalan', 'The Sixth Sense', '1999'),
                    ('163', 'tt1291584', "Gavin O'Connor", 'Warrior', '2011'),
                    ('164', 'tt0107290', 'Steven Spielberg', 'Jurassic Park', '1993'),
                    ('165', 'tt4729430', 'Sergio Pablos', 'Klaus', '2019'),
                    ('166', 'tt0117951', 'Danny Boyle', 'Trainspotting', '1996'),
                    ('167', 'tt0120382', 'Peter Weir', 'The Truman Show', '1998'),
                    ('168', 'tt0031381', 'Victor Fleming', 'Gone with the Wind', '1939'),
                    ('169', 'tt0266543', 'Andrew Stanton', 'Finding Nemo', '2003'),
                    ('170', 'tt0079944', 'Andrei Tarkovsky', 'Stalker', '1979'),
                    ('171', 'tt0050986', 'Ingmar Bergman', 'Smultronstället', '1957'),
                    ('172', 'tt0353969', 'Bong Joon Ho', 'Salinui chueok', '2003'),
                    ('173', 'tt0266697', 'Quentin Tarantino', 'Kill Bill: Vol. 1', '2003'),
                    ('174', 'tt0083658', 'Ridley Scott', 'Blade Runner', '1982'),
                    ('175', 'tt0050212', 'David Lean', 'The Bridge on the River Kwai', '1957'),
                    ('176', 'tt12361974', 'Zack Snyder', "Zack Snyder's Justice League", '2021'),
                    ('177', 'tt0116282', 'Joel Coen', 'Fargo', '1996'),
                    ('178', 'tt3011894', 'Damián Szifron', 'Relatos salvajes', '2014'),
                    ('179', 'tt0046438', 'Yasujirô Ozu', 'Tôkyô monogatari', '1953'),
                    ('180', 'tt3170832', 'Lenny Abrahamson', 'Room', '2015'),
                    ('181', 'tt1205489', 'Clint Eastwood', 'Gran Torino', '2008'),
                    ('182', 'tt0041959', 'Carol Reed', 'The Third Man', '1949'),
                    ('183', 'tt0047296', 'Elia Kazan', 'On the Waterfront', '1954'),
                    ('184', 'tt0077416', 'Michael Cimino', 'The Deer Hunter', '1978'),
                    ('185', 'tt0107207', 'Jim Sheridan', 'In the Name of the Father', '1993'),
                    ('186', 'tt0978762', 'Adam Elliot', 'Mary and Max', '2009'),
                    ('187', 'tt0112471', 'Richard Linklater', 'Before Sunrise', '1995'),
                    ('188', 'tt2278388', 'Wes Anderson', 'The Grand Budapest Hotel', '2014'),
                    ('189', 'tt0264464', 'Steven Spielberg', 'Catch Me If You Can', '2002'),
                    ('190', 'tt2267998', 'David Fincher', 'Gone Girl', '2014'),
                    ('191', 'tt2119532', 'Mel Gibson', 'Hacksaw Ridge', '2016'),
                    ('192', 'tt1392214', 'Denis Villeneuve', 'Prisoners', '2013'),
                    ('193', 'tt0060827', 'Ingmar Bergman', 'Persona', '1966'),
                    ('194', 'tt0015324', 'Buster Keaton', 'Sherlock Jr.', '1924'),
                    ('195', 'tt8108198', 'Sriram Raghavan', 'Andhadhun', '2018'),
                    ('196', 'tt0118715', 'Joel Coen', 'The Big Lebowski', '1998'),
                    ('197', 'tt0035446', 'Ernst Lubitsch', 'To Be or Not to Be', '1942'),
                    ('198', 'tt0072684', 'Stanley Kubrick', 'Barry Lyndon', '1975'),
                    ('199', 'tt0017925', 'Clyde Bruckman', 'The General', '1926'),
                    ('200', 'tt1950186', 'James Mangold', 'Ford v Ferrari', '2019'),
                    ('201', 'tt0892769', 'Dean DeBlois', 'How to Train Your Dragon', '2010'),
                    ('202', 'tt2024544', 'Steve McQueen', '12 Years a Slave', '2013'),
                    ('203', 'tt0116231', 'Yavuz Turgul', 'Eskiya', '1996'),
                    ('204', 'tt0077711', 'Ingmar Bergman', 'Höstsonaten', '1978'),
                    ('205', 'tt0031679', 'Frank Capra', 'Mr. Smith Goes to Washington', '1939'),
                    ('206', 'tt1392190', 'George Miller', 'Mad Max: Fury Road', '2015'),
                    ('207', 'tt0066763', 'Hrishikesh Mukherjee', 'Anand', '1971'),
                    ('208', 'tt0097165', 'Peter Weir', 'Dead Poets Society', '1989'),
                    ('209', 'tt0405159', 'Clint Eastwood', 'Million Dollar Baby', '2004'),
                    ('210', 'tt1201607', 'David Yates', 'Harry Potter and the Deathly Hallows: Part 2', '2011'),
                    ('211', 'tt0092005', 'Rob Reiner', 'Stand by Me', '1986'),
                    ('212', 'tt0074958', 'Sidney Lumet', 'Network', '1976'),
                    ('213', 'tt0052618', 'William Wyler', 'Ben-Hur', '1959'),
                    ('214', 'tt1028532', 'Lasse Hallström', "Hachi: A Dog's Tale", '2009'),
                    ('215', 'tt4016934', 'Chan-wook Park', 'Ah-ga-ssi', '2016'),
                    ('216', 'tt0061512', 'Stuart Rosenberg', 'Cool Hand Luke', '1967'),
                    ('217', 'tt3315342', 'James Mangold', 'Logan', '2017'),
                    ('218', 'tt0091763', 'Oliver Stone', 'Platoon', '1986'),
                    ('219', 'tt0046268', 'Henri-Georges Clouzot', 'Le salaire de la peur', '1953'),
                    ('220', 'tt0758758', 'Sean Penn', 'Into the Wild', '2007'),
                    ('221', 'tt1979320', 'Ron Howard', 'Rush', '2013'),
                    ('222', 'tt0113247', 'Mathieu Kassovitz', 'La haine', '1995'),
                    ('223', 'tt0079470', 'Terry Jones', 'Life of Brian', '1979'),
                    ('224', 'tt0053198', 'François Truffaut', 'Les quatre cents coups', '1959'),
                    ('225', 'tt0019254', 'Carl Theodor Dreyer', "La passion de Jeanne d'Arc", '1928'),
                    ('226', 'tt1895587', 'Tom McCarthy', 'Spotlight', '2015'),
                    ('227', 'tt0395169', 'Terry George', 'Hotel Rwanda', '2004'),
                    ('228', 'tt7060344', 'Ram Kumar', 'Ratsasan', '2018'),
                    ('229', 'tt1954470', 'Anurag Kashyap', 'Gangs of Wasseypur', '2012'),
                    ('230', 'tt0245712', 'Alejandro G. Iñárritu', 'Amores perros', '2000'),
                    ('231', 'tt2948372', 'Pete Docter', 'Soul', '2020'),
                    ('232', 'tt0060107', 'Andrei Tarkovsky', 'Andrei Rublev', '1966'),
                    ('233', 'tt0198781', 'Pete Docter', 'Monsters, Inc.', '2001'),
                    ('234', 'tt0075148', 'John G. Avildsen', 'Rocky', '1976'),
                    ('235', 'tt0087544', 'Hayao Miyazaki', 'Kaze no tani no Naushika', '1984'),
                    ('236', 'tt0032976', 'Alfred Hitchcock', 'Rebecca', '1940'),
                    ('237', 'tt0097223', 'Emir Kusturica', 'Dom za vesanje', '1988'),
                    ('238', 'tt0381681', 'Richard Linklater', 'Before Sunset', '2004'),
                    ('239', 'tt0118694', 'Kar-Wai Wong', 'Fa yeung nin wah', '2000'),
                    ('240', 'tt0048021', 'Jules Dassin', 'Du rififi chez les hommes', '1955'),
                    ('241', 'tt0405508', 'Rakeysh Omprakash Mehra', 'Rang De Basanti', '2006'),
                    ('242', 'tt0087884', 'Wim Wenders', 'Paris, Texas', '1984'),
                    ('243', 'tt8613070', 'Céline Sciamma', 'Portrait de la jeune fille en feu', '2019'),
                    ('244', 'tt3417422', 'Jeethu Joseph', 'Drishyam', '2013'),
                    ('245', 'tt0025316', 'Frank Capra', 'It Happened One Night', '1934'), (
                        '246', 'tt0169858', 'Hideaki Anno',
                        'Shin seiki Evangelion Gekijô-ban: Air/Magokoro wo, kimi ni',
                        '1997'), ('247', 'tt4430212', 'Nishikant Kamat', 'Drishyam', '2015'),
                    ('248', 'tt5323662', 'Naoko Yamada', 'Koe no katachi', '2016'),
                    ('249', 'tt2991224', 'Zaza Urushadze', 'Mandariinid', '2013'),
                    ('250', 'tt0058946', 'Gillo Pontecorvo', 'La battaglia di Algeri', '1966')]

    print(movie_tuples)
    movie_list = [{'rank': _[0], 'id': _[1], 'director': _[2], 'eng_name': _[3], 'year': _[4], 'chi_name': ''} for _ in
                  movie_tuples]



    print(movie_list)
    for movie in movie_list:
        if datasheet.records.filter(fldARNFRGuXJA=movie['id']).count() == 0:
            info = get_douban_info(movie['id'])
            print('要插入的：', info['chineseName'])

            if info['chineseName'] != 'not found':
                try:
                    datasheet.records.create({
                        "fldARNFRGuXJA": movie['id'],
                        "fldDBZht5ouSc": info['chineseName'],
                        "fldJuCfA75BqE": movie['eng_name'],
                        "fld0cm9AErPTO": info['directorName'],
                        "fldsFUuAKMdiJ": movie['director'],
                        "fldvMAgTJLi35": movie['year']
                    })
                except:
                    print('插入异常')
            else:
                print('没找到')
            # print(info['chineseName'])
            sleep(8)
'Star Wars: Episode V - The Empire Strikes Back'
'Star Wars: Episode V - The Empire Strikes Back'
