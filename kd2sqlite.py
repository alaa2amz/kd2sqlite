
import xml.sax
import sqlite3
import datetime
import urllib.request as UR
import gzip
# 6355_5801_952_13108
# kanjidic2 header
#('霓', 38675)
# 飴
# dic_ref instead of number and it must converted to text
# skip_misclass is text q_code
kanji_dic_link = "http://www.edrdg.org/kanjidic/kanjidic2.xml.gz"
downloaded_kanjidic_fileName = "kd2web.xml.gz"
    

class kanjidicHandler(xml.sax.handler.ContentHandler):
    """class to convert kanjiDic2.xml to sqlite tables  """
    
    
    
    crntElmnt = ""  # current element.
    crntAtrs = {}  # current attributes.
    crntChar = ""   # current kanji character.
    crntID = 0      # current character id "utf-8 code to decimal"
    count4ID = 0    # count for strok count occurances in the smae character
    processed_kanji_counter = 0
    # tables tuples.

    file_version = ""
    database_version = ""
    date_of_creation = ""
    #timestamp = datetime.datetime
    date_of_generation = ""

    character = []
    cp_value = []
    cp_type = []
    rad_value = []
    rad_type = []
    grade = []
    stroke_count = []
    variant = []
    var_type = []
    freq = []
    jlpt = []
    dic_ref = []
    dr_type = []
    rad_name = []
    q_code = []
    qc_type = []
    reading = []
    r_type = []
    meaning = []
    m_lang = []
    nanori = []





    def startDocument(self):
        print("document Startet")

    def startElement(self, name, attrs):
        self.crntElmnt = name
        self.crntAtrs = attrs
        if name == "stroke_count":
            self.count4ID += 1

        if name == "character":
            self.processed_kanji_counter += 1

    def endElement(self, name):
        self.crntElmnt = ""
        self.crntAtrs = ""
        if name == "character":
            self.count4ID = 0
            print("no of kanjis prrocessed",self.processed_kanji_counter)


    def characters(self, content):

        if self.crntElmnt == "file_version":
            self.file_version = content

        if self.crntElmnt == "database_version":
            self.database_version = content

        if self.crntElmnt == "date_of_creation":
            self.date_of_creation = content



        if self.crntElmnt == "literal":
            self.crntChar = content
            kid = ord(content) # kanji utf-8 to used as id after converting it to decimal integer
            self.crntID = kid
            tmpTuple = (kid ,content)
            self.character.append(tmpTuple)

        elif self.crntElmnt == "cp_value":
            cp_id = None
            if self.crntAtrs["cp_type"] not in self.cp_type:
                self.cp_type.append(self.crntAtrs["cp_type"])
                cp_id = self.cp_type.index(self.crntAtrs["cp_type"])
            else:
                cp_id = self.cp_type.index(self.crntAtrs["cp_type"])
            tmpTuple = (self.crntID, content, cp_id)
            self.cp_value.append(tmpTuple)

        elif self.crntElmnt == "rad_value":
            rad_id = None
            if self.crntAtrs["rad_type"] not in self.rad_type:
                self.rad_type.append(self.crntAtrs["rad_type"])
                rad_id = self.rad_type.index(self.crntAtrs["rad_type"])
            else:
                rad_id = self.rad_type.index(self.crntAtrs["rad_type"])
            tmpTuple = (self.crntID, content, rad_id)
            self.rad_value.append(tmpTuple)

        elif self.crntElmnt == "grade":
            tmpTuple = (self.crntID, content)
            self.grade.append(tmpTuple)

        elif self.crntElmnt == "stroke_count":
            tmpTuple = (self.crntID, content, self.count4ID)
            self.stroke_count.append(tmpTuple)

        elif self.crntElmnt == "variant":
            var_id = None
            if self.crntAtrs["var_type"] not in self.var_type:
                self.var_type.append(self.crntAtrs["var_type"])
                var_id = self.var_type.index(self.crntAtrs["var_type"])
            else:
                var_id = self.var_type.index(self.crntAtrs["var_type"])
            tmpTuple = (self.crntID, content, var_id)
            self.variant.append(tmpTuple)

        elif self.crntElmnt == "freq":
            tmpTuple = (self.crntID, content)
            self.freq.append(tmpTuple)

        elif self.crntElmnt == "rad_name":
            tmpTuple = (self.crntID, content)
            self.rad_name.append(tmpTuple)

        elif self.crntElmnt == "jlpt":
            tmpTuple = (self.crntID, content)
            self.jlpt.append(tmpTuple)

        elif self.crntElmnt == "dic_ref":
            m_vol = self.crntAtrs.get("m_vol")
            m_page = self.crntAtrs.get("m_page")
            dic_id = None
            if self.crntAtrs["dr_type"] not in self.dr_type:
                self.dr_type.append(self.crntAtrs["dr_type"])
                dic_id = self.dr_type.index(self.crntAtrs["dr_type"])
            else:
                dic_id = self.dr_type.index(self.crntAtrs["dr_type"])
            tmpTuple = (self.crntID, content, dic_id, m_vol, m_page)
            self.dic_ref.append(tmpTuple)

        elif self.crntElmnt == "q_code":
            skip_misclass = self.crntAtrs.get("skip_misclass")
            qc_id = None
            if self.crntAtrs["qc_type"] not in self.qc_type:
                self.qc_type.append(self.crntAtrs["qc_type"])
                qc_id = self.qc_type.index(self.crntAtrs["qc_type"])
            else:
                qc_id = self.qc_type.index(self.crntAtrs["qc_type"])
            tmpTuple = (self.crntID, content,qc_id , skip_misclass)
            self.q_code.append(tmpTuple)

        elif self.crntElmnt == "reading":
            r_status = self.crntAtrs.get("r_status")
            rt_id = None
            if self.crntAtrs["r_type"] not in self.r_type:
                self.r_type.append(self.crntAtrs["r_type"])
                rt_id = self.r_type.index(self.crntAtrs["r_type"])
            else:
                rt_id = self.r_type.index(self.crntAtrs["r_type"])
            tmpTuple = (self.crntID, content, rt_id, r_status)
            self.reading.append(tmpTuple)

        elif self.crntElmnt == "meaning":
            lang_id = None
            lang = self.crntAtrs.get("m_lang", "en")
            if lang not in self.m_lang:
                self.m_lang.append(lang)
                lang_id = self.m_lang.index(lang)
            else:
                lang_id = self.m_lang.index(lang)
            tmpTuple = (self.crntID, content, lang_id)
            self.meaning.append(tmpTuple)

        elif self.crntElmnt == "nanori":
            tmpTuple = (self.crntID, content)
            self.nanori.append(tmpTuple)

    def endDocument(self):
        schema_file = open("kanjidic2_schema.sql","r")
        schema = schema_file.read()



        kf = open("kanjidic2_" + self.date_of_creation + ".db","w")
        kf.close()
        connection = sqlite3.connect("kanjidic2_" + self.date_of_creation + ".db" )
        cursor = connection.cursor()
        cursor.executescript(schema)

        cursor.execute("insert into header values (?,?,?,?,?)", (self.file_version, self.database_version, self.date_of_creation, self.date_of_generation, ""))

        cursor.executemany("insert into character values (?,?)", self.character)

        cursor.executemany("insert into	cp_type	values (?,?)", enumerate(self.cp_type))
        cursor.executemany("insert into	cp_value values (?,?,?)", self.cp_value)

        cursor.executemany("insert into	rad_type values (?,?)", enumerate(self.rad_type))
        cursor.executemany("insert into	rad_value values (?,?,?)", self.rad_value)

        cursor.executemany("insert into	grade values (?,?)", self.grade)
        cursor.executemany("insert into	stroke_count values (?,?,?)", self.stroke_count)

        cursor.executemany("insert into	var_type values (?,?)", enumerate(self.var_type))
        cursor.executemany("insert into	variant	values (?,?,?)", self.variant)

        cursor.executemany("insert into	freq	values (?,?)", self.freq)
        cursor.executemany("insert into	jlpt	values (?,?)", self.jlpt)

        cursor.executemany("insert into	dr_type	values (?,?)", enumerate(self.dr_type))
        cursor.executemany("insert into	dic_ref	values (?,?,?,?,?)", self.dic_ref)

        cursor.executemany("insert into	rad_name	values (?,?)", self.rad_name)

        cursor.executemany("insert into	qc_type	values (?,?)", enumerate(self.qc_type))
        cursor.executemany("insert into	q_code	values (?,?,?,?)", self.q_code)

        cursor.executemany("insert into	r_type	values (?,?)", enumerate(self.r_type))
        cursor.executemany("insert into	reading	values (?,?,?,?)", self.reading)

        cursor.executemany("insert into	m_lang	values (?,?)", enumerate(self.m_lang))
        cursor.executemany("insert into	meaning	values (?,?,?)", self.meaning)

        cursor.executemany("insert into	nanori	values (?,?)", self.nanori)


        connection.commit()
        print("Done.")






handler = kanjidicHandler()


import xml.sax
#ff = open("kanjidic2.xml","r")
kf2 = UR.urlretrieve(kanji_dic_link,downloaded_kanjidic_fileName)
kf3 = gzip.open(downloaded_kanjidic_fileName)
xml.sax.make_parser()
xml.sax.parse(kf3, handler)

