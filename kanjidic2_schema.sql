
--foreign key (house_id) references houses(id),
create table header
    (
    file_version text,
    database_version text,
    date_of_creation text,
    date_of_generation text,
    input_file_name text
    );
    
create table character --mainkanjitable.
	(
	ch_id integer,
	literal text,

	primary key (ch_id, literal)
	);

create table cp_value --encodings.
	(
	ch_id integer,
	cp_value text,
	cp_type_id integer,

	foreign key (ch_id) references character(ch_id),
	foreign key (cp_type_id) references cp_type(cp_type_id),
	primary key (ch_id, cp_value, cp_type_id)
	);

--/meta
create table cp_type --code point type.
	(
	cp_type_id integer,
	cp_type_name text,

	primary key (cp_type_id, cp_type_name)
	);

create table rad_value --bushu or radical number.
	(
	ch_id integer,
	rad_value integer,
	rad_type_id integer,

	foreign key (ch_id) references character(ch_id),
	foreign key (rad_type_id) references rad_type(rad_type_id),
	primary key (ch_id, rad_value, rad_type_id)
	);

--/meta
create table rad_type --KangXi Zidian. or nelson_c.
	(
	rad_type_id integer,
	rad_type_name text,

	primary key (rad_type_id, rad_type_name)
	);

-- start of misc.

create table grade --of elementary school per year.
	(
	ch_id integer,
	grade integer,

	foreign key (ch_id) references character(ch_id),
	primary key (ch_id, grade)
	);

create table stroke_count
	(
	ch_id integer,
	count integer,
	count_no integer, --if zero the most accurate for the same kanji.
	
	foreign key (ch_id) references character(ch_id),
	primary key (ch_id, count, count_no)
	);

create table variant --related kanji characters.
	(
	ch_id integer,
	var_value text,
	var_type_id integer,

	foreign key (ch_id) references character(ch_id),
	foreign key (var_type_id) references var_type(var_type_id),
	primary key (ch_id, var_value, var_type_id)
	);

--/ meta
create table var_type --name of jis 208 jis 212 etc.
	(
	var_type_id integer,
	vartype_name text,

	primary key (var_type_id, vartype_name)
	);

create table freq -- frequancy of usage in nwewspapers.
	(
	ch_id integer,
	freq_value integer,

	foreign key (ch_id) references character(ch_id),
	primary key (ch_id, freq_value)
	);

create table jlpt -- jlpt test level.
	(
	ch_id integer,
	jlpt_level integer,

	foreign key (ch_id) references character(ch_id),
	primary key (ch_id, jlpt_level)
	);

create table rad_name -- name if the kanji itself is used as radical
	(
	ch_id integer,
	rad_name text,

	foreign key (ch_id) references character(ch_id),
	primary key (ch_id, rad_name)
	);

-- end of misc

create table dic_ref
	(
	ch_id integer,
	dic_ref text,
	dr_type_id integer,
	m_volume integer,
	m_page integer,

	foreign key (ch_id) references character(ch_id),
	foreign key (dr_type_id) references dr_type(dr_type_id),	
	primary key (ch_id, dic_ref, dr_type_id, m_volume)
	);

-- / meta
create table dr_type
	(
	dr_type_id integer,
	dr_type_name text,

	primary key (dr_type_id, dr_type_name)
	);

create table q_code
	(
	ch_id integer,
	q_code text,
	qc_type_id integer,
	skip_misclass text,

	foreign key (ch_id) references character(ch_id),
	foreign key (qc_type_id) references qc_type(qc_type_id),	
	primary key (ch_id, q_code, qc_type_id)
	);

-- / meta
create table qc_type
	(
	qc_type_id integer,
	qc_type_name text,

	primary key (qc_type_id, qc_type_name)
	);

create table reading
	(
	ch_id integer,
	reading_value text,
	r_type_id integer,
	r_status texr,

	foreign key (ch_id) references character(ch_id),
	foreign key (r_type_id) references r_type(r_type_id),	
	primary key (ch_id, reading_value, r_type_id)
	);

-- / meta
create table r_type
	(
	r_type_id integer,
	r_type_name text,

	primary key (r_type_id, r_type_name)
	);

create table meaning
	(
	ch_id integer,
	meaning_value text,
	m_lang_id integer,

	foreign key (ch_id) references character(ch_id),
	foreign key (m_lang_id) references m_lang(m_lang_id),	
	primary key (ch_id, meaning_value, m_lang_id)
	);

-- / meta
create table m_lang
	(
	m_lang_id integer,
	m_lang_code_value text,

	primary key (m_lang_id, m_lang_code_value)
	);

create table nanori
	(
	ch_id integer,
	nanori_value text,

	foreign key (ch_id) references character(ch_id)
	primary key (ch_id, nanori_value)
	);
	
create view kanji_finder as

    select 
    character.ch_id as id, 
    character.literal as kanji,
    
    cp_value.cp_value as code,
    cp_type.cp_type_name as code_type,
    
    rad_value.rad_value as radical_number,
    rad_type.rad_type_name as radical_type,
    
    grade.grade as grade,
    stroke_count.count as stroke_count,
    stroke_count.count_no as miscount,
    
    variant.var_value as variant_code,
    var_type.vartype_name as variant_code_type,
    
    freq.freq_value as frequancy,
    jlpt.jlpt_level as jlpt_level,
    
    dic_ref.dic_ref as reference_number,
    dic_ref.m_volume as reference_volume,
    dic_ref.m_page as reference_page,
    dr_type.dr_type_name as reference_name, 
    
    q_code.q_code as query_code,
    q_code.skip_misclass as skip_misclass,
    qc_type.qc_type_name as query_method_name,
    
    reading.reading_value as reading,
    reading.r_status as jouyou_limit,
    r_type.r_type_name as reading_type,
    
    meaning.meaning_value as meaning,
    m_lang.m_lang_code_value as meaning_lang_code,
    
    nanori.nanori_value as nanori_reading,
    
    rad_name.rad_name as radical_name 
    
    from 
    character
    left join cp_value on cp_value.ch_id = character.ch_id
     join cp_type on cp_value.cp_type_id = cp_type.cp_type_id 
    
    left join rad_value on rad_value.ch_id = character.ch_id
     join rad_type on rad_type.rad_type_id = rad_value.rad_type_id 
    
    left join grade on grade.ch_id = character.ch_id
    left join stroke_count on stroke_count.ch_id = character.ch_id
    
    left join variant on variant.ch_id = character.ch_id
     join var_type on var_type.var_type_id = variant.var_type_id
    
    left join freq on freq.ch_id = character.ch_id
    left join jlpt on jlpt.ch_id = character.ch_id
    left join rad_name on rad_name.ch_id = character.ch_id
    
    left join dic_ref on dic_ref.ch_id = character.ch_id
     join dr_type on dr_type.dr_type_id = dic_ref.dr_type_id
    
    left join q_code on q_code.ch_id = character.ch_id
     join qc_type on qc_type.qc_type_id = q_code.qc_type_id

    left join reading on reading.ch_id = character.ch_id
     join r_type on r_type.r_type_id = reading.r_type_id
    
    left join meaning on meaning.ch_id = character.ch_id
     join m_lang on m_lang.m_lang_id = meaning.m_lang_id
    
    left join nanori on nanori.ch_id = character.ch_id





