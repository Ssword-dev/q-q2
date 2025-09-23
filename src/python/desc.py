import json
import re

descriptions = {
    "Liberation Day": {
        "shortDescription": "Commemoration of a nation's liberation from occupation, oppression, or foreign rule.",
        "longDescription": "N/A"
    },
    "Afghanistan Independence Day": {
        "shortDescription": "Marks Afghanistan's independence from British influence in 1919.",
        "longDescription": "N/A"
    },
    "Mojahedin's Victory Day": {
        "shortDescription": "Commemorates the victory of Afghan Mujahideen forces against Soviet troops in the 1980s.",
        "longDescription": "N/A"
    },
    "Islamic Emirate Victory Day": {
        "shortDescription": "Marks the Taliban's takeover of Afghanistan and establishment of the Islamic Emirate.",
        "longDescription": "N/A"
    },
    "American Withdrawal Day": {
        "shortDescription": "Commemorates the final withdrawal of U.S. forces from Afghanistan in 2021.",
        "longDescription": "N/A"
    },
    "Prophet's Birthday": {
        "shortDescription": "Islamic holiday celebrating the birth of the Prophet Muhammad.",
        "longDescription": "N/A"
    },
    "First Day of Ramadan": {
        "shortDescription": "The beginning of the Islamic holy month of fasting, prayer, and reflection.",
        "longDescription": "N/A"
    },
    "Eid al-Fitr": {
        "shortDescription": "Islamic festival marking the end of Ramadan, celebrated with communal prayers and feasts.",
        "longDescription": "N/A"
    },
    "Day of Arafah": {
        "shortDescription": "The day before Eid al-Adha, considered one of the holiest days in Islam, especially during Hajj.",
        "longDescription": "N/A"
    },
    "Eid al-Adha": {
        "shortDescription": "Festival of Sacrifice, commemorating Abraham\u2019s willingness to sacrifice his son as an act of obedience to God.",
        "longDescription": "N/A"
    },
    "New Year's Day": {
        "shortDescription": "Celebration of the first day of the Gregorian calendar year, often marked with festivities worldwide.",
        "longDescription": "N/A"
    },
    "Epiphany": {
        "shortDescription": "Christian holiday celebrating the revelation of Christ to the Gentiles, often linked to the visit of the Magi.",
        "longDescription": "N/A"
    },
    "Good Friday": {
        "shortDescription": "Christian observance commemorating the crucifixion of Jesus Christ.",
        "longDescription": "N/A"
    },
    "Easter Sunday": {
        "shortDescription": "Christian holiday celebrating the resurrection of Jesus Christ from the dead.",
        "longDescription": "N/A"
    },
    "Easter Monday": {
        "shortDescription": "The day after Easter Sunday, observed in many Christian-majority countries as a public holiday.",
        "longDescription": "N/A"
    },
    "May Day": {
        "shortDescription": "International Workers' Day, celebrating labor rights and workers' achievements, often on May 1st.",
        "longDescription": "N/A"
    },
    "Ascension Day": {
        "shortDescription": "Christian holiday commemorating the ascension of Jesus into heaven, celebrated 40 days after Easter.",
        "longDescription": "N/A"
    },
    "Whit Sunday": {
        "shortDescription": "Also called Pentecost; Christian festival marking the descent of the Holy Spirit on the apostles.",
        "longDescription": "N/A"
    },
    "Midsummer Eve": {
        "shortDescription": "Celebration on the eve of Midsummer, often linked to solstice traditions, bonfires, and festivities.",
        "longDescription": "N/A"
    },
    "Midsummer Day": {
        "shortDescription": "Traditional holiday celebrating the summer solstice and the longest days of the year.",
        "longDescription": "N/A"
    },
    "All Saints' Day": {
        "shortDescription": "Christian festival honoring all saints, known and unknown, celebrated on November 1.",
        "longDescription": "N/A"
    },
    "Independence Day": {
        "shortDescription": "Celebration of a nation\u2019s independence from colonial or foreign rule.",
        "longDescription": "N/A"
    },
    "Christmas Eve": {
        "shortDescription": "The evening before Christmas Day, often celebrated with festive meals and family gatherings.",
        "longDescription": "N/A"
    },
    "Immaculate Conception": {
        "shortDescription": "a Roman Catholic doctrine stating that Mary, the mother of Jesus, was preserved from the stain of original sin from the moment of her conception.",
        "longDescription": "N/A"
    },
    "Christmas Day": {
        "shortDescription": "Christian holiday celebrating the birth of Jesus Christ, observed on December 25.",
        "longDescription": "N/A"
    },
    "Second Day of Christmas": {
        "shortDescription": "Also known as Boxing Day or St. Stephen\u2019s Day, observed the day after Christmas in many countries.",
        "longDescription": "N/A"
    },
    "\u00c5land's Autonomy Day": {
        "shortDescription": "Celebration of the \u00c5land Islands\u2019 autonomous status within Finland, established in 1920.",
        "longDescription": "N/A"
    },
    "Summer Day": {
        "shortDescription": "Traditional festival marking the arrival of summer, often celebrated with outdoor festivities.",
        "longDescription": "N/A"
    },
    "Nowruz Day": {
        "shortDescription": "Persian New Year, celebrated on the spring equinox, symbolizing renewal and new beginnings.",
        "longDescription": "N/A"
    },
    "Catholic Easter Sunday; Orthodox Easter Sunday": {
        "shortDescription": "Christian holiday celebrating the resurrection of Jesus Christ; observed on different dates by Catholic and Orthodox churches.",
        "longDescription": "N/A"
    },
    "International Workers' Day": {
        "shortDescription": "Also known as May Day, celebrates labor rights and the contributions of workers worldwide.",
        "longDescription": "N/A"
    },
    "Mother Teresa Canonization Day": {
        "shortDescription": "Marks the canonization of Mother Teresa as a saint by the Catholic Church.",
        "longDescription": "N/A"
    },
    "Alphabet Day": {
        "shortDescription": "Holiday celebrating the creation or adoption of a national alphabet, often tied to cultural identity.",
        "longDescription": "N/A"
    },
    "Flag and Independence Day": {
        "shortDescription": "Celebration of both a nation\u2019s independence and its national flag as a symbol of sovereignty.",
        "longDescription": "N/A"
    },
    "National Youth Day": {
        "shortDescription": "Day dedicated to recognizing and empowering the role of youth in national development.",
        "longDescription": "N/A"
    },
    "Amazigh New Year": {
        "shortDescription": "Also called Yennayer, the new year according to the Amazigh (Berber) calendar, marking agricultural cycles.",
        "longDescription": "N/A"
    },
    "Labor Day": {
        "shortDescription": "Public holiday honoring workers and labor movements; often coincides with or is distinct from May Day.",
        "longDescription": "N/A"
    },
    "Ashura; Independence Day": {
        "shortDescription": "Ashura is an Islamic holy day marking the martyrdom of Husayn ibn Ali; paired here with national independence celebrations.",
        "longDescription": "N/A"
    },
    "Revolution Day": {
        "shortDescription": "Commemorates a national revolution or significant uprising leading to political change.",
        "longDescription": "N/A"
    },
    "Islamic New Year": {
        "shortDescription": "Marks the beginning of the Islamic lunar calendar year, starting with the month of Muharram.",
        "longDescription": "N/A"
    },
    "Eid al-Fitr Holiday": {
        "shortDescription": "Public holiday following Eid al-Fitr, extending celebrations at the end of Ramadan.",
        "longDescription": "N/A"
    },
    "Saint Peter's Day": {
        "shortDescription": "Christian feast day honoring Saint Peter, one of Jesus\u2019 apostles, often marked with local celebrations.",
        "longDescription": "N/A"
    },
    "Saint Julian's Day": {
        "shortDescription": "Religious feast dedicated to Saint Julian, celebrated with parish or community events.",
        "longDescription": "N/A"
    },
    "Virgin Mary of Can\u00f2lich": {
        "shortDescription": "Feast day in Andorra dedicated to Our Lady of Can\u00f2lich, the patron saint of Sant Juli\u00e0 de L\u00f2ria.",
        "longDescription": "N/A"
    },
    "Sant Juli\u00e0 de L\u00f2ria Festival": {
        "shortDescription": "Local festival in the parish of Sant Juli\u00e0 de L\u00f2ria, Andorra, featuring cultural and religious events.",
        "longDescription": "N/A"
    },
    "Andorra la Vella Festival": {
        "shortDescription": "Annual town festival in Andorra la Vella, including processions, concerts, and community gatherings.",
        "longDescription": "N/A"
    },
    "Saint Michael of Engolasters' Day": {
        "shortDescription": "Religious feast day in Andorra honoring Saint Michael, associated with the chapel of Engolasters.",
        "longDescription": "N/A"
    },
    "Parish foundation day": {
        "shortDescription": "Local celebration marking the anniversary of the establishment of a parish community.",
        "longDescription": "N/A"
    },
    "Escaldes-Engordany Festival": {
        "shortDescription": "Cultural and religious festival held in the Escaldes-Engordany parish of Andorra.",
        "longDescription": "N/A"
    },
    "Liberation Movement Day": {
        "shortDescription": "National holiday commemorating the struggle for liberation from colonial or oppressive rule.",
        "longDescription": "N/A"
    },
    "Day off for Liberation Movement Day": {
        "shortDescription": "Observed as a substitute holiday when Liberation Movement Day falls on a weekend.",
        "longDescription": "N/A"
    },
    "Carnival Day": {
        "shortDescription": "Festive day before Lent, marked by parades, costumes, and public celebrations.",
        "longDescription": "N/A"
    },
    "Day off for Carnival Day": {
        "shortDescription": "Additional public holiday granted in connection with Carnival festivities.",
        "longDescription": "N/A"
    },
    "International Women's Day": {
        "shortDescription": "Global day celebrating the social, economic, cultural, and political achievements of women, held on March 8.",
        "longDescription": "N/A"
    },
    "Southern Africa Liberation Day": {
        "shortDescription": "Commemoration of liberation movements in Southern Africa and solidarity with their struggles.",
        "longDescription": "N/A"
    },
    "Peace and National Reconciliation Day": {
        "shortDescription": "Day promoting unity, peace, and reconciliation after periods of conflict or division.",
        "longDescription": "N/A"
    },
    "International Worker's Day": {
        "shortDescription": "Also known as May Day, celebrating workers\u2019 rights and achievements worldwide.",
        "longDescription": "N/A"
    },
    "Day off for International Worker's Day": {
        "shortDescription": "Substitute holiday provided when International Worker\u2019s Day falls on a weekend.",
        "longDescription": "N/A"
    },
    "National Heroes' Day": {
        "shortDescription": "Holiday honoring individuals who made significant sacrifices for the nation\u2019s independence or freedom.",
        "longDescription": "N/A"
    },
    "All Souls' Day": {
        "shortDescription": "Christian holiday commemorating all the faithful departed, observed on November 2.",
        "longDescription": "N/A"
    },
    "National Independence Day": {
        "shortDescription": "Celebration of the country\u2019s declaration of independence and sovereignty.",
        "longDescription": "N/A"
    },
    "Day off for National Independence Day": {
        "shortDescription": "Substitute holiday observed when National Independence Day falls on a weekend.",
        "longDescription": "N/A"
    },
    "Christmas and Family Day": {
        "shortDescription": "Holiday combining the Christian celebration of Christmas with emphasis on family gatherings.",
        "longDescription": "N/A"
    },
    "Day off for Christmas and Family Day": {
        "shortDescription": "Additional public holiday observed in lieu of Christmas and Family Day.",
        "longDescription": "N/A"
    },
    "James Ronald Webster Day": {
        "shortDescription": "Honors James Ronald Webster, the political leader considered the father of modern Anguilla.",
        "longDescription": "N/A"
    },
    "King's Birthday": {
        "shortDescription": "Celebration of the reigning monarch\u2019s birthday, observed as a public holiday.",
        "longDescription": "N/A"
    },
    "Anguilla Day": {
        "shortDescription": "National holiday commemorating Anguilla\u2019s declaration of separation from Saint Kitts and Nevis in 1967.",
        "longDescription": "N/A"
    },
    "August Monday": {
        "shortDescription": "Main day of Anguilla\u2019s summer carnival, celebrated with parades, boat races, and festivities.",
        "longDescription": "N/A"
    },
    "August Thursday": {
        "shortDescription": "Continuation of carnival celebrations in Anguilla, featuring music and cultural events.",
        "longDescription": "N/A"
    },
    "National Heroes and Heroines Day": {
        "shortDescription": "Honors individuals who contributed significantly to national identity and independence.",
        "longDescription": "N/A"
    },
    "Boxing Day": {
        "shortDescription": "Holiday celebrated the day after Christmas, traditionally associated with charity and gift-giving.",
        "longDescription": "N/A"
    },
    "Special Public Holiday": {
        "shortDescription": "Occasional holiday declared by the government for unique national events or observances.",
        "longDescription": "N/A"
    },
    "Labour Day": {
        "shortDescription": "Public holiday celebrating workers and the labor movement.",
        "longDescription": "N/A"
    },
    "Carnival Monday": {
        "shortDescription": "Part of carnival festivities, featuring street parades, music, and dance.",
        "longDescription": "N/A"
    },
    "Carnival Tuesday": {
        "shortDescription": "Climax of carnival celebrations, often featuring masquerades and large parades.",
        "longDescription": "N/A"
    },
    "Sir Vere Cornwall Bird Snr. Day": {
        "shortDescription": "Honors Sir Vere Cornwall Bird Sr., Antigua and Barbuda\u2019s first Prime Minister.",
        "longDescription": "N/A"
    },
    "National Day of Remembrance for Truth and Justice": {
        "shortDescription": "Argentine holiday remembering victims of the military dictatorship (1976\u20131983).",
        "longDescription": "N/A"
    },
    "Veteran's Day and the Fallen in the Malvinas War": {
        "shortDescription": "Commemoration of veterans and those who died in the 1982 Falklands/Malvinas War.",
        "longDescription": "N/A"
    },
    "Maundy Thursday": {
        "shortDescription": "Christian holy day commemorating the Last Supper of Jesus with his disciples.",
        "longDescription": "N/A"
    },
    "May Revolution Day": {
        "shortDescription": "Marks the May 1810 revolution that led to Argentina\u2019s independence movement.",
        "longDescription": "N/A"
    },
    "Pass to the Immortality of General Don Mart\u00edn Miguel de G\u00fcemes": {
        "shortDescription": "Honors the death of General Mart\u00edn Miguel de G\u00fcemes, leader in Argentina\u2019s War of Independence.",
        "longDescription": "N/A"
    },
    "Pass to the Immortality of General Don Manuel Belgrano": {
        "shortDescription": "Commemorates the death of Manuel Belgrano, creator of the Argentine flag and independence leader.",
        "longDescription": "N/A"
    },
    "Pass to the Immortality of General Don Jos\u00e9 de San Mart\u00edn": {
        "shortDescription": "Honors the death of Jos\u00e9 de San Mart\u00edn, Argentine general and liberator of South America.",
        "longDescription": "N/A"
    },
    "Respect for Cultural Diversity Day": {
        "shortDescription": "Promotes respect for cultural diversity, formerly known as Columbus Day in Argentina.",
        "longDescription": "N/A"
    },
    "National Sovereignty Day": {
        "shortDescription": "Marks Argentina\u2019s defense of its sovereignty during the Battle of Vuelta de Obligado (1845).",
        "longDescription": "N/A"
    },
    "Bridge Public Holiday": {
        "shortDescription": "Extra holiday added to create a long weekend, usually near another public holiday.",
        "longDescription": "N/A"
    },
    "Anniversary of the Battle of Salta": {
        "shortDescription": "Commemorates the 1813 victory of Argentine forces over Spanish royalists in Salta.",
        "longDescription": "N/A"
    },
    "Day of Memory of General Don Mart\u00edn Miguel de G\u00fcemes": {
        "shortDescription": "Local commemoration of the life and legacy of General G\u00fcemes.",
        "longDescription": "N/A"
    },
    "Feasts of the Lord and the Virgin of Miracle": {
        "shortDescription": "Salta\u2019s religious festival venerating Christ and the Virgin Mary under the title of \u2018El Milagro\u2019.",
        "longDescription": "N/A"
    },
    "Exaltation of the Holy Cross Day": {
        "shortDescription": "Christian feast celebrating the cross as a symbol of salvation.",
        "longDescription": "N/A"
    },
    "Saint Louis the King of France's Day": {
        "shortDescription": "Feast day of Saint Louis IX, King of France, celebrated as a local patronal festival.",
        "longDescription": "N/A"
    },
    "National Day of Remembrance for Truth and Justice; Provincial Day of Remembrance for Truth and Justice": {
        "shortDescription": "Combined national and provincial observance honoring victims of Argentina\u2019s dictatorship.",
        "longDescription": "N/A"
    },
    "Commemoration of the Battle of Caseros": {
        "shortDescription": "Marks the 1852 battle in which Justo Jos\u00e9 de Urquiza defeated Juan Manuel de Rosas, reshaping Argentine politics.",
        "longDescription": "N/A"
    },
    "State Worker's Day": {
        "shortDescription": "Holiday celebrating the contributions of state employees.",
        "longDescription": "N/A"
    },
    "Saint Michael the Archangel's Day": {
        "shortDescription": "Christian feast honoring Saint Michael the Archangel, patron of protection and justice.",
        "longDescription": "N/A"
    },
    "Day of Remembrance for Truth and Justice; National Day of Remembrance for Truth and Justice": {
        "shortDescription": "Day to reflect on human rights and honor victims of Argentina\u2019s dictatorship.",
        "longDescription": "N/A"
    },
    "Day of the Death of Juan Facundo Quiroga": {
        "shortDescription": "Remembers the assassination of Quiroga, an important Argentine caudillo in the 19th century.",
        "longDescription": "N/A"
    },
    "Provincial Autonomy Day": {
        "shortDescription": "Celebrates the recognition of provincial autonomy within Argentina.",
        "longDescription": "N/A"
    },
    "La Rioja Foundation Day": {
        "shortDescription": "Marks the foundation of the city of La Rioja, Argentina.",
        "longDescription": "N/A"
    },
    "Anniversary of the Death of Enrique Angelelli": {
        "shortDescription": "Remembers Bishop Enrique Angelelli, a cleric and human rights advocate assassinated in 1976.",
        "longDescription": "N/A"
    },
    "Anniversary of the Death of \u00c1ngel Vicente Pe\u00f1aloza": {
        "shortDescription": "Commemorates the death of \u00c1ngel Vicente Pe\u00f1aloza, a federalist leader in Argentina.",
        "longDescription": "N/A"
    },
    "Tinkunaco Festival": {
        "shortDescription": "Traditional festival in La Rioja, Argentina, symbolizing reconciliation between Spanish settlers and indigenous peoples.",
        "longDescription": "N/A"
    },
    "Teacher's Day": {
        "shortDescription": "Holiday honoring teachers and their role in education, observed in Argentina on September 11.",
        "longDescription": "N/A"
    },
    "Birthday of Mamerto Esqui\u00fa": {
        "shortDescription": "Celebrates the birth of Friar Mamerto Esqui\u00fa, an Argentine priest and politician.",
        "longDescription": "N/A"
    },
    "Catamarca Autonomy Day": {
        "shortDescription": "Marks the establishment of Catamarca Province\u2019s autonomy within Argentina.",
        "longDescription": "N/A"
    },
    "Miracle Day": {
        "shortDescription": "Commemoration of the \u2018Se\u00f1or y Virgen del Milagro\u2019 in Salta, Argentina.",
        "longDescription": "N/A"
    },
    "Saint James' Day": {
        "shortDescription": "Christian feast honoring Saint James the Apostle, patron saint of Spain and many communities.",
        "longDescription": "N/A"
    },
    "Anniversary of the Battle of Tucum\u00e1n": {
        "shortDescription": "Marks the 1812 victory of Argentine forces under Manuel Belgrano over Spanish royalists.",
        "longDescription": "N/A"
    },
    "Plebiscite 1902 Trevelin": {
        "shortDescription": "Commemoration of the 1902 plebiscite in Trevelin, Chubut, where Welsh settlers chose Argentine sovereignty.",
        "longDescription": "N/A"
    },
    "Anniversary of the arrival of the first Welsh settlers": {
        "shortDescription": "Marks the arrival of Welsh immigrants in Patagonia, Argentina, in 1865.",
        "longDescription": "N/A"
    },
    "National Petroleum Day": {
        "shortDescription": "Celebrates the discovery of petroleum in Comodoro Rivadavia in 1907, key to Argentina\u2019s industry.",
        "longDescription": "N/A"
    },
    "Tehuelches and Mapuches declare loyalty to the Argentine flag": {
        "shortDescription": "Commemorates the 1810s oath of loyalty to Argentina by indigenous groups in Patagonia.",
        "longDescription": "N/A"
    },
    "Day of the Province of Tierra del Fuego, Antarctica and the South Atlantic Islands": {
        "shortDescription": "Regional holiday celebrating Argentina\u2019s southernmost province.",
        "longDescription": "N/A"
    },
    "Selk'Nam Genocide Day": {
        "shortDescription": "Day of remembrance for the genocide of the Selk\u2019nam people in Tierra del Fuego.",
        "longDescription": "N/A"
    },
    "Anniversary of the Death of General Manuel Belgrano; Pass to the Immortality of General Don Manuel Belgrano": {
        "shortDescription": "Marks the death of General Manuel Belgrano, creator of Argentina\u2019s flag.",
        "longDescription": "N/A"
    },
    "Anniversary of the Death of General Jos\u00e9 Francisco de San Mart\u00edn; Pass to the Immortality of General Don Jos\u00e9 de San Mart\u00edn": {
        "shortDescription": "Honors the death of Jos\u00e9 de San Mart\u00edn, liberator of Argentina, Chile, and Peru.",
        "longDescription": "N/A"
    },
    "Jujuy Exodus Day": {
        "shortDescription": "Commemorates the 1812 mass evacuation ordered by General Belgrano during the Argentine War of Independence.",
        "longDescription": "N/A"
    },
    "Jujuy Political Autonomy Day": {
        "shortDescription": "Marks the political autonomy of Jujuy Province in Argentina.",
        "longDescription": "N/A"
    },
    "Pachamama Day": {
        "shortDescription": "Traditional Andean celebration honoring Pachamama (Mother Earth).",
        "longDescription": "N/A"
    },
    "Day of the Virgin of the Rosary of R\u00edo Blanco and Paypaya": {
        "shortDescription": "Festival in Jujuy Province honoring the Virgin of the Rosary of R\u00edo Blanco and Paypaya.",
        "longDescription": "N/A"
    },
    "Great Day of Jujuy": {
        "shortDescription": "Regional celebration of Jujuy Province\u2019s heritage and history.",
        "longDescription": "N/A"
    },
    "Saint John Bosco's Day": {
        "shortDescription": "Catholic feast honoring Saint John Bosco, patron saint of youth and educators.",
        "longDescription": "N/A"
    },
    "Anniversary of the Death of N\u00e9stor Carlos Kirchner": {
        "shortDescription": "Commemorates the death of N\u00e9stor Kirchner, former President of Argentina (2003\u20132007).",
        "longDescription": "N/A"
    },
    "Commemoration of the workers shot in the Patagonian Strikes": {
        "shortDescription": "Remembers the rural workers killed during the strikes in Patagonia (1920\u20131921).",
        "longDescription": "N/A"
    },
    "Christmas and Epiphany Day": {
        "shortDescription": "Combined Christian holiday celebrating Christmas and the visit of the Magi (Epiphany).",
        "longDescription": "N/A"
    },
    "Army Day": {
        "shortDescription": "Holiday recognizing the founding and contributions of the Argentine Army.",
        "longDescription": "N/A"
    },
    "Women's Day": {
        "shortDescription": "International Women\u2019s Day (March 8), celebrating women\u2019s achievements and advocating for equality.",
        "longDescription": "N/A"
    },
    "Genocide Memorial Day": {
        "shortDescription": "Day of remembrance for victims of genocide, often tied to Argentina\u2019s human rights history.",
        "longDescription": "N/A"
    },
    "Victory and Peace Day": {
        "shortDescription": "Commemorates the end of World War II and the triumph of peace over fascism.",
        "longDescription": "N/A"
    },
    "Republic Day": {
        "shortDescription": "Celebration of the establishment of the republic, observed in various countries.",
        "longDescription": "N/A"
    },
    "New Year's Eve": {
        "shortDescription": "Celebration marking the final day of the year, December 31.",
        "longDescription": "N/A"
    },
    "Betico Day": {
        "shortDescription": "Aruban holiday honoring Gilberto Fran\u00e7ois \u2018Betico\u2019 Croes, leader of Aruba\u2019s independence movement.",
        "longDescription": "N/A"
    },
    "Monday before Ash Wednesday": {
        "shortDescription": "Part of carnival season, preceding Ash Wednesday and the start of Lent.",
        "longDescription": "N/A"
    },
    "National Anthem and Flag Day": {
        "shortDescription": "Celebration of a country\u2019s national anthem and flag as symbols of identity and unity.",
        "longDescription": "N/A"
    },
    "King's Day": {
        "shortDescription": "Dutch holiday celebrating the birthday of the King, observed with orange-themed festivities.",
        "longDescription": "N/A"
    },
    "Australia Day": {
        "shortDescription": "National day of Australia, commemorating the arrival of the First Fleet at Sydney Cove in 1788.",
        "longDescription": "N/A"
    },
    "Canberra Day": {
        "shortDescription": "Public holiday in the Australian Capital Territory, celebrating the founding of Canberra in 1913.",
        "longDescription": "N/A"
    },
    "ANZAC Day": {
        "shortDescription": "Australian and New Zealand holiday commemorating soldiers who served and died in wars and conflicts.",
        "longDescription": "N/A"
    },
    "Easter Saturday": {
        "shortDescription": "Christian holiday on the Saturday before Easter Sunday, observed as a day of reflection.",
        "longDescription": "N/A"
    },
    "Reconciliation Day": {
        "shortDescription": "Holiday in the Australian Capital Territory promoting reconciliation between Indigenous and non-Indigenous Australians.",
        "longDescription": "N/A"
    },
    "Picnic Day": {
        "shortDescription": "Public holiday in the Northern Territory of Australia, encouraging community gatherings and leisure.",
        "longDescription": "N/A"
    },
    "The Royal Queensland Show": {
        "shortDescription": "Annual agricultural show in Brisbane, Australia, showcasing farming, produce, and entertainment.",
        "longDescription": "N/A"
    },
    "Adelaide Cup Day": {
        "shortDescription": "Public holiday in South Australia marking the Adelaide Cup horse race.",
        "longDescription": "N/A"
    },
    "Proclamation Day": {
        "shortDescription": "South Australian holiday commemorating the reading of the proclamation establishing government in 1836.",
        "longDescription": "N/A"
    },
    "Eight Hours Day": {
        "shortDescription": "Australian holiday celebrating the labor movement\u2019s achievement of the eight-hour workday.",
        "longDescription": "N/A"
    },
    "Grand Final Day": {
        "shortDescription": "Public holiday in Victoria marking the Australian Football League Grand Final weekend.",
        "longDescription": "N/A"
    },
    "Melbourne Cup Day": {
        "shortDescription": "Victoria\u2019s holiday for the Melbourne Cup, Australia\u2019s most famous horse race.",
        "longDescription": "N/A"
    },
    "Western Australia Day": {
        "shortDescription": "Public holiday celebrating the founding of the Swan River Colony in 1829.",
        "longDescription": "N/A"
    },
    "Corpus Christi": {
        "shortDescription": "Christian feast day celebrating the real presence of the body and blood of Christ in the Eucharist.",
        "longDescription": "N/A"
    },
    "National Day": {
        "shortDescription": "General term for a country\u2019s celebration of independence or founding.",
        "longDescription": "N/A"
    },
    "Martyrs' Day": {
        "shortDescription": "Holiday honoring those who died for national independence or freedom.",
        "longDescription": "N/A"
    },
    "Spring Festival": {
        "shortDescription": "Chinese Lunar New Year, celebrating the beginning of the traditional lunisolar calendar year.",
        "longDescription": "N/A"
    },
    "Victory over Fascism Day": {
        "shortDescription": "Commemoration of the defeat of fascism in World War II.",
        "longDescription": "N/A"
    },
    "National Liberation Day": {
        "shortDescription": "Marks the liberation of a country from colonial or foreign rule.",
        "longDescription": "N/A"
    },
    "Armed Forces Day": {
        "shortDescription": "Holiday honoring the service and sacrifice of a nation\u2019s military forces.",
        "longDescription": "N/A"
    },
    "Victory Day": {
        "shortDescription": "Commemoration of victory in World War II, typically over Nazi Germany in 1945.",
        "longDescription": "N/A"
    },
    "National Flag Day": {
        "shortDescription": "Celebrates the adoption and symbolism of a country\u2019s national flag.",
        "longDescription": "N/A"
    },
    "International Azerbaijanis Solidarity Day": {
        "shortDescription": "Holiday uniting Azerbaijani people worldwide in shared identity and culture.",
        "longDescription": "N/A"
    },
    "Day off": {
        "shortDescription": "General term for a substitute or compensatory holiday.",
        "longDescription": "N/A"
    },
    "Municipal elections": {
        "shortDescription": "Public holiday or observance to allow citizens to vote in local elections.",
        "longDescription": "N/A"
    },
    "Majority Rule Day": {
        "shortDescription": "Bahamian holiday commemorating the 1967 elections that led to majority rule in parliament.",
        "longDescription": "N/A"
    },
    "Randol Fawkes Labour Day": {
        "shortDescription": "Bahamian holiday honoring Sir Randol Fawkes, leader of the labor movement.",
        "longDescription": "N/A"
    },
    "Emancipation Day": {
        "shortDescription": "Marks the abolition of slavery in former British colonies.",
        "longDescription": "N/A"
    },
    "National Heroes Day": {
        "shortDescription": "Commemorates individuals recognized as national heroes for their service and sacrifice.",
        "longDescription": "N/A"
    },
    "Ashura": {
        "shortDescription": "Islamic holy day commemorating the martyrdom of Hussein ibn Ali at Karbala.",
        "longDescription": "N/A"
    },
    "International Mother's language Day": {
        "shortDescription": "UNESCO day promoting linguistic and cultural diversity.",
        "longDescription": "N/A"
    },
    "Sheikh Mujibur Rahman's Birthday and Children's Day": {
        "shortDescription": "Bangladesh holiday celebrating the birth of Sheikh Mujibur Rahman, Father of the Nation, alongside Children\u2019s Day.",
        "longDescription": "N/A"
    },
    "Bengali New Year's Day": {
        "shortDescription": "Pahela Baishakh, the traditional Bengali New Year celebration.",
        "longDescription": "N/A"
    },
    "National Mourning Day": {
        "shortDescription": "Bangladesh\u2019s day of mourning for the assassination of Sheikh Mujibur Rahman in 1975.",
        "longDescription": "N/A"
    },
    "Errol Barrow Day": {
        "shortDescription": "Barbadian holiday celebrating the birthday of Errol Barrow, first Prime Minister of Barbados.",
        "longDescription": "N/A"
    },
    "Kadooment Day": {
        "shortDescription": "Barbados carnival finale, featuring street parades and music.",
        "longDescription": "N/A"
    },
    "Orthodox Christmas Day": {
        "shortDescription": "Christian celebration of Jesus Christ\u2019s birth, according to the Julian calendar (January 7).",
        "longDescription": "N/A"
    },
    "Radunitsa": {
        "shortDescription": "Belarusian Orthodox day of commemoration of the dead, observed after Easter.",
        "longDescription": "N/A"
    },
    "Independence Day of the Republic of Belarus": {
        "shortDescription": "Celebrates the liberation of Minsk from Nazi occupation in 1944.",
        "longDescription": "N/A"
    },
    "October Revolution Day": {
        "shortDescription": "Holiday commemorating the 1917 Bolshevik Revolution in Russia, formerly widely celebrated in Soviet states.",
        "longDescription": "N/A"
    },
    "Catholic Christmas Day": {
        "shortDescription": "Christian celebration of Jesus Christ\u2019s birth, December 25 (Gregorian calendar).",
        "longDescription": "N/A"
    },
    "Catholic Easter; Orthodox Easter": {
        "shortDescription": "Christian holiday celebrating the resurrection of Jesus, observed by both Catholic and Orthodox traditions.",
        "longDescription": "N/A"
    },
    "Armistice Day": {
        "shortDescription": "Commemoration of the end of World War I on November 11, honoring fallen soldiers.",
        "longDescription": "N/A"
    },
    "George Price Day": {
        "shortDescription": "Belizean holiday honoring George Price, first Prime Minister of Belize.",
        "longDescription": "N/A"
    },
    "National Heroes and Benefactors Day": {
        "shortDescription": "Belize holiday honoring those who contributed to the country\u2019s independence and well-being.",
        "longDescription": "N/A"
    },
    "Holy Saturday": {
        "shortDescription": "Christian observance on the day between Good Friday and Easter Sunday.",
        "longDescription": "N/A"
    },
    "Saint George's Caye Day": {
        "shortDescription": "Belize holiday commemorating the 1798 Battle of St. George\u2019s Caye, securing independence from Spain.",
        "longDescription": "N/A"
    },
    "Indigenous Peoples' Resistance Day": {
        "shortDescription": "Holiday honoring the resistance of indigenous peoples against colonialism.",
        "longDescription": "N/A"
    },
    "Garifuna Settlement Day": {
        "shortDescription": "Belize holiday marking the 1802 arrival of the Garifuna people.",
        "longDescription": "N/A"
    },
    "Vodoun Festival": {
        "shortDescription": "Haitian celebration of Vodoun religion and heritage.",
        "longDescription": "N/A"
    },
    "Bermuda Day": {
        "shortDescription": "Bermuda\u2019s national holiday marking the start of summer and celebrating heritage.",
        "longDescription": "N/A"
    },
    "Mary Prince Day": {
        "shortDescription": "Bermuda holiday honoring Mary Prince, an abolitionist and first Black woman to publish an autobiography in Britain.",
        "longDescription": "N/A"
    },
    "Remembrance Day": {
        "shortDescription": "Day honoring those who died in military service, typically around November 11.",
        "longDescription": "N/A"
    },
    "Birth Anniversary of His Majesty the King": {
        "shortDescription": "Bhutan holiday celebrating the reigning monarch\u2019s birthday.",
        "longDescription": "N/A"
    },
    "Birth Anniversary of the 3rd Druk Gyalpo": {
        "shortDescription": "Bhutan holiday celebrating the birth of King Jigme Dorji Wangchuck, the 3rd monarch.",
        "longDescription": "N/A"
    },
    "Coronation of His Majesty the King": {
        "shortDescription": "Celebrates the coronation of Bhutan\u2019s current king.",
        "longDescription": "N/A"
    },
    "Birth Anniversary of the 4th Druk Gyalpo - Constitution Day; Descending Day of Lord Buddha": {
        "shortDescription": "Bhutan holiday celebrating the 4th monarch\u2019s birth, Constitution Day, and the Buddha\u2019s descent from heaven.",
        "longDescription": "N/A"
    },
    "Winter Solstice": {
        "shortDescription": "Traditional observance marking the shortest day of the year.",
        "longDescription": "N/A"
    },
    "Traditional Day of Offering": {
        "shortDescription": "Bhutanese holiday for merit-making and offerings to local deities.",
        "longDescription": "N/A"
    },
    "Losar": {
        "shortDescription": "Tibetan New Year festival celebrated in Bhutan and the Himalayan region.",
        "longDescription": "N/A"
    },
    "Death Anniversary of Zhabdrung": {
        "shortDescription": "Commemorates the death of Zhabdrung Ngawang Namgyal, Bhutan\u2019s unifier.",
        "longDescription": "N/A"
    },
    "Lord Buddha's Parinirvana": {
        "shortDescription": "Buddhist holiday marking the passing of the Buddha into nirvana.",
        "longDescription": "N/A"
    },
    "Birth Anniversary of Guru Rinpoche": {
        "shortDescription": "Holiday celebrating the birth of Guru Rinpoche (Padmasambhava), who brought Buddhism to Bhutan.",
        "longDescription": "N/A"
    },
    "First Sermon of Lord Buddha": {
        "shortDescription": "Buddhist holiday commemorating the Buddha\u2019s first sermon at Sarnath.",
        "longDescription": "N/A"
    },
    "Blessed Rainy Day": {
        "shortDescription": "Bhutanese holiday marking the end of the monsoon and ritual bathing for purification.",
        "longDescription": "N/A"
    },
    "Dassain": {
        "shortDescription": "Hindu festival celebrated in Bhutan and Nepal, honoring Goddess Durga\u2019s victory over evil.",
        "longDescription": "N/A"
    },
    "Dassain; Thimphu Tshechu": {
        "shortDescription": "Combination of Hindu festival Dassain and Bhutan\u2019s Thimphu Tshechu religious festival.",
        "longDescription": "N/A"
    },
    "Thimphu Drubchoe": {
        "shortDescription": "Bhutanese Buddhist festival featuring sacred masked dances and rituals.",
        "longDescription": "N/A"
    },
    "Thimphu Tshechu": {
        "shortDescription": "Major Bhutanese festival of religious dances dedicated to Guru Rinpoche.",
        "longDescription": "N/A"
    },
    "Plurinational State Foundation Day": {
        "shortDescription": "Bolivia\u2019s national holiday celebrating the founding of the plurinational state in 2009.",
        "longDescription": "N/A"
    },
    "Aymara New Year": {
        "shortDescription": "Bolivian holiday marking the Aymara indigenous New Year (Willkakuti).",
        "longDescription": "N/A"
    },
    "National Dignity Day": {
        "shortDescription": "Bolivia holiday commemorating the country\u2019s dignity and sovereignty.",
        "longDescription": "N/A"
    },
    "Beni Day": {
        "shortDescription": "Departmental holiday celebrating the foundation of Beni Department, Bolivia.",
        "longDescription": "N/A"
    },
    "Cochabamba Day": {
        "shortDescription": "Departmental holiday for Cochabamba Department, Bolivia.",
        "longDescription": "N/A"
    },
    "Chuquisaca Day": {
        "shortDescription": "Departmental holiday for Chuquisaca Department, Bolivia.",
        "longDescription": "N/A"
    },
    "La Paz Day": {
        "shortDescription": "Departmental holiday celebrating the foundation of La Paz, Bolivia.",
        "longDescription": "N/A"
    },
    "Pando Day": {
        "shortDescription": "Departmental holiday for Pando Department, Bolivia.",
        "longDescription": "N/A"
    },
    "Carnival in Oruro": {
        "shortDescription": "Bolivia\u2019s UNESCO-recognized carnival, famous for traditional dances and costumes.",
        "longDescription": "N/A"
    },
    "Potos\u00ed Day": {
        "shortDescription": "Departmental holiday for Potos\u00ed, Bolivia, commemorating its founding.",
        "longDescription": "N/A"
    },
    "Santa Cruz Day": {
        "shortDescription": "Departmental holiday celebrating the founding of Santa Cruz, Bolivia.",
        "longDescription": "N/A"
    },
    "La Tablada": {
        "shortDescription": "Commemoration of the 1817 battle near Tarija in Bolivia\u2019s independence war.",
        "longDescription": "N/A"
    },
    "Rincon Day": {
        "shortDescription": "Holiday celebrating Rincon in Bonaire.",
        "longDescription": "N/A"
    },
    "Bonaire Day": {
        "shortDescription": "Bonaire\u2019s national holiday celebrating its heritage and culture.",
        "longDescription": "N/A"
    },
    "Bridge Holiday": {
        "shortDescription": "Additional day off used to create long weekends next to other holidays.",
        "longDescription": "N/A"
    },
    "Saba Day": {
        "shortDescription": "National holiday of Saba, Caribbean Netherlands, celebrated on the first Friday of December.",
        "longDescription": "N/A"
    },
    "Statia Day": {
        "shortDescription": "National holiday of Sint Eustatius, Caribbean Netherlands, celebrated on November 16.",
        "longDescription": "N/A"
    },
    "Catholic Good Friday; Orthodox Good Friday": {
        "shortDescription": "Christian observance of the crucifixion of Jesus Christ, observed by both Catholic and Orthodox churches.",
        "longDescription": "N/A"
    },
    "Catholic Easter Monday; Orthodox Easter Monday": {
        "shortDescription": "The day after Easter Sunday, celebrated by Catholics and Orthodox Christians with family gatherings and traditions.",
        "longDescription": "N/A"
    },
    "Orthodox Christmas Eve": {
        "shortDescription": "The evening before Christmas in the Orthodox Christian tradition, often marked by religious services and family meals.",
        "longDescription": "N/A"
    },
    "International Labor Day": {
        "shortDescription": "Global celebration of workers and the labor movement, observed on May 1 in many countries.",
        "longDescription": "N/A"
    },
    "Statehood Day": {
        "shortDescription": "Holiday commemorating the proclamation or recognition of statehood in a nation or region.",
        "longDescription": "N/A"
    },
    "Catholic Christmas Eve": {
        "shortDescription": "The evening before Christmas Day in Catholic tradition, often celebrated with midnight mass and family meals.",
        "longDescription": "N/A"
    },
    "Orthodox Good Friday": {
        "shortDescription": "Orthodox Christian observance of the crucifixion of Jesus Christ, held according to the Julian calendar.",
        "longDescription": "N/A"
    },
    "Catholic Easter Monday": {
        "shortDescription": "Public holiday in many Catholic countries marking the day after Easter Sunday.",
        "longDescription": "N/A"
    },
    "Day of establishment of Br\u010dko District": {
        "shortDescription": "Marks the creation of the autonomous Br\u010dko District within Bosnia and Herzegovina.",
        "longDescription": "N/A"
    },
    "Orthodox New Year": {
        "shortDescription": "Celebration of the new year according to the Julian calendar, often on January 14.",
        "longDescription": "N/A"
    },
    "Dayton Agreement Day": {
        "shortDescription": "Commemoration of the Dayton Peace Agreement, which ended the Bosnian War in 1995.",
        "longDescription": "N/A"
    },
    "New Year's Day Holiday": {
        "shortDescription": "Public holiday marking the first day of the new calendar year.",
        "longDescription": "N/A"
    },
    "Sir Seretse Khama Day": {
        "shortDescription": "Holiday in Botswana honoring the first president, Sir Seretse Khama.",
        "longDescription": "N/A"
    },
    "President's Day": {
        "shortDescription": "Holiday honoring the role and office of the president, observed in Botswana and other countries.",
        "longDescription": "N/A"
    },
    "President's Day Holiday": {
        "shortDescription": "Extended observance of President's Day in Botswana.",
        "longDescription": "N/A"
    },
    "Botswana Day": {
        "shortDescription": "National holiday celebrating Botswana's independence from Britain in 1966.",
        "longDescription": "N/A"
    },
    "Botswana Day Holiday": {
        "shortDescription": "Continuation of Botswana Day celebrations.",
        "longDescription": "N/A"
    },
    "Universal Fraternization Day": {
        "shortDescription": "Brazilian holiday observed on January 1 promoting peace, unity, and brotherhood.",
        "longDescription": "N/A"
    },
    "Tiradentes' Day": {
        "shortDescription": "Brazilian national holiday commemorating Joaquim Jos\u00e9 da Silva Xavier (Tiradentes), a leader of the independence movement executed in 1792.",
        "longDescription": "N/A"
    },
    "Worker's Day": {
        "shortDescription": "Celebration of labor rights and workers, observed on May 1 in Brazil.",
        "longDescription": "N/A"
    },
    "Our Lady of Aparecida": {
        "shortDescription": "Brazil\u2019s patron saint day, honoring Our Lady of Aparecida, celebrated on October 12.",
        "longDescription": "N/A"
    },
    "Republic Proclamation Day": {
        "shortDescription": "Commemorates the proclamation of the Brazilian Republic on November 15, 1889.",
        "longDescription": "N/A"
    },
    "National Day of Zumbi and Black Awareness": {
        "shortDescription": "Holiday recognizing Afro-Brazilian history, resistance to slavery, and honoring Zumbi dos Palmares.",
        "longDescription": "N/A"
    },
    "Evangelical Day": {
        "shortDescription": "Holiday recognizing Brazil\u2019s evangelical Christian communities.",
        "longDescription": "N/A"
    },
    "Founding of Acre": {
        "shortDescription": "Commemorates the annexation of Acre into Brazil following conflicts with Bolivia.",
        "longDescription": "N/A"
    },
    "Amazonia Day": {
        "shortDescription": "Holiday highlighting the cultural and ecological importance of the Amazon region.",
        "longDescription": "N/A"
    },
    "Signing of the Petropolis Treaty": {
        "shortDescription": "Marks the treaty in which Bolivia ceded Acre to Brazil in 1903.",
        "longDescription": "N/A"
    },
    "Saint John's Day": {
        "shortDescription": "Christian feast day celebrating Saint John the Baptist, marked by bonfires and festivities.",
        "longDescription": "N/A"
    },
    "Political Emancipation of Alagoas": {
        "shortDescription": "Commemorates Alagoas gaining political autonomy from Pernambuco in 1817.",
        "longDescription": "N/A"
    },
    "Elevation of Amazonas to province": {
        "shortDescription": "Marks the political elevation of Amazonas to provincial status in Brazil.",
        "longDescription": "N/A"
    },
    "Saint Joseph's Day": {
        "shortDescription": "Christian feast honoring Saint Joseph, husband of Mary.",
        "longDescription": "N/A"
    },
    "Creation of the Federal Territory": {
        "shortDescription": "Commemoration of the creation of certain federal territories in Brazil.",
        "longDescription": "N/A"
    },
    "Bahia Independence Day": {
        "shortDescription": "Celebrates Bahia\u2019s independence from Portuguese rule on July 2, 1823.",
        "longDescription": "N/A"
    },
    "Abolition of slavery in Cear\u00e1": {
        "shortDescription": "Marks Cear\u00e1 becoming the first Brazilian province to abolish slavery in 1884.",
        "longDescription": "N/A"
    },
    "Our Lady of Assumption": {
        "shortDescription": "Catholic feast of the Assumption of the Virgin Mary into Heaven.",
        "longDescription": "N/A"
    },
    "Founding of Brasilia; Tiradentes' Day": {
        "shortDescription": "Marks the inauguration of Brazil\u2019s capital, Bras\u00edlia, coinciding with Tiradentes' Day.",
        "longDescription": "N/A"
    },
    "Our Lady of Penha": {
        "shortDescription": "Holiday honoring Our Lady of Penha, a Marian devotion particularly celebrated in Esp\u00edrito Santo.",
        "longDescription": "N/A"
    },
    "Foundation of Goi\u00e1s city": {
        "shortDescription": "Marks the founding of the historic city of Goi\u00e1s, a former state capital.",
        "longDescription": "N/A"
    },
    "Foundation of Goi\u00e2nia": {
        "shortDescription": "Holiday marking the establishment of Goi\u00e2nia, capital of Goi\u00e1s state.",
        "longDescription": "N/A"
    },
    "Maranh\u00e3o joining to independence of Brazil": {
        "shortDescription": "Commemorates Maranh\u00e3o\u2019s adhesion to Brazil\u2019s independence movement in 1823.",
        "longDescription": "N/A"
    },
    "Tiradentes' Day; Tiradentes' Execution": {
        "shortDescription": "Commemoration of Tiradentes, a martyr of Brazilian independence, executed in 1792.",
        "longDescription": "N/A"
    },
    "State Creation Day": {
        "shortDescription": "Holiday marking the creation of a Brazilian state.",
        "longDescription": "N/A"
    },
    "Gr\u00e3o-Par\u00e1 joining to independence of Brazil": {
        "shortDescription": "Celebrates Gr\u00e3o-Par\u00e1 region\u2019s integration into Brazil\u2019s independence.",
        "longDescription": "N/A"
    },
    "State Founding Day": {
        "shortDescription": "Commemoration of the founding of a state within Brazil.",
        "longDescription": "N/A"
    },
    "Pernambuco Revolution": {
        "shortDescription": "Marks the 1817 revolution in Pernambuco against Portuguese colonial rule.",
        "longDescription": "N/A"
    },
    "Piau\u00ed Day": {
        "shortDescription": "Commemorates Piau\u00ed\u2019s declaration of support for Brazilian independence in 1823.",
        "longDescription": "N/A"
    },
    "Political Emancipation of Paran\u00e1": {
        "shortDescription": "Holiday marking Paran\u00e1\u2019s separation from S\u00e3o Paulo in 1853.",
        "longDescription": "N/A"
    },
    "Saint George's Day": {
        "shortDescription": "Feast day of Saint George, a popular saint in Brazil.",
        "longDescription": "N/A"
    },
    "Rio Grande do Norte Day": {
        "shortDescription": "Celebrates the creation and history of Rio Grande do Norte state.",
        "longDescription": "N/A"
    },
    "Urua\u00e7u and Cunha\u00fa Martyrs Day": {
        "shortDescription": "Honors Catholic martyrs killed in Rio Grande do Norte during Dutch invasions in the 17th century.",
        "longDescription": "N/A"
    },
    "Gaucho Day": {
        "shortDescription": "Celebrates gaucho culture and traditions in southern Brazil.",
        "longDescription": "N/A"
    },
    "Santa Catarina State Day": {
        "shortDescription": "Commemorates the state of Santa Catarina\u2019s history and foundation.",
        "longDescription": "N/A"
    },
    "Saint Catherine of Alexandria Day": {
        "shortDescription": "Catholic feast honoring Saint Catherine, patron saint of Santa Catarina state.",
        "longDescription": "N/A"
    },
    "Sergipe Political Emancipation Day": {
        "shortDescription": "Marks Sergipe\u2019s separation from Bahia in 1820.",
        "longDescription": "N/A"
    },
    "Constitutionalist Revolution": {
        "shortDescription": "Commemorates S\u00e3o Paulo\u2019s 1932 uprising demanding a new constitution.",
        "longDescription": "N/A"
    },
    "Autonomy Day": {
        "shortDescription": "Holiday recognizing a state\u2019s autonomy within Brazil.",
        "longDescription": "N/A"
    },
    "Our Lady of Nativity": {
        "shortDescription": "Catholic feast celebrating the birth of the Virgin Mary.",
        "longDescription": "N/A"
    },
    "Lavity Stoutt's Birthday": {
        "shortDescription": "Public holiday in the British Virgin Islands honoring the territory\u2019s first Chief Minister.",
        "longDescription": "N/A"
    },
    "Sovereign's Birthday": {
        "shortDescription": "Celebration of the reigning monarch\u2019s official birthday in the British Virgin Islands.",
        "longDescription": "N/A"
    },
    "Virgin Islands Day": {
        "shortDescription": "Holiday celebrating the culture and identity of the Virgin Islands.",
        "longDescription": "N/A"
    },
    "Emancipation Monday": {
        "shortDescription": "Marks the beginning of Emancipation Festival, commemorating the abolition of slavery in the Virgin Islands.",
        "longDescription": "N/A"
    },
    "Emancipation Tuesday": {
        "shortDescription": "Second day of Emancipation Festival celebrations.",
        "longDescription": "N/A"
    },
    "Emancipation Wednesday": {
        "shortDescription": "Third day of Emancipation Festival celebrations.",
        "longDescription": "N/A"
    },
    "Heroes and Foreparents Day": {
        "shortDescription": "Holiday honoring national heroes and ancestors of the Virgin Islands.",
        "longDescription": "N/A"
    },
    "The Great March of 1949 and Restoration Day": {
        "shortDescription": "Commemorates the protest march that led to constitutional reforms in the Virgin Islands.",
        "longDescription": "N/A"
    },
    "Lunar New Year": {
        "shortDescription": "Traditional new year celebration in East Asian cultures based on the lunar calendar.",
        "longDescription": "N/A"
    },
    "Sultan Hassanal Bolkiah's Birthday": {
        "shortDescription": "Public holiday in Brunei marking the birthday of the Sultan.",
        "longDescription": "N/A"
    },
    "Isra' and Mi'raj": {
        "shortDescription": "Islamic holiday marking the Prophet Muhammad\u2019s night journey and ascension.",
        "longDescription": "N/A"
    },
    "Anniversary of the revelation of the Quran": {
        "shortDescription": "Islamic holiday commemorating the first revelation of the Quran to Prophet Muhammad.",
        "longDescription": "N/A"
    },
    "Easter": {
        "shortDescription": "Christian holiday celebrating the resurrection of Jesus Christ.",
        "longDescription": "N/A"
    },
    "Labor Day and International Workers' Solidarity Day": {
        "shortDescription": "Holiday celebrating workers and labor rights.",
        "longDescription": "N/A"
    },
    "Day of Slavonic Alphabet, Bulgarian Enlightenment and Culture": {
        "shortDescription": "Holiday in Bulgaria celebrating literacy, education, and Slavic culture.",
        "longDescription": "N/A"
    },
    "Unification Day": {
        "shortDescription": "Commemoration of Bulgaria\u2019s unification in 1885.",
        "longDescription": "N/A"
    },
    "Proclamation of Independence Day": {
        "shortDescription": "Marks Bulgaria\u2019s declaration of independence in 1908.",
        "longDescription": "N/A"
    },
    "Mawlid": {
        "shortDescription": "Islamic holiday marking the birthday of the Prophet Muhammad.",
        "longDescription": "N/A"
    },
    "Unity Day": {
        "shortDescription": "Holiday celebrating national unity and identity.",
        "longDescription": "N/A"
    },
    "Commemoration of the Assassination of President Cyprien Ntaryamira": {
        "shortDescription": "Burundi holiday honoring the president assassinated in 1994.",
        "longDescription": "N/A"
    },
    "National Day of Patriotism and Commemoration of the Death of President Pierre Nkurunziza": {
        "shortDescription": "Burundi holiday honoring the late president and celebrating patriotism.",
        "longDescription": "N/A"
    },
    "Commemoration of the Assassination of National Hero, Prince Louis Rwagasore": {
        "shortDescription": "Burundi holiday honoring independence leader Prince Louis Rwagasore, assassinated in 1961.",
        "longDescription": "N/A"
    },
    "Commemoration of the Assassination of President Melchior Ndadaye": {
        "shortDescription": "Holiday remembering Burundi\u2019s first democratically elected president, killed in 1993.",
        "longDescription": "N/A"
    },
    "Democracy and Freedom Day": {
        "shortDescription": "Burundi national holiday celebrating democracy and liberty.",
        "longDescription": "N/A"
    },
    "Ash Wednesday": {
        "shortDescription": "Christian observance marking the beginning of Lent.",
        "longDescription": "N/A"
    },
    "International Children's Day": {
        "shortDescription": "Global celebration promoting children\u2019s rights and welfare.",
        "longDescription": "N/A"
    },
    "Brava Municipality Day": {
        "shortDescription": "Local holiday in Cape Verde celebrating the municipality of Brava.",
        "longDescription": "N/A"
    },
    "Boa Vista Municipality Day": {
        "shortDescription": "Holiday marking the founding or identity of Boa Vista municipality in Cape Verde.",
        "longDescription": "N/A"
    },
    "Santa Catarina de Santiago Municipality Day": {
        "shortDescription": "Celebration of Santa Catarina de Santiago municipality in Cape Verde.",
        "longDescription": "N/A"
    },
    "Santa Catarina do Fogo Municipality Day": {
        "shortDescription": "Holiday for the municipality of Santa Catarina do Fogo in Cape Verde.",
        "longDescription": "N/A"
    },
    "Santa Cruz Municipality Day": {
        "shortDescription": "Local holiday in Cape Verde celebrating Santa Cruz municipality.",
        "longDescription": "N/A"
    },
    "Maio Municipality Day": {
        "shortDescription": "Cape Verde holiday for Maio municipality.",
        "longDescription": "N/A"
    },
    "Assumption Day; Mosteiros Municipality Day": {
        "shortDescription": "Catholic feast of the Assumption combined with Mosteiros Municipality Day in Cape Verde.",
        "longDescription": "N/A"
    },
    "Santo Ant\u00e3o Island Day": {
        "shortDescription": "Holiday in Cape Verde celebrating the island of Santo Ant\u00e3o.",
        "longDescription": "N/A"
    },
    "Pa\u00fal Municipality Day": {
        "shortDescription": "Local holiday celebrating Pa\u00fal municipality in Cape Verde.",
        "longDescription": "N/A"
    },
    "Porto Novo Municipality Day": {
        "shortDescription": "Holiday honoring Porto Novo municipality in Cape Verde.",
        "longDescription": "N/A"
    },
    "Praia Municipality Day": {
        "shortDescription": "Celebration of the capital city municipality, Praia, in Cape Verde.",
        "longDescription": "N/A"
    },
    "Ribeira Brava Municipality Day": {
        "shortDescription": "Local holiday in Cape Verde for Ribeira Brava municipality.",
        "longDescription": "N/A"
    },
    "Ribeira Grande Municipality Day": {
        "shortDescription": "Cape Verde holiday celebrating Ribeira Grande municipality.",
        "longDescription": "N/A"
    },
    "Ribeira Grande de Santiago Municipality Day": {
        "shortDescription": "Holiday honoring Ribeira Grande de Santiago municipality in Cape Verde.",
        "longDescription": "N/A"
    },
    "S\u00e3o Domingos Municipality Day": {
        "shortDescription": "Municipal holiday in Cape Verde for S\u00e3o Domingos.",
        "longDescription": "N/A"
    },
    "S\u00e3o Filipe Municipality Day; Worker's Day": {
        "shortDescription": "Celebration in the municipality of S\u00e3o Filipe, coinciding with International Workers\u2019 Day on May 1st, honoring labor rights and the community\u2019s heritage.",
        "longDescription": "N/A"
    },
    "Sal Municipality Day": {
        "shortDescription": "Local holiday in Sal, Cape Verde, dedicated to the municipality\u2019s cultural identity and community achievements.",
        "longDescription": "N/A"
    },
    "S\u00e3o Miguel Municipality Day": {
        "shortDescription": "Day recognizing the founding and culture of S\u00e3o Miguel municipality in Cape Verde.",
        "longDescription": "N/A"
    },
    "S\u00e3o Louren\u00e7o dos \u00d3rg\u00e3os Municipality Day": {
        "shortDescription": "Holiday honoring the traditions and community of S\u00e3o Louren\u00e7o dos \u00d3rg\u00e3os municipality in Cape Verde.",
        "longDescription": "N/A"
    },
    "S\u00e3o Salvador do Mundo Municipality Day": {
        "shortDescription": "Day celebrating the creation, culture, and identity of S\u00e3o Salvador do Mundo municipality in Cape Verde.",
        "longDescription": "N/A"
    },
    "S\u00e3o Vicente Municipality Day": {
        "shortDescription": "Holiday marking the founding and development of S\u00e3o Vicente municipality in Cape Verde.",
        "longDescription": "N/A"
    },
    "Tarrafal de Santiago Municipality Day": {
        "shortDescription": "Celebration of Tarrafal de Santiago\u2019s community, culture, and municipal history.",
        "longDescription": "N/A"
    },
    "Tarrafal de S\u00e3o Nicolau Municipality Day": {
        "shortDescription": "Local holiday dedicated to the culture and history of Tarrafal de S\u00e3o Nicolau municipality.",
        "longDescription": "N/A"
    },
    "International New Year Day": {
        "shortDescription": "Observed worldwide on January 1st, marking the start of the new calendar year.",
        "longDescription": "N/A"
    },
    "Day of Victory over the Genocidal Regime": {
        "shortDescription": "Cambodian holiday remembering the overthrow of the Khmer Rouge regime in 1979.",
        "longDescription": "N/A"
    },
    "International Women's Rights Day": {
        "shortDescription": "Observed globally on March 8th, celebrating women\u2019s achievements and advocating for gender equality.",
        "longDescription": "N/A"
    },
    "Khmer New Year's Day": {
        "shortDescription": "Major Cambodian festival held in April, marking the traditional solar new year with cultural rituals and celebrations.",
        "longDescription": "N/A"
    },
    "HM King Norodom Sihamoni's Birthday": {
        "shortDescription": "National holiday in Cambodia honoring the reigning king\u2019s birthday.",
        "longDescription": "N/A"
    },
    "HM Queen Norodom Monineath Sihanouk the Queen-Mother's Birthday": {
        "shortDescription": "Holiday celebrating the birthday of Cambodia\u2019s Queen Mother.",
        "longDescription": "N/A"
    },
    "HM King Norodom Sihanouk Mourning Day": {
        "shortDescription": "Day of remembrance for the late King Norodom Sihanouk of Cambodia.",
        "longDescription": "N/A"
    },
    "HM King Norodom Sihamoni's Coronation Day": {
        "shortDescription": "Holiday marking the coronation of King Norodom Sihamoni in Cambodia.",
        "longDescription": "N/A"
    },
    "Visaka Bochea Day": {
        "shortDescription": "Buddhist holiday in Cambodia commemorating the birth, enlightenment, and death of the Buddha.",
        "longDescription": "N/A"
    },
    "Royal Ploughing Ceremony": {
        "shortDescription": "Traditional Cambodian ceremony marking the beginning of the rice-growing season.",
        "longDescription": "N/A"
    },
    "Pchum Ben Day": {
        "shortDescription": "Buddhist religious holiday in Cambodia where families honor their ancestors through offerings.",
        "longDescription": "N/A"
    },
    "Water Festival": {
        "shortDescription": "Major Cambodian festival celebrating the reversal of the Tonl\u00e9 Sap River current, featuring boat races and cultural events.",
        "longDescription": "N/A"
    },
    "Peace Day in Cambodia": {
        "shortDescription": "Holiday marking the Paris Peace Agreements of 1991 that ended years of conflict in Cambodia.",
        "longDescription": "N/A"
    },
    "Youth Day": {
        "shortDescription": "Celebration of young people\u2019s contributions to national development, observed in several countries.",
        "longDescription": "N/A"
    },
    "Canada Day": {
        "shortDescription": "Canada\u2019s national holiday on July 1st, marking the confederation of the country in 1867.",
        "longDescription": "N/A"
    },
    "Family Day": {
        "shortDescription": "Canadian holiday emphasizing family time, observed on varying dates in several provinces.",
        "longDescription": "N/A"
    },
    "Victoria Day": {
        "shortDescription": "Canadian holiday in May celebrating Queen Victoria\u2019s birthday and the start of summer.",
        "longDescription": "N/A"
    },
    "British Columbia Day": {
        "shortDescription": "Provincial holiday in British Columbia celebrating local heritage and community pride.",
        "longDescription": "N/A"
    },
    "National Day for Truth and Reconciliation": {
        "shortDescription": "Canadian holiday on September 30th honoring survivors of residential schools and Indigenous reconciliation.",
        "longDescription": "N/A"
    },
    "Louis Riel Day": {
        "shortDescription": "Holiday in Manitoba honoring M\u00e9tis leader Louis Riel, observed on the third Monday of February.",
        "longDescription": "N/A"
    },
    "New Brunswick Day": {
        "shortDescription": "Provincial holiday in New Brunswick celebrating local history and culture.",
        "longDescription": "N/A"
    },
    "Canada Day; Memorial Day": {
        "shortDescription": "Joint observance in Newfoundland and Labrador combining Canada Day with remembrance of soldiers fallen in WWI.",
        "longDescription": "N/A"
    },
    "Heritage Day": {
        "shortDescription": "Holiday in Nova Scotia celebrating cultural diversity and community heritage.",
        "longDescription": "N/A"
    },
    "National Aboriginal Day": {
        "shortDescription": "Canadian holiday (now National Indigenous Peoples Day) recognizing the cultures and contributions of First Nations, Inuit, and M\u00e9tis.",
        "longDescription": "N/A"
    },
    "Civic Holiday": {
        "shortDescription": "General holiday observed across many Canadian provinces in early August, often under different local names.",
        "longDescription": "N/A"
    },
    "Nunavut Day": {
        "shortDescription": "Holiday marking the creation of Nunavut as a Canadian territory on July 9, 1999.",
        "longDescription": "N/A"
    },
    "Islander Day": {
        "shortDescription": "Holiday in Prince Edward Island focusing on family and community life, observed in February.",
        "longDescription": "N/A"
    },
    "National Patriots' Day": {
        "shortDescription": "Quebec holiday honoring the 1837\u20131838 Patriotes who fought for democratic rights.",
        "longDescription": "N/A"
    },
    "Saint John the Baptist Day": {
        "shortDescription": "Quebec\u2019s national holiday on June 24th, celebrating French-Canadian culture and identity.",
        "longDescription": "N/A"
    },
    "Saskatchewan Day": {
        "shortDescription": "Provincial holiday in Saskatchewan celebrating local history and culture.",
        "longDescription": "N/A"
    },
    "Discovery Day": {
        "shortDescription": "Holiday in Yukon marking the discovery of gold in the Klondike in 1896.",
        "longDescription": "N/A"
    },
    "General Election Day": {
        "shortDescription": "Public holiday in Canada to facilitate voter participation during federal elections.",
        "longDescription": "N/A"
    },
    "Barth\u00e9lemy Boganda Day": {
        "shortDescription": "Central African Republic holiday honoring Barth\u00e9lemy Boganda, the nation\u2019s founding father.",
        "longDescription": "N/A"
    },
    "General Prayer Day": {
        "shortDescription": "Religious day of prayer and reflection, observed in several Christian-majority nations.",
        "longDescription": "N/A"
    },
    "Freedom and Democracy Day": {
        "shortDescription": "Holiday commemorating democratic movements and the restoration of civil liberties.",
        "longDescription": "N/A"
    },
    "Navy Day": {
        "shortDescription": "Celebration honoring the naval forces of a country and their service.",
        "longDescription": "N/A"
    },
    "National Day of Indigenous Peoples": {
        "shortDescription": "Holiday recognizing the rights, heritage, and contributions of Indigenous communities.",
        "longDescription": "N/A"
    },
    "Saint Peter and Saint Paul's Day": {
        "shortDescription": "Christian feast honoring apostles Peter and Paul.",
        "longDescription": "N/A"
    },
    "Our Lady of Mount Carmel": {
        "shortDescription": "Catholic feast day venerating the Virgin Mary under the title of Our Lady of Mount Carmel.",
        "longDescription": "N/A"
    },
    "Meeting of Two Worlds' Day": {
        "shortDescription": "Commemoration of the encounter between Europeans and Indigenous peoples in the Americas.",
        "longDescription": "N/A"
    },
    "Reformation Day": {
        "shortDescription": "Protestant Christian holiday commemorating Martin Luther\u2019s Reformation in 1517.",
        "longDescription": "N/A"
    },
    "Assault and Capture of Cape Arica": {
        "shortDescription": "Chilean holiday marking a key victory in the War of the Pacific in 1880.",
        "longDescription": "N/A"
    },
    "Nativity of Bernardo O'Higgins": {
        "shortDescription": "Holiday celebrating the birth of Bernardo O\u2019Higgins, Chile\u2019s independence leader.",
        "longDescription": "N/A"
    },
    "Chinese New Year": {
        "shortDescription": "Major traditional festival celebrating the start of the lunar new year in Chinese culture.",
        "longDescription": "N/A"
    },
    "Chinese New Year's Eve": {
        "shortDescription": "Eve of the Chinese New Year, marked with family reunions and traditions.",
        "longDescription": "N/A"
    },
    "Tomb-Sweeping Day": {
        "shortDescription": "Chinese festival where families clean ancestors\u2019 graves and make offerings.",
        "longDescription": "N/A"
    },
    "Dragon Boat Festival": {
        "shortDescription": "Chinese holiday featuring dragon boat races and rice dumplings, honoring poet Qu Yuan.",
        "longDescription": "N/A"
    },
    "Mid-Autumn Festival": {
        "shortDescription": "Chinese harvest festival celebrating the full moon with lanterns and mooncakes.",
        "longDescription": "N/A"
    },
    "Territory Day": {
        "shortDescription": "Holiday in Northern Territory, Australia, marking self-government in 1978.",
        "longDescription": "N/A"
    },
    "Act of Self Determination Day": {
        "shortDescription": "Commemoration in New Caledonia of the 1987 referendum on independence.",
        "longDescription": "N/A"
    },
    "Sacred Heart; Saint Peter and Saint Paul's Day": {
        "shortDescription": "Religious feast honoring the Sacred Heart of Jesus and apostles Peter and Paul.",
        "longDescription": "N/A"
    },
    "Battle of Boyac\u00e1": {
        "shortDescription": "Colombian holiday commemorating the 1819 battle that secured independence from Spain.",
        "longDescription": "N/A"
    },
    "Independence of Cartagena": {
        "shortDescription": "Colombian holiday celebrating Cartagena\u2019s declaration of independence from Spain in 1811.",
        "longDescription": "N/A"
    },
    "Cheikh al Maarouf Day": {
        "shortDescription": "Comorian holiday honoring religious leader Cheikh al Maarouf.",
        "longDescription": "N/A"
    },
    "Maore Day": {
        "shortDescription": "Comorian day commemorating claims over Mayotte (Maore).",
        "longDescription": "N/A"
    },
    "Election Partial Day Holiday": {
        "shortDescription": "Special holiday allowing citizens to participate in partial elections.",
        "longDescription": "N/A"
    },
    "Day after New Year's Day": {
        "shortDescription": "Observed in some countries as a continuation of New Year festivities on January 2nd.",
        "longDescription": "N/A"
    },
    "Anzac Day": {
        "shortDescription": "Holiday in Australia and New Zealand honoring soldiers who served and died in wars, especially Gallipoli.",
        "longDescription": "N/A"
    },
    "Day of the House of Ariki": {
        "shortDescription": "Cook Islands holiday recognizing the traditional council of chiefs.",
        "longDescription": "N/A"
    },
    "Cook Islands Gospel Day": {
        "shortDescription": "Holiday celebrating the arrival of Christianity in the Cook Islands.",
        "longDescription": "N/A"
    },
    "Juan Santamar\u00eda Day": {
        "shortDescription": "Costa Rican holiday honoring national hero Juan Santamar\u00eda, who died in the Battle of Rivas in 1856.",
        "longDescription": "N/A"
    },
    "Annexation of the Party of Nicoya to Costa Rica": {
        "shortDescription": "Costa Rican holiday marking the 1824 annexation of Nicoya from Nicaragua.",
        "longDescription": "N/A"
    },
    "Mother's Day": {
        "shortDescription": "Holiday honoring mothers and motherhood, celebrated on different dates worldwide.",
        "longDescription": "N/A"
    },
    "Anti-Fascist Struggle Day": {
        "shortDescription": "Croatian holiday commemorating the resistance against fascism during World War II.",
        "longDescription": "N/A"
    },
    "Victory and Homeland Thanksgiving Day and Croatian Veterans Day": {
        "shortDescription": "Holiday in Croatia marking victory in the Homeland War and honoring veterans.",
        "longDescription": "N/A"
    },
    "Commemoration of the Assault of the Moncada garrison": {
        "shortDescription": "Cuban holiday remembering the 1953 attack that sparked the Cuban Revolution.",
        "longDescription": "N/A"
    },
    "Day of the National Rebellion": {
        "shortDescription": "Cuban holiday marking the beginning of the revolution against Batista in 1953.",
        "longDescription": "N/A"
    },
    "Cura\u00e7ao Day": {
        "shortDescription": "Holiday celebrating Cura\u00e7ao\u2019s autonomy within the Kingdom of the Netherlands.",
        "longDescription": "N/A"
    },
    "Green Monday": {
        "shortDescription": "Cypriot holiday marking the start of Lent with outdoor picnics and kite flying.",
        "longDescription": "N/A"
    },
    "Greek Independence Day": {
        "shortDescription": "Holiday celebrating Greece\u2019s declaration of independence from the Ottoman Empire in 1821.",
        "longDescription": "N/A"
    },
    "Cyprus National Day": {
        "shortDescription": "Holiday marking the start of the Greek Cypriot struggle for independence from Britain in 1955.",
        "longDescription": "N/A"
    },
    "Cyprus Independence Day": {
        "shortDescription": "Cypriot holiday celebrating independence from the United Kingdom in 1960.",
        "longDescription": "N/A"
    },
    "Greek National Day": {
        "shortDescription": "Greece\u2019s national holiday on March 25, commemorating the start of the War of Independence against Ottoman rule in 1821.",
        "longDescription": "N/A"
    },
    "Day After Christmas": {
        "shortDescription": "Public holiday observed on December 26, often serving as a continuation of Christmas celebrations.",
        "longDescription": "N/A"
    },
    "Independent Czech State Restoration Day; New Year's Day": {
        "shortDescription": "Czech holiday on January 1 marking both the new year and the restoration of Czech independence in 1993.",
        "longDescription": "N/A"
    },
    "Saints Cyril and Methodius Day": {
        "shortDescription": "Holiday celebrating the two Byzantine brothers who created the Glagolitic alphabet and spread Christianity among the Slavs.",
        "longDescription": "N/A"
    },
    "Jan Hus Day": {
        "shortDescription": "Czech holiday on July 6 honoring reformer Jan Hus, who was executed for his religious teachings in 1415.",
        "longDescription": "N/A"
    },
    "Independent Czechoslovak State Day": {
        "shortDescription": "Holiday on October 28 marking the creation of Czechoslovakia in 1918.",
        "longDescription": "N/A"
    },
    "Struggle for Freedom and Democracy Day and International Students' Day": {
        "shortDescription": "Czech holiday on November 17 commemorating student protests in 1939 and 1989 against oppression.",
        "longDescription": "N/A"
    },
    "Independence Day Holiday": {
        "shortDescription": "General public holiday commemorating a nation\u2019s independence from colonial or foreign rule.",
        "longDescription": "N/A"
    },
    "Arafat Day": {
        "shortDescription": "Islamic holy day observed on the second day of the Hajj pilgrimage at Mount Arafat, preceding Eid al-Adha.",
        "longDescription": "N/A"
    },
    "Prophet Muhammad's Birthday": {
        "shortDescription": "Islamic holiday celebrating the birth of the Prophet Muhammad, known as Mawlid al-Nabi.",
        "longDescription": "N/A"
    },
    "National Day of Community Service": {
        "shortDescription": "Holiday encouraging citizens to participate in volunteer work and civic improvement.",
        "longDescription": "N/A"
    },
    "Lady of Altagracia": {
        "shortDescription": "Dominican Republic holiday on January 21 honoring Our Lady of Altagracia, the country\u2019s patron saint.",
        "longDescription": "N/A"
    },
    "Juan Pablo Duarte Day": {
        "shortDescription": "Dominican Republic holiday celebrating the birth of Juan Pablo Duarte, one of the nation\u2019s founding fathers.",
        "longDescription": "N/A"
    },
    "Restoration Day": {
        "shortDescription": "Dominican Republic holiday on August 16 marking the start of the 1863 war that restored independence from Spain.",
        "longDescription": "N/A"
    },
    "Our Lady of Mercedes Day": {
        "shortDescription": "Religious holiday in the Dominican Republic honoring Our Lady of Mercy, patroness of the nation.",
        "longDescription": "N/A"
    },
    "National Hero Laurent D\u00e9sir\u00e9 Kabila Day": {
        "shortDescription": "Holiday in the Democratic Republic of Congo honoring the former president Laurent-D\u00e9sir\u00e9 Kabila, assassinated in 2001.",
        "longDescription": "N/A"
    },
    "National Hero Patrice Emery Lumumba Day": {
        "shortDescription": "Holiday in the Democratic Republic of Congo honoring independence leader Patrice Lumumba.",
        "longDescription": "N/A"
    },
    "Day of the Struggle of Simon Kimbangu and African Consciousness": {
        "shortDescription": "Commemoration in the DRC of Simon Kimbangu, religious leader and anti-colonial figure, and African identity.",
        "longDescription": "N/A"
    },
    "Revolution and Armed Forces Day": {
        "shortDescription": "Cuban holiday on December 2 marking the landing of Fidel Castro and his rebels in 1956.",
        "longDescription": "N/A"
    },
    "Parents' Day": {
        "shortDescription": "Holiday celebrating parents and their role in family and society, observed on varying dates worldwide.",
        "longDescription": "N/A"
    },
    "Congolese Genocide Memorial Day": {
        "shortDescription": "Day of remembrance for victims of mass atrocities in the Democratic Republic of Congo.",
        "longDescription": "N/A"
    },
    "The Battle of Pichincha": {
        "shortDescription": "Ecuadorian holiday commemorating the 1822 battle that secured Quito\u2019s independence from Spanish rule.",
        "longDescription": "N/A"
    },
    "Declaration of Independence of Quito": {
        "shortDescription": "Holiday marking Quito\u2019s declaration of independence from Spain on August 10, 1809.",
        "longDescription": "N/A"
    },
    "Independence of Guayaquil": {
        "shortDescription": "Holiday celebrating Guayaquil\u2019s independence from Spain on October 9, 1820.",
        "longDescription": "N/A"
    },
    "Independence of Cuenca": {
        "shortDescription": "Holiday commemorating the independence of Cuenca, Ecuador, on November 3, 1820.",
        "longDescription": "N/A"
    },
    "Coptic Christmas Day": {
        "shortDescription": "Christian holiday observed on January 7 by Coptic Orthodox Christians, celebrating the birth of Jesus Christ.",
        "longDescription": "N/A"
    },
    "January 25th Revolution and National Police Day": {
        "shortDescription": "Egyptian holiday marking both the 2011 revolution and National Police Day.",
        "longDescription": "N/A"
    },
    "Sinai Liberation Day": {
        "shortDescription": "Egyptian holiday on April 25 marking the final withdrawal of Israeli troops from Sinai in 1982.",
        "longDescription": "N/A"
    },
    "June 30 Revolution Day": {
        "shortDescription": "Egyptian holiday commemorating the 2013 protests that led to the ousting of President Mohamed Morsi.",
        "longDescription": "N/A"
    },
    "July 23 Revolution Day": {
        "shortDescription": "Egyptian holiday marking the 1952 revolution that ended the monarchy and established a republic.",
        "longDescription": "N/A"
    },
    "Father's Day": {
        "shortDescription": "Holiday honoring fathers and fatherhood, observed on varying dates worldwide.",
        "longDescription": "N/A"
    },
    "Celebrations of San Salvador": {
        "shortDescription": "Festivities in El Salvador honoring Jesus Christ, the Divine Savior of the World, patron of the country.",
        "longDescription": "N/A"
    },
    "Feast of San Salvador": {
        "shortDescription": "Religious holiday in El Salvador dedicated to the nation\u2019s patron, the Divine Savior of the World.",
        "longDescription": "N/A"
    },
    "African Liberation Day": {
        "shortDescription": "Pan-African holiday observed on May 25 celebrating the progress of African independence movements.",
        "longDescription": "N/A"
    },
    "Patron Saint Festival of Annob\u00f3n": {
        "shortDescription": "Local festival in Equatorial Guinea honoring the patron saint of Annob\u00f3n Island.",
        "longDescription": "N/A"
    },
    "Orthodox Christmas": {
        "shortDescription": "Christian holiday on January 7 celebrating the birth of Jesus, observed by Orthodox churches.",
        "longDescription": "N/A"
    },
    "Orthodox Easter": {
        "shortDescription": "Christian holiday celebrating the resurrection of Jesus, observed according to the Orthodox calendar.",
        "longDescription": "N/A"
    },
    "Ethiopian New Year": {
        "shortDescription": "Holiday marking the Ethiopian New Year (Enkutatash), celebrated in September.",
        "longDescription": "N/A"
    },
    "Finding of the True Cross": {
        "shortDescription": "Ethiopian Orthodox holiday celebrating the discovery of the cross on which Jesus was crucified.",
        "longDescription": "N/A"
    },
    "Spring Day": {
        "shortDescription": "Seasonal holiday marking the arrival of spring and renewal of nature.",
        "longDescription": "N/A"
    },
    "Independence Restoration Day": {
        "shortDescription": "Holiday marking the restoration of independence after foreign occupation.",
        "longDescription": "N/A"
    },
    "Birthday of Late King Sobhuza": {
        "shortDescription": "Eswatini holiday celebrating the birthday of King Sobhuza II, who led the nation to independence.",
        "longDescription": "N/A"
    },
    "Adwa Victory Day": {
        "shortDescription": "Ethiopian holiday commemorating the 1896 victory over Italian forces at the Battle of Adwa.",
        "longDescription": "N/A"
    },
    "Ethiopian Patriots' Victory Day": {
        "shortDescription": "Holiday celebrating Ethiopia\u2019s liberation from Italian occupation in 1941.",
        "longDescription": "N/A"
    },
    "Downfall of the Dergue Regime Day": {
        "shortDescription": "Ethiopian holiday commemorating the 1991 fall of the Derg dictatorship.",
        "longDescription": "N/A"
    },
    "Finding of True Cross": {
        "shortDescription": "Ethiopian Orthodox holiday celebrating the discovery of the cross of Christ.",
        "longDescription": "N/A"
    },
    "Peat Cutting Day": {
        "shortDescription": "Traditional holiday in the Falkland Islands marking the start of the peat-cutting season.",
        "longDescription": "N/A"
    },
    "Christmas Holiday": {
        "shortDescription": "Public holiday celebrating the birth of Jesus Christ.",
        "longDescription": "N/A"
    },
    "Great Prayer Day": {
        "shortDescription": "Danish holiday dedicated to prayer, reflection, and church services, traditionally held in spring.",
        "longDescription": "N/A"
    },
    "Saint Olaf's Day": {
        "shortDescription": "Holiday honoring Saint Olaf, patron saint of Norway, celebrated on July 29.",
        "longDescription": "N/A"
    },
    "Girmit Day": {
        "shortDescription": "Fijian holiday commemorating the arrival of Indian indentured laborers to Fiji.",
        "longDescription": "N/A"
    },
    "Ratu Sir Lala Sukuna Day": {
        "shortDescription": "Fijian holiday honoring statesman Ratu Sir Lala Sukuna, considered the father of modern Fiji.",
        "longDescription": "N/A"
    },
    "Fiji Day": {
        "shortDescription": "Fijian national holiday on October 10 marking independence from the United Kingdom in 1970.",
        "longDescription": "N/A"
    },
    "Diwali": {
        "shortDescription": "Hindu festival of lights celebrating the victory of light over darkness and good over evil.",
        "longDescription": "N/A"
    },
    "Prophet Mohammed's Birthday": {
        "shortDescription": "Islamic holiday marking the birth of the Prophet Muhammad, known as Mawlid.",
        "longDescription": "N/A"
    },
    "Mi-Careme": {
        "shortDescription": "Mid-Lent festival celebrated with costumes and festivities in French-speaking regions.",
        "longDescription": "N/A"
    },
    "Abolition of Slavery": {
        "shortDescription": "Holiday commemorating the abolition of slavery in territories once under colonial rule.",
        "longDescription": "N/A"
    },
    "Victor Schoelcher Day": {
        "shortDescription": "French Caribbean holiday honoring Victor Schoelcher, who worked for the abolition of slavery.",
        "longDescription": "N/A"
    },
    "Citizenship Day": {
        "shortDescription": "Holiday dedicated to celebrating civic responsibility and national identity.",
        "longDescription": "N/A"
    },
    "Missionary Day": {
        "shortDescription": "Holiday recognizing the work of Christian missionaries in spreading faith and education.",
        "longDescription": "N/A"
    },
    "Mat\u0101ri'i": {
        "shortDescription": "Traditional Polynesian celebration in Tahiti marking the Pleiades constellation and the beginning of the harvest season.",
        "longDescription": "N/A"
    },
    "Feast of Saint Peter Chanel": {
        "shortDescription": "Holiday honoring Saint Peter Chanel, missionary and martyr, patron saint of Oceania.",
        "longDescription": "N/A"
    },
    "Saints Peter and Paul Day": {
        "shortDescription": "Christian feast day celebrating the apostles Peter and Paul.",
        "longDescription": "N/A"
    },
    "Women's Rights Day": {
        "shortDescription": "Holiday promoting gender equality and recognizing women\u2019s achievements.",
        "longDescription": "N/A"
    },
    "Africa Liberation Day": {
        "shortDescription": "Pan-African holiday commemorating the progress of independence movements across Africa.",
        "longDescription": "N/A"
    },
    "July 22 Revolution Day": {
        "shortDescription": "Egyptian holiday marking the July 1952 revolution that ended the monarchy.",
        "longDescription": "N/A"
    },
    "Laylat al-Qadr": {
        "shortDescription": "Islamic holy night during Ramadan commemorating the first revelation of the Quran to Muhammad.",
        "longDescription": "N/A"
    },
    "National Unity Day": {
        "shortDescription": "Holiday promoting national cohesion and unity among citizens.",
        "longDescription": "N/A"
    },
    "Day of Victory over Fascism": {
        "shortDescription": "Holiday commemorating the Allied victory over fascism in World War II.",
        "longDescription": "N/A"
    },
    "Saint Andrew's Day": {
        "shortDescription": "Christian feast honoring Saint Andrew, patron saint of Scotland and other countries.",
        "longDescription": "N/A"
    },
    "Day of Family Sanctity and Respect for Parents": {
        "shortDescription": "Holiday promoting the importance of family values and honoring parents.",
        "longDescription": "N/A"
    },
    "Dormition of the Mother of God": {
        "shortDescription": "Orthodox Christian feast marking the Virgin Mary\u2019s death and assumption into heaven.",
        "longDescription": "N/A"
    },
    "Holiday of Svetitskhovloba, Robe of Jesus": {
        "shortDescription": "Georgian Orthodox holiday commemorating the Svetitskhoveli Cathedral and the robe of Christ.",
        "longDescription": "N/A"
    },
    "Public Holiday": {
        "shortDescription": "General designation for a government-declared non-working day.",
        "longDescription": "N/A"
    },
    "German Unity Day": {
        "shortDescription": "German national holiday on October 3 marking the reunification of East and West Germany in 1990.",
        "longDescription": "N/A"
    },
    "80th anniversary of the liberation from Nazism and the end of the Second World War in Europe": {
        "shortDescription": "Commemoration marking 80 years since the defeat of Nazi Germany in 1945.",
        "longDescription": "N/A"
    },
    "Repentance and Prayer Day": {
        "shortDescription": "German Protestant holiday dedicated to prayer and reflection.",
        "longDescription": "N/A"
    },
    "World Children's Day": {
        "shortDescription": "International day promoting children\u2019s rights, well-being, and protection.",
        "longDescription": "N/A"
    },
    "Augsburg Peace Festival": {
        "shortDescription": "German holiday celebrating the 1555 Peace of Augsburg, promoting religious coexistence.",
        "longDescription": "N/A"
    },
    "Eid ul-Fitr": {
        "shortDescription": "Islamic festival marking the end of Ramadan, celebrated with prayers, feasts, and charity.",
        "longDescription": "N/A"
    },
    "Eid ul-Adha": {
        "shortDescription": "Islamic festival commemorating the willingness of Ibrahim to sacrifice his son.",
        "longDescription": "N/A"
    },
    "Founders' Day": {
        "shortDescription": "Public holiday honoring the founding fathers of Ghana.",
        "longDescription": "N/A"
    },
    "Kwame Nkrumah Memorial Day": {
        "shortDescription": "Day honoring Ghana\u2019s first president, Kwame Nkrumah.",
        "longDescription": "N/A"
    },
    "Farmer's Day": {
        "shortDescription": "Celebration of farmers and agriculture in Ghana.",
        "longDescription": "N/A"
    },
    "Winter Midterm Bank Holiday": {
        "shortDescription": "School midterm break observed as a holiday.",
        "longDescription": "N/A"
    },
    "Workers' Memorial Day": {
        "shortDescription": "Commemoration of workers who died or were injured on the job.",
        "longDescription": "N/A"
    },
    "Spring Bank Holiday": {
        "shortDescription": "Public holiday marking the late May break in the UK.",
        "longDescription": "N/A"
    },
    "Late Summer Bank Holiday": {
        "shortDescription": "Public holiday marking the late August break in the UK.",
        "longDescription": "N/A"
    },
    "Gibraltar National Day": {
        "shortDescription": "Celebration of Gibraltar\u2019s self-determination.",
        "longDescription": "N/A"
    },
    "Ochi Day": {
        "shortDescription": "Greek holiday commemorating refusal of Mussolini\u2019s ultimatum in 1940.",
        "longDescription": "N/A"
    },
    "Glorifying Mother of God": {
        "shortDescription": "Religious feast dedicated to the Virgin Mary.",
        "longDescription": "N/A"
    },
    "Guam Discovery Day": {
        "shortDescription": "Commemoration of the discovery of Guam by Ferdinand Magellan in 1521.",
        "longDescription": "N/A"
    },
    "Lady of Camarin Day": {
        "shortDescription": "Feast of Guam\u2019s patron saint, Our Lady of Camarin.",
        "longDescription": "N/A"
    },
    "May Day Bank Holiday": {
        "shortDescription": "Holiday for International Workers' Day in the UK.",
        "longDescription": "N/A"
    },
    "Summer Bank Holiday": {
        "shortDescription": "Public holiday marking the end of summer in the UK.",
        "longDescription": "N/A"
    },
    "Africa Day": {
        "shortDescription": "Commemoration of the founding of the African Union in 1963.",
        "longDescription": "N/A"
    },
    "Day after Prophet's Birthday": {
        "shortDescription": "Holiday observed the day after the Prophet Mohammed\u2019s birthday.",
        "longDescription": "N/A"
    },
    "Day after Night of Power": {
        "shortDescription": "Holiday following the Islamic holy night Laylat al-Qadr.",
        "longDescription": "N/A"
    },
    "Day after Eid al-Adha": {
        "shortDescription": "Public holiday after Eid ul-Adha celebrations.",
        "longDescription": "N/A"
    },
    "Day of the Beginning of the Armed Struggle": {
        "shortDescription": "Angolan holiday marking the start of armed resistance against colonial rule.",
        "longDescription": "N/A"
    },
    "Pidjiguiti Day": {
        "shortDescription": "Commemoration of the Pidjiguiti massacre in Guinea-Bissau, 1959.",
        "longDescription": "N/A"
    },
    "Arrival Day": {
        "shortDescription": "Commemorates the arrival of indentured laborers in Guyana.",
        "longDescription": "N/A"
    },
    "CARICOM Day": {
        "shortDescription": "Celebrates the founding of the Caribbean Community (CARICOM).",
        "longDescription": "N/A"
    },
    "Day after Christmas": {
        "shortDescription": "Also known as Boxing Day, the day after Christmas.",
        "longDescription": "N/A"
    },
    "Holi": {
        "shortDescription": "Hindu spring festival of colors and love.",
        "longDescription": "N/A"
    },
    "National Independence Day; New Year's Day": {
        "shortDescription": "Dual observance of independence and the new year.",
        "longDescription": "N/A"
    },
    "Ancestry Day": {
        "shortDescription": "Honors cultural and ancestral heritage.",
        "longDescription": "N/A"
    },
    "Agriculture and Labor Day": {
        "shortDescription": "Celebrates workers and agriculture.",
        "longDescription": "N/A"
    },
    "Flag Day and University Day": {
        "shortDescription": "Holiday celebrating national symbols and education.",
        "longDescription": "N/A"
    },
    "Armed Forces Day; Commemoration of the Battle of Vertieres": {
        "shortDescription": "Honors the military and a decisive Haitian battle.",
        "longDescription": "N/A"
    },
    "Shrove Monday": {
        "shortDescription": "Christian observance before Lent, part of Carnival.",
        "longDescription": "N/A"
    },
    "Fat Tuesday": {
        "shortDescription": "Mardi Gras, final day before Lent.",
        "longDescription": "N/A"
    },
    "Death of Dessalines": {
        "shortDescription": "Marks the assassination of Haitian revolutionary leader Jean-Jacques Dessalines.",
        "longDescription": "N/A"
    },
    "Day of the Dead": {
        "shortDescription": "Commemoration of deceased loved ones.",
        "longDescription": "N/A"
    },
    "Panamerican Day": {
        "shortDescription": "Celebrates unity among the nations of the Americas.",
        "longDescription": "N/A"
    },
    "Morazan Weekend": {
        "shortDescription": "Holiday in Honduras honoring Francisco Moraz\u00e1n.",
        "longDescription": "N/A"
    },
    "The second day of Chinese New Year": {
        "shortDescription": "Part of Lunar New Year celebrations.",
        "longDescription": "N/A"
    },
    "The third day of Chinese New Year": {
        "shortDescription": "Continued celebration of Lunar New Year.",
        "longDescription": "N/A"
    },
    "The Buddha's Birthday": {
        "shortDescription": "Commemoration of the birth of Siddhartha Gautama.",
        "longDescription": "N/A"
    },
    "Hong Kong S.A.R. Establishment Day": {
        "shortDescription": "Marks the 1997 handover of Hong Kong to China.",
        "longDescription": "N/A"
    },
    "The Day following Mid-Autumn Festival": {
        "shortDescription": "Day after the Chinese Mid-Autumn Festival.",
        "longDescription": "N/A"
    },
    "Double Ninth Festival": {
        "shortDescription": "Chinese festival on the ninth day of the ninth lunar month.",
        "longDescription": "N/A"
    },
    "The first weekday after Christmas Day": {
        "shortDescription": "Public holiday following Christmas in Hong Kong.",
        "longDescription": "N/A"
    },
    "State Foundation Day": {
        "shortDescription": "Celebrates the founding of a state or nation.",
        "longDescription": "N/A"
    },
    "First Day of Summer": {
        "shortDescription": "Traditional holiday marking the start of summer in Iceland.",
        "longDescription": "N/A"
    },
    "Commerce Day": {
        "shortDescription": "Holiday promoting trade and commerce.",
        "longDescription": "N/A"
    },
    "Dussehra; Gandhi Jayanti": {
        "shortDescription": "Dual holiday: Hindu festival of victory and Mahatma Gandhi\u2019s birthday.",
        "longDescription": "N/A"
    },
    "Buddha Purnima": {
        "shortDescription": "Celebrates the birth of the Buddha.",
        "longDescription": "N/A"
    },
    "Janmashtami": {
        "shortDescription": "Hindu festival celebrating Krishna\u2019s birth.",
        "longDescription": "N/A"
    },
    "Mahavir Jayanti": {
        "shortDescription": "Celebrates the birth of Lord Mahavira, founder of Jainism.",
        "longDescription": "N/A"
    },
    "Maha Shivaratri": {
        "shortDescription": "Hindu festival dedicated to Lord Shiva.",
        "longDescription": "N/A"
    },
    "Guru Nanak Jayanti": {
        "shortDescription": "Celebrates the birth of Guru Nanak, founder of Sikhism.",
        "longDescription": "N/A"
    },
    "Christmas": {
        "shortDescription": "Christian holiday celebrating the birth of Jesus Christ.",
        "longDescription": "N/A"
    },
    "Dr. B. R. Ambedkar's Jayanti": {
        "shortDescription": "Birthday of Dr. B.R. Ambedkar, Indian reformer.",
        "longDescription": "N/A"
    },
    "Andhra Pradesh Foundation Day": {
        "shortDescription": "Anniversary of the founding of Andhra Pradesh state.",
        "longDescription": "N/A"
    },
    "Magh Bihu": {
        "shortDescription": "Harvest festival in Assam, India.",
        "longDescription": "N/A"
    },
    "Assam Day": {
        "shortDescription": "Celebrates the culture and history of Assam.",
        "longDescription": "N/A"
    },
    "Chhath Puja": {
        "shortDescription": "Hindu festival dedicated to the Sun God.",
        "longDescription": "N/A"
    },
    "Bihar Day": {
        "shortDescription": "Marks the founding of Bihar state in India.",
        "longDescription": "N/A"
    },
    "Chhattisgarh Foundation Day": {
        "shortDescription": "Commemoration of the statehood of Chhattisgarh, India.",
        "longDescription": "N/A"
    },
    "Goa Liberation Day": {
        "shortDescription": "Marks the end of Portuguese rule in Goa in 1961.",
        "longDescription": "N/A"
    },
    "Uttarayan": {
        "shortDescription": "Hindu kite festival celebrating the harvest.",
        "longDescription": "N/A"
    },
    "Gujarat Day": {
        "shortDescription": "Celebrates the formation of Gujarat state in India.",
        "longDescription": "N/A"
    },
    "Sardar Vallabhbhai Patel Jayanti": {
        "shortDescription": "Birthday of Indian leader Sardar Vallabhbhai Patel.",
        "longDescription": "N/A"
    },
    "Himachal Day": {
        "shortDescription": "Celebrates the founding of Himachal Pradesh state in India.",
        "longDescription": "N/A"
    },
    "Haryana Foundation Day": {
        "shortDescription": "Marks the creation of Haryana state in India.",
        "longDescription": "N/A"
    },
    "Jharkhand Formation Day": {
        "shortDescription": "Commemorates the creation of Jharkhand state in India.",
        "longDescription": "N/A"
    },
    "Karnataka Rajyotsava": {
        "shortDescription": "Celebrates the founding of Karnataka state in India.",
        "longDescription": "N/A"
    },
    "Onam; Prophet's Birthday": {
        "shortDescription": "Dual holiday: harvest festival in Kerala and Prophet Mohammed\u2019s birthday.",
        "longDescription": "N/A"
    },
    "Kerala Foundation Day": {
        "shortDescription": "Anniversary of Kerala\u2019s statehood.",
        "longDescription": "N/A"
    },
    "Gudi Padwa": {
        "shortDescription": "Hindu New Year festival celebrated in Maharashtra.",
        "longDescription": "N/A"
    },
    "Chhatrapati Shivaji Maharaj Jayanti": {
        "shortDescription": "Birth anniversary of Maratha king Shivaji.",
        "longDescription": "N/A"
    },
    "Maharashtra Day": {
        "shortDescription": "Marks the founding of Maharashtra state in India.",
        "longDescription": "N/A"
    },
    "Madhya Pradesh Foundation Day": {
        "shortDescription": "Commemorates the founding of Madhya Pradesh state.",
        "longDescription": "N/A"
    },
    "Mizoram State Day": {
        "shortDescription": "Celebrates the creation of Mizoram state in India.",
        "longDescription": "N/A"
    },
    "Nagaland State Inauguration Day": {
        "shortDescription": "Anniversary of Nagaland\u2019s statehood.",
        "longDescription": "N/A"
    },
    "Odisha Day": {
        "shortDescription": "Commemorates the formation of Odisha state in India.",
        "longDescription": "N/A"
    },
    "Maha Vishuva Sankranti / Pana Sankranti": {
        "shortDescription": "Odia New Year festival.",
        "longDescription": "N/A"
    },
    "Guru Gobind Singh Jayanti": {
        "shortDescription": "Birthday of the 10th Sikh Guru, Guru Gobind Singh.",
        "longDescription": "N/A"
    },
    "Vaisakhi": {
        "shortDescription": "Punjabi harvest festival and Sikh New Year.",
        "longDescription": "N/A"
    },
    "Lohri": {
        "shortDescription": "Punjabi winter harvest festival celebrated with bonfires and dance.",
        "longDescription": "N/A"
    },
    "Punjab Day": {
        "shortDescription": "Commemoration of the foundation of the Punjab state in India.",
        "longDescription": "N/A"
    },
    "Janmashtami; Puducherry De Jure Transfer Day": {
        "shortDescription": "Dual holiday: Krishna\u2019s birth and transfer of Puducherry to India.",
        "longDescription": "N/A"
    },
    "Puducherry Liberation Day": {
        "shortDescription": "Marks the end of French rule in Puducherry.",
        "longDescription": "N/A"
    },
    "Rajasthan Day": {
        "shortDescription": "Commemorates the founding of Rajasthan state in India.",
        "longDescription": "N/A"
    },
    "Maharana Pratap Jayanti": {
        "shortDescription": "Birthday of Rajput king Maharana Pratap.",
        "longDescription": "N/A"
    },
    "Sikkim State Day": {
        "shortDescription": "Anniversary of Sikkim joining India in 1975.",
        "longDescription": "N/A"
    },
    "Pongal": {
        "shortDescription": "Tamil harvest festival honoring the Sun god.",
        "longDescription": "N/A"
    },
    "Thiruvalluvar Day / Mattu Pongal": {
        "shortDescription": "Celebrates Tamil poet Thiruvalluvar and cattle festival.",
        "longDescription": "N/A"
    },
    "Uzhavar Thirunal": {
        "shortDescription": "Tamil Nadu festival honoring farmers.",
        "longDescription": "N/A"
    },
    "Dr. B. R. Ambedkar's Jayanti; Puthandu": {
        "shortDescription": "Dual holiday: Ambedkar\u2019s birthday and Tamil New Year.",
        "longDescription": "N/A"
    },
    "Telangana Formation Day": {
        "shortDescription": "Anniversary of Telangana state\u2019s formation in 2014.",
        "longDescription": "N/A"
    },
    "Bathukamma Festival": {
        "shortDescription": "Floral festival celebrated by women in Telangana.",
        "longDescription": "N/A"
    },
    "UP Formation Day": {
        "shortDescription": "Marks the creation of Uttar Pradesh state in India.",
        "longDescription": "N/A"
    },
    "Pohela Boishakh": {
        "shortDescription": "Bengali New Year festival.",
        "longDescription": "N/A"
    },
    "Rabindra Jayanti": {
        "shortDescription": "Birth anniversary of poet Rabindranath Tagore.",
        "longDescription": "N/A"
    },
    "Eid al-Fitr Second Day": {
        "shortDescription": "Second day of celebrations marking the end of Ramadan.",
        "longDescription": "N/A"
    },
    "Day of Silence": {
        "shortDescription": "Balinese New Year (Nyepi), a day of silence and fasting.",
        "longDescription": "N/A"
    },
    "Vesak Day": {
        "shortDescription": "Buddhist festival marking Buddha\u2019s birth, enlightenment, and death.",
        "longDescription": "N/A"
    },
    "Pancasila Day": {
        "shortDescription": "Commemoration of Indonesia\u2019s founding principles.",
        "longDescription": "N/A"
    },
    "Islamic Revolution Day": {
        "shortDescription": "Marks the victory of the Islamic Revolution in Iran in 1979.",
        "longDescription": "N/A"
    },
    "Iranian Oil Industry Nationalization Day": {
        "shortDescription": "Commemorates the 1951 nationalization of Iran\u2019s oil industry.",
        "longDescription": "N/A"
    },
    "Last Day of Year": {
        "shortDescription": "Iranian celebration of the last day of the Persian calendar year.",
        "longDescription": "N/A"
    },
    "Nowruz": {
        "shortDescription": "Persian New Year festival marking the spring equinox.",
        "longDescription": "N/A"
    },
    "Martyrdom of Imam Ali; Nowruz Holiday": {
        "shortDescription": "Dual observance of Imam Ali\u2019s death and Nowruz.",
        "longDescription": "N/A"
    },
    "Nowruz Holiday": {
        "shortDescription": "Additional public holiday for Nowruz celebrations.",
        "longDescription": "N/A"
    },
    "Eid al-Fitr Holiday; Islamic Republic Day": {
        "shortDescription": "Dual holiday: Eid celebrations and Republic Day in Iran.",
        "longDescription": "N/A"
    },
    "Nature's Day": {
        "shortDescription": "Iranian festival celebrating nature on the 13th day of Nowruz.",
        "longDescription": "N/A"
    },
    "Death of Imam Khomeini": {
        "shortDescription": "Anniversary of Ayatollah Khomeini\u2019s death in 1989.",
        "longDescription": "N/A"
    },
    "15 Khordad Uprising": {
        "shortDescription": "Commemoration of protests against the Shah in 1963.",
        "longDescription": "N/A"
    },
    "Tasua": {
        "shortDescription": "Shia observance on the day before Ashura.",
        "longDescription": "N/A"
    },
    "Arbaeen": {
        "shortDescription": "Shia observance marking 40 days after Ashura.",
        "longDescription": "N/A"
    },
    "Death of Prophet Muhammad and Martyrdom of Hasan ibn Ali": {
        "shortDescription": "Shia day of mourning for the Prophet and Imam Hasan.",
        "longDescription": "N/A"
    },
    "Martyrdom of Ali al-Rida": {
        "shortDescription": "Commemoration of the death of Imam Ali al-Rida.",
        "longDescription": "N/A"
    },
    "Martyrdom of Hasan al-Askari": {
        "shortDescription": "Commemoration of the death of Imam Hasan al-Askari.",
        "longDescription": "N/A"
    },
    "Birthday of Muhammad and Imam Ja'far al-Sadiq": {
        "shortDescription": "Dual birthday of Prophet Muhammad and Imam Ja'far.",
        "longDescription": "N/A"
    },
    "Martyrdom of Fatima": {
        "shortDescription": "Shia mourning day for the Prophet\u2019s daughter Fatima.",
        "longDescription": "N/A"
    },
    "Birthday of Imam Ali": {
        "shortDescription": "Birth of Imam Ali, first Shia Imam.",
        "longDescription": "N/A"
    },
    "Birthday of Mahdi": {
        "shortDescription": "Celebration of the birth of the twelfth Imam, al-Mahdi.",
        "longDescription": "N/A"
    },
    "Martyrdom of Imam Ja'far al-Sadiq": {
        "shortDescription": "Commemoration of the death of Imam Ja'far al-Sadiq.",
        "longDescription": "N/A"
    },
    "Eid al-Ghadeer": {
        "shortDescription": "Shia festival commemorating Prophet Muhammad\u2019s sermon at Ghadir Khumm.",
        "longDescription": "N/A"
    },
    "Commemoration of the Saddam Baath crimes against the Iraqi people": {
        "shortDescription": "Day remembering atrocities committed under Saddam Hussein.",
        "longDescription": "N/A"
    },
    "Eid al-Ghadir": {
        "shortDescription": "Alternative spelling of Eid al-Ghadeer, Shia festival.",
        "longDescription": "N/A"
    },
    "Saint Brigid's Day": {
        "shortDescription": "Irish feast day for Saint Brigid, patroness of Ireland.",
        "longDescription": "N/A"
    },
    "Saint Patrick's Day": {
        "shortDescription": "Irish national holiday celebrating Saint Patrick.",
        "longDescription": "N/A"
    },
    "June Bank Holiday": {
        "shortDescription": "Irish public holiday on the first Monday in June.",
        "longDescription": "N/A"
    },
    "August Bank Holiday": {
        "shortDescription": "Irish public holiday on the first Monday in August.",
        "longDescription": "N/A"
    },
    "October Bank Holiday": {
        "shortDescription": "Irish public holiday on the last Monday in October.",
        "longDescription": "N/A"
    },
    "TT Bank Holiday": {
        "shortDescription": "Public holiday for the Isle of Man TT motorcycle races.",
        "longDescription": "N/A"
    },
    "Tynwald Day": {
        "shortDescription": "National day of the Isle of Man, with parliament ceremony.",
        "longDescription": "N/A"
    },
    "Rosh Hashanah": {
        "shortDescription": "Jewish New Year festival.",
        "longDescription": "N/A"
    },
    "Yom Kippur": {
        "shortDescription": "Jewish Day of Atonement, the holiest day of the year.",
        "longDescription": "N/A"
    },
    "Sukkot": {
        "shortDescription": "Jewish festival of booths, commemorating the desert wanderings.",
        "longDescription": "N/A"
    },
    "Simchat Torah / Shemini Atzeret": {
        "shortDescription": "Jewish holidays celebrating the Torah and end of Sukkot.",
        "longDescription": "N/A"
    },
    "Pesach": {
        "shortDescription": "Jewish Passover festival commemorating the Exodus from Egypt.",
        "longDescription": "N/A"
    },
    "Seventh day of Pesach": {
        "shortDescription": "Marks the end of Passover with Red Sea crossing remembrance.",
        "longDescription": "N/A"
    },
    "Shavuot": {
        "shortDescription": "Jewish festival of receiving the Torah at Mount Sinai.",
        "longDescription": "N/A"
    },
    "Capodanno": {
        "shortDescription": "Italian New Year\u2019s Day celebration.",
        "longDescription": "N/A"
    },
    "Epifania del Signore": {
        "shortDescription": "Italian Epiphany, marking the visit of the Magi.",
        "longDescription": "N/A"
    },
    "Pasqua di Resurrezione": {
        "shortDescription": "Italian Easter Sunday, celebrating Christ\u2019s resurrection.",
        "longDescription": "N/A"
    },
    "Luned\u00ec dell'Angelo": {
        "shortDescription": "Easter Monday in Italy, celebrated with family outings.",
        "longDescription": "N/A"
    },
    "Festa della Liberazione": {
        "shortDescription": "Italian Liberation Day, commemorating 1945 freedom from fascism.",
        "longDescription": "N/A"
    },
    "Festa dei Lavoratori": {
        "shortDescription": "Italian Labor Day on May 1st.",
        "longDescription": "N/A"
    },
    "Festa della Repubblica": {
        "shortDescription": "Republic Day marking Italy\u2019s 1946 referendum.",
        "longDescription": "N/A"
    },
    "Assunzione della Vergine": {
        "shortDescription": "Feast of the Assumption of Mary on August 15th.",
        "longDescription": "N/A"
    },
    "Tutti i Santi": {
        "shortDescription": "All Saints' Day in Italy on November 1st.",
        "longDescription": "N/A"
    },
    "Immacolata Concezione": {
        "shortDescription": "Feast of the Immaculate Conception on December 8th.",
        "longDescription": "N/A"
    },
    "Natale": {
        "shortDescription": "Christmas Day celebration in Italy.",
        "longDescription": "N/A"
    },
    "Santo Stefano": {
        "shortDescription": "Saint Stephen\u2019s Day on December 26th.",
        "longDescription": "N/A"
    },
    "San Gerlando": {
        "shortDescription": "Feast of Saint Gerlando, patron of Agrigento.",
        "longDescription": "N/A"
    },
    "San Baudolino": {
        "shortDescription": "Feast of Saint Baudolino, patron of Alessandria.",
        "longDescription": "N/A"
    },
    "San Ciriaco": {
        "shortDescription": "Feast of Saint Cyriacus, patron of Ancona.",
        "longDescription": "N/A"
    },
    "San Grato": {
        "shortDescription": "Feast of Saint Gratus, patron of Aosta.",
        "longDescription": "N/A"
    },
    "Sant'Emidio": {
        "shortDescription": "Feast of Saint Emygdius, patron of Ascoli Piceno.",
        "longDescription": "N/A"
    },
    "San Massimo D'Aveia": {
        "shortDescription": "Feast of Saint Maximus of Aveia, patron of L'Aquila.",
        "longDescription": "N/A"
    },
    "San Donato D'Arezzo": {
        "shortDescription": "Feast of Saint Donatus, patron of Arezzo.",
        "longDescription": "N/A"
    },
    "San Secondo di Asti": {
        "shortDescription": "Feast of Saint Secundus, patron of Asti.",
        "longDescription": "N/A"
    },
    "San Modestino": {
        "shortDescription": "Feast of Saint Modestinus, patron of Avellino.",
        "longDescription": "N/A"
    },
    "San Nicola": {
        "shortDescription": "Feast of Saint Nicholas, patron of Bari.",
        "longDescription": "N/A"
    },
    "Sant'Alessandro di Bergamo": {
        "shortDescription": "Feast of Saint Alexander, patron of Bergamo.",
        "longDescription": "N/A"
    },
    "San Martino": {
        "shortDescription": "Feast of Saint Martin, patron of Tours, also celebrated in Italy.",
        "longDescription": "N/A"
    },
    "San Bartolomeo apostolo": {
        "shortDescription": "Feast of Saint Bartholomew the Apostle.",
        "longDescription": "N/A"
    },
    "San Petronio": {
        "shortDescription": "Feast of Saint Petronius, patron of Bologna.",
        "longDescription": "N/A"
    },
    "San Lorenzo da Brindisi": {
        "shortDescription": "Feast of Saint Lawrence of Brindisi.",
        "longDescription": "N/A"
    },
    "Santi Faustino e Giovita": {
        "shortDescription": "Feast of Saints Faustinus and Jovita, patrons of Brescia.",
        "longDescription": "N/A"
    },
    "San Nicola Pellegrino": {
        "shortDescription": "Feast of Saint Nicholas the Pilgrim, patron of Trani.",
        "longDescription": "N/A"
    },
    "San Riccardo di Andria": {
        "shortDescription": "Feast of Saint Richard, patron of Andria.",
        "longDescription": "N/A"
    },
    "San Ruggero": {
        "shortDescription": "Feast of Saint Roger, patron of Barletta.",
        "longDescription": "N/A"
    },
    "Assunzione della Vergine; Maria Santissima Assunta": {
        "shortDescription": "Feast of the Assumption of Mary, honored under multiple titles.",
        "longDescription": "N/A"
    },
    "Luned\u00ec di Pentecoste": {
        "shortDescription": "Whit Monday, the day after Pentecost.",
        "longDescription": "N/A"
    },
    "San Saturnino di Cagliari": {
        "shortDescription": "Feast of Saint Saturninus, patron of Cagliari.",
        "longDescription": "N/A"
    },
    "San Giorgio": {
        "shortDescription": "Feast of Saint George, widely celebrated across Italy.",
        "longDescription": "N/A"
    },
    "San Sebastiano": {
        "shortDescription": "Feast of Saint Sebastian, patron of Rome.",
        "longDescription": "N/A"
    },
    "San Giustino di Chieti": {
        "shortDescription": "Feast of Saint Justin of Chieti.",
        "longDescription": "N/A"
    },
    "San Michele Arcangelo": {
        "shortDescription": "Feast of Saint Michael the Archangel.",
        "longDescription": "N/A"
    },
    "Sant'Abbondio": {
        "shortDescription": "Feast of Saint Abbondio, patron of Como.",
        "longDescription": "N/A"
    },
    "Sant'Omobono": {
        "shortDescription": "Feast of Saint Homobonus, patron of Cremona.",
        "longDescription": "N/A"
    },
    "Madonna del Pilerio": {
        "shortDescription": "Feast of Our Lady of Pilerio, patroness of Cosenza.",
        "longDescription": "N/A"
    },
    "Sant'Agata": {
        "shortDescription": "Feast of Saint Agatha, patroness of Catania.",
        "longDescription": "N/A"
    },
    "San Vitaliano": {
        "shortDescription": "Feast of Saint Vitalian, patron of Capua.",
        "longDescription": "N/A"
    },
    "Madonna della Visitazione": {
        "shortDescription": "Feast of the Visitation of Mary.",
        "longDescription": "N/A"
    },
    "Madonna del Fuoco": {
        "shortDescription": "Feast of Our Lady of Fire, patroness of Forl\u00ec.",
        "longDescription": "N/A"
    },
    "San Giovanni Battista": {
        "shortDescription": "Feast of Saint John the Baptist.",
        "longDescription": "N/A"
    },
    "Madonna dei Sette Veli": {
        "shortDescription": "Feast of Our Lady of the Seven Veils, patroness of Foggia.",
        "longDescription": "N/A"
    },
    "Maria Santissima Assunta": {
        "shortDescription": "Feast of the Assumption of Mary.",
        "longDescription": "N/A"
    },
    "San Silverio": {
        "shortDescription": "Feast of Saint Silverius, patron of Ponza.",
        "longDescription": "N/A"
    },
    "Santi Ilario e Taziano": {
        "shortDescription": "Feast of Saints Hilary and Tatian, patrons of Gorizia.",
        "longDescription": "N/A"
    },
    "San Lorenzo": {
        "shortDescription": "Feast of Saint Lawrence, deacon and martyr.",
        "longDescription": "N/A"
    },
    "San Leonardo da Porto Maurizio": {
        "shortDescription": "Feast of Saint Leonard, missionary preacher.",
        "longDescription": "N/A"
    },
    "San Pietro Celestino": {
        "shortDescription": "Feast of Saint Peter Celestine, pope and hermit.",
        "longDescription": "N/A"
    },
    "San Dionigi": {
        "shortDescription": "Feast of Saint Denis, bishop and martyr.",
        "longDescription": "N/A"
    },
    "Sant'Oronzo": {
        "shortDescription": "Feast of Saint Orontius, patron of Lecce.",
        "longDescription": "N/A"
    },
    "Santa Giulia": {
        "shortDescription": "Feast of Saint Julia, patroness of Livorno.",
        "longDescription": "N/A"
    },
    "San Bassiano": {
        "shortDescription": "Feast of Saint Bassianus, patron of Lodi.",
        "longDescription": "N/A"
    },
    "Festa della Liberazione; San Marco Evangelista": {
        "shortDescription": "Dual holiday: Liberation Day and feast of Saint Mark.",
        "longDescription": "N/A"
    },
    "Santa Maria Goretti": {
        "shortDescription": "Feast of Saint Maria Goretti, young martyr.",
        "longDescription": "N/A"
    },
    "San Paolino di Lucca": {
        "shortDescription": "Feast of Saint Paulinus, patron of Lucca.",
        "longDescription": "N/A"
    },
    "San Giuliano l'ospitaliere": {
        "shortDescription": "Feast of Saint Julian the Hospitaller.",
        "longDescription": "N/A"
    },
    "Madonna della Lettera": {
        "shortDescription": "Feast of Our Lady of the Letter, patroness of Messina.",
        "longDescription": "N/A"
    },
    "Sant'Ambrogio": {
        "shortDescription": "Feast of Saint Ambrose, patron of Milan.",
        "longDescription": "N/A"
    },
    "Sant'Anselmo da Baggio": {
        "shortDescription": "Feast of Saint Anselm, bishop of Lucca.",
        "longDescription": "N/A"
    },
    "San Geminiano": {
        "shortDescription": "Feast of Saint Geminianus, patron of Modena.",
        "longDescription": "N/A"
    },
    "San Francesco d'Assisi": {
        "shortDescription": "Feast of Saint Francis, patron of Italy.",
        "longDescription": "N/A"
    },
    "Madonna della Bruna": {
        "shortDescription": "Feast of Our Lady of the Brown, patroness of Matera.",
        "longDescription": "N/A"
    },
    "San Gennaro": {
        "shortDescription": "Feast of Saint Januarius, patron of Naples.",
        "longDescription": "N/A"
    },
    "San Gaudenzio": {
        "shortDescription": "Feast of Saint Gaudentius, patron of Novara.",
        "longDescription": "N/A"
    },
    "Nostra Signora della Neve": {
        "shortDescription": "Feast of Our Lady of the Snows.",
        "longDescription": "N/A"
    },
    "Sant'Archelao": {
        "shortDescription": "Feast of Saint Archelaus, patron of Oristano.",
        "longDescription": "N/A"
    },
    "Santa Rosalia": {
        "shortDescription": "Feast of Saint Rosalia, patroness of Palermo.",
        "longDescription": "N/A"
    },
    "Sant'Antonino di Piacenza": {
        "shortDescription": "Feast of Saint Antoninus, patron of Piacenza.",
        "longDescription": "N/A"
    },
    "Sant'Antonio di Padova": {
        "shortDescription": "Feast of Saint Anthony of Padua.",
        "longDescription": "N/A"
    },
    "San Cetteo": {
        "shortDescription": "Feast of Saint Cetteus, patron of Pescara.",
        "longDescription": "N/A"
    },
    "Santa Chiara d'Assisi": {
        "shortDescription": "Feast of Saint Clare of Assisi.",
        "longDescription": "N/A"
    },
    "San Ranieri": {
        "shortDescription": "Feast of Saint Ranieri, patron of Pisa.",
        "longDescription": "N/A"
    },
    "Madonna delle Grazie": {
        "shortDescription": "Feast of Our Lady of Graces.",
        "longDescription": "N/A"
    },
    "Sant'Ilario di Poitiers": {
        "shortDescription": "Feast of Saint Hilary of Poitiers.",
        "longDescription": "N/A"
    },
    "San Jacopo": {
        "shortDescription": "Feast of Saint James, patron of Pistoia.",
        "longDescription": "N/A"
    },
    "San Crescentino": {
        "shortDescription": "Feast of Saint Crescentinus, patron of Urbino.",
        "longDescription": "N/A"
    },
    "San Terenzio di Pesaro": {
        "shortDescription": "Feast of Saint Terence, patron of Pesaro.",
        "longDescription": "N/A"
    },
    "San Siro": {
        "shortDescription": "Feast of Saint Syrus, patron of Pavia.",
        "longDescription": "N/A"
    },
    "San Gerardo di Potenza": {
        "shortDescription": "Feast of Saint Gerard, patron of Potenza.",
        "longDescription": "N/A"
    },
    "Sant'Apollinare": {
        "shortDescription": "Feast of Saint Apollinaris, patron of Ravenna.",
        "longDescription": "N/A"
    },
    "San Prospero Vescovo": {
        "shortDescription": "Feast of Saint Prosper, patron of Reggio Emilia.",
        "longDescription": "N/A"
    },
    "San Giorgio Martire": {
        "shortDescription": "Feast of Saint George the Martyr.",
        "longDescription": "N/A"
    },
    "Santa Barbara": {
        "shortDescription": "Feast of Saint Barbara, patroness of miners and artillerymen.",
        "longDescription": "N/A"
    },
    "Santi Pietro e Paolo": {
        "shortDescription": "Feast of Saints Peter and Paul.",
        "longDescription": "N/A"
    },
    "San Bellino": {
        "shortDescription": "Feast of Saint Bellino, patron of Rovigo.",
        "longDescription": "N/A"
    },
    "San Matteo Evangelista": {
        "shortDescription": "Feast of Saint Matthew the Evangelist.",
        "longDescription": "N/A"
    },
    "Sant'Ansano": {
        "shortDescription": "Feast of Saint Ansanus, patron of Siena.",
        "longDescription": "N/A"
    },
    "San Gervasio e San Protasio": {
        "shortDescription": "Feast of Saints Gervasius and Protasius, patrons of Milan.",
        "longDescription": "N/A"
    },
    "San Giuseppe": {
        "shortDescription": "Feast of Saint Joseph, patron of workers.",
        "longDescription": "N/A"
    },
    "Santa Lucia": {
        "shortDescription": "Feast of Saint Lucy, patroness of the blind.",
        "longDescription": "N/A"
    },
    "San Ponziano": {
        "shortDescription": "Feast of Saint Pontian, pope and martyr.",
        "longDescription": "N/A"
    },
    "Nostra Signora della Misericordia": {
        "shortDescription": "Feast of Our Lady of Mercy.",
        "longDescription": "N/A"
    },
    "San Cataldo": {
        "shortDescription": "Feast of Saint Catald, patron of Taranto.",
        "longDescription": "N/A"
    },
    "San Berardo da Pagliara": {
        "shortDescription": "Feast of Saint Berard, patron of Teramo.",
        "longDescription": "N/A"
    },
    "San Vigilio": {
        "shortDescription": "Feast of Saint Vigilius, patron of Trento.",
        "longDescription": "N/A"
    },
    "Sant'Alberto degli Abati": {
        "shortDescription": "Feast of Saint Albert of Trapani.",
        "longDescription": "N/A"
    },
    "San Valentino": {
        "shortDescription": "Feast of Saint Valentine, associated with love.",
        "longDescription": "N/A"
    },
    "San Giusto": {
        "shortDescription": "Feast of Saint Justus, patron of Trieste.",
        "longDescription": "N/A"
    },
    "San Liberale": {
        "shortDescription": "Feast day of Saint Liberalis, patron saint of Treviso, Italy.",
        "longDescription": "N/A"
    },
    "Santi Ermacora e Fortunato": {
        "shortDescription": "Feast day of Saints Hermagoras and Fortunatus, patrons of Udine, Italy.",
        "longDescription": "N/A"
    },
    "San Vittore il Moro": {
        "shortDescription": "Feast day of Saint Victor the Moor, venerated in Milan, Italy.",
        "longDescription": "N/A"
    },
    "Sant'Eusebio di Vercelli": {
        "shortDescription": "Feast of Saint Eusebius, first bishop of Vercelli, Italy.",
        "longDescription": "N/A"
    },
    "Madonna della Salute": {
        "shortDescription": "Venetian feast dedicated to the Virgin Mary for protection from plague.",
        "longDescription": "N/A"
    },
    "Madonna di Monte Berico": {
        "shortDescription": "Vicenza celebration honoring the Virgin Mary apparition at Monte Berico.",
        "longDescription": "N/A"
    },
    "San Zeno": {
        "shortDescription": "Feast of Saint Zeno, patron saint of Verona, Italy.",
        "longDescription": "N/A"
    },
    "Santa Rosa da Viterbo": {
        "shortDescription": "Feast of Saint Rose, patron saint of Viterbo, Italy.",
        "longDescription": "N/A"
    },
    "San Leoluca": {
        "shortDescription": "Feast of Saint Leoluca, patron saint of Corleone, Sicily.",
        "longDescription": "N/A"
    },
    "National Peace Day": {
        "shortDescription": "Day to promote peace and reconciliation in the nation.",
        "longDescription": "N/A"
    },
    "Day after the Eid al-Fitr": {
        "shortDescription": "Holiday marking the second day of Eid celebrations.",
        "longDescription": "N/A"
    },
    "National Labour Day": {
        "shortDescription": "Public holiday celebrating workers and labor rights.",
        "longDescription": "N/A"
    },
    "Coming of Age Day": {
        "shortDescription": "Japanese holiday celebrating young people reaching adulthood.",
        "longDescription": "N/A"
    },
    "Foundation Day": {
        "shortDescription": "Japanese holiday marking the founding of the nation.",
        "longDescription": "N/A"
    },
    "Emperor's Birthday": {
        "shortDescription": "National holiday celebrating the birthday of the Emperor of Japan.",
        "longDescription": "N/A"
    },
    "Vernal Equinox Day": {
        "shortDescription": "Japanese holiday marking the spring equinox and balance of day and night.",
        "longDescription": "N/A"
    },
    "Showa Day": {
        "shortDescription": "Japanese holiday honoring Emperor Showa and reflecting on his era.",
        "longDescription": "N/A"
    },
    "Greenery Day": {
        "shortDescription": "Japanese holiday appreciating nature and the environment.",
        "longDescription": "N/A"
    },
    "Children's Day": {
        "shortDescription": "Japanese holiday celebrating children\u2019s health and happiness.",
        "longDescription": "N/A"
    },
    "Marine Day": {
        "shortDescription": "Japanese holiday honoring the ocean and maritime prosperity.",
        "longDescription": "N/A"
    },
    "Mountain Day": {
        "shortDescription": "Japanese holiday to appreciate mountains and nature.",
        "longDescription": "N/A"
    },
    "Respect for the Aged Day": {
        "shortDescription": "Japanese holiday honoring elderly citizens.",
        "longDescription": "N/A"
    },
    "Autumnal Equinox": {
        "shortDescription": "Japanese holiday marking the autumn equinox.",
        "longDescription": "N/A"
    },
    "Sports Day": {
        "shortDescription": "Japanese holiday promoting sports and active lifestyles.",
        "longDescription": "N/A"
    },
    "Culture Day": {
        "shortDescription": "Japanese holiday celebrating culture, arts, and academic freedom.",
        "longDescription": "N/A"
    },
    "Labor Thanksgiving Day": {
        "shortDescription": "Japanese holiday giving thanks for labor and production.",
        "longDescription": "N/A"
    },
    "Substitute Holiday": {
        "shortDescription": "Day off when a national holiday falls on a Sunday.",
        "longDescription": "N/A"
    },
    "Early May Bank Holiday": {
        "shortDescription": "UK holiday on the first Monday of May.",
        "longDescription": "N/A"
    },
    "Kazakhstan's People Solidarity Holiday": {
        "shortDescription": "Holiday celebrating unity and solidarity of Kazakhstan\u2019s people.",
        "longDescription": "N/A"
    },
    "Defender of the Fatherland Day": {
        "shortDescription": "Kazakh holiday honoring armed forces and veterans.",
        "longDescription": "N/A"
    },
    "Capital Day": {
        "shortDescription": "Kazakhstan holiday celebrating the capital city Astana.",
        "longDescription": "N/A"
    },
    "Madaraka Day": {
        "shortDescription": "Kenya holiday marking self-rule gained in 1963.",
        "longDescription": "N/A"
    },
    "Mazingira Day": {
        "shortDescription": "Kenya\u2019s Environment Day promoting ecological conservation.",
        "longDescription": "N/A"
    },
    "Mashujaa Day": {
        "shortDescription": "Kenya holiday honoring national heroes and heroines.",
        "longDescription": "N/A"
    },
    "Jamhuri Day": {
        "shortDescription": "Kenya\u2019s Republic Day, marking independence as a republic.",
        "longDescription": "N/A"
    },
    "Eid-al-Fitr": {
        "shortDescription": "Muslim festival marking the end of Ramadan fasting.",
        "longDescription": "N/A"
    },
    "Easter Monday; National Health Day": {
        "shortDescription": "Post-Easter holiday also observed as a health awareness day.",
        "longDescription": "N/A"
    },
    "National Health Day": {
        "shortDescription": "Day dedicated to promoting public health awareness.",
        "longDescription": "N/A"
    },
    "Gospel Day": {
        "shortDescription": "Christian celebration in Pacific nations for spreading of the Gospel.",
        "longDescription": "N/A"
    },
    "National Day - Independence Anniversary": {
        "shortDescription": "Celebration of a nation\u2019s independence anniversary.",
        "longDescription": "N/A"
    },
    "Human Rights and Peace Day": {
        "shortDescription": "Holiday promoting peace and human rights in Kyrgyzstan.",
        "longDescription": "N/A"
    },
    "Fatherland Defender's Day": {
        "shortDescription": "Military holiday honoring servicemen in Kyrgyzstan.",
        "longDescription": "N/A"
    },
    "Nooruz Mairamy": {
        "shortDescription": "Spring equinox festival in Central Asia, marking the New Year.",
        "longDescription": "N/A"
    },
    "Day of the People's April Revolution": {
        "shortDescription": "Holiday marking Kyrgyzstan\u2019s April 2010 revolution.",
        "longDescription": "N/A"
    },
    "Days of History and Commemoration of Ancestors": {
        "shortDescription": "Kyrgyz holiday honoring history and ancestors.",
        "longDescription": "N/A"
    },
    "Orozo Ait": {
        "shortDescription": "Kyrgyz celebration of Eid al-Fitr after Ramadan.",
        "longDescription": "N/A"
    },
    "Kurman Ait": {
        "shortDescription": "Kyrgyz celebration of Eid al-Adha, festival of sacrifice.",
        "longDescription": "N/A"
    },
    "Lao New Year's Day": {
        "shortDescription": "Traditional Lao New Year (Pi Mai Lao).",
        "longDescription": "N/A"
    },
    "Lao National Day": {
        "shortDescription": "Celebration of Lao People\u2019s Democratic Republic foundation.",
        "longDescription": "N/A"
    },
    "Restoration of Independence Day": {
        "shortDescription": "Latvia\u2019s day marking restoration of independence from USSR.",
        "longDescription": "N/A"
    },
    "Republic of Latvia Proclamation Day": {
        "shortDescription": "Latvia\u2019s national day marking the 1918 independence declaration.",
        "longDescription": "N/A"
    },
    "Armenian Orthodox Christmas Day": {
        "shortDescription": "Armenian Apostolic celebration of Christmas on January 6.",
        "longDescription": "N/A"
    },
    "Saint Maron's Day": {
        "shortDescription": "Lebanese Maronite Christian feast of Saint Maron.",
        "longDescription": "N/A"
    },
    "Feast of the Annunciation": {
        "shortDescription": "Christian feast celebrating the angel\u2019s announcement to Mary.",
        "longDescription": "N/A"
    },
    "Orthodox Holy Saturday": {
        "shortDescription": "Orthodox Christian day before Easter Sunday.",
        "longDescription": "N/A"
    },
    "Resistance and Liberation Day": {
        "shortDescription": "Italy\u2019s holiday marking liberation from Nazi occupation.",
        "longDescription": "N/A"
    },
    "Moshoeshoe's Day": {
        "shortDescription": "Lesotho holiday honoring King Moshoeshoe I.",
        "longDescription": "N/A"
    },
    "Africa/Heroes Day": {
        "shortDescription": "Holiday in African nations celebrating national heroes.",
        "longDescription": "N/A"
    },
    "Workers' Day": {
        "shortDescription": "International holiday celebrating labor and workers\u2019 rights.",
        "longDescription": "N/A"
    },
    "Decoration Day": {
        "shortDescription": "Liberian holiday to honor the graves of the dead.",
        "longDescription": "N/A"
    },
    "J. J. Roberts Memorial Birthday": {
        "shortDescription": "Liberia holiday honoring Joseph Jenkins Roberts, first president.",
        "longDescription": "N/A"
    },
    "Fasting and Prayer Day": {
        "shortDescription": "Liberian day of national fasting and prayer.",
        "longDescription": "N/A"
    },
    "National Unification and Integration Day": {
        "shortDescription": "Liberia holiday promoting national unity.",
        "longDescription": "N/A"
    },
    "Tubman Administration Goodwill Day": {
        "shortDescription": "Liberia holiday honoring President William Tubman.",
        "longDescription": "N/A"
    },
    "Anniversary of the February 17 Revolution": {
        "shortDescription": "Libya holiday marking the 2011 revolution.",
        "longDescription": "N/A"
    },
    "National Environmental Sanitation Day": {
        "shortDescription": "Nigeria holiday promoting public sanitation awareness.",
        "longDescription": "N/A"
    },
    "Candlemas": {
        "shortDescription": "Christian feast of the Presentation of Jesus at the Temple.",
        "longDescription": "N/A"
    },
    "Nativity of Mary": {
        "shortDescription": "Christian feast celebrating the Virgin Mary\u2019s birth.",
        "longDescription": "N/A"
    },
    "Day of Restoration of the State of Lithuania": {
        "shortDescription": "Lithuania\u2019s national day marking 1918 independence.",
        "longDescription": "N/A"
    },
    "Day of Restoration of Independence of Lithuania": {
        "shortDescription": "Lithuania holiday marking 1990 independence from USSR.",
        "longDescription": "N/A"
    },
    "Day of Dew and Saint John": {
        "shortDescription": "Lithuanian midsummer solstice celebration (Jonin\u0117s).",
        "longDescription": "N/A"
    },
    "Europe Day": {
        "shortDescription": "European holiday celebrating peace and unity in Europe.",
        "longDescription": "N/A"
    },
    "Chinese New Year's Day": {
        "shortDescription": "Beginning of the lunar new year in Chinese tradition.",
        "longDescription": "N/A"
    },
    "National Day of the People's Republic of China": {
        "shortDescription": "China\u2019s national day on October 1.",
        "longDescription": "N/A"
    },
    "Macao S.A.R. Establishment Day": {
        "shortDescription": "Holiday marking Macao\u2019s return to China in 1999.",
        "longDescription": "N/A"
    },
    "John Chilembwe Day": {
        "shortDescription": "Malawi holiday honoring Reverend John Chilembwe, independence hero.",
        "longDescription": "N/A"
    },
    "Martyrs Day": {
        "shortDescription": "Malawi holiday commemorating martyrs of independence struggle.",
        "longDescription": "N/A"
    },
    "Kamuzu Day": {
        "shortDescription": "Malawi holiday honoring Dr. Hastings Kamuzu Banda.",
        "longDescription": "N/A"
    },
    "Birthday of HM Yang di-Pertuan Agong": {
        "shortDescription": "Malaysia holiday celebrating the King\u2019s official birthday.",
        "longDescription": "N/A"
    },
    "Malaysia Day": {
        "shortDescription": "National holiday marking formation of Malaysia in 1963.",
        "longDescription": "N/A"
    },
    "Deepavali": {
        "shortDescription": "Hindu festival of lights celebrated in Malaysia.",
        "longDescription": "N/A"
    },
    "Thaipusam": {
        "shortDescription": "Hindu festival honoring Lord Murugan in Malaysia.",
        "longDescription": "N/A"
    },
    "Birthday of the Sultan of Johor": {
        "shortDescription": "State holiday in Johor, Malaysia.",
        "longDescription": "N/A"
    },
    "The Sultan of Johor Hol": {
        "shortDescription": "Religious commemoration of Sultan Abu Bakar in Johor.",
        "longDescription": "N/A"
    },
    "Beginning of Ramadan": {
        "shortDescription": "First day of Ramadan fasting month.",
        "longDescription": "N/A"
    },
    "Birthday of The Sultan of Kedah": {
        "shortDescription": "State holiday in Kedah, Malaysia.",
        "longDescription": "N/A"
    },
    "Birthday of the Sultan of Kelantan": {
        "shortDescription": "State holiday in Kelantan, Malaysia.",
        "longDescription": "N/A"
    },
    "Nuzul Al-Quran Day": {
        "shortDescription": "Holiday marking the Quran\u2019s revelation to Prophet Muhammad.",
        "longDescription": "N/A"
    },
    "Declaration of Independence Day": {
        "shortDescription": "Malaysia holiday marking independence from Britain (1957).",
        "longDescription": "N/A"
    },
    "Birthday of the Governor of Malacca": {
        "shortDescription": "State holiday in Malacca, Malaysia.",
        "longDescription": "N/A"
    },
    "Birthday of the Sultan of Negeri Sembilan": {
        "shortDescription": "State holiday in Negeri Sembilan, Malaysia.",
        "longDescription": "N/A"
    },
    "The Sultan of Pahang Hol": {
        "shortDescription": "Religious commemoration of Sultan Abu Bakar in Pahang.",
        "longDescription": "N/A"
    },
    "Birthday of the Sultan of Pahang": {
        "shortDescription": "State holiday in Pahang, Malaysia.",
        "longDescription": "N/A"
    },
    "George Town Heritage Day": {
        "shortDescription": "Penang holiday celebrating UNESCO recognition of George Town.",
        "longDescription": "N/A"
    },
    "Birthday of the Governor of Penang": {
        "shortDescription": "State holiday in Penang, Malaysia.",
        "longDescription": "N/A"
    },
    "Birthday of the Sultan of Perak": {
        "shortDescription": "State holiday in Perak, Malaysia.",
        "longDescription": "N/A"
    },
    "Birthday of the Raja of Perlis": {
        "shortDescription": "State holiday in Perlis, Malaysia.",
        "longDescription": "N/A"
    },
    "Birthday of The Sultan of Selangor": {
        "shortDescription": "State holiday in Selangor, Malaysia.",
        "longDescription": "N/A"
    },
    "Anniversary of the Installation of the Sultan of Terengganu": {
        "shortDescription": "Holiday marking ruler\u2019s enthronement in Terengganu.",
        "longDescription": "N/A"
    },
    "Birthday of the Sultan of Terengganu": {
        "shortDescription": "State holiday in Terengganu, Malaysia.",
        "longDescription": "N/A"
    },
    "Pesta Kaamatan": {
        "shortDescription": "Harvest festival in Sabah, Malaysia.",
        "longDescription": "N/A"
    },
    "Birthday of the Governor of Sabah": {
        "shortDescription": "State holiday in Sabah, Malaysia.",
        "longDescription": "N/A"
    },
    "Birthday of HM Yang di-Pertuan Agong; Dayak Festival Day": {
        "shortDescription": "Joint celebration of King\u2019s birthday and Dayak festival in Sarawak.",
        "longDescription": "N/A"
    },
    "Dayak Festival Day": {
        "shortDescription": "Harvest festival celebrated by Dayak people in Sarawak.",
        "longDescription": "N/A"
    },
    "Birthday of the Governor of Sarawak": {
        "shortDescription": "State holiday in Sarawak, Malaysia.",
        "longDescription": "N/A"
    },
    "Sarawak Independence Day": {
        "shortDescription": "Sarawak holiday marking independence before Malaysia formation.",
        "longDescription": "N/A"
    },
    "Federal Territory Day": {
        "shortDescription": "Holiday for Kuala Lumpur, Putrajaya, and Labuan.",
        "longDescription": "N/A"
    },
    "Hajj Day": {
        "shortDescription": "Holiday marking the pilgrimage to Mecca (Hajj).",
        "longDescription": "N/A"
    },
    "Mawlid al-Nabi": {
        "shortDescription": "Islamic holiday marking Prophet Muhammad\u2019s birth.",
        "longDescription": "N/A"
    },
    "The Day Maldives Embraced Islam": {
        "shortDescription": "Holiday marking Maldives\u2019 conversion to Islam in 1153.",
        "longDescription": "N/A"
    },
    "National Day of the Republic of Mali": {
        "shortDescription": "Independence Day of Mali.",
        "longDescription": "N/A"
    },
    "Prophet's Baptism": {
        "shortDescription": "Christian holiday marking the baptism of Jesus.",
        "longDescription": "N/A"
    },
    "Feast of Saint Paul's Shipwreck": {
        "shortDescription": "Malta holiday commemorating St. Paul\u2019s shipwreck.",
        "longDescription": "N/A"
    },
    "Feast of Saint Joseph": {
        "shortDescription": "Christian feast honoring Saint Joseph, spouse of Mary.",
        "longDescription": "N/A"
    },
    "Freedom Day": {
        "shortDescription": "Malta holiday marking British troop withdrawal in 1979.",
        "longDescription": "N/A"
    },
    "Sette Giugno": {
        "shortDescription": "Malta holiday commemorating 1919 riots against British rule.",
        "longDescription": "N/A"
    },
    "Feast of Saint Peter and Saint Paul": {
        "shortDescription": "Christian feast celebrating apostles Peter and Paul.",
        "longDescription": "N/A"
    },
    "Feast of the Assumption": {
        "shortDescription": "Christian feast of Mary\u2019s assumption into heaven.",
        "longDescription": "N/A"
    },
    "Feast of Our Lady of Victories": {
        "shortDescription": "Malta holiday celebrating victory of 1565 Great Siege.",
        "longDescription": "N/A"
    },
    "Feast of the Immaculate Conception": {
        "shortDescription": "Christian feast celebrating Mary\u2019s conception without sin.",
        "longDescription": "N/A"
    },
    "Nuclear Victims Remembrance Day": {
        "shortDescription": "Marshall Islands holiday remembering nuclear test victims.",
        "longDescription": "N/A"
    },
    "Fisherman's Day": {
        "shortDescription": "Marshall Islands holiday honoring fishermen and fishing traditions.",
        "longDescription": "N/A"
    },
    "Dri-jerbal Day": {
        "shortDescription": "Marshall Islands labor day honoring workers.",
        "longDescription": "N/A"
    },
    "Manit Day": {
        "shortDescription": "Marshall Islands cultural heritage day.",
        "longDescription": "N/A"
    },
    "Independence and Republic Day": {
        "shortDescription": "Marshall Islands national independence day.",
        "longDescription": "N/A"
    },
    "Arrival of Indentured Laborers": {
        "shortDescription": "Mauritius holiday remembering Indian laborers\u2019 arrival in 1834.",
        "longDescription": "N/A"
    },
    "Chinese Spring Festival": {
        "shortDescription": "Chinese Lunar New Year celebration.",
        "longDescription": "N/A"
    },
    "Ugadi": {
        "shortDescription": "New Year festival for Telugu and Kannada communities.",
        "longDescription": "N/A"
    },
    "Ganesh Chaturthi": {
        "shortDescription": "Hindu festival honoring Lord Ganesha.",
        "longDescription": "N/A"
    },
    "Benito Ju\u00e1rez's birthday": {
        "shortDescription": "Mexico holiday celebrating former president Benito Ju\u00e1rez.",
        "longDescription": "N/A"
    },
    "Micronesian Culture and Tradition Day": {
        "shortDescription": "Holiday celebrating FSM\u2019s cultural traditions.",
        "longDescription": "N/A"
    },
    "Federated States of Micronesia Day": {
        "shortDescription": "FSM holiday celebrating independence.",
        "longDescription": "N/A"
    },
    "United Nations Day": {
        "shortDescription": "International holiday celebrating the UN\u2019s founding.",
        "longDescription": "N/A"
    },
    "Independence Day; Self Government Day": {
        "shortDescription": "FSM holiday marking independence and self-government.",
        "longDescription": "N/A"
    },
    "FSM Veterans of Foreign Wars Day": {
        "shortDescription": "Day honoring military veterans in Micronesia.",
        "longDescription": "N/A"
    },
    "Presidents Day": {
        "shortDescription": "Holiday honoring FSM presidents.",
        "longDescription": "N/A"
    },
    "Kosrae State Constitution Day": {
        "shortDescription": "Kosrae holiday marking adoption of state constitution.",
        "longDescription": "N/A"
    },
    "Kosrae Liberation Day": {
        "shortDescription": "Kosrae holiday celebrating liberation from Japanese rule.",
        "longDescription": "N/A"
    },
    "Kosrae Disability Day": {
        "shortDescription": "Day raising awareness on disabilities in Kosrae.",
        "longDescription": "N/A"
    },
    "Micronesian Culture and Tradition Day; Pohnpei Cultural Day": {
        "shortDescription": "Cultural holiday in Pohnpei celebrating Micronesian heritage.",
        "longDescription": "N/A"
    },
    "Pohnpei Constitution Day": {
        "shortDescription": "Holiday in Pohnpei State, FSM, marking adoption of its constitution.",
        "longDescription": "N/A"
    },
    "State Charter Day": {
        "shortDescription": "Public holiday celebrating the granting of a state charter.",
        "longDescription": "N/A"
    },
    "Chuuk State Constitution Day": {
        "shortDescription": "FSM holiday marking Chuuk State\u2019s constitution adoption.",
        "longDescription": "N/A"
    },
    "Yap Day": {
        "shortDescription": "Cultural holiday in Yap State celebrating traditions and heritage.",
        "longDescription": "N/A"
    },
    "Yap State Constitution Day": {
        "shortDescription": "FSM holiday marking Yap\u2019s state constitution adoption.",
        "longDescription": "N/A"
    },
    "Day of Rejoicing": {
        "shortDescription": "Moldova holiday celebrating independence from the USSR (1990).",
        "longDescription": "N/A"
    },
    "International Workers' Solidarity Day": {
        "shortDescription": "Labor holiday celebrated worldwide on May 1.",
        "longDescription": "N/A"
    },
    "Europe Day; Victory Day and Commemoration of the heroes fallen for Independence of Fatherland": {
        "shortDescription": "Moldovan holiday combining Europe Day and WWII Victory Day.",
        "longDescription": "N/A"
    },
    "Republic of Moldova Independence Day": {
        "shortDescription": "National holiday marking Moldova\u2019s independence from USSR (1991).",
        "longDescription": "N/A"
    },
    "National Language Day": {
        "shortDescription": "Moldova\u2019s holiday celebrating the Romanian language.",
        "longDescription": "N/A"
    },
    "Saint Devote's Day": {
        "shortDescription": "Monaco holiday honoring its patron saint, Saint Devote.",
        "longDescription": "N/A"
    },
    "Prince's Day": {
        "shortDescription": "Monaco holiday celebrating the reigning prince.",
        "longDescription": "N/A"
    },
    "National Festival and People's Revolution Anniversary": {
        "shortDescription": "Mongolia holiday marking the 1921 revolution.",
        "longDescription": "N/A"
    },
    "Genghis Khan's Birthday": {
        "shortDescription": "Mongolia holiday celebrating the birth of Genghis Khan.",
        "longDescription": "N/A"
    },
    "National Freedom and Independence Day": {
        "shortDescription": "Montenegro\u2019s holiday celebrating independence from Ottoman rule.",
        "longDescription": "N/A"
    },
    "Njegos Day": {
        "shortDescription": "Montenegro holiday honoring Petar II Petrovi\u0107-Njego\u0161, poet and ruler.",
        "longDescription": "N/A"
    },
    "Day of Prayer and Thanksgiving": {
        "shortDescription": "Religious holiday of gratitude and worship.",
        "longDescription": "N/A"
    },
    "Festival Day": {
        "shortDescription": "National cultural celebration day.",
        "longDescription": "N/A"
    },
    "Throne Day": {
        "shortDescription": "Morocco holiday celebrating the King\u2019s accession to the throne.",
        "longDescription": "N/A"
    },
    "Oued Ed-Dahab Day": {
        "shortDescription": "Morocco holiday marking return of Oued Ed-Dahab region.",
        "longDescription": "N/A"
    },
    "Green March": {
        "shortDescription": "Morocco holiday marking the 1975 Green March reclaiming Western Sahara.",
        "longDescription": "N/A"
    },
    "International Fraternalism Day": {
        "shortDescription": "Holiday promoting unity and brotherhood.",
        "longDescription": "N/A"
    },
    "Heroes' Day": {
        "shortDescription": "Namibia holiday honoring those who died in the independence struggle.",
        "longDescription": "N/A"
    },
    "Peace and Reconciliation Day": {
        "shortDescription": "Namibia holiday promoting reconciliation and unity.",
        "longDescription": "N/A"
    },
    "Cassinga Day": {
        "shortDescription": "Namibia holiday commemorating the 1978 Cassinga massacre.",
        "longDescription": "N/A"
    },
    "Genocide Remembrance Day": {
        "shortDescription": "Day remembering victims of the Herero and Nama genocide.",
        "longDescription": "N/A"
    },
    "Day of the Namibian Women and International Human Rights Day": {
        "shortDescription": "Holiday celebrating women\u2019s rights and human rights in Namibia.",
        "longDescription": "N/A"
    },
    "Burial ceremony of Dr. Sam Shafiishuna Nujoma": {
        "shortDescription": "Special day honoring Namibia\u2019s first president.",
        "longDescription": "N/A"
    },
    "Day following Independence Day": {
        "shortDescription": "Namibia holiday granting an extra day off after Independence Day.",
        "longDescription": "N/A"
    },
    "Easter Tuesday": {
        "shortDescription": "Christian holiday observed after Easter Monday.",
        "longDescription": "N/A"
    },
    "RONPHOS Handover": {
        "shortDescription": "Nauru holiday marking phosphate company\u2019s handover.",
        "longDescription": "N/A"
    },
    "Ibumin Earoeni Day": {
        "shortDescription": "Traditional celebration in Nauru.",
        "longDescription": "N/A"
    },
    "Sir Hammer DeRoburt Day": {
        "shortDescription": "Nauru holiday honoring the country\u2019s founding president.",
        "longDescription": "N/A"
    },
    "Angam Day": {
        "shortDescription": "Nauru holiday celebrating national survival and rebirth.",
        "longDescription": "N/A"
    },
    "Day following Christmas": {
        "shortDescription": "Public holiday granting an extra day after Christmas.",
        "longDescription": "N/A"
    },
    "Prithvi Jayanti": {
        "shortDescription": "Nepal holiday honoring King Prithvi Narayan Shah, founder of modern Nepal.",
        "longDescription": "N/A"
    },
    "Nepali New Year": {
        "shortDescription": "Festival marking the beginning of the Nepali calendar year.",
        "longDescription": "N/A"
    },
    "International Labour Day": {
        "shortDescription": "Holiday celebrating workers\u2019 rights on May 1.",
        "longDescription": "N/A"
    },
    "Maghe Sankranti": {
        "shortDescription": "Nepali festival marking the sun\u2019s movement into Capricorn.",
        "longDescription": "N/A"
    },
    "Sonam Lhochhar": {
        "shortDescription": "Tamang New Year festival in Nepal.",
        "longDescription": "N/A"
    },
    "Gyalpo Lhosar": {
        "shortDescription": "Sherpa New Year festival in Nepal.",
        "longDescription": "N/A"
    },
    "Fagu Poornima": {
        "shortDescription": "Nepali celebration of Holi, the festival of colors.",
        "longDescription": "N/A"
    },
    "Buddha Jayanti": {
        "shortDescription": "Festival marking the birth of Lord Buddha.",
        "longDescription": "N/A"
    },
    "Fulpati": {
        "shortDescription": "Seventh day of Dashain festival in Nepal.",
        "longDescription": "N/A"
    },
    "Maha Ashtami": {
        "shortDescription": "Eighth day of Dashain festival honoring goddess Durga.",
        "longDescription": "N/A"
    },
    "Maha Navami": {
        "shortDescription": "Ninth day of Dashain festival with religious ceremonies.",
        "longDescription": "N/A"
    },
    "Bijaya Dashami": {
        "shortDescription": "Main day of Dashain festival celebrating victory of good over evil.",
        "longDescription": "N/A"
    },
    "Ekadashi": {
        "shortDescription": "Hindu fasting day observed twice a month.",
        "longDescription": "N/A"
    },
    "Laxmi Pooja": {
        "shortDescription": "Festival worshiping Goddess Lakshmi during Tihar.",
        "longDescription": "N/A"
    },
    "Gai Tihar": {
        "shortDescription": "Day of Tihar festival dedicated to cows.",
        "longDescription": "N/A"
    },
    "Gobardhan Pooja; Mha Pooja": {
        "shortDescription": "Tihar rituals worshiping oxen and celebrating self-purification.",
        "longDescription": "N/A"
    },
    "Bhai Tika": {
        "shortDescription": "Final day of Tihar festival celebrating bond between brothers and sisters.",
        "longDescription": "N/A"
    },
    "Chhath Parva": {
        "shortDescription": "Hindu festival dedicated to Sun God, popular in Nepal.",
        "longDescription": "N/A"
    },
    "Tamu Lhochhar": {
        "shortDescription": "Gurung New Year festival in Nepal.",
        "longDescription": "N/A"
    },
    "Id-ul-Fitr": {
        "shortDescription": "Muslim holiday marking the end of Ramadan.",
        "longDescription": "N/A"
    },
    "Bakrid": {
        "shortDescription": "Muslim festival of sacrifice, Eid al-Adha.",
        "longDescription": "N/A"
    },
    "Martyr's Day": {
        "shortDescription": "Nepal holiday honoring national martyrs.",
        "longDescription": "N/A"
    },
    "National Democracy Day": {
        "shortDescription": "Nepal holiday celebrating democracy\u2019s establishment.",
        "longDescription": "N/A"
    },
    "Ram Navami": {
        "shortDescription": "Hindu festival celebrating the birth of Lord Rama.",
        "longDescription": "N/A"
    },
    "Janai Poornima": {
        "shortDescription": "Nepali Hindu festival where men change their sacred thread.",
        "longDescription": "N/A"
    },
    "Shree Krishna Janmashtami": {
        "shortDescription": "Hindu festival celebrating the birth of Lord Krishna.",
        "longDescription": "N/A"
    },
    "Ghatasthapana": {
        "shortDescription": "First day of Dashain festival in Nepal, marking the invocation of Goddess Durga.",
        "longDescription": "N/A"
    },
    "Duwadashi": {
        "shortDescription": "Hindu observance falling on the twelfth lunar day, often linked with Ekadashi fast conclusion.",
        "longDescription": "N/A"
    },
    "Tihar Holiday": {
        "shortDescription": "Festival of lights in Nepal, similar to Diwali, honoring gods, animals, and siblings.",
        "longDescription": "N/A"
    },
    "Waitangi Day": {
        "shortDescription": "New Zealand holiday commemorating the signing of the Treaty of Waitangi in 1840.",
        "longDescription": "N/A"
    },
    "Matariki": {
        "shortDescription": "M\u0101ori New Year festival in New Zealand, marked by the rising of the Pleiades star cluster.",
        "longDescription": "N/A"
    },
    "Auckland Anniversary Day": {
        "shortDescription": "Regional holiday celebrating the founding of Auckland, New Zealand.",
        "longDescription": "N/A"
    },
    "Canterbury Anniversary Day": {
        "shortDescription": "Regional holiday marking the founding of Canterbury province, New Zealand.",
        "longDescription": "N/A"
    },
    "Chatham Islands Anniversary Day": {
        "shortDescription": "Regional holiday marking settlement of the Chatham Islands, New Zealand.",
        "longDescription": "N/A"
    },
    "Hawke's Bay Anniversary Day": {
        "shortDescription": "Regional holiday celebrating Hawke's Bay province in New Zealand.",
        "longDescription": "N/A"
    },
    "Marlborough Anniversary Day": {
        "shortDescription": "Regional holiday marking establishment of Marlborough province, New Zealand.",
        "longDescription": "N/A"
    },
    "Nelson Anniversary Day": {
        "shortDescription": "Regional holiday commemorating settlement of Nelson province, New Zealand.",
        "longDescription": "N/A"
    },
    "Otago Anniversary Day": {
        "shortDescription": "Regional holiday marking Scottish settlement of Otago, New Zealand.",
        "longDescription": "N/A"
    },
    "Southland Anniversary Day": {
        "shortDescription": "Regional holiday celebrating the establishment of Southland province, New Zealand.",
        "longDescription": "N/A"
    },
    "Taranaki Anniversary Day": {
        "shortDescription": "Regional holiday marking founding of Taranaki province, New Zealand.",
        "longDescription": "N/A"
    },
    "Wellington Anniversary Day": {
        "shortDescription": "Regional holiday celebrating settlement of Wellington, New Zealand.",
        "longDescription": "N/A"
    },
    "West Coast Anniversary Day": {
        "shortDescription": "Regional holiday marking establishment of West Coast province, New Zealand.",
        "longDescription": "N/A"
    },
    "South Canterbury Anniversary Day": {
        "shortDescription": "Regional holiday celebrating South Canterbury region, New Zealand.",
        "longDescription": "N/A"
    },
    "Battle of San Jacinto Day": {
        "shortDescription": "Nicaragua holiday commemorating the 1856 battle against filibuster William Walker.",
        "longDescription": "N/A"
    },
    "Descent of Saint Dominic": {
        "shortDescription": "Religious celebration in Nicaragua honoring Saint Dominic during annual festivities.",
        "longDescription": "N/A"
    },
    "Ascent of Saint Dominic": {
        "shortDescription": "Closing celebration of Saint Dominic\u2019s festival in Nicaragua.",
        "longDescription": "N/A"
    },
    "National Concord Day": {
        "shortDescription": "Niger holiday promoting unity and peace after the Tuareg conflict.",
        "longDescription": "N/A"
    },
    "Anniversary of the CNSP Coup": {
        "shortDescription": "Niger holiday marking the military coup of 2023.",
        "longDescription": "N/A"
    },
    "Anniversary of the Proclamation of Independence": {
        "shortDescription": "Niger holiday celebrating independence from France in 1960.",
        "longDescription": "N/A"
    },
    "Democracy Day": {
        "shortDescription": "Nigeria holiday commemorating the return to democracy in 1999.",
        "longDescription": "N/A"
    },
    "Day of Mourning for President Muhammadu Buhari": {
        "shortDescription": "Nigeria observance honoring late President Buhari.",
        "longDescription": "N/A"
    },
    "Takai Commission Holiday": {
        "shortDescription": "Local observance in Nigeria tied to traditional leadership or commission events.",
        "longDescription": "N/A"
    },
    "Constitution Day Holiday": {
        "shortDescription": "Public holiday in Nigeria marking the adoption of the constitution.",
        "longDescription": "N/A"
    },
    "Peniamina Gospel Day": {
        "shortDescription": "Samoa holiday marking introduction of Christianity by Peniamina in 1830.",
        "longDescription": "N/A"
    },
    "Bounty Day": {
        "shortDescription": "Norfolk Island holiday commemorating the Bounty mutineers\u2019 arrival in 1856.",
        "longDescription": "N/A"
    },
    "Show Day": {
        "shortDescription": "Agricultural fair holiday in Norfolk Island.",
        "longDescription": "N/A"
    },
    "National Uprising Day": {
        "shortDescription": "North Macedonia holiday marking the 1941 anti-fascist uprising.",
        "longDescription": "N/A"
    },
    "Macedonian Revolutionary Struggle Day": {
        "shortDescription": "North Macedonia holiday honoring the 1893 revolutionary movement.",
        "longDescription": "N/A"
    },
    "Saint Clement of Ohrid Day": {
        "shortDescription": "Holiday in North Macedonia honoring patron saint Clement of Ohrid.",
        "longDescription": "N/A"
    },
    "Commonwealth Covenant Day": {
        "shortDescription": "Northern Mariana Islands holiday celebrating political union with the U.S.",
        "longDescription": "N/A"
    },
    "Commonwealth Cultural Day": {
        "shortDescription": "Northern Mariana Islands holiday promoting cultural heritage.",
        "longDescription": "N/A"
    },
    "Sultan's Accession Day": {
        "shortDescription": "Oman holiday celebrating the Sultan\u2019s ascension to the throne.",
        "longDescription": "N/A"
    },
    "Kashmir Solidarity Day": {
        "shortDescription": "Pakistan holiday expressing support for Kashmiris.",
        "longDescription": "N/A"
    },
    "Pakistan Day": {
        "shortDescription": "Pakistan holiday commemorating the Lahore Resolution of 1940 and Republic Day.",
        "longDescription": "N/A"
    },
    "Youm-e-Takbeer": {
        "shortDescription": "Pakistan holiday marking 1998 nuclear tests.",
        "longDescription": "N/A"
    },
    "Iqbal Day": {
        "shortDescription": "Pakistan holiday honoring poet-philosopher Allama Iqbal.",
        "longDescription": "N/A"
    },
    "Quaid-e-Azam Day": {
        "shortDescription": "Pakistan holiday celebrating the birth of founder Muhammad Ali Jinnah.",
        "longDescription": "N/A"
    },
    "Senior Citizens Day": {
        "shortDescription": "Panama holiday honoring elderly citizens.",
        "longDescription": "N/A"
    },
    "Hijri New Year": {
        "shortDescription": "Islamic New Year observed in Panama and other countries.",
        "longDescription": "N/A"
    },
    "Separation Day": {
        "shortDescription": "Panama holiday marking separation from Colombia in 1903.",
        "longDescription": "N/A"
    },
    "Colon Day": {
        "shortDescription": "Panama holiday celebrating the city of Col\u00f3n\u2019s role in independence.",
        "longDescription": "N/A"
    },
    "Los Santos Uprising Day": {
        "shortDescription": "Panama holiday marking 1821 uprising in Los Santos against Spain.",
        "longDescription": "N/A"
    },
    "Papua New Guinea Remembrance Day": {
        "shortDescription": "Holiday honoring PNG soldiers who died in World War II.",
        "longDescription": "N/A"
    },
    "Grand Chief Sir Michael Somare Remembrance Day": {
        "shortDescription": "PNG holiday honoring the country\u2019s founding leader.",
        "longDescription": "N/A"
    },
    "National Repentance Day": {
        "shortDescription": "PNG holiday dedicated to prayer and forgiveness.",
        "longDescription": "N/A"
    },
    "Patriots Day": {
        "shortDescription": "Paraguay holiday honoring those who fought for independence.",
        "longDescription": "N/A"
    },
    "National Holiday": {
        "shortDescription": "Paraguay general observance marking statehood.",
        "longDescription": "N/A"
    },
    "Chaco Armistice Day": {
        "shortDescription": "Paraguay holiday marking end of Chaco War with Bolivia in 1935.",
        "longDescription": "N/A"
    },
    "Asuncion Foundation's Day": {
        "shortDescription": "Paraguay holiday celebrating the founding of Asunci\u00f3n in 1537.",
        "longDescription": "N/A"
    },
    "Boqueron Battle Day": {
        "shortDescription": "Paraguay holiday marking a major battle of the Chaco War.",
        "longDescription": "N/A"
    },
    "Caacupe Virgin Day": {
        "shortDescription": "Paraguay holiday celebrating Virgin of Caacup\u00e9, patron saint.",
        "longDescription": "N/A"
    },
    "Battle of Arica and Flag Day": {
        "shortDescription": "Peru holiday commemorating 1880 battle and honoring national flag.",
        "longDescription": "N/A"
    },
    "Peruvian Air Force Day": {
        "shortDescription": "Peru holiday honoring the nation\u2019s air force.",
        "longDescription": "N/A"
    },
    "Great Military Parade Day": {
        "shortDescription": "Peru national holiday featuring military parades.",
        "longDescription": "N/A"
    },
    "Battle of Jun\u00edn Day": {
        "shortDescription": "Peru holiday marking independence battle of 1824.",
        "longDescription": "N/A"
    },
    "Rose of Lima Day": {
        "shortDescription": "Peru holiday honoring Saint Rose of Lima, patron saint of the Americas.",
        "longDescription": "N/A"
    },
    "Battle of Angamos Day": {
        "shortDescription": "Peru holiday commemorating 1879 naval battle during War of the Pacific.",
        "longDescription": "N/A"
    },
    "Battle of Ayacucho Day": {
        "shortDescription": "Peru holiday marking decisive 1824 independence battle.",
        "longDescription": "N/A"
    },
    "Black Saturday": {
        "shortDescription": "Philippines observance on Holy Saturday before Easter.",
        "longDescription": "N/A"
    },
    "Day of Valor": {
        "shortDescription": "Philippines holiday honoring WWII heroes, especially Bataan defenders.",
        "longDescription": "N/A"
    },
    "Ninoy Aquino Day": {
        "shortDescription": "Philippines holiday honoring assassinated senator Benigno Aquino Jr.",
        "longDescription": "N/A"
    },
    "Bonifacio Day": {
        "shortDescription": "Philippines holiday celebrating revolutionary leader Andres Bonifacio.",
        "longDescription": "N/A"
    },
    "Rizal Day": {
        "shortDescription": "Philippines holiday commemorating national hero Jose Rizal.",
        "longDescription": "N/A"
    },
    "Elections special day": {
        "shortDescription": "Philippines holiday for national or local elections.",
        "longDescription": "N/A"
    },
    "Additional special day": {
        "shortDescription": "Philippines flexible holiday declared by government.",
        "longDescription": "N/A"
    },
    "All Saints' Day Eve": {
        "shortDescription": "Philippines observance on October 31 ahead of All Saints\u2019 Day.",
        "longDescription": "N/A"
    },
    "Pitcairn Day": {
        "shortDescription": "Pitcairn Islands holiday marking settlement by Bounty mutineers.",
        "longDescription": "N/A"
    },
    "National Day of the Third of May": {
        "shortDescription": "Poland holiday marking 1791 Constitution Day.",
        "longDescription": "N/A"
    },
    "Pentecost": {
        "shortDescription": "Christian feast marking descent of the Holy Spirit on apostles.",
        "longDescription": "N/A"
    },
    "Day of Portugal, Cam\u00f5es, and the Portuguese Communities": {
        "shortDescription": "Portugal holiday celebrating national poet Cam\u00f5es and communities worldwide.",
        "longDescription": "N/A"
    },
    "Saint Joanna's Day": {
        "shortDescription": "Portugal religious observance honoring Saint Joanna.",
        "longDescription": "N/A"
    },
    "Feast of Our Lady of Graces": {
        "shortDescription": "Portugal holiday celebrating Our Lady of Graces.",
        "longDescription": "N/A"
    },
    "Feast of Our Lady of Mi\u00e9rcoles": {
        "shortDescription": "Local feast day in Portugal honoring Mary.",
        "longDescription": "N/A"
    },
    "Saint Elizabeth's Day": {
        "shortDescription": "Portugal holiday honoring Saint Elizabeth of Portugal.",
        "longDescription": "N/A"
    },
    "Municipal Holiday of Faro": {
        "shortDescription": "Regional holiday in Faro, Portugal.",
        "longDescription": "N/A"
    },
    "Municipal Holiday of Guarda": {
        "shortDescription": "Regional holiday in Guarda, Portugal.",
        "longDescription": "N/A"
    },
    "Municipal Holiday of Leiria": {
        "shortDescription": "Regional holiday in Leiria, Portugal.",
        "longDescription": "N/A"
    },
    "Municipal Holiday of Portalegre": {
        "shortDescription": "Regional holiday in Portalegre, Portugal.",
        "longDescription": "N/A"
    },
    "Bocage Day": {
        "shortDescription": "Portugal holiday honoring poet Manuel Bocage in Set\u00fabal.",
        "longDescription": "N/A"
    },
    "Feast of Our Lady of Sorrows": {
        "shortDescription": "Christian feast commemorating the sorrows of Virgin Mary.",
        "longDescription": "N/A"
    },
    "Saint Matthew's Day": {
        "shortDescription": "Christian feast honoring apostle Matthew.",
        "longDescription": "N/A"
    },
    "Day of the Autonomous Region of the Azores": {
        "shortDescription": "Portugal holiday celebrating Azores\u2019 autonomy.",
        "longDescription": "N/A"
    },
    "Day of the Autonomous Region of Madeira and the Madeiran Communities": {
        "shortDescription": "Portugal holiday celebrating Madeira\u2019s autonomy and diaspora.",
        "longDescription": "N/A"
    },
    "1st Octave": {
        "shortDescription": "Religious observance marking the eighth day after a major feast.",
        "longDescription": "N/A"
    },
    "Presidents' Day": {
        "shortDescription": "Qatar holiday honoring the nation\u2019s leadership.",
        "longDescription": "N/A"
    },
    "National Sports Day": {
        "shortDescription": "Qatar holiday promoting health and physical activity.",
        "longDescription": "N/A"
    },
    "Qatar National Day": {
        "shortDescription": "Qatar holiday celebrating independence from Britain in 1971.",
        "longDescription": "N/A"
    },
    "New Year's Holiday": {
        "shortDescription": "Qatar holiday marking Gregorian New Year.",
        "longDescription": "N/A"
    },
    "Saint John the Baptist": {
        "shortDescription": "Christian feast celebrating birth of John the Baptist.",
        "longDescription": "N/A"
    },
    "Unification of the Romanian Principalities Day": {
        "shortDescription": "Romania holiday celebrating 1859 union of Wallachia and Moldavia.",
        "longDescription": "N/A"
    },
    "New Year Holidays": {
        "shortDescription": "Russia holiday marking New Year celebrations.",
        "longDescription": "N/A"
    },
    "Holiday of Spring and Labor": {
        "shortDescription": "Russia holiday marking International Workers\u2019 Day on May 1.",
        "longDescription": "N/A"
    },
    "Russia Day": {
        "shortDescription": "Russia national holiday celebrating sovereignty declaration in 1990.",
        "longDescription": "N/A"
    },
    "Memorial Day of Genocide perpetrated against the Tutsi in 1994": {
        "shortDescription": "Rwanda holiday remembering genocide victims.",
        "longDescription": "N/A"
    },
    "Umuganura Day": {
        "shortDescription": "Rwanda harvest festival and national thanksgiving holiday.",
        "longDescription": "N/A"
    },
    "Saint Helena Day": {
        "shortDescription": "Saint Helena holiday commemorating discovery of the island in 1502.",
        "longDescription": "N/A"
    },
    "Ratting Day": {
        "shortDescription": "Saint Helena holiday marking the eradication of rats in 1960s.",
        "longDescription": "N/A"
    },
    "Anniversary Day": {
        "shortDescription": "Saint Helena holiday commemorating British annexation in 1834.",
        "longDescription": "N/A"
    },
    "Carnival Day - Last Lap": {
        "shortDescription": "Saint Kitts & Nevis holiday marking final day of Carnival celebrations.",
        "longDescription": "N/A"
    },
    "Culturama Day - Last Lap": {
        "shortDescription": "Saint Kitts & Nevis holiday marking final day of Culturama festival.",
        "longDescription": "N/A"
    },
    "National Workers' Day": {
        "shortDescription": "Saint Lucia holiday marking International Workers\u2019 Day.",
        "longDescription": "N/A"
    },
    "National Spiritual Baptist Day": {
        "shortDescription": "Saint Lucia holiday honoring the Spiritual Baptist faith.",
        "longDescription": "N/A"
    },
    "The Day After New Year's Day": {
        "shortDescription": "Saint Lucia public holiday extending New Year celebrations.",
        "longDescription": "N/A"
    },
    "Day After Good Friday": {
        "shortDescription": "Saint Lucia public holiday observed on Easter Saturday.",
        "longDescription": "N/A"
    },
    "Anniversary of the Liberation of the Republic and Feast of Saint Agatha": {
        "shortDescription": "San Marino holiday celebrating liberation and patron saint.",
        "longDescription": "N/A"
    },
    "Anniversary of the Arengo": {
        "shortDescription": "San Marino holiday marking establishment of popular assembly in 1906.",
        "longDescription": "N/A"
    },
    "Investiture of Captains Regent": {
        "shortDescription": "San Marino holiday marking swearing-in of heads of state (twice yearly).",
        "longDescription": "N/A"
    },
    "Anniversary of the Fall of Fascism and Freedom Day": {
        "shortDescription": "San Marino holiday commemorating 1943 fall of fascism.",
        "longDescription": "N/A"
    },
    "Saint Marinus' Day, Anniversary of the Founding of the Republic": {
        "shortDescription": "San Marino national holiday celebrating founding by Saint Marinus.",
        "longDescription": "N/A"
    },
    "Commemoration of the Dead": {
        "shortDescription": "San Marino observance honoring deceased relatives and citizens.",
        "longDescription": "N/A"
    },
    "Day of King Amador": {
        "shortDescription": "S\u00e3o Tom\u00e9 and Pr\u00edncipe holiday honoring slave rebellion leader King Amador.",
        "longDescription": "N/A"
    },
    "Agricultural Reform Day": {
        "shortDescription": "S\u00e3o Tom\u00e9 holiday marking land reforms.",
        "longDescription": "N/A"
    },
    "S\u00e3o Tom\u00e9 Day": {
        "shortDescription": "S\u00e3o Tom\u00e9 holiday celebrating the island\u2019s naming after Saint Thomas.",
        "longDescription": "N/A"
    },
    "Discovery of Pr\u00edncipe Island": {
        "shortDescription": "Holiday marking discovery of Pr\u00edncipe by Portuguese explorers.",
        "longDescription": "N/A"
    },
    "S\u00e3o Louren\u00e7o Day": {
        "shortDescription": "S\u00e3o Tom\u00e9 holiday honoring Saint Lawrence.",
        "longDescription": "N/A"
    },
    "Founding Day Holiday": {
        "shortDescription": "Saudi Arabia holiday marking state\u2019s founding in 1727.",
        "longDescription": "N/A"
    },
    "National Day Holiday": {
        "shortDescription": "Saudi Arabia holiday celebrating unification in 1932.",
        "longDescription": "N/A"
    },
    "Grand Magal of Touba": {
        "shortDescription": "Senegal pilgrimage festival honoring Sufi leader Amadou Bamba.",
        "longDescription": "N/A"
    },
    "New Year Holiday": {
        "shortDescription": "Senegal holiday marking Gregorian New Year.",
        "longDescription": "N/A"
    },
    "Polling Day": {
        "shortDescription": "Senegal holiday for national elections.",
        "longDescription": "N/A"
    },
    "Sint Maarten Day": {
        "shortDescription": "Sint Maarten holiday celebrating island\u2019s patron saint.",
        "longDescription": "N/A"
    },
    "Day of the Establishment of the Slovak Republic": {
        "shortDescription": "Slovakia holiday marking independence in 1993.",
        "longDescription": "N/A"
    },
    "Slovak National Uprising Anniversary": {
        "shortDescription": "Slovakia holiday commemorating 1944 anti-Nazi uprising.",
        "longDescription": "N/A"
    },
    "Day of Our Lady of the Seven Sorrows": {
        "shortDescription": "Slovakia holiday honoring Virgin Mary, patron saint of Slovakia.",
        "longDescription": "N/A"
    },
    "Struggle for Freedom and Democracy Day": {
        "shortDescription": "Slovakia holiday marking 1989 Velvet Revolution.",
        "longDescription": "N/A"
    },
    "Pre\u0161eren's Day, the Slovenian Cultural Holiday": {
        "shortDescription": "Slovenia holiday celebrating national poet France Pre\u0161eren.",
        "longDescription": "N/A"
    },
    "Day of Uprising Against Occupation": {
        "shortDescription": "Slovenia holiday commemorating WWII anti-fascist resistance.",
        "longDescription": "N/A"
    },
    "Day of Remembrance for the Dead": {
        "shortDescription": "Slovenia holiday honoring deceased relatives.",
        "longDescription": "N/A"
    },
    "Independence and Unity Day": {
        "shortDescription": "Slovenia holiday marking independence referendum of 1990.",
        "longDescription": "N/A"
    },
    "National Day of Thanksgiving": {
        "shortDescription": "Solomon Islands holiday for national gratitude.",
        "longDescription": "N/A"
    },
    "Central Province Day": {
        "shortDescription": "Solomon Islands holiday celebrating Central Province.",
        "longDescription": "N/A"
    },
    "Choiseul Province Day": {
        "shortDescription": "Solomon Islands holiday celebrating Choiseul Province.",
        "longDescription": "N/A"
    },
    "Guadalcanal Province Day": {
        "shortDescription": "Solomon Islands holiday celebrating Guadalcanal Province.",
        "longDescription": "N/A"
    },
    "Isabel Province Day": {
        "shortDescription": "Solomon Islands holiday celebrating Isabel Province.",
        "longDescription": "N/A"
    },
    "Makira-Ulawa Province Day": {
        "shortDescription": "Solomon Islands holiday celebrating Makira-Ulawa Province.",
        "longDescription": "N/A"
    },
    "Malaita Province Day": {
        "shortDescription": "Solomon Islands holiday celebrating Malaita Province.",
        "longDescription": "N/A"
    },
    "Rennell and Bellona Province Day": {
        "shortDescription": "Solomon Islands holiday celebrating Rennell and Bellona Province.",
        "longDescription": "N/A"
    },
    "Temotu Province Day; Whit Monday": {
        "shortDescription": "Solomon Islands holiday for Temotu Province and Christian Whit Monday.",
        "longDescription": "N/A"
    },
    "Temotu Province Day": {
        "shortDescription": "Solomon Islands holiday celebrating Temotu Province.",
        "longDescription": "N/A"
    },
    "Western Province Day": {
        "shortDescription": "Solomon Islands holiday celebrating Western Province.",
        "longDescription": "N/A"
    },
    "Independence Day; Islamic New Year": {
        "shortDescription": "Somalia holiday marking independence and Islamic New Year.",
        "longDescription": "N/A"
    },
    "Day of Reconciliation": {
        "shortDescription": "South Africa holiday promoting national unity after apartheid.",
        "longDescription": "N/A"
    },
    "Day of Goodwill": {
        "shortDescription": "South Africa holiday observed on December 26 for charity and kindness.",
        "longDescription": "N/A"
    },
    "Human Rights Day": {
        "shortDescription": "South Africa holiday commemorating 1960 Sharpeville Massacre.",
        "longDescription": "N/A"
    },
    "National Women's Day": {
        "shortDescription": "South Africa holiday honoring women\u2019s march against apartheid laws in 1956.",
        "longDescription": "N/A"
    },
    "Possession Day": {
        "shortDescription": "South Georgia holiday commemorating British claim of island in 1775.",
        "longDescription": "N/A"
    },
    "Shackleton Day": {
        "shortDescription": "South Georgia holiday honoring explorer Ernest Shackleton.",
        "longDescription": "N/A"
    },
    "Mid-winter Day": {
        "shortDescription": "South Georgia holiday celebrating midwinter in the Antarctic region.",
        "longDescription": "N/A"
    },
    "Environment Day": {
        "shortDescription": "South Georgia holiday promoting environmental awareness.",
        "longDescription": "N/A"
    },
    "Korean New Year": {
        "shortDescription": "South Korea holiday celebrating Lunar New Year (Seollal).",
        "longDescription": "N/A"
    },
    "The day preceding Korean New Year": {
        "shortDescription": "South Korea holiday before Seollal celebrations.",
        "longDescription": "N/A"
    },
    "The second day of Korean New Year": {
        "shortDescription": "South Korea holiday after Seollal celebrations.",
        "longDescription": "N/A"
    },
    "Independence Movement Day": {
        "shortDescription": "South Korea holiday commemorating 1919 March 1st independence movement.",
        "longDescription": "N/A"
    },
    "Buddha's Birthday; Children's Day": {
        "shortDescription": "South Korea holiday celebrating Buddha\u2019s birth and national Children\u2019s Day.",
        "longDescription": "N/A"
    },
    "National Foundation Day": {
        "shortDescription": "South Korea holiday marking legendary founding of Gojoseon in 2333 BC.",
        "longDescription": "N/A"
    },
    "Hangul Day": {
        "shortDescription": "South Korea holiday celebrating creation of Korean alphabet in 1443.",
        "longDescription": "N/A"
    },
    "Chuseok": {
        "shortDescription": "South Korea harvest festival similar to Thanksgiving.",
        "longDescription": "N/A"
    },
    "The day preceding Chuseok": {
        "shortDescription": "South Korea holiday before Chuseok celebrations.",
        "longDescription": "N/A"
    },
    "The second day of Chuseok": {
        "shortDescription": "South Korea holiday after Chuseok celebrations.",
        "longDescription": "N/A"
    },
    "Alternative holiday for Independence Movement Day": {
        "shortDescription": "South Korea substitute holiday when March 1st overlaps weekend.",
        "longDescription": "N/A"
    },
    "Alternative holiday for Buddha's Birthday; Alternative holiday for Children's Day": {
        "shortDescription": "South Korea substitute holiday for Buddha\u2019s Birthday or Children\u2019s Day.",
        "longDescription": "N/A"
    },
    "Alternative holiday for Chuseok": {
        "shortDescription": "South Korea substitute holiday when Chuseok overlaps weekend.",
        "longDescription": "N/A"
    },
    "Temporary Public Holiday": {
        "shortDescription": "South Korea government-declared holiday for special occasions.",
        "longDescription": "N/A"
    },
    "Presidential Election Day": {
        "shortDescription": "South Korea public holiday for presidential elections.",
        "longDescription": "N/A"
    },
    "Peace Agreement Day": {
        "shortDescription": "South Sudan holiday commemorating peace accords.",
        "longDescription": "N/A"
    },
    "SPLA Day": {
        "shortDescription": "South Sudan holiday honoring Sudan People\u2019s Liberation Army.",
        "longDescription": "N/A"
    },
    "Andalusia Day": {
        "shortDescription": "Spain holiday celebrating autonomy of Andalusia region.",
        "longDescription": "N/A"
    },
    "Monday following National Day": {
        "shortDescription": "Spain observance when National Day is shifted to Monday.",
        "longDescription": "N/A"
    },
    "Asturia Day": {
        "shortDescription": "Spain holiday celebrating autonomy of Asturias region.",
        "longDescription": "N/A"
    },
    "Cantabria Institutions Day": {
        "shortDescription": "Spain holiday celebrating establishment of Cantabria\u2019s parliament.",
        "longDescription": "N/A"
    },
    "Our Lady of the Bien Aparecida": {
        "shortDescription": "Cantabria holiday honoring its patron saint.",
        "longDescription": "N/A"
    },
    "Santa Maria of Africa": {
        "shortDescription": "Ceuta holiday honoring patroness Virgin Mary of Africa.",
        "longDescription": "N/A"
    },
    "Castile and Le\u00f3n Day": {
        "shortDescription": "Spain holiday celebrating autonomy of Castile and Le\u00f3n region.",
        "longDescription": "N/A"
    },
    "Castilla-La Mancha Day": {
        "shortDescription": "Spain holiday celebrating autonomy of Castilla-La Mancha region.",
        "longDescription": "N/A"
    },
    "Day of the Canary Islands": {
        "shortDescription": "Spain holiday celebrating autonomy of Canary Islands.",
        "longDescription": "N/A"
    },
    "National Day of Catalonia": {
        "shortDescription": "Commemoration of the fall of Barcelona in 1714 during the War of Spanish Succession, celebrated as Catalonia's national holiday.",
        "longDescription": "N/A"
    },
    "Extremadura Day": {
        "shortDescription": "Regional holiday in Extremadura, Spain, marking its cultural identity and autonomy.",
        "longDescription": "N/A"
    },
    "Galician Literature Day": {
        "shortDescription": "Celebration of the literary heritage of Galicia, honoring a chosen Galician author each year.",
        "longDescription": "N/A"
    },
    "Galician National Day": {
        "shortDescription": "Commemoration of Galician cultural and political identity.",
        "longDescription": "N/A"
    },
    "Day of the Balearic Islands": {
        "shortDescription": "Holiday in the Balearic Islands celebrating the Statute of Autonomy.",
        "longDescription": "N/A"
    },
    "Murcia Day": {
        "shortDescription": "Regional holiday celebrating the Statute of Autonomy of the Region of Murcia.",
        "longDescription": "N/A"
    },
    "Madrid Day": {
        "shortDescription": "Commemorates the 1808 uprising of Madrid citizens against Napoleonic troops.",
        "longDescription": "N/A"
    },
    "Saint Francis Xavier's Day": {
        "shortDescription": "Feast of Saint Francis Xavier, patron saint of Navarre, Spain.",
        "longDescription": "N/A"
    },
    "La Rioja Day": {
        "shortDescription": "Regional holiday commemorating the autonomy of La Rioja.",
        "longDescription": "N/A"
    },
    "Valencian Community Day": {
        "shortDescription": "Commemorates the entry of King James I into Valencia in 1238.",
        "longDescription": "N/A"
    },
    "Tamil Thai Pongal Day": {
        "shortDescription": "Tamil harvest festival giving thanks to the Sun God.",
        "longDescription": "N/A"
    },
    "Sinhala and Tamil New Year": {
        "shortDescription": "New Year festival in Sri Lanka based on the sun\u2019s movement into Aries.",
        "longDescription": "N/A"
    },
    "Day Before Sinhala and Tamil New Year": {
        "shortDescription": "Preparatory day for the Sinhala and Tamil New Year festivities.",
        "longDescription": "N/A"
    },
    "Maha Sivarathri Day": {
        "shortDescription": "Hindu festival dedicated to the worship of Lord Shiva.",
        "longDescription": "N/A"
    },
    "Deepavali Festival Day": {
        "shortDescription": "Festival of Lights celebrated by Hindus, symbolizing victory of light over darkness.",
        "longDescription": "N/A"
    },
    "Duruthu Full Moon Poya Day": {
        "shortDescription": "Marks Buddha\u2019s first visit to Sri Lanka to resolve disputes.",
        "longDescription": "N/A"
    },
    "Nawam Full Moon Poya Day": {
        "shortDescription": "Celebrates the appointment of Buddha\u2019s chief disciples Sariputta and Moggallana.",
        "longDescription": "N/A"
    },
    "Medin Full Moon Poya Day": {
        "shortDescription": "Commemorates Buddha\u2019s first visit to his father\u2019s home after Enlightenment.",
        "longDescription": "N/A"
    },
    "Bak Full Moon Poya Day": {
        "shortDescription": "Marks the second visit of the Buddha to Sri Lanka.",
        "longDescription": "N/A"
    },
    "Vesak Full Moon Poya Day": {
        "shortDescription": "Celebrates the birth, enlightenment, and death of the Buddha.",
        "longDescription": "N/A"
    },
    "Day Following Vesak Full Moon Poya Day": {
        "shortDescription": "Day after Vesak, continuing the observances.",
        "longDescription": "N/A"
    },
    "Poson Full Moon Poya Day": {
        "shortDescription": "Marks the introduction of Buddhism to Sri Lanka by Mahinda.",
        "longDescription": "N/A"
    },
    "Esala Full Moon Poya Day": {
        "shortDescription": "Commemorates Buddha\u2019s first sermon, celebrated with the Kandy Perahera.",
        "longDescription": "N/A"
    },
    "Nikini Full Moon Poya Day": {
        "shortDescription": "Marks the First Dhamma Council and the retreat season for monks.",
        "longDescription": "N/A"
    },
    "Binara Full Moon Poya Day": {
        "shortDescription": "Commemorates the ordination of the first Buddhist nuns.",
        "longDescription": "N/A"
    },
    "Vap Full Moon Poya Day": {
        "shortDescription": "Marks the end of the monastic rains retreat.",
        "longDescription": "N/A"
    },
    "Il Full Moon Poya Day": {
        "shortDescription": "Commemorates the Buddha preaching the Abhidhamma to the gods.",
        "longDescription": "N/A"
    },
    "Unduvap Full Moon Poya Day": {
        "shortDescription": "Marks the arrival of the sacred Bodhi tree sapling in Sri Lanka.",
        "longDescription": "N/A"
    },
    "Coptic Christmas": {
        "shortDescription": "Orthodox Christian celebration of the birth of Jesus on January 7.",
        "longDescription": "N/A"
    },
    "Coptic Easter": {
        "shortDescription": "Celebration of the resurrection of Jesus according to the Coptic Orthodox Church.",
        "longDescription": "N/A"
    },
    "Day of Freedoms": {
        "shortDescription": "Public holiday marking freedoms and democracy (varies by country).",
        "longDescription": "N/A"
    },
    "Indigenous People Day": {
        "shortDescription": "Honors the history and cultures of Indigenous peoples.",
        "longDescription": "N/A"
    },
    "Day of the Maroons": {
        "shortDescription": "Commemoration of escaped enslaved peoples who formed independent communities.",
        "longDescription": "N/A"
    },
    "Easter Sunday; Sunday": {
        "shortDescription": "Christian festival celebrating the resurrection of Jesus Christ.",
        "longDescription": "N/A"
    },
    "National Day of Sweden": {
        "shortDescription": "Commemorates Gustav Vasa\u2019s election in 1523 and adoption of a new constitution in 1809.",
        "longDescription": "N/A"
    },
    "Sunday; Whit Sunday": {
        "shortDescription": "Christian feast of Pentecost, marking the descent of the Holy Spirit.",
        "longDescription": "N/A"
    },
    "Sunday": {
        "shortDescription": "General Christian observance day of rest and worship.",
        "longDescription": "N/A"
    },
    "Saint Berchtold's Day": {
        "shortDescription": "Swiss holiday celebrated after New Year\u2019s Day, mostly in certain cantons.",
        "longDescription": "N/A"
    },
    "Genevan Fast": {
        "shortDescription": "Day of fasting and thanksgiving in the Canton of Geneva.",
        "longDescription": "N/A"
    },
    "Battle of Naefels Victory Day": {
        "shortDescription": "Swiss holiday commemorating the 1388 victory of Glarus over Habsburg forces.",
        "longDescription": "N/A"
    },
    "Saint Nicholas of Fl\u00fce": {
        "shortDescription": "Feast of the patron saint of Switzerland, Nicholas of Fl\u00fce.",
        "longDescription": "N/A"
    },
    "Saints Peter and Paul": {
        "shortDescription": "Feast of apostles Peter and Paul, significant in Catholic tradition.",
        "longDescription": "N/A"
    },
    "Prayer Monday": {
        "shortDescription": "Swiss Protestant holiday observed after Pentecost.",
        "longDescription": "N/A"
    },
    "Gregorian Easter Sunday; Julian Easter Sunday": {
        "shortDescription": "Christian Easter celebrated on either Gregorian or Julian calendar dates.",
        "longDescription": "N/A"
    },
    "Tishreen Liberation War Day": {
        "shortDescription": "Syrian holiday marking the October War of 1973 against Israel.",
        "longDescription": "N/A"
    },
    "Founding Day of the Republic of China": {
        "shortDescription": "Marks the founding of the ROC on January 1, 1912.",
        "longDescription": "N/A"
    },
    "Peace Memorial Day": {
        "shortDescription": "Commemorates the 1947 February 28 Incident in Taiwan.",
        "longDescription": "N/A"
    },
    "Children's Day; Tomb-Sweeping Day": {
        "shortDescription": "Celebrates children\u2019s rights and honors ancestors by cleaning graves.",
        "longDescription": "N/A"
    },
    "Confucius' Birthday": {
        "shortDescription": "Honors the birth of the Chinese philosopher Confucius.",
        "longDescription": "N/A"
    },
    "Taiwan Restoration and Guningtou Victory Memorial Day": {
        "shortDescription": "Marks Taiwan\u2019s liberation from Japan in 1945 and military victory at Guningtou in 1949.",
        "longDescription": "N/A"
    },
    "International Nowruz Day": {
        "shortDescription": "Persian New Year festival marking the spring equinox.",
        "longDescription": "N/A"
    },
    "Zanzibar Revolution Day": {
        "shortDescription": "Commemorates the 1964 revolution that overthrew the Sultanate of Zanzibar.",
        "longDescription": "N/A"
    },
    "The Sheikh Abeid Amani Karume Day": {
        "shortDescription": "Honors the first president of Zanzibar.",
        "longDescription": "N/A"
    },
    "Union Celebrations": {
        "shortDescription": "Celebrates the union of Tanganyika and Zanzibar in 1964 to form Tanzania.",
        "longDescription": "N/A"
    },
    "International Trade Fair": {
        "shortDescription": "Annual Tanzanian event promoting trade and commerce.",
        "longDescription": "N/A"
    },
    "Peasants' Day": {
        "shortDescription": "Tanzanian holiday honoring farmers\u2019 contributions to the economy.",
        "longDescription": "N/A"
    },
    "The Mwalimu Nyerere Day and Climax of the Uhuru Torch Race": {
        "shortDescription": "Commemorates Tanzania\u2019s founding father Julius Nyerere and national unity.",
        "longDescription": "N/A"
    },
    "National Children's Day": {
        "shortDescription": "Celebrates children and promotes child welfare.",
        "longDescription": "N/A"
    },
    "Chakri Memorial Day": {
        "shortDescription": "Thailand holiday honoring the Chakri dynasty kings.",
        "longDescription": "N/A"
    },
    "Songkran Festival": {
        "shortDescription": "Thai New Year festival, celebrated with water-related traditions.",
        "longDescription": "N/A"
    },
    "National Labor Day": {
        "shortDescription": "Public holiday honoring workers and labor rights.",
        "longDescription": "N/A"
    },
    "HM King Bhumibol Adulyadej the Great's Birthday; National Day; National Father's Day": {
        "shortDescription": "Marks the late king\u2019s birthday, observed as National and Father\u2019s Day in Thailand.",
        "longDescription": "N/A"
    },
    "Coronation Day": {
        "shortDescription": "Marks the coronation of the Thai monarch.",
        "longDescription": "N/A"
    },
    "HM Queen Suthida's Birthday": {
        "shortDescription": "Celebrates the birthday of Queen Suthida of Thailand.",
        "longDescription": "N/A"
    },
    "HM King Maha Vajiralongkorn's Birthday": {
        "shortDescription": "Celebrates the birthday of Thailand\u2019s reigning king.",
        "longDescription": "N/A"
    },
    "HM Queen Sirikit The Queen Mother's Birthday; National Mother's Day": {
        "shortDescription": "Marks Queen Sirikit\u2019s birthday, also celebrated as Mother\u2019s Day.",
        "longDescription": "N/A"
    },
    "HM King Bhumibol Adulyadej Memorial Day": {
        "shortDescription": "Commemorates the passing of King Bhumibol.",
        "longDescription": "N/A"
    },
    "HM King Chulalongkorn Memorial Day": {
        "shortDescription": "Honors King Rama V for his reforms in Thailand.",
        "longDescription": "N/A"
    },
    "Makha Bucha": {
        "shortDescription": "Buddhist holiday marking the gathering of 1,250 monks to hear Buddha\u2019s teachings.",
        "longDescription": "N/A"
    },
    "Visakha Bucha": {
        "shortDescription": "Buddhist holiday celebrating the birth, enlightenment, and passing of Buddha.",
        "longDescription": "N/A"
    },
    "Buddhist Lent Day": {
        "shortDescription": "Marks the beginning of the Buddhist monks\u2019 three-month retreat.",
        "longDescription": "N/A"
    },
    "Asarnha Bucha": {
        "shortDescription": "Commemorates the Buddha\u2019s first sermon at Deer Park.",
        "longDescription": "N/A"
    },
    "Veteran's Day": {
        "shortDescription": "Honors military veterans.",
        "longDescription": "N/A"
    },
    "Popular Consultation Day": {
        "shortDescription": "Day for national referendum or consultation (specific to certain countries).",
        "longDescription": "N/A"
    },
    "Day of Our Lady of Immaculate Conception and Timor-Leste Patroness": {
        "shortDescription": "Catholic feast and national holiday in East Timor.",
        "longDescription": "N/A"
    },
    "Holy Friday": {
        "shortDescription": "Christian holiday commemorating the crucifixion of Jesus.",
        "longDescription": "N/A"
    },
    "Tokehega Day": {
        "shortDescription": "Holiday commemorating the Treaty of Tokehega between Tokelau and the U.S.",
        "longDescription": "N/A"
    },
    "Birthday of the Reigning Sovereign of Tonga": {
        "shortDescription": "Celebrates Tonga\u2019s monarch\u2019s birthday.",
        "longDescription": "N/A"
    },
    "Birthday of the Heir to the Crown of Tonga": {
        "shortDescription": "Honors the crown prince or princess of Tonga.",
        "longDescription": "N/A"
    },
    "Anniversary of the Coronation of HM King George Tupou I": {
        "shortDescription": "Marks the coronation of Tonga\u2019s first king.",
        "longDescription": "N/A"
    },
    "Spiritual Baptist Liberation Day": {
        "shortDescription": "Commemorates the repeal of laws prohibiting the Spiritual Baptist faith in Trinidad and Tobago.",
        "longDescription": "N/A"
    },
    "Indian Arrival Day": {
        "shortDescription": "Marks the arrival of the first Indian indentured laborers to Trinidad in 1845.",
        "longDescription": "N/A"
    },
    "Corpus Christi; Labor Day": {
        "shortDescription": "Christian feast celebrating the Eucharist; also a workers' rights holiday in some countries.",
        "longDescription": "N/A"
    },
    "African Emancipation Day": {
        "shortDescription": "Commemorates the abolition of slavery and honors African heritage.",
        "longDescription": "N/A"
    },
    "Revolution and Youth Day": {
        "shortDescription": "Celebrates youth participation in national revolutions or independence struggles.",
        "longDescription": "N/A"
    },
    "Evacuation Day": {
        "shortDescription": "Marks the British evacuation from New York City in 1783, ending the American Revolution.",
        "longDescription": "N/A"
    },
    "National Sovereignty and Children's Day": {
        "shortDescription": "Turkish holiday combining celebration of independence and honoring children.",
        "longDescription": "N/A"
    },
    "Labour and Solidarity Day": {
        "shortDescription": "International Workers\u2019 Day observed on May 1.",
        "longDescription": "N/A"
    },
    "Commemoration of Atat\u00fcrk, Youth and Sports Day": {
        "shortDescription": "Turkish holiday marking Atat\u00fcrk\u2019s legacy and celebrating youth and sports.",
        "longDescription": "N/A"
    },
    "Democracy and National Unity Day": {
        "shortDescription": "Turkish holiday honoring those who defended democracy during the 2016 coup attempt.",
        "longDescription": "N/A"
    },
    "Constitution and State Flag Day": {
        "shortDescription": "Celebrates adoption of national constitution and flag (Turkmenistan).",
        "longDescription": "N/A"
    },
    "International Neutrality Day": {
        "shortDescription": "Marks Turkmenistan\u2019s official neutrality status recognized by the UN.",
        "longDescription": "N/A"
    },
    "Commonwealth Day": {
        "shortDescription": "Celebrates unity and cooperation among Commonwealth nations.",
        "longDescription": "N/A"
    },
    "JAGS McCartney Day": {
        "shortDescription": "Turks and Caicos holiday honoring national hero James Alexander George Smith McCartney.",
        "longDescription": "N/A"
    },
    "National Heritage Day": {
        "shortDescription": "Holiday to celebrate cultural heritage (observed in multiple countries).",
        "longDescription": "N/A"
    },
    "Tuvalu Day": {
        "shortDescription": "Commemorates Tuvalu's independence and identity.",
        "longDescription": "N/A"
    },
    "The Day of the Bombing": {
        "shortDescription": "Remembrance of a historic bombing event (specific to Pacific island nations).",
        "longDescription": "N/A"
    },
    "Cyclone Day": {
        "shortDescription": "Marks survival and resilience following devastating cyclones.",
        "longDescription": "N/A"
    },
    "Niutao Day": {
        "shortDescription": "Local celebration of Niutao Island, Tuvalu.",
        "longDescription": "N/A"
    },
    "Nukufetau Day": {
        "shortDescription": "Local celebration of Nukufetau Island, Tuvalu.",
        "longDescription": "N/A"
    },
    "Golden Jubilee": {
        "shortDescription": "50th anniversary celebration of independence or institution.",
        "longDescription": "N/A"
    },
    "Big Day": {
        "shortDescription": "Colloquial term for a major national celebration in Tuvalu.",
        "longDescription": "N/A"
    },
    "Nanumaga Day": {
        "shortDescription": "Local celebration of Nanumaga Island, Tuvalu.",
        "longDescription": "N/A"
    },
    "Day of the Flood": {
        "shortDescription": "Remembrance of a historic flooding disaster in Tuvalu.",
        "longDescription": "N/A"
    },
    "Happy Day": {
        "shortDescription": "Local Tuvalu holiday celebrating community joy and unity.",
        "longDescription": "N/A"
    },
    "NRM Liberation Day": {
        "shortDescription": "Ugandan holiday marking the 1986 victory of the National Resistance Movement.",
        "longDescription": "N/A"
    },
    "Archbishop Janani Luwum Day": {
        "shortDescription": "Ugandan holiday honoring Archbishop Janani Luwum, a Christian martyr.",
        "longDescription": "N/A"
    },
    "Uganda Martyrs' Day": {
        "shortDescription": "Commemorates Christian converts killed in the late 1800s in Uganda.",
        "longDescription": "N/A"
    },
    "Battle of the Boyne": {
        "shortDescription": "Commemorates the 1690 battle in Ireland between Protestant William III and Catholic James II.",
        "longDescription": "N/A"
    },
    "Three Kings Day": {
        "shortDescription": "Christian feast of the Epiphany, celebrating the Magi\u2019s visit to baby Jesus.",
        "longDescription": "N/A"
    },
    "Transfer Day": {
        "shortDescription": "Marks the 1917 transfer of the U.S. Virgin Islands from Denmark to the U.S.",
        "longDescription": "N/A"
    },
    "Holy Thursday": {
        "shortDescription": "Christian observance of the Last Supper of Jesus Christ.",
        "longDescription": "N/A"
    },
    "Columbus Day and Puerto Rico Friendship Day": {
        "shortDescription": "Marks Columbus\u2019 arrival in the Americas and Puerto Rico\u2019s friendship with the U.S.",
        "longDescription": "N/A"
    },
    "Liberty Day": {
        "shortDescription": "Celebrates freedom and independence (observed in various nations).",
        "longDescription": "N/A"
    },
    "Christmas Second Day": {
        "shortDescription": "Also known as Boxing Day, celebrated the day after Christmas.",
        "longDescription": "N/A"
    },
    "Seward's Day": {
        "shortDescription": "Alaskan holiday commemorating the purchase of Alaska from Russia.",
        "longDescription": "N/A"
    },
    "Indigenous Peoples' Day": {
        "shortDescription": "Honors Native American peoples and their history.",
        "longDescription": "N/A"
    },
    "Alaska Day": {
        "shortDescription": "Commemorates the formal transfer of Alaska from Russia to the U.S. in 1867.",
        "longDescription": "N/A"
    },
    "Martin Luther King, Jr & Robert E. Lee's Birthday": {
        "shortDescription": "Observed in some U.S. states to honor both MLK Jr. and Confederate General Robert E. Lee.",
        "longDescription": "N/A"
    },
    "George Washington & Thomas Jefferson's Birthday": {
        "shortDescription": "State holiday combining celebration of U.S. presidents Washington and Jefferson.",
        "longDescription": "N/A"
    },
    "Confederate Memorial Day": {
        "shortDescription": "Commemorates soldiers who died fighting for the Confederacy during the U.S. Civil War.",
        "longDescription": "N/A"
    },
    "Jefferson Davis Birthday": {
        "shortDescription": "Honors the president of the Confederate States of America.",
        "longDescription": "N/A"
    },
    "Columbus Day / American Indian Heritage Day / Fraternal Day": {
        "shortDescription": "Multiple observances on the same date in Alabama.",
        "longDescription": "N/A"
    },
    "George Washington's Birthday and Daisy Gatson Bates Day": {
        "shortDescription": "Arkansas holiday honoring the first U.S. president and civil rights leader Daisy Bates.",
        "longDescription": "N/A"
    },
    "Dr. Martin Luther King Jr. / Civil Rights Day": {
        "shortDescription": "Holiday honoring Martin Luther King Jr. and the civil rights movement.",
        "longDescription": "N/A"
    },
    "Lincoln/Washington Presidents' Day": {
        "shortDescription": "State observance combining Abraham Lincoln and George Washington\u2019s birthdays.",
        "longDescription": "N/A"
    },
    "Susan B. Anthony Day": {
        "shortDescription": "Honors women\u2019s rights activist Susan B. Anthony.",
        "longDescription": "N/A"
    },
    "Cesar Chavez Day": {
        "shortDescription": "Honors labor leader and civil rights activist C\u00e9sar Ch\u00e1vez.",
        "longDescription": "N/A"
    },
    "Day After Thanksgiving": {
        "shortDescription": "U.S. holiday observed the Friday after Thanksgiving.",
        "longDescription": "N/A"
    },
    "Washington-Lincoln Day": {
        "shortDescription": "Honors both George Washington and Abraham Lincoln.",
        "longDescription": "N/A"
    },
    "Frances Xavier Cabrini Day": {
        "shortDescription": "Colorado holiday honoring Mother Cabrini, the first U.S. citizen to be canonized as a saint.",
        "longDescription": "N/A"
    },
    "Lincoln's Birthday": {
        "shortDescription": "Commemorates the birth of Abraham Lincoln.",
        "longDescription": "N/A"
    },
    "Inauguration Day; Martin Luther King Jr. Day": {
        "shortDescription": "Combination holiday observed in Washington, D.C. when MLK Day falls near Inauguration Day.",
        "longDescription": "N/A"
    },
    "Friday After Thanksgiving": {
        "shortDescription": "Holiday observed in some states as an official day off following Thanksgiving.",
        "longDescription": "N/A"
    },
    "State Holiday": {
        "shortDescription": "General designation for holidays not tied to federal observances.",
        "longDescription": "N/A"
    },
    "Prince Jonah Kuhio Kalanianaole Day": {
        "shortDescription": "Hawaii holiday honoring Prince Kuhio, who worked for Native Hawaiian rights.",
        "longDescription": "N/A"
    },
    "Kamehameha Day": {
        "shortDescription": "Hawaiian holiday honoring King Kamehameha the Great.",
        "longDescription": "N/A"
    },
    "Martin Luther King Jr. / Idaho Human Rights Day": {
        "shortDescription": "Idaho holiday honoring MLK Jr. and human rights.",
        "longDescription": "N/A"
    },
    "Casimir Pulaski Day": {
        "shortDescription": "Illinois holiday honoring Revolutionary War hero Casimir Pulaski.",
        "longDescription": "N/A"
    },
    "Primary Election Day": {
        "shortDescription": "State holiday for holding primary elections.",
        "longDescription": "N/A"
    },
    "Election Day": {
        "shortDescription": "U.S. holiday for federal, state, and local elections.",
        "longDescription": "N/A"
    },
    "Mardi Gras": {
        "shortDescription": "Carnival celebration held before Ash Wednesday, especially in Louisiana.",
        "longDescription": "N/A"
    },
    "Patriots' Day": {
        "shortDescription": "Commemorates the battles of Lexington and Concord during the American Revolution.",
        "longDescription": "N/A"
    },
    "American Indian Heritage Day": {
        "shortDescription": "Recognizes the contributions and culture of Native Americans.",
        "longDescription": "N/A"
    },
    "Washington's and Lincoln's Birthday": {
        "shortDescription": "Combined holiday honoring both presidents.",
        "longDescription": "N/A"
    },
    "Truman Day": {
        "shortDescription": "Missouri holiday honoring President Harry S. Truman.",
        "longDescription": "N/A"
    },
    "Dr. Martin Luther King Jr. and Robert E. Lee's Birthdays": {
        "shortDescription": "Combined holiday in some states honoring both figures.",
        "longDescription": "N/A"
    },
    "Lincoln's and Washington's Birthdays": {
        "shortDescription": "State observance of U.S. presidents\u2019 birthdays.",
        "longDescription": "N/A"
    },
    "Arbor Day": {
        "shortDescription": "Holiday promoting tree planting and care.",
        "longDescription": "N/A"
    },
    "Nevada Day": {
        "shortDescription": "Commemorates Nevada\u2019s admission to the Union.",
        "longDescription": "N/A"
    },
    "Indigenous Peoples' Day / Columbus Day": {
        "shortDescription": "Dual observance of Indigenous heritage and Columbus\u2019 landing.",
        "longDescription": "N/A"
    },
    "Native Americans' Day": {
        "shortDescription": "Holiday in South Dakota and California honoring Native Americans.",
        "longDescription": "N/A"
    },
    "Emancipation Day In Texas; Juneteenth National Independence Day": {
        "shortDescription": "Commemorates the emancipation of enslaved African Americans in Texas, June 19, 1865.",
        "longDescription": "N/A"
    },
    "Texas Independence Day": {
        "shortDescription": "Marks Texas\u2019 declaration of independence from Mexico in 1836.",
        "longDescription": "N/A"
    },
    "San Jacinto Day": {
        "shortDescription": "Commemorates the 1836 Battle of San Jacinto, securing Texas independence.",
        "longDescription": "N/A"
    },
    "Lyndon Baines Johnson Day": {
        "shortDescription": "Texas holiday honoring President Lyndon B. Johnson.",
        "longDescription": "N/A"
    },
    "Washington and Lincoln Day": {
        "shortDescription": "State holiday combining both presidents.",
        "longDescription": "N/A"
    },
    "Pioneer Day": {
        "shortDescription": "Utah holiday celebrating Mormon pioneers\u2019 arrival in 1847.",
        "longDescription": "N/A"
    },
    "George Washington Day": {
        "shortDescription": "Virginia\u2019s state holiday honoring George Washington.",
        "longDescription": "N/A"
    },
    "Town Meeting Day": {
        "shortDescription": "Vermont holiday marking the tradition of local self-governance.",
        "longDescription": "N/A"
    },
    "Bennington Battle Day": {
        "shortDescription": "Vermont holiday commemorating the 1777 Revolutionary War battle.",
        "longDescription": "N/A"
    },
    "West Virginia Day": {
        "shortDescription": "Marks West Virginia\u2019s admission to the Union in 1863.",
        "longDescription": "N/A"
    },
    "Day of the Family": {
        "shortDescription": "Celebrates the importance of family values and unity.",
        "longDescription": "N/A"
    },
    "Day of Memory and Honor": {
        "shortDescription": "Honors veterans of World War II in former Soviet countries.",
        "longDescription": "N/A"
    },
    "Teachers and Instructors Day": {
        "shortDescription": "Celebrates the contributions of teachers and educators.",
        "longDescription": "N/A"
    },
    "Father Lini Day": {
        "shortDescription": "Vanuatu holiday honoring Father Walter Lini, the nation\u2019s founding prime minister.",
        "longDescription": "N/A"
    },
    "Custom Chief's Day": {
        "shortDescription": "Vanuatu holiday celebrating traditional leaders and chiefs.",
        "longDescription": "N/A"
    },
    "Solemnity of Mary, Mother of God": {
        "shortDescription": "Catholic holy day celebrating Mary as Mother of God.",
        "longDescription": "N/A"
    },
    "Anniversary of the Foundation of Vatican City": {
        "shortDescription": "Marks the founding of Vatican City in 1929.",
        "longDescription": "N/A"
    },
    "Name Day of the Holy Father": {
        "shortDescription": "Celebration of the Pope\u2019s namesake saint.",
        "longDescription": "N/A"
    },
    "Anniversary of the Election of the Holy Father": {
        "shortDescription": "Marks the anniversary of the Pope\u2019s election.",
        "longDescription": "N/A"
    },
    "Saint Joseph the Worker's Day": {
        "shortDescription": "Catholic feast honoring Saint Joseph as the patron of workers.",
        "longDescription": "N/A"
    },
    "Solemnity of Pentecost": {
        "shortDescription": "Christian feast commemorating the descent of the Holy Spirit.",
        "longDescription": "N/A"
    },
    "Solemnity of Holy Trinity": {
        "shortDescription": "Catholic feast celebrating the doctrine of the Holy Trinity.",
        "longDescription": "N/A"
    },
    "Corpus Domini": {
        "shortDescription": "Catholic feast of the Body and Blood of Christ.",
        "longDescription": "N/A"
    },
    "Saints Peter and Paul's Day": {
        "shortDescription": "Feast day of apostles Peter and Paul.",
        "longDescription": "N/A"
    },
    "Day Before Assumption of Mary": {
        "shortDescription": "Preparatory day before the Feast of the Assumption.",
        "longDescription": "N/A"
    },
    "Assumption of Mary Day": {
        "shortDescription": "Catholic feast celebrating Mary\u2019s assumption into heaven.",
        "longDescription": "N/A"
    },
    "Day After Assumption of Mary": {
        "shortDescription": "Observance following the Assumption feast.",
        "longDescription": "N/A"
    },
    "Saint John the Evangelist's Day": {
        "shortDescription": "Feast day of Saint John the Apostle.",
        "longDescription": "N/A"
    },
    "Last Day of the Year": {
        "shortDescription": "Celebration of New Year\u2019s Eve.",
        "longDescription": "N/A"
    },
    "Monday of Carnival": {
        "shortDescription": "Part of pre-Lenten Carnival festivities.",
        "longDescription": "N/A"
    },
    "Tuesday of Carnival": {
        "shortDescription": "Mardi Gras, final day of Carnival before Lent.",
        "longDescription": "N/A"
    },
    "Declaration of Independence": {
        "shortDescription": "Marks Venezuela\u2019s independence from Spain in 1811.",
        "longDescription": "N/A"
    },
    "Battle of Carabobo": {
        "shortDescription": "Commemorates the decisive 1821 battle in Venezuela\u2019s independence war.",
        "longDescription": "N/A"
    },
    "Birthday of Simon Bolivar": {
        "shortDescription": "Celebrates the birth of Venezuelan independence leader Sim\u00f3n Bol\u00edvar.",
        "longDescription": "N/A"
    },
    "Day of Indigenous Resistance": {
        "shortDescription": "Venezuelan holiday replacing Columbus Day to honor Indigenous peoples.",
        "longDescription": "N/A"
    },
    "Lunar New Year's Eve": {
        "shortDescription": "The evening before the Lunar New Year.",
        "longDescription": "N/A"
    },
    "Second Day of Lunar New Year": {
        "shortDescription": "Continuing celebrations of the Lunar New Year.",
        "longDescription": "N/A"
    },
    "Third Day of Lunar New Year": {
        "shortDescription": "Third day of Lunar New Year festivities.",
        "longDescription": "N/A"
    },
    "Fourth Day of Lunar New Year": {
        "shortDescription": "Fourth day of Lunar New Year festivities.",
        "longDescription": "N/A"
    },
    "Hung Kings' Commemoration Day": {
        "shortDescription": "Vietnamese holiday honoring the legendary H\u00f9ng Kings.",
        "longDescription": "N/A"
    },
    "Liberation Day/Reunification Day": {
        "shortDescription": "Marks the fall of Saigon in 1975 and Vietnam\u2019s reunification.",
        "longDescription": "N/A"
    },
    "29 of Lunar New Year": {
        "shortDescription": "Part of the extended Vietnamese New Year celebrations (Tet).",
        "longDescription": "N/A"
    },
    "Kenneth Kaunda Day": {
        "shortDescription": "Zambian holiday honoring the nation\u2019s first president Kenneth Kaunda.",
        "longDescription": "N/A"
    },
    "Africa Freedom Day": {
        "shortDescription": "Pan-African holiday commemorating the founding of the OAU in 1963.",
        "longDescription": "N/A"
    },
    "Farmers' Day": {
        "shortDescription": "Holiday recognizing the contributions of farmers.",
        "longDescription": "N/A"
    },
    "National Prayer Day": {
        "shortDescription": "Day for national reflection and prayer (observed in Zambia).",
        "longDescription": "N/A"
    },
    "Robert Gabriel Mugabe National Youth Day": {
        "shortDescription": "Zimbabwean holiday honoring the former president\u2019s birthday.",
        "longDescription": "N/A"
    },
    "Good Friday; Independence Day": {
        "shortDescription": "Christian holiday commemorating Jesus\u2019 crucifixion; also paired with independence in some countries.",
        "longDescription": "N/A"
    },
    "Zimbabwe Heroes' Day": {
        "shortDescription": "Honors those who fought for Zimbabwe\u2019s liberation.",
        "longDescription": "N/A"
    },
    "Defense Forces Day": {
        "shortDescription": "Celebrates Zimbabwe\u2019s national military forces.",
        "longDescription": "N/A"
    }
}


def filter_similar_keys(data: dict) -> dict:
    """
    Removes duplicate keys that only differ by a parenthesized suffix.
    Keeps the version without parentheses if available.
    """
    new_dict = {}
    for key, value in data.items():
        # Strip out parenthesized part and extra spaces
        base_key = re.sub(r"\s*\(.*?\)", "", key).strip()
        
        # Prefer the version without parentheses if duplicates exist
        if base_key not in new_dict or "(" in key:
            new_dict[base_key] = value
    return new_dict


def get_base_key(key: str) -> str:
    # Strip out parenthesized part and extra spaces
    base_key = re.sub(r"\s*\(.*?\)", "", key).strip()
    return base_key

def get_description_for(holiday: str):
    key = get_base_key(holiday)
    
    if key in descriptions:
        return descriptions[key]
    
    return {
        "shortDescription": "N/A",
        "longDescription": "N/A"
    }