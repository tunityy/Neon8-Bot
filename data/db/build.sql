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
	user_id				INTEGER,
    guild_id			INTEGER
);

CREATE TABLE IF NOT EXISTS dynamic_stats (
	user_name			TEXT,
	user_display_name   TEXT,
    utc_timestamp		TEXT,
	local_timestamp		TEXT,
	updateable			TEXT,
	note_title			TEXT,
	note_contents		TEXT,
	user_id				INTEGER,
    guild_id			INTEGER
);