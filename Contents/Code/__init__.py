#################################################################################
# HTTP Anidb Metadata Agent (HAMA) By ZeroQI, Forked from Atomicstrawberry v0.4 #
#################################################################################

### Global initialisation ################################################################################################################################################
import os, re, time, datetime, string # Functions used per module: os (read), re (sub, match), time (sleep), datetim (datetime).

### Language Priorities ###
SECONDS_BETWEEN_REQUESTS     = 2
SPLIT_CHARS                  = [';', ':', '*', '?', ',', '.', '~', '-', '\\', '/' ] #Space is implied, characters forbidden by os filename limitations
FILTER_CHARS                 = "\\/:*?<>|~-; "
WEB_LINK                     = "<A HREF='%s' target='_blank'>%s</A>"

### These are words which cause extra noise due to being uninteresting for doing searches on ###########################################################################
FILTER_SEARCH_WORDS          = [                                                                                                      # Lowercase only
  'a',  'of', 'an', 'the', 'motion', 'picture', 'special', 'oav', 'ova', 'tv', 'special', 'eternal', 'final', 'last', 'one', 'movie', # En 
  'princess', 'theater',                                                                                                              # En Continued
  'to', 'wa', 'ga', 'no', 'age', 'da', 'chou', 'super', 'yo', 'de', 'chan', 'hime',                                                   # Jp 
  'le', 'la', 'un', 'les', 'nos', 'vos', 'des', 'ses',                                                                                # Fr 
  'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi'                                # Roman digits 
]

### AniDB, TVDB, AniDB mod agent for XBMC XML's, and Plex URL and path variable definition ###########################################################################
ANIDB_TVDB_MAPPING           = 'anime-list-master.xml'                                                     # ScudLee mapping file local
ANIDB_TVDB_MAPPING_URL       = 'http://rawgithub.com/ScudLee/anime-lists/master/anime-list-master.xml'     # ScudLee mapping file url
ANIDB_TVDB_MAPPING_FEEDBACK  = 'http://github.com/ScudLee/anime-lists/issues/new?title=%s&body=%s'         # ScudLee mapping file git feedback url
ANIDB_COLLECTION_MAPPING     = 'anime-movieset-list.xml'                                                   # ScudLee AniDB movies collections XML mapping file
ANIDB_COLLECTION_MAPPING_URL = 'http://rawgithub.com/ScudLee/anime-lists/master/anime-movieset-list.xml'   # ScudLee collection mapping file

ANIDB_ANIME_TITLES           = 'anime-titles.xml'                                                          # AniDB title database decompressed in Hama.bundle\Contents\Resources
ANIDB_ANIME_TITLES_URL       = 'http://anidb.net/api/anime-titles.xml.gz'                                  # AniDB title database file contain all ids, all languages
ANIDB_HTTP_API_URL           = 'http://api.anidb.net:9001/httpapi?request=anime&client=hama&clientver=1&protover=1&aid='
ANIDB_PIC_BASE_URL           = 'http://img7.anidb.net/pics/anime/'                                         # AniDB picture directory
ANIDB_SERIE_URL              = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%s'                    # AniDB link to the anime
ANIDB_SERIE_CACHE            = 'AniDB'                                                                     # AniDB link to the anime
ANIDB_EPISODE_URL            = 'http://anidb.net/perl-bin/animedb.pl?show=ep&eid=%s'                       # AniDB link to the episode
ANIDB_RELATION_URL           = 'http://anidb.net/perl-bin/animedb.pl?show=rel&aid=%s'                      # AniDB link to the relation graph

TVDB_API_KEY                 = 'A27AD9BE0DA63333'                                                          # TVDB API key register URL: http://thetvdb.com/?tab=apiregister
TVDB_HTTP_API_URL            = 'http://thetvdb.com/api/%s/series/%s/all/en.xml'                            # TVDB Serie XML for episodes sumaries for now
TVDB_BANNERS_URL             = 'http://thetvdb.com/api/%s/series/%s/banners.xml'                           # TVDB Serie pictures xml: fanarts, posters, banners   
TVDB_IMAGES_URL              = 'http://thetvdb.com/banners/'                                               # TVDB picture directory
TVDB_SERIE_URL               = 'http://thetvdb.com/?tab=series&id=%s'                                      #
TVDB_SERIE_CACHE             = 'TVDB'                                                                      #
TVDB_SEASON_URL              = 'http://thetvdb.com/?tab=season&seriesid=%s&seasonid=%s'                    #
TVDB_EPISODE_URL             = 'http://thetvdb.com/?tab=episode&seriesid=%s&seasonid=%s&id=%s'             #
TVDB_SEARCH_URL              = 'http://thetvdb.com/?tab=listseries&function=Search&string=%s'              #

TMDB_BASE_URL                = 'https://api.tmdb.org/3/'
TMDB_CONFIG_URL              = TMDB_BASE_URL + 'configuration?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'
TMDB_IMAGES_URL              = TMDB_BASE_URL + 'movie/%s/images?api_key=7f4a0bd0bd3315bb832e17feda70b5cd'
TMDB_SEARCH_URL              = TMDB_BASE_URL + 'search/movie?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&query=%s&year=%s&language=%s&include_adult=%s'
TMDB_SEARCH_URL_BY_IMDBID    = TMDB_BASE_URL + 'find/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&external_source=imdb_id'
TMDB_MOVIE_URL               = TMDB_BASE_URL + 'movie/%s?api_key=7f4a0bd0bd3315bb832e17feda70b5cd&append_to_response=releases,credits&language=%s'
TMDB_ARTWORK_ITEM_LIMIT      = 15
TMDB_SCORE_RATIO             = .3   # How much weight to give ratings vs. vote counts when picking best posters/backdrop. 0 means use only ratings.

OMDB_HTTP_API_URL            = "http://www.omdbapi.com/?i="

THEME_URL                    = 'http://tvthemes.plexapp.com/%s.mp3'                                        # Plex TV Theme url

### List of AniDB category names useful as genre. 1st variable mark 18+ categories. The 2nd variable will actually cause a flag to appear in Plex ####################
RESTRICTED_GENRE_NAMES    = [ '18 Restricted', 'Pornography' ]
RESTRICTED_CONTENT_RATING = "NC-17"
GENRE_NAMES               = [
  ### Audience categories - all useful but not used often ############################################################################################################
  'Josei', 'Kodomo', 'Mina', 'Seinen', 'Shoujo', 'Shounen',
  
  ### Elements - many useful #########################################################################################################################################
  'Action', 'Martial Arts', 'Swordplay', 'Adventure', 'Angst', 'Anthropomorphism', 'Comedy', 'Parody', 'Slapstick', 'Super Deformed', 'Detective', 'Ecchi', 'Fantasy',
  'Contemporary Fantasy', 'Dark Fantasy', 'Ghost', 'High Fantasy', 'Magic', 'Vampire', 'Zombie', 'Harem', 'Reverse Harem', 'Henshin', 'Horror', 'Incest',
  'Mahou Shoujo', 'Pornography', 'Yaoi', 'Yuri', 'Romance', 'Love Polygon', 'Shoujo Ai', 'Shounen Ai', 'Sci-Fi', 'Alien', 'Mecha', 'Space Travel', 'Time Travel', 
  'Thriller', 'Western',                                             
      
  ### Fetishes. Leaving out most porn genres #########################################################################################################################
  'Futanari', 'Lolicon', 'Shotacon', 'Tentacle', 'Trap', 'Reverse Trap',
  
  ### Original Work - mainly useful ##################################################################################################################################
  'Game', 'Action Game', 'Dating Sim - Visual Novel', 'Erotic Game', 'RPG', 'Manga', '4-koma', 'Movie', 'Novel',
  
  ### Setting - most of the places aren't genres, some Time stuff is useful ##########################################################################################
  'Fantasy World', 'Parallel Universe', 'Virtual Reality', 'Hell', 'Space', 'Mars', 'Space Colony', 'Shipboard', 'Alternative Universe', 'Past', 'Present', 'Future',
  'Historical', '1920s', 'Bakumatsu - Meiji Period', 'Edo Period', 'Heian Period', 'Sengoku Period', 'Victorian Period', 'World War I', 'World War II',
  'Alternative Present',
  
  ### Themes - many useful ###########################################################################################################################################
  'Anti-War', 'Art', 'Music', 'Band', 'Idol', 'Photography', 'Christmas', 'Coming of Age', 'Conspiracy', 'Cooking', 'Cosplay', 'Cyberpunk', 'Daily Life', 'Earthquake',
  'Post-War', 'Post-apocalypse', 'War', 'Dystopia', 'Friendship', 'Law and Order', 'Cops', 'Special Squads', 'Military', 'Airforce', 'Feudal Warfare', 'Navy',
  'Politics', 'Proxy Battles', 'Racism', 'Religion', 'School Life', 'All-boys School', 'All-girls School', 'Art School', 'Clubs', 'College', 'Delinquents', 
  'Elementary School', 'High School', 'School Dormitory', 'Student Council', 'Transfer Student', 'Sports', 'Acrobatics', 'Archery', 'Badminton', 'Baseball', 
  'Basketball', 'Board Games', 'Chess', 'Go', 'Mahjong', 'Shougi', 'Combat', 'Boxing', 'Judo', 'Kendo', 'Muay Thai', 'Wrestling', 'Cycling', 'Dodgeball', 'Fishing',
  'Football', 'Golf', 'Gymnastics', 'Horse Riding', 'Ice Skating', 'Inline Skating', 'Motorsport', 'Formula Racing', 'Street Racing', 'Rugby', 'Swimming', 'Tennis',
  'Track and Field', 'Volleyball', 'Steampunk', 'Summer Festival', 'Tragedy', 'Underworld', 'Assassin', 'Bounty Hunter', 'Mafia', 'Yakuza', 'Pirate', 'Terrorist',
  'Thief'
]

### AniDB resources (external links) translation dictionary ###
AniDB_Resources = { "1":["http://www.animenewsnetwork.com/encyclopedia/anime.php?id=%s", "ANN"                ], #
                    "2":["http://myanimelist.net/anime/%s"                             , "MAL"                ], #
                    "3":["http://www.animenfo.com/animetitle,%s,%s,a.html"             , "AnimeNfo"           ], #
                    "4":["%s"                                                          , "Official page (jp)" ], #
                    "5":["%s"                                                          , "Official page (en)" ], #
                    "6":["http://en.wikipedia.org/wiki/%s"                             , "Wiki (en)"          ], #
                    "7":["http://ja.wikipedia.org/wiki/%s"                             , "Wiki (jp)"          ], #
                    "8":["http://cal.syoboi.jp/tid/%s/time"                            , "Schedule"           ], #
                    "9":["http://www.allcinema.net/prog/show_c.php?num_c=%s"           , "Allcinema"          ], #
                   "10":["http://anison.info/data/program/%s.html"                     , "Anison"             ], #
                   "11":["http://lain.gr.jp/%s"                                        , ".lain"              ], #
                   "14":["http://vndb.org/v%s"                                         , "VNDB"               ], #
                   "15":["http://www.anime.marumegane.com/%s.html"                     , "Marumegane"         ], #
                   "19":["http://ko.wikipedia.org/wiki/%s"                             , "Wiki (ko)"          ], #
                   "20":["http://zh.wikipedia.org/wiki/%s"                             , "Wiki (zh)"          ]  #
      } # Analysed the AniDB serie page output and compared to the XML file to extract above values
      
### TheTVDB.com language codes ###
#THETVDB_LANGUAGES_CODE = { 'cs':'28', 'da':'10', 'de':'14', 'el':'20', 'en': '7', 'es':'16', 'fi':'11', 'fr':'17',
#                           'he':'24', 'hu':'19', 'it':'15', 'ja':'25', 'ko':'32', 'nl':'13', 'no': '9', 'pl':'18',
#                           'pt':'26', 'ru':'22', 'sv': '8', 'tr':'21', 'zh': '6' 
#                         } #Not yet used

### Global variables ###
networkLock                  = Thread.Lock() #ValueError if in Start()
lastRequestTime              = None
AniDB_title_tree             = None
AniDB_collection_tree        = None
AniDB_TVDB_mapping_tree      = None

### Pre-Defined Start function #########################################################################################################################################
def Start():
  Log.Debug('### HTTP Anidb Metadata Agent (HAMA) Started ##############################################################################################################')

  msgContainer = ValidatePrefs()
  if msgContainer.header == 'Error': Log("ValidatePrefs - Error")
  else:
    MessageContainer('Success', "HAMA started")
    #global SERIE_LANGUAGE_PRIORITY, EPISODE_LANGUAGE_PRIORITY
    #SERIE_LANGUAGE_PRIORITY   = [ Prefs['SerieLanguage1'], Prefs['SerieLanguage2'], Prefs['SerieLanguage3'] ] #override default language
    #EPISODE_LANGUAGE_PRIORITY = [ Prefs['EpisodeLanguage1'], Prefs['EpisodeLanguage2']                      ] #override default language
  HTTP.CacheTime           = CACHE_1HOUR * 24 * 7  
  global AniDB_title_tree, AniDB_TVDB_mapping_tree, AniDB_collection_tree, networkLock #only this one to make search after start faster
  AniDB_title_tree         = HamaCommonAgent().xmlElementFromFile(ANIDB_ANIME_TITLES      , ANIDB_ANIME_TITLES_URL      ) # AniDB's:   anime-titles.xml
  AniDB_TVDB_mapping_tree  = HamaCommonAgent().xmlElementFromFile(ANIDB_TVDB_MAPPING      , ANIDB_TVDB_MAPPING_URL      ) # ScudLee's: anime-list-master.xml 
  AniDB_collection_tree    = HamaCommonAgent().xmlElementFromFile(ANIDB_COLLECTION_MAPPING, ANIDB_COLLECTION_MAPPING_URL) # ScudLee's: anime-movieset-list.xml 
  
### Pre-Defined ValidatePrefs function Values in "DefaultPrefs.json", accessible in Settings>Tab:Plex Media Server>Sidebar:Agents>Tab:Movies/TV Shows>Tab:HamaTV #######
def ValidatePrefs():
  Log.Info('HAMA - ValidatePrefs initialised')
  result     = 'Success'
  msg        = 'HAMA - Provided preference values are ok'
  log_string = ""
  settings   = ['GetTvdbFanart', 'GetTvdbPosters', 'GetTvdbBanners', 'GetAnidbPoster', 'UseWebLinks', 'MinimumWeight', 'SerieLanguage1', 'SerieLanguage2', 'SerieLanguage3', 'EpisodeLanguage1', 'EpisodeLanguage2']
  for key in settings: #for key, value in enumerate(settings):
    try: temp = Prefs[key]
    except:
      result = 'Error'
      msg    = "Couldn't get values '%s', probably a missing/empty/outdated 'DefaultPrefs.json' so replace it" % key
      Log.Error(msg)
  if result=='Success': Log.Info(msg)
  return MessageContainer(result, msg)

### test all values of list against another, only defined in Python 2.5+ ##################################################################################
def all(iterable):
  for element in iterable: 
    if not element: return False
  return True

### main metadata agent ################################################################################################################################################
class HamaCommonAgent:

  ### Local search ###
  def searchByName(self, results, media, lang, manual, movie):
  
    Log.Debug("=== searchByName - Begin - ================================================================================================")
    origTitle               = ( media.title if movie else media.show )
    year                    = media.year
    SERIE_LANGUAGE_PRIORITY = [ Prefs['SerieLanguage1'].encode('utf-8'), Prefs['SerieLanguage2'].encode('utf-8'), Prefs['SerieLanguage3'].encode('utf-8') ]
    Log("SearchByName (%s,%s,%s,%s) title: %s, filename: %s" % (results, lang, str(media), str(manual), media.name, media.filename ))
    if manual == False: ### Automatic mode ###
      name   = String.Unquote(media.filename)
      path = name.split('/')
      origTitle = path[ len(path)-2 ]
      Log.Debug("SearchByName - Filename: " + path[ len(path)-2 ] )
    if year is not None: origTitle=origTitle+" (%s)" % str(year)
    
    global AniDB_title_tree
    if not AniDB_title_tree:
      Log.Debug( "SearchByName - HAD TO RELOAD AniDB Tree, so not kept in memory ###########" )
      AniDB_title_tree = self.xmlElementFromFile(ANIDB_ANIME_TITLES, ANIDB_ANIME_TITLES_URL)
    
    ### Clear cache manually ###
    if origTitle.startswith("clear-cache"): HTTP.ClearCache()

    ### aid:xxxxx Fetch the exact serie XML form AniDB (Caching it) from the anime-id ###
    origTitle = origTitle.encode('utf-8')
    if origTitle.startswith("aid:"): #NEEDS UTF-8
      Log.Debug( "SearchByName - aid: '%s'" % origTitle )
      aidstring = origTitle.split(':', 2) #str(origTitle[4:])
      aid  = aidstring[1]
      if len(aidstring) == 3:
        langTitle = aidstring[2]
        mainTitle = None
      else: langTitle, mainTitle = self.getMainTitle(AniDB_title_tree.xpath("/animetitles/anime[@aid='%s']/*" % aid), SERIE_LANGUAGE_PRIORITY)
      Log.Debug( "SearchByName - aid: %s, Main title: %s, Title: %s" % (aidstring[1], mainTitle, langTitle) )
      results.Append(MetadataSearchResult(id=aid, name=langTitle, year=year, lang=Locale.Language.English, score=100))
      return 
    
    ### Local exact search ###
    elements      = list(AniDB_title_tree.iterdescendants())
    cleansedTitle = self.cleanse_title (origTitle)
    Log.Debug( "SearchByName - exact search - checking title: " + repr(origTitle) )
    for title in elements:
      if title.get('aid'): aid = title.get('aid')
      elif title.get('type') in ('main', 'official', 'syn', 'short'): #title.get('{http://www.w3.org/XML/1998/namespace}lang') in SERIE_LANGUAGE_PRIORITY or title.get('type') == 'main'):
        if origTitle== title.text or cleansedTitle == self.cleanse_title (title.text):
          Log.Debug("SearchByName: Local exact search - Strict match '%s' matched title: '%s' with aid: %s" % (origTitle, title.text, aid))
          langTitle, mainTitle = self.getMainTitle(title.getparent(), SERIE_LANGUAGE_PRIORITY)
          results.Append(MetadataSearchResult(id=aid, name=langTitle, year=None, lang=Locale.Language.English, score=100))
          return
          
    ### local keyword search ###
    matchedTitles  = [ ]
    matchedWords   = { }
    words          = [ ]
    log_string     = "SearchByName - Keyword search - Matching '%s' with: " % origTitle
    for word in self.splitByChars(origTitle, SPLIT_CHARS):
      word = self.cleanse_title (word)
      if word != "" and word not in FILTER_SEARCH_WORDS and len(word) > 1:
        words.append (word.encode('utf-8'))
        log_string += "'%s', " % word
    Log.Debug(log_string[:-2]) #remove last 2 chars
    if len(words)==0: # or len( self.splitByChars(origTitle, SPLIT_CHARS) )<=1:
      Log.Debug("SearchByName: Local exact search - NO KEYWORD: title: '%s'" % (origTitle))
      return None # No result found
    
    for title in elements:
      if title.get('aid'): aid = title.get('aid')
      elif title.get('{http://www.w3.org/XML/1998/namespace}lang') in SERIE_LANGUAGE_PRIORITY or title.get('type')=='main':
        sample = self.cleanse_title (title.text)
        sample = sample.encode('utf-8')
        for word in words:
          if word in sample:
            index  = len(matchedTitles)-1
            if index >=0 and matchedTitles[index][0] == aid:
              if title.get('type') == 'main':               matchedTitles[index][1] = title.text #aid.zfill(5) + ' ' + title.text
              if not title.text in matchedTitles[index][2]: matchedTitles[index][2].append(title.text)
            else:
              matchedTitles.append([aid, title.text, [title.text] ]) #aid.zfill(5) + ' ' + title.text
              if word in matchedWords: matchedWords[word].append(sample)
              else:                    matchedWords[word]= [sample]
    log_string="SearchByName - Keywords: "
    for key, value in matchedWords.iteritems(): log_string += key + " (" + str(len(value)) + "), "
    Log.Debug(log_string)  
    if len(matchedTitles)==0: return None

    ### calculate scores + Buid results ###
    log_string = "searchByName - similarity with '%s': " % origTitle 
    for match in matchedTitles:
      scores = []                                                                             
      for title in match[2]: # Calculate distance without space and characters
        a = self.cleanse_title(title)
        b = cleansedTitle
        score = int(100 - (100*float(Util.LevenshteinDistance(a,b)) / float(max(len(a),len(b))) )) #To-Do: LongestCommonSubstring(first, second). use that?
        scores.append(score)              
      bestScore = max(scores)
      results.Append(MetadataSearchResult(id=match[0], name=match[1], year=year, lang=Locale.Language.English, score=bestScore))
      log_string += match[1] + " (%s%%), " % '{:>2}'.format(str(bestScore))
    Log.Debug(log_string)
    results.Sort('score', descending=True)
    Log.Debug("=== searchByName - End - =================================================================================================")
	
  ### Parse the AniDB anime title XML ##################################################################################################################################
  def parseAniDBXml(self, metadata, media, lang, force, movie):
  
    getElementText  = lambda el, xp : el.xpath(xp)[0].text if el.xpath(xp) and el.xpath(xp)[0].text else ""  # helper for getting text from XML element
    GetAnidbPoster  = Prefs['GetAnidbPoster']
    GetTvdbPosters  = Prefs['GetTvdbPosters'   ]
    GetTvdbFanart   = Prefs['GetTvdbFanart'    ]
    GetTvdbBanners  = Prefs['GetTvdbBanners'   ]
    UseWebLinks     = Prefs['UseWebLinks'      ]
    MinimumWeight   = Prefs['MinimumWeight'    ]
    SERIE_LANGUAGE_PRIORITY   = [ Prefs['SerieLanguage1'].encode('utf-8'), Prefs['SerieLanguage2'].encode('utf-8'), Prefs['SerieLanguage3'].encode('utf-8') ] #override default language
    EPISODE_LANGUAGE_PRIORITY = [ Prefs['EpisodeLanguage1'].encode('utf-8'), Prefs['EpisodeLanguage2'].encode('utf-8') ] #override default language
    error_log                 = { 'AniDB posters missing':   [], 'TVDB posters missing':   [], 'anime-list anidbid missing': [], 
                                  'AniDB summaries missing': [], 'TVDB summaries missing': [], 'anime-list tvdbid missing':  [], 'anime-list studio logos': [], 'Plex themes missing': [], 'Missing episodes': [] }
    global AniDB_title_tree, AniDB_TVDB_mapping_tree, AniDB_collection_tree
    
    Log.Debug('--- Begin -------------------------------------------------------------------------------------------')
    Log.Debug("parseAniDBXml (%s, %s, %s)" % (metadata, media, force) )

    ### AniDB Serie MXL ###
    Log.Debug("parseAniDBXml - AniDB Serie XML: " + ANIDB_HTTP_API_URL + metadata.id + ", " + ANIDB_SERIE_CACHE +"/"+metadata.id+".xml" )
    try:    anime = self.urlLoadXml( ANIDB_HTTP_API_URL + metadata.id, ANIDB_SERIE_CACHE +"/"+metadata.id+".xml" ).xpath('/anime')[0]          # Put AniDB serie xml (cached if able) into 'anime'
    except: 
      Log.Debug("parseAniDBXml - AniDB Serie XML: Exception raised" )
      raise ValueError
    else:  Log.Debug("parseAniDBXml - AniDB Serie XML: Loaded OK" )
     
    ### AniDB Movie setting ### 
    movie2 = (True if getElementText(anime, 'type')=='Movie' else False)
    # if movie and not movie2:   #metadata = TV_Serie ???? #Load metadata for TV shows instead of selected Movie    category. Can it be done (ie do like the tv show folder setting was selected)
    # elif not movie and movie2: #metadata = Movie ????    #Load metadata for Movies   instead of selected TV_Serie category. Can it be done (ie do like the movie   folder setting was selected)
      
    ### AniDB Title ###
    try:     title, orig = self.getMainTitle(anime.xpath('/anime/titles/title'), SERIE_LANGUAGE_PRIORITY)
    except:  Log.Debug("parseAniDBXml - AniDB Title: Exception raised" )
    else:
      title=title.encode("utf-8")
      orig =orig.encode("utf-8")
      if title != "" and title == str(metadata.title):
        Log.Debug("parseAniDBXml - AniDB title need no change: '%s' original title: '%s' metadata.title '%s'" % (title, orig, metadata.title) )
        metadata.title = title #why anidbid stays in front
      else:
        metadata.title = title
        if movie and orig != "" and orig != metadata.original_title: metadata.original_title = orig # If it's a movie, Update original title in metadata http://forums.plexapp.com/index.php/topic/25584-setting-metadata-original-title-and-sort-title-still-not-possible/
        Log.Debug("parseAniDBXml - AniDB title changed: '%s' original title: '%s'" % (title, orig) )

    ### AniDB Start Date ###
    startdate  = getElementText(anime, 'startdate')
    if startdate == "":                                                            Log.Debug("parseAniDBXml - AniDB Start Date: None")
    elif metadata.originally_available_at == Datetime.ParseDate(startdate).date(): Log.Debug("parseAniDBXml - AniDB Start Date: " + str(metadata.originally_available_at) + "*")
    else:
      metadata.originally_available_at = Datetime.ParseDate(startdate).date()
      if movie: metadata.year          = metadata.originally_available_at.year
      Log.Debug("parseAniDBXml - AniDB Start Date: " + str(metadata.originally_available_at))
    
    ### AniDB Ratings ###
    rating = getElementText(anime, 'ratings/permanent')
    if rating == "":                       Log.Debug("parseAniDBXml - AniDB Ratings: None")
    elif float(rating) == metadata.rating: Log.Debug("parseAniDBXml - AniDB Ratings: " + str(float(rating)) + "*")
    else: 
      metadata.rating = float(rating)
      Log.Debug("parseAniDBXml - AniDB Ratings: " + str(float(rating)))
    
    ### AniDB Genres ###
    genres = {}
    for category in anime.xpath('categories/category'):
      name   = getElementText(category, 'name')
      weight = category.get('weight')
      if name in GENRE_NAMES and weight >= MinimumWeight: genres [ name ] = int(weight)
      if name in RESTRICTED_GENRE_NAMES and metadata.content_rating != RESTRICTED_CONTENT_RATING: metadata.content_rating = RESTRICTED_CONTENT_RATING
    sortedGenres = sorted(genres.items(), key=lambda x: x[1],  reverse=True)
    log_string   = "AniDB Genres (Weight): "
    genres = []
    for genre in sortedGenres: genres.append(genre[0].encode("utf-8") ) 
    if all(x in metadata.genres for x in genres): Log.Debug(log_string+str(sortedGenres)+"*") #set(sortedGenres).issubset(set(metadata.genres)):
    else:
      Log.Debug("parseAniDBXml - genres: " + str( sortedGenres) + " " + str(genres))
      metadata.genres.clear()
      for genre in sortedGenres:
        metadata.genres.add(genre[0])
        log_string += "%s (%s) " % (genre[0], str(genre[1]))
      Log.Debug(log_string)
    
    ### AniDB Collections ###
    self.anidbCollectionMapping(metadata, anime)
    
    ### AniDB Creator data -  Aside from the animation studio, none of this maps to Series entries, so save it for episodes ###
    studio          = ""
    metadata.studio = ""
    if movie:
      metadata.writers.clear()
      metadata.producers.clear()
      metadata.directors.clear()
    else:
      writers   = []
      directors = []
      producers = []
    
    log_string = "AniDB Creator data: " 
    for creator in anime.xpath('creators/name'):
      nameType = creator.get('type')
      if nameType == "Animation Work": ### Studio ###
        studio = creator.text
        if studio != metadata.studio: metadata.studio = creator.text
        log_string += "Studio: %s, " % creator.text
    
      if "Direction" in nameType:
        if movie: metadata.directors.add(creator.text)
        else:     directors.append(creator.text)
        log_string += "%s is director, " % creator.text
        
      if nameType == "Series Composition":
        if movie: metadata.producers.add(creator.text)
        else:     producers.append(creator.text)
        log_string += "%s is producer, " % creator.text
        
      if nameType == "Original Work" or "Script" in nameType or "Screenplay" in nameType:
        if movie: metadata.writers.add(creator.text)
        else:     writers.append(creator.text)
        log_string += "%s is writer, " % creator.text
    Log.Debug(log_string)

    ### TVDB get id (+etc...) through mapping file ###
    Log.Debug("parseAniDBXml - parseAniDBXml - TVDB - AniDB-TVDB mapping file")
    tvdbid, tmdbid, imdbid, defaulttvdbseason, mappingList, mapping_studio = self.anidbTvdbMapping(metadata, error_log, studio) ### tvdb id ###
    #if not defaulttvdbseason defaulttvdbseason = "1"
    Log.Debug("parseAniDBXml - TVDB - defaulttvdbseason: " + defaulttvdbseason)
    tvdbSummary      = {}
    tvdbposternumber = 0

    ### Movie posters ###
    if imdbid.isalnum():
      self.getImagesFromTMDBbyIMDBID(metadata, imdbid, 99)  #The Movie Database is least prefered by the mapping file, only when imdbid missing
      self.getImagesFromOMDB        (metadata, imdbid, 99)  #IMDB has a single poster, downloading through OMDB xml, prefered by mapping file
    elif tmdbid.isdigit():
      self.getImagesFromTMDB        (metadata, tmdbid, 99)  #The Movie Database is least prefered by the mapping file, only when imdbid missing
    else:  Log.Debug("parseAniDBXml - No IMDB nor TMDB id in mapping file")

    if tvdbid.isdigit():
    
      ### TVDB - Fanart, Poster and Banner ###
      if GetTvdbPosters or GetTvdbFanart or GetTvdbBanners:
        tvdbposternumber = self.getImagesFromTVDB(metadata, media, tvdbid, movie, defaulttvdbseason)
        if tvdbposternumber == 0:  error_log['TVDB posters missing'].append(WEB_LINK % (TVDB_SERIE_URL % tvdbid, title))
     
      ### TVDB - Load serie XML ###
      Log.Debug("parseAniDBXml - TVDB - loading serie xml: " + tvdbid)
      try:     tvdbanime = self.urlLoadXml( TVDB_HTTP_API_URL % (TVDB_API_KEY, tvdbid), TVDB_SERIE_CACHE+"/"+tvdbid+".xml" ).xpath('/Data')[0]
      except:  tvdbanime = None
      else:
        tvdbtitle = getElementText(tvdbanime, 'Series/SeriesName')
        Log.Debug("parseAniDBXml - TVDB - loaded serie xml: " + tvdbid + " " + tvdbtitle)
      
        ### TVDB - Build 'tvdbSummary' table ###
        Log.Debug("parseAniDBXml - TVDB - Build 'tvdbSummary' table")
        summary_missing = []
        summary_present = []
        for episode in tvdbanime.xpath('Episode'):
          seasonid        = getElementText(episode, 'seasonid'       )
          SeasonNumber    = getElementText(episode, 'SeasonNumber'   )
          EpisodeNumber   = getElementText(episode, 'EpisodeNumber'  )
          EpisodeName     = getElementText(episode, 'EpisodeName'    )
          Overview        = getElementText(episode, 'Overview'       )
          absolute_number = getElementText(episode, 'absolute_number')
          id              = getElementText(episode, 'id'             )
          numbering       = " s" + SeasonNumber + "e" + EpisodeNumber
          episodeWarning  = ""
          if Overview=="":
            error_log['AniDB summaries missing'].append(WEB_LINK % (ANIDB_SERIE_URL % metadata.id, metadata.id))
            summary_missing.append(numbering)
          else: summary_present.append(numbering)
          if UseWebLinks: Overview = WEB_LINK % (TVDB_EPISODE_URL%(tvdbid, seasonid, id), "TVDB") + " " + Overview
            # ("" if Overview=="" else "Episode Overview Empty\n")
            #WEB_LINK % (TVDB_SERIE_URL  %(tvdbid              ),  "TVDB"            ) + " > " + WEB_LINK % (TVDB_SEASON_URL %(tvdbid, seasonid    ), "Season "+SeasonNumber) + " > "
          tvdbSummary [ (numbering if absolute_number=="" else "s"+SeasonNumber+"e"+absolute_number) ] = Overview
        Log.Debug("parseAniDBXml - TVDB - Build 'tvdbSummary' table:" + str(sorted(summary_present)) ) #Log.Debug("TVDB - Episodes without Summary: " + str(sorted(summary_missing)) )
      
      ### Plex - Plex Theme song - https://plexapp.zendesk.com/hc/en-us/articles/201178657-Current-TV-Themes ###
      # if in current folder, or the parent one /  url = local / elif  in common theme song folder / try language priority / try root of common theme song folder / try remote server
      #if filename in metadata.themes:  Log.Debug("parseAniDBXml - Theme song - already added from local copy")
      url = THEME_URL % tvdbid
      if    url in metadata.themes:  Log.Debug("parseAniDBXml - Theme song - already added")
      else:
        filename = "Plex/%s.mp3" % metadata.id
        if Data.Exists(filename):
          Log.Debug("parseAniDBXml - Theme song - not added but present locally: adding it from local file")
          theme_song = Data.Load(filename)
          metadata.themes[filename] = Proxy.Media(theme_song)
        elif Prefs['GetPlexThemes']:
          if self.http_status_code(THEME_URL % tvdbid) == 200:
            try:                  theme_song = HTTP.Request(url, cacheTime=None)
            except Exception, e:  Log.Debug("parseAniDBXml - Theme song - not added previously and not present locally but on Plex servers, however download failed: %s" % url)
            else:
              Log.Debug("parseAniDBXml - Theme song - not added previously and not present locally but on Plex servers, and download suceeded: %s" % url)
              try:     Data.Save(filename, theme_song)
              except:  Log.Debug("parseAniDBXml - Plugin Data Folder not created, no local cache")
              metadata.themes[url] = Proxy.Media(theme_song)
          else:
            Log.Debug("parseAniDBXml - Theme song - Theme song not present on Plex servers for tvdbid: %s" % tvdbid)
            try:     tvdb_title = getElementText(tvdbanime, '/Data/Series/SeriesName')
            except:
              tvdb_title= "title error, Not in serie XML"
              error_log ['anime-list tvdbid missing'].append("anidbid: %s, title: '%s', tvdbid: %s, Not in serie XML, %s" % (metadata.id.zfill(5), orig, tvdbid.zfill(5), WEB_LINK % (TVDB_SERIE_URL % tvdbid, "TVDB") ) )
            error_log   ['Plex themes missing'      ].append("anidbid: %s, title: '%s', tvdbid: %s, title: '%s' <a href='mailto:themes@plexapp.com?cc=&subject=Missing%%20theme%%20song%%20-%%20&#39;%s%%20-%%20%s.mp3&#39;'>Upload</a>" % (metadata.id.zfill(5), orig, tvdbid.zfill(5), tvdb_title, tvdb_title, tvdbid) )
    
    ### AniDB Posters ###
    Log.Debug("parseAniDBXml - AniDB Poster")
    if getElementText(anime, 'picture') == "": error_log['AniDB posters missing'].append(WEB_LINK % (ANIDB_SERIE_URL % metadata.id, metadata.id) + "" + metadata.title)
    elif GetAnidbPoster: # or tvdbposternumber == 0:
      bannerRealUrl = ANIDB_PIC_BASE_URL + getElementText(anime, 'picture');
      if not bannerRealUrl in metadata.posters:
        filename = "AniDB/%s" % getElementText(anime, 'picture')
        if Data.Exists(filename):  poster = Data.Load(filename)
        else:
          poster = HTTP.Request(bannerRealUrl, cacheTime=None).content
          try: Data.Save(filename, poster)
          except:  Log.Debug("parseAniDBXml - Plugin Data Folder not created, no local cache")
        try:    metadata.posters[ bannerRealUrl ] = Proxy.Media(poster, sort_order=99) # metadata.posters[ bannerRealUrl ] = Proxy.Media(HTTP.Request(bannerRealUrl, cacheTime=None).content, sort_order=99)
        except: Log.Debug("parseAniDBXml - Picture adding issue")
      
    ### AniDB Serie/Movie description + link ###
    Log.Debug("parseAniDBXml - AniDB description + link")
    description = ""
    try:                  description = re.sub(r'http://anidb\.net/[a-z]{2}[0-9]+ \[(.+?)\]', r'\1', getElementText(anime, 'description')) + "\n" # Remove wiki-style links to staff, characters etc
    except Exception, e:  Log.Debug("Exception: " + str(e))
    else:
      if description == "": error_log['AniDB summaries missing'].append(WEB_LINK % (ANIDB_SERIE_URL % metadata.id, metadata.id) + " " + metadata.title) 
    if UseWebLinks:
      Log.Debug("parseAniDBXml - AniDB - TVDB - ANN links") 
      description += "\nAniDB.net: " +                      WEB_LINK % (ANIDB_SERIE_URL    % metadata.id, "serie page"    ) +" - "
      description +=                                        WEB_LINK % (ANIDB_RELATION_URL % metadata.id, "relation graph") +"\n"
      if tvdbid.isdigit(): description += "TheTVDB.com: " + WEB_LINK % (TVDB_SERIE_URL     % tvdbid,      "serie page"    ) +"\n"
      try: #works but uses all length of the description field (html code takes more length than displayed chars)
        ann_id       = anime.xpath("resources/resource[@type='1']/externalentity/identifier")[0].text
        description += "AnimeNewsNetwork.com: " + WEB_LINK % (AniDB_Resources["1"][0] % ann_id, "serie page") +"\n"
      except: Log.Debug("parseAniDBXml - AniDB description + link exception")
    metadata.summary = description
    
    if not movie: ### TV Serie specific #################################################################################################################
      numEpisodes   = 0
      totalDuration = 0
      mapped_eps    = []
      missing_eps   = []
      specials = {'S': [0, 'Special'], 'C': [100, 'Opening/Ending'], 'T': [200, 'Trailer'], 'P': [300, 'Parody'], 'O': [400, 'Other']}
      for episode in anime.xpath('episodes/episode'):   ### Episode Specific ###########################################################################################

        eid         = episode.get('id')
        epNum       = episode.xpath('epno')[0]
        epNumType   = epNum.get('type') 
        season      = ("1" if epNumType == "1" else "0" ) #Type 1 Episodes 2 Specials 3 C (Openings, Endings) 4 Trailers
        epNumVal    = (epNum.text if epNumType == "1" else str( int(epNum.text[1:]) + specials[ epNum.text[0] ][0] ) )

        if not (season in media.seasons and epNumVal in media.seasons[season].episodes):
          Log.Debug("parseAniDBXml - Season: '%s', Episode: '%s' => '%s' not on disk" % (season, epNum.text, epNumVal) )
          if epNumType == "1": missing_eps.append(" s" + season + "e" + epNumVal )
          continue                                                                         
        Log.Debug("parseAniDBXml - Season: '%s', Episode: '%s' => '%s' Present on disk" % (season, epNum.text, epNumVal))
        episodeObj = metadata.seasons[season].episodes[epNumVal]
        Log.Debug("parseAniDBXml - Season end")
        #if season not in metadata.seasons
        
        ### AniDB Writers, Producers, Directors ###
        if not all(x in writers for x in episodeObj.writers):
          episodeObj.writers.clear()
          for writer in writers: episodeObj.writers.add(writer)
        if not all(x in producers for x in episodeObj.producers):
          episodeObj.producers.clear()
          for producer in producers: episodeObj.producers.add(producer)
        if all(x in directors for x in episodeObj.directors):
          episodeObj.directors.clear()
          for director in directors: episodeObj.directors.add(director)
          
        try:    rating = getElementText(episode, 'rating')
        except: pass
        else:
          if rating != "" and rating != episodeObj.rating:
            Log.Debug("parseAniDBXml - Rating: '%s'" % str( float(rating) ) )
            episodeObj.rating = float(rating)
          else: Log.Debug("parseAniDBXml - Rating: '%s'*" % str( float(rating) ) )
        
        ### AniDBN turn the YYYY-MM-DD airdate in each episode into a Date ###
        airdate = getElementText(episode, 'airdate')
        if airdate != "":
          match = re.match("([1-2][0-9]{3})-([0-1][0-9])-([0-3][0-9])", airdate)
          if match:
            try:   episodeObj.originally_available_at = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError, e: Log.Debug("parseAniDBXml - AniDB parseAirDate - Date out of range: " + str(e))

        ### AniDB Get the correct episode title ###
        Log.Debug("parseAniDBXml - Ep title:" )
        ep_title, main = self.getMainTitle (episode.xpath('title'), EPISODE_LANGUAGE_PRIORITY)
        Log.Debug("parseAniDBXml - Ep title:" )
        if ep_title == "": 
          episodeObj.title = specials[ epNum.text[0] ][1] + ' ' + epNum.text[1:] #on one line?
        elif ep_title != episodeObj.title:
            Log.Debug("parseAniDBXml - Ep title: '%s'" % ep_title )
            episodeObj.title = ep_title
        else: Log.Debug("parseAniDBXml - Ep title: '%s' *" % ep_title )
        
        ### TVDB mapping episode summary ###
        anidb_ep = 's' + season + 'e' + epNumVal
        tvdb_ep  = ""
        summary  = ""
        if tvdbid.isdigit():
          if anidb_ep in mappingList and mappingList[anidb_ep] in tvdbSummary: tvdb_ep = mappingList [ anidb_ep ]
          elif defaulttvdbseason=="a" and anidb_ep in tvdbSummary:             tvdb_ep = anidb_ep
          elif "s"+defaulttvdbseason+"e"+str(epNumVal) in tvdbSummary:    tvdb_ep = "s"+defaulttvdbseason+"e"+str(epNumVal)
          if not tvdb_ep == "": 
            summary = ( tvdbSummary [ tvdb_ep ] if tvdb_ep != None else "" )
            mapped_eps.append( anidb_ep + ">" + tvdb_ep ) #if tvdb_ep != anidb_ep: # Because if there is specific no mapping to be done, no point seeing the logs
        if UseWebLinks:  summary = WEB_LINK % (ANIDB_EPISODE_URL % eid, "AniDB") + " " + summary
        episodeObj.summary = summary

        ### AniDB Duration ###
        duration = getElementText(episode, 'length')
        if duration != "":
          episodeObj.duration = int(duration) * 1000 * 60 # Plex save duration in millisecs, AniDB stores it in minutes
          if season == "1":
            numEpisodes   += 1
            totalDuration += episodeObj.duration
      
      if len(missing_eps)>0:  error_log['Missing episodes'].append("anidbid: %s, Title: '%s', Missing Episodes: %s" % (metadata.id.zfill(5), title, missing_eps))
      convert      = lambda text: int(text) if text.isdigit() else text 
      alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    
      ### AniDB Final post-episode titles cleanup ###
      Log.Debug("parseAniDBXml - DURATION: %s, numEpisodes: %s" %(totalDuration, numEpisodes) )
      if numEpisodes: metadata.duration = int(totalDuration) / int(numEpisodes) #if movie getting scrapped as episode number by scanner...

    ### HAMA - Load logs, add non-present entried then Write log files to Plug-in /Support/Data/com.plexapp.agents.hama/DataItems ### 
    for log in error_log:
      if error_log[log] != []:
        if not Data.Exists(log+".htm"): 
          string=""
          if log == 'TVDB posters missing': string = WEB_LINK % ("http://thetvdb.com/wiki/index.php/Posters",              "Restrictions") + "<BR />\n"
          if log == 'Plex themes missing':  string = WEB_LINK % ("https://plexapp.zendesk.com/hc/en-us/articles/201572843","Restrictions") + "<BR />\n"
        else:                               string = Data.Load(log+".htm")
        for entry in error_log[log]:  
          if entry not in string:  Data.Save(log+".htm", string + entry + "<BR />\r\n")
    Log.Debug('--- end -------------------------------------------------------------------------------------------------')

  ### Get the tvdbId from the AnimeId #######################################################################################################################
  def anidbTvdbMapping(self, metadata, error_log, studio):
    
    mappingList    = {}
    mapping_studio = ""
    global AniDB_TVDB_mapping_tree
    if not AniDB_TVDB_mapping_tree: AniDB_TVDB_mapping_tree = self.xmlElementFromFile(ANIDB_TVDB_MAPPING, ANIDB_TVDB_MAPPING_URL) # Load XML file

    for anime in AniDB_TVDB_mapping_tree.iterchildren('anime'):
      if metadata.id == anime.get("anidbid"):
        tvdbid            = anime.get('tvdbid')            
        tmdbid            = anime.get('tmdbid')
        imdbid            = anime.get('imdbid')
        defaulttvdbseason = anime.get('defaulttvdbseason')
        try:    name      = anime.xpath("name")[0].text
        except: name      = ""
        
        if not tvdbid.isdigit():
          if tvdbid=="" or tvdbid=="unknown":
            error_log ['anime-list tvdbid missing'].append("anidbid: %s title: '%s' has no matching tvdbid ('%s') in mapping file" % (metadata.id.zfill(5), name, tvdbid) + \
            WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:%s &#39;%s&#39; tvdbid:" % (metadata.id, name), String.StripTags( XML.StringFromElement(anime, encoding='utf8')) ), "Submit bug report") )
            Log("anidbTvdbMapping - Missing tvdbid for anidbid %s" % metadata.id);
            # Semi-colon, %0A Line Feed, %09 Tab or ('	'), ```  code block # #xml.etree.ElementTree.tostring
            #dict = {';':"%3B", '\n':"%0A", '	':"%09"} for item in dict: temp.replace(item, list[item]) description += temp
        else:
          try: ### mapping list ###
            for season in anime.iterchildren('mapping-list'):
              for string in season.text.split(';'):
                if string=="": continue
                eps = string.split('-')
                mappingList [ 's' + season.get("anidbseason") + 'e' + eps[0] ] = 's' + season.get("tvdbseason") + 'e' + eps[1]   #save mapping in the format s1e123
          except: mappingList = {}

        try:    mapping_studio  = anime.xpath("supplemental-info/studio")[0].text
        except: mapping_studio  = ""
        else:   metadata.studio = mapping_studio
        if studio + mapping_studio == "":           error_log['anime-list studio logos'].append("Aid: %s '%s' AniDB and anime-list are both missing the studio" % (metadata.id.zfill(5), name) )
        elif studio != "" and mapping_studio != "": error_log['anime-list studio logos'].append("Aid: %s '%s' AniDB have studio '%s' and XML have '%s'"         % (metadata.id.zfill(5), name, studio, mapping_studio) + \
          WEB_LINK % (ANIDB_TVDB_MAPPING_FEEDBACK % ("aid:%s &#39;%s&#39; tvdbid:" % (metadata.id, name), String.StripTags( XML.StringFromElement(anime, encoding='utf8')) ), "Submit bug report (need GIT account)"))
         
        Log.Debug("parseAniDBXml - AniDB-TVDB Mapping - anidb:%s tvbdid: %s studio: %s defaulttvdbseason: %s" % (metadata.id, tvdbid, mapping_studio, str(defaulttvdbseason)) )
        return tvdbid, tmdbid, imdbid, defaulttvdbseason, mappingList, mapping_studio

    error_log['anime-list anidbid missing'].append("anidbid: " + metadata.id.zfill(5))
    Log.Debug('anidbTvdbMapping('+metadata.id+') found no matching anidbid...')
    return "", "",[], ""

  ### AniDB collection mapping #######################################################################################################################
  def anidbCollectionMapping(self, metadata, anime):

    SERIE_LANGUAGE_PRIORITY   = [ Prefs['SerieLanguage1'].encode('utf-8'), Prefs['SerieLanguage2'].encode('utf-8'), Prefs['SerieLanguage3'].encode('utf-8') ] #override default language
    global AniDB_collection_tree
    if not AniDB_collection_tree: AniDB_collection_tree = self.xmlElementFromFile(ANIDB_COLLECTION_MAPPING, ANIDB_COLLECTION_MAPPING_URL)

    ### AniDB related anime List creation ###
    related_anime_list = []
    for relatedAnime in anime.xpath('/anime/relatedanime/anime'): related_anime_list.append(relatedAnime.get('id')) #type  = relatedAnime.get('type') #title = relatedAnime.text
    Log.Debug("anidbCollectionMapping - related_anime_list: " + str(related_anime_list))

    ### AniDB search in collection XML ###
    for element in AniDB_collection_tree.iter("anime"):
      anidbid = element.get('anidbid')
      title   = element.text
      if anidbid == metadata.id or anidbid in related_anime_list:
        set         = element.getparent()
        title, main = self.getMainTitle(set.xpath('titles')[0], SERIE_LANGUAGE_PRIORITY)
        metadata.collections.add(title) #metadata.collections.clear()
        Log.Debug('anidbCollectionMapping - anidbid (%s) is part of collection: %s' % (metadata.id, title) )
        return True

    Log.Debug('anidbCollectionMapping - anidbid is not part of any collection:' )
    return False

  ### [banners.xml] Attempt to get the TVDB's image data ###############################################################################################################
  def getImagesFromTVDB(self, metadata, media, tvdbid, movie, defaulttvdbseason=1):
    GetAnidbPoster = Prefs['GetAnidbPoster'];
    GetTvdbPosters = Prefs['GetTvdbPosters'];
    GetTvdbFanart  = Prefs['GetTvdbFanart' ];
    GetTvdbBanners = Prefs['GetTvdbBanners'];
    #getElementText    = lambda el, xp : el.xpath(xp)[0].text if el.xpath(xp) and el.xpath(xp)[0].text else ""  # helper for getting text from XML element

    try:     bannersXml = XML.ElementFromURL( TVDB_BANNERS_URL % (TVDB_API_KEY, tvdbid), cacheTime=CACHE_1HOUR * 24 * 7 * 30) # don't bother with the full zip, all we need is the banners 
    except:  return
    else:    Log.Debug("getImagesFromTVDB - Loading XML: " + TVDB_BANNERS_URL % (TVDB_API_KEY, tvdbid))
    
    num        = 0
    posternum  = 0
    log_string = ""
    for banner in bannersXml.xpath('Banner'):
      num += 1
      Language       = banner.xpath('Language'   )[0].text      #if Language not in ['en', 'jp']: continue #might add selected title languages in that
      id             = banner.xpath('id'         )[0].text
      bannerType     = banner.xpath('BannerType' )[0].text
      bannerType2    = banner.xpath('BannerType2')[0].text
      bannerPath     = banner.xpath('BannerPath' )[0].text
      rating         =(banner.xpath('Rating'     )[0].text if banner.xpath('Rating') else "")
      season         =(banner.xpath('Season'     )[0].text if banner.xpath('season') else "")

      if movie and not bannerType in ('fanart', 'poster'):
        #Log.Debug("getImagesFromTVDB - skipping banner as it's a movie and not fanart or poster: " + id)
        continue
      if season and not defaulttvdbseason == season:
        #Log.Debug("getImagesFromTVDB - skipping season poster as not defaulttvdbseason so wrong season: " + id)
        continue
      if not movie and not season in metadata.seasons: season = "1"
      proxyFunc      =(Proxy.Preview if bannerType=='fanart' else Proxy.Media)
      bannerRealUrl  = TVDB_IMAGES_URL + bannerPath
      bannerThumbUrl = TVDB_IMAGES_URL + (banner.xpath('ThumbnailPath')[0].text if bannerType=='fanart' else bannerPath)
      metaType       = (metadata.art                     if bannerType=='fanart' else \
                        metadata.posters                 if bannerType=='poster' else \
                        metadata.banners                 if bannerType=='series' or  bannerType2=='seasonwide' else \
                        metadata.seasons[season].posters if bannerType=='season' and bannerType2=='season'     else None)
      if bannerType == 'poster':
        posternum += 1
        log_string += id + ", " 
      if GetTvdbFanart  and   bannerType == 'fanart' or \
         GetTvdbPosters and ( bannerType == 'poster' or bannerType2 == 'season' and not movie ) or \
         GetTvdbBanners and not movie and ( bannerType == 'series' or bannerType2 == 'seasonwide'):
        if not bannerRealUrl in metaType:
          filename = "TVDB/" + bannerPath
          if Data.Exists(filename):
            Log.Debug("getImagesFromTVDB - Loading locally: " + filename)
            poster = Data.Load(filename)
          else:
            try:     poster = HTTP.Request(bannerThumbUrl, cacheTime=None).content
            except:  Log.Debug('getImagesFromTVDB - error downloading banner url1: %s, url2: %s' % (bannerRealUrl, bannerThumbUrl))
            else:
              Log.Debug("getImagesFromTVDB - adding url: " + bannerRealUrl)
              try:             Data.Save(filename, poster)
              except IOError:  Log.Debug("Plugin data Folder not created, no local cache")
          metaType[bannerRealUrl] = proxyFunc(poster, 1 if num == defaulttvdbseason else num +1)
          Log.Debug("getImagesFromTVDB - pic url: '%s', sort order: '%d'" % (bannerRealUrl, 1 if num == defaulttvdbseason else num +1))
          #if not movie and metaType == metadata.seasons[season].posters:  metadata.posters[bannerRealUrl] = proxyFunc(poster, sort_order=num+50) #Add season posters to posters
    Log.Debug("getImagesFromTVDB - Item number: %s, posters: %s, Poster ids: %s" % (str(num), str(posternum), log_string))
    return posternum
    
  ### Download TMDB pics ##################################################################################################################################
  def getImagesFromTMDB(self, metadata, tmdbid, num=99):
 
    Log.Debug("getImagesFromTMDB")
    config_dict      = self.get_json(url=TMDB_CONFIG_URL         , cache_time=CACHE_1WEEK * 2)
    tmdb_images_dict = self.get_json(url=TMDB_IMAGES_URL % tmdbid, cache_time=CACHE_1WEEK * 2)

    metaTypes = [metadata.posters,                        metadata.art]
    filenames = [tmdb_images_dict['posters'], tmdb_images_dict['backdrops'] ]
    for metatype, tmdb_images in zip(metaTypes, filenames):
    
      max_average = max([(lambda p: p['vote_average'] or 5)(p) for p in tmdb_images_dict])
      max_count   = max([(lambda p: p['vote_count'  ]     )(p) for p in tmdb_images_dict]) or 1
      valid_names = list()
      for i, images in enumerate(tmdb_images_dict):
        score  = (images['vote_average'] / max_average) * TMDB_SCORE_RATIO + (images['vote_count'] / max_count) * (1 - TMDB_SCORE_RATIO)
        tmdb_images[i]['score'] = score
        if Prefs['localart'] and backdrop['iso_639_1'] == 'en':  tmdb_images[i]['score'] = float(images['score']) + 1  # Boost the score for localized art (according to the preference).
        if backdrop['iso_639_1'] not in (lang, 'en', None):      tmdb_images[i]['score'] = float(images['score']) - 1  # Discount score for foreign art.
      
      # Images download
      for i, images in enumerate(sorted(tmdb_images, key=lambda k: k['score'], reverse=True)):
        if i > TMDB_ARTWORK_ITEM_LIMIT:  break
        else:
          image_url = config_dict['images']['base_url'] + 'original' + images['file_path']
          thumb_url = config_dict['images']['base_url'] + 'w300'     + images['file_path']
          valid_names.append(image_url)
          if image_url not in metatype:
            Log.Debug("getImagesFromTMDB - Loading: " + thumb_url)
            try:    metatype[image_url] = Proxy.Preview(HTTP.Request(thumb_url), sort_order=i+1)
            except: Log.Debug("getImagesFromTBDB - adding pictrure failed")
      #metatype.validate_keys(valid_names)

  ### Download TMDB poster and background through IMDB ID #################################################################################################
  def getImagesFromTMDBbyIMDBID(self, metadata, imdbid, num=99):
 
    Log.Debug("getImagesFromTMDBbyIMDBID")
    config_dict = self.get_json(TMDB_CONFIG_URL,                   cache_time=CACHE_1WEEK * 2)
    tmdb_json   = self.get_json(TMDB_SEARCH_URL_BY_IMDBID %imdbid, cache_time=CACHE_1WEEK * 2) #tmdb_json[x]: 'poster_path', 'backdrop_path', 'adult', 'id', 'original_title', release_date', 'popularity', 'title', 'vote_average','vote_count'

    valid_names = list()
    Log.Debug("getImagesFromTMDBbyIMDBID - " + TMDB_SEARCH_URL_BY_IMDBID % imdbid)
    if tmdb_json is not None:
      metaTypes = [metadata.posters,                        metadata.art]
      filenames = [tmdb_json['movie_results'][0]['poster_path'], tmdb_json['movie_results'][0]['backdrop_path'] ]
      for metatype, filename in zip(metaTypes, filenames):
        image_url = config_dict['images']['base_url'] + 'original' + filename
        thumb_url = config_dict['images']['base_url'] + 'w300'     + filename
        Log.Debug("Poster: '%s', Background: '%s'" % (image_url, thumb_url) )
        valid_names.append(image_url)
        if not image_url in metatype:
          try:     metadata_download (metatype, image_url, num, "TMDBb/%s.jpg" % imdbid)  #metatype[image_url] = Proxy.Preview(HTTP.Request(thumb_url), sort_order=90)
          except:  Log.Debug("failed")
          else:    Log.Debug("getImagesFromTBDBbyIMDBID - " + image_url)
        #metatype.validate_keys(valid_names)
    else:  Log.Debug("getImagesFromTMDBbyIMDBID - tmdb_json is None")
    
  ### Fetch the IMDB poster using OMDB HTTP API ###########################################################################################################
  def getImagesFromOMDB(self, metadata, imdbid, num=99):
    Log.Debug("getImagesFromOMDB - imdbid: '%s', url: '%s'" % (imdbid, OMDB_HTTP_API_URL + imdbid))
    try:         #with self.get_json(OMDB_HTTP_API_URL + tmdbid, cache_time=CACHE_1WEEK * 56) as OMDB:  metadata_download (metadata.posters, OMDB['Poster'], num, filename="OMDB/%s.jpg" % imdbid)
      OMDB = self.get_json(OMDB_HTTP_API_URL + imdbid, cache_time=CACHE_1WEEK * 56)
      Log.Debug("getImagesFromOMDB - test" + OMDB['Poster'])
      if not OMDB['Poster'] in metadata.posters:  metadata.posters[ OMDB['Poster'] ] = Proxy.Media( HTTP.Request(OMDB['Poster'], cacheTime=None).content, num) #metadata_download (metadata.posters, OMDB['Poster'], num, "OMDB/%s.jpg" % imdbid)
    except:  Log.Debug("getImagesFromOMDB - url: failed")
    else:    Log.Debug("getImagesFromOMDB - url: '%s' downloaded" % OMDB['Poster'])

  #########################################################################################################################################################
  def metadata_download (metatype, url, num=99, filename="", url_thumbnail=None):

    if url in metatype:
      Log.Debug("image_download - url: %s, num: %d, filename: %s already present in Plex" % (url, num, filename))
      return
    #Log.Debug("metadata_download - url: %s, num: %d, filename: %s " % (url, num, filename))
    if not filename == "" and Data.Exists(filename):
      Log.Debug("image_download - url: '%s', num: '%d', filename: '%s' was not in plex, was in Hama local disk cache" % (url, num, filename))
      image = Data.Load(filename)
    else:
      #if self.http_status_code(url) == 200:
      try:
        file = HTTP.Request( (url if url_thumbnail is None else url_thumbnail) , cacheTime=None).content
        Data.Save(filename, file)
      except Exception, e:  Log.Debug("metadata_download - Plugin Data Folder not created for filename '%s', no local cache, or download failed - exception e: %s" % (filename, e))
      else:                 Log.Debug("metadata_download - url: '%s', num: '%d', filename: '%s' was not in plex, was not in HAMA disk cache" % (url, num, filename))
      
    try:     metatype[ url ] = (Proxy.Media if url_thumbnail is None else Proxy.Preview) (image, num)
    except:  Log.Debug("metadata_download - issue adding picture to plex")
    return

  ### get_json file, TMDB API supports only JSON now ######################################################################################################
  #@staticmethod
  def get_json(self, url, cache_time=CACHE_1MONTH):
    try:     tmdb_dict = JSON.ObjectFromURL(url, sleep=2.0, cacheTime=cache_time)
    except:  Log('get_json - Error fetching JSON from The Movie Database.')
    else:    return tmdb_dict

  ### Pull down the XML (and cache it) for a given anime ID ############################################################################################################
  def urlLoadXml(self, url, filename=""):
    Log.Debug ("urlLoadXml - url: %s, filename: %s" % (url, filename))
    
    global lastRequestTime
    try:
      networkLock.acquire()
      if lastRequestTime is not None:
        delta = datetime.datetime.utcnow() - lastRequestTime
        if delta.seconds < SECONDS_BETWEEN_REQUESTS: time.sleep(SECONDS_BETWEEN_REQUESTS - delta.seconds)
      lastRequestTime = datetime.datetime.utcnow()
      result          = HTTP.Request(url, headers={'Accept-Encoding':''}, timeout=60, cacheTime=CACHE_1HOUR * 24 * 7 * 2 )
    except URLError as e:
      if   hasattr(e, 'reason'):  Log("urlLoadXml - We failed to reach a server: " + e.reason)
      elif hasattr(e, 'code'  ):  Log("urlLoadXml - The server couldn't fulfill the request: " + e.code)
    else:
      if result == "<error>Banned</error>": Log("urlLoadXml - You have been Banned by AniDB") #to test
      else:
      	if filename=="": Log.Debug("urlLoadXml: Filename empty") #and Prefs['TVDB-Local-cache']==true: #to enable when json file updated
        else:
      	  try:                  Data.Save(filename, result)
      	  except Exception, e:  Log.Debug("urlLoadXml: Serie XML could not be saved locally" + e)  #Catch ALL
      	  else:                 Log.Debug("urlLoadXml: Serie XML saved locally successfully") 
      	return XML.ElementFromString(result)
    finally: networkLock.release()

  ### Import XML file from 'Data' folder into an XML element ##############################################################################################
  def xmlElementFromFile (self, filename, url=None):

    if url is not None:
      try:
        string  = HTTP.Request(url, timeout=60, cacheTime=CACHE_1HOUR * 24 * 7 * 2 ).content
        element = XML.ElementFromString( string )
      except:  Log.Debug("xmlElementFromFile - Loading XML file from url failed: " + url)
      else:
        Log.Debug("xmlElementFromFile - Loading XML file from url worked: " + url)
        try:     Data.Save(filename, string)
        except:  Log.Debug("Plugin Data Folder not created, no local cache")
        return element
    else:  Log.Debug("xmlElementFromFile - No url provided")
    
    try:    element = XML.ElementFromString( Data.Load(filename) )
    except:
      Log.Debug("xmlElementFromFile - Loading XML file from Data folder failed: " + filename)
      try:     Resource.Load(filename)
      except:
        Log.Debug("xmlElementFromFile - Loading XML file from Ressource folder failed: " + filename)
        raise ValueError
      else:  Log.Debug("xmlElementFromFile - Loading XML file from Ressource folder worked: " + filename)
    else:    Log.Debug("xmlElementFromFile - Loading XML file from Data folder worked")
    return element

  ### http_code retrieves the http status code of a url by requesting header data only from the host or None if an error occurs ###
  def http_status_code(self, url):
    from urlparse import urlparse
    import httplib
    o = urlparse(url)
    try:
      conn = httplib.HTTPConnection(o.netloc)
      conn.request("HEAD", o.path)
      return conn.getresponse().status
    except StandardError: return None
      
  ### Cleanse title of FILTER_CHARS and translate anidb '`' ############################################################################################################
  def cleanse_title(self, title):
    title=title.encode('utf-8')
    return title.replace("`", "'").translate(string.maketrans('', ''), FILTER_CHARS).lower() # None in the translate call was giving an error of 'TypeError: expected a character buffer object'. So, we construct a blank translation table instead.

  ### Split a string per list of chars #################################################################################################################################
  def splitByChars(self, string, separators=SPLIT_CHARS):
    for i in separators: string.replace(" ", i)
    return string.split()

  ### extract the series/movie/Episode title #################################################################################################################################
  def getMainTitle(self, titles, LANGUAGE_PRIORITY):
    Log.Debug("getMainTitle - LANGUAGE_PRIORITY: " + str(LANGUAGE_PRIORITY))
    if not 'main' in LANGUAGE_PRIORITY: LANGUAGE_PRIORITY.append('main')                         # Add main to the selection if not present
    langTitles = ["" for index in range(len(LANGUAGE_PRIORITY)+1)]                               # LANGUAGE_PRIORITY: title order including main title, then choosen title

    for title in titles:                                                                         # Loop through all languages listed in the anime XML
      type = title.get('type')                                                                   # IF Serie: Main, official, Synonym, short. If episode: None
      lang = title.get('{http://www.w3.org/XML/1998/namespace}lang')                             # Get the language, 'xml:lang' attribute need hack to read properly
       
      if type == 'main' or type == None and langTitles[ LANGUAGE_PRIORITY.index('main') ] == "": # type==none is for mapping episode language
        langTitles [ LANGUAGE_PRIORITY.index('main') ] = title.text
 
      if lang in LANGUAGE_PRIORITY and type in ['main', 'official', None]:                       # type==none is for mapping file language     
         langTitles [ LANGUAGE_PRIORITY.index(lang) ] = title.text        
                                                                                              
    Log.Debug("getMainTitle - LANGUAGE titles: " + str(langTitles))
    for index in range( len(LANGUAGE_PRIORITY)-1 ):
      if langTitles [ index ] != '' :
        langTitles [len(LANGUAGE_PRIORITY)] = langTitles [ index ]
        break
                                                                                               
    return langTitles[len(LANGUAGE_PRIORITY)], langTitles[ LANGUAGE_PRIORITY.index('main') ]
    
### TV Agent declaration ###############################################################################################################################################
class HamaTVAgent(Agent.TV_Shows, HamaCommonAgent):
  name             = 'HamaTV'
  languages        = [ Locale.Language.English, ]
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles']
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None
  
  def search(self, results,  media, lang, manual): self.searchByName (results,  media, lang, manual, False )
  def update(self, metadata, media, lang, force ): self.parseAniDBXml(metadata, media, lang, force,  False )

### Movie Agent declaration ############################################################################################################################################
class HamaMovieAgent(Agent.Movies, HamaCommonAgent):
  name             = 'HamaMovies'
  languages        = [ Locale.Language.English, ]
  accepts_from     = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles']
  primary_provider = True
  fallback_agent   = False
  contributes_to   = None
  
  def search(self, results,  media, lang, manual): self.searchByName (results,  media, lang, manual, True )
  def update(self, metadata, media, lang, force ): self.parseAniDBXml(metadata, media, lang, force,  True )
