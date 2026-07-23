-- =====================================================
-- SEED DATA : RSS SOURCES
-- =====================================================

INSERT INTO rss_sources (
    source_name,
    rss_url,
    website_url,
    category,
    status
)

VALUES

(
    'Kompas',
    'https://rss.kompas.com/rss',
    'https://www.kompas.com',
    'General',
    TRUE
),

(
    'CNN Indonesia Nasional',
    'https://www.cnnindonesia.com/nasional/rss',
    'https://www.cnnindonesia.com',
    'Nasional',
    TRUE
),

(
    'CNN Indonesia Ekonomi',
    'https://www.cnnindonesia.com/ekonomi/rss',
    'https://www.cnnindonesia.com',
    'Ekonomi',
    TRUE
),

(
    'CNN Indonesia Teknologi',
    'https://www.cnnindonesia.com/teknologi/rss',
    'https://www.cnnindonesia.com',
    'Teknologi',
    TRUE
),

(
    'Tempo Nasional',
    'https://rss.tempo.co/nasional',
    'https://www.tempo.co',
    'Nasional',
    TRUE
),

(
    'Tempo Bisnis',
    'https://rss.tempo.co/bisnis',
    'https://www.tempo.co',
    'Ekonomi',
    TRUE
),

(
    'Antara',
    'https://www.antaranews.com/rss/terkini.xml',
    'https://www.antaranews.com',
    'General',
    TRUE
);