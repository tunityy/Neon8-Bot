CREATE TABLE IF NOT EXISTS dynamic_stats (
	user_name			TEXT,
	user_display_name   TEXT,
    character_name		TEXT,
	hunger				INTEGER,
	humanity			INTEGER,
	stains				INTEGER,
	current_willpower	INTEGER,
	total_willpower		INTEGER,
	superficial_damage	INTEGER,
	aggravated_damage	INTEGER,
	health				INTEGER,
	user_id				INTEGER,
    guild_id			INTEGER
);

CREATE TABLE notes (
	user_name				TEXT,
	user_display_name		TEXT,
	user_id					INTEGER,
	local_timestamp			TEXT,
	utc_timestamp			TEXT,
	updateable				TEXT,
	note_title				TEXT,
	note_contents			TEXT,
	edited					TEXT,
	edited_by_name			TEXT,
	edited_by_display_name	TEXT,
	edited_by_id			INTEGER,
	edit_local_timestamp	TEXT,
	edit_utc_timestamp		TEXT,
	guild_id				INTEGER
);

CREATE TABLE attributes (
	user_name			TEXT,
	user_display_name	TEXT,
	character_name		TEXT,
	strength			INTEGER,
	dexterity			INTEGER,
	stamina				INTEGER,
	charisma			INTEGER,
	manipulation		INTEGER,
	composure			INTEGER,
	intelligence		INTEGER,
	wits				INTEGER,
	resolve				INTEGER,
	user_id				INTEGER,
	guild_id			INTEGER
);

CREATE TABLE skills (
	user_name				TEXT,
	user_display_name		TEXT,
	character_name			TEXT,
	athletics				INTEGER,
	athletics_specialty		TEXT,
	brawl					INTEGER,
	brawl_specialty			TEXT,
	craft					INTEGER,
	craft_specialty			TEXT,
	drive					INTEGER,
	drive_specialty			TEXT,
	firearms				INTEGER,
	firearms_specialty		TEXT,
	larceny					INTEGER,
	larceny_specialty		TEXT,
	melee					INTEGER,
	melee_specialty			TEXT,
	stealth					INTEGER,
	stealth_specialty		TEXT,
	survival				INTEGER,
	survival_specialty		TEXT,
	animal_ken				INTEGER,
	animal_ken_specialty	TEXT,
	etiquette				INTEGER,
	etiquette_specialty		TEXT,
	insight					INTEGER,
	insight_specialty		TEXT,
	intimidation			INTEGER,
	intimidation_specialty	TEXT,
	leadership				INTEGER,
	leadership_specialty	TEXT,
	performance				INTEGER,
	performance_specialty	TEXT,
	persuasion				INTEGER,
	persuasion_specialty	TEXT,
	streetwise				INTEGER,
	streetwise_specialty	TEXT,
	subterfuge				INTEGER,
	subterfuge_specialty	TEXT,
	academics				INTEGER,
	academics_specialty		TEXT,
	awareness				INTEGER,
	awareness_specialty		TEXT,
	finance					INTEGER,
	finance_specialty		TEXT,
	investigation			INTEGER,
	investigation_specialty	TEXT,
	medicine				INTEGER,
	medicine_specialty		TEXT,
	occult					INTEGER,
	occult_specialty		TEXT,
	politics				INTEGER,
	politics_specialty		TEXT,
	science					INTEGER,
	science_specialty		TEXT,
	technology				INTEGER,
	technology_specialty	TEXT,
	user_id					INTEGER,
	guild_id				INTEGER
);