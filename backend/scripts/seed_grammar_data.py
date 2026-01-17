"""
Seed script to populate database with grammar topics and exercises.
This creates the foundation for the grammar learning system.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app.models.grammar import GrammarTopic, GrammarExercise


def create_grammar_topics():
    """Create 50+ grammar topics with German explanations."""

    topics = [
        # ========== CASES (Fälle) ==========
        {
            "name_de": "Nominativ",
            "name_en": "Nominative Case",
            "category": "cases",
            "subcategory": "nominative",
            "difficulty_level": "A1",
            "order_index": 1,
            "description_de": "Der Nominativ ist der erste Fall und wird für das Subjekt verwendet.",
            "explanation_de": """Der Nominativ bezeichnet das Subjekt des Satzes, also die Person oder Sache, die etwas tut.

**Verwendung:**
- Subjekt des Satzes: "Der Mann arbeitet."
- Nach dem Verb 'sein': "Das ist ein Buch."

**Frage:** Wer oder was?

**Artikel:**
- Maskulin: der Mann
- Feminin: die Frau
- Neutrum: das Kind
- Plural: die Männer/Frauen/Kinder

**Beispiele:**
- Der Lehrer erklärt die Grammatik.
- Die Katze schläft auf dem Sofa.
- Das Auto ist neu.
- Die Kinder spielen im Park."""
        },
        {
            "name_de": "Akkusativ",
            "name_en": "Accusative Case",
            "category": "cases",
            "subcategory": "accusative",
            "difficulty_level": "A2",
            "order_index": 2,
            "description_de": "Der Akkusativ wird für direkte Objekte verwendet.",
            "explanation_de": """Der Akkusativ bezeichnet das direkte Objekt, also die Person oder Sache, auf die sich die Handlung bezieht.

**Verwendung:**
- Direktes Objekt: "Ich sehe den Mann."
- Nach bestimmten Präpositionen: durch, für, gegen, ohne, um
- Zeitangaben: "Ich bleibe einen Monat."

**Frage:** Wen oder was?

**Artikel:**
- Maskulin: den Mann (Änderung!)
- Feminin: die Frau (keine Änderung)
- Neutrum: das Kind (keine Änderung)
- Plural: die Männer (keine Änderung)

**Beispiele:**
- Ich kaufe einen Apfel.
- Sie liebt den Film.
- Wir besuchen das Museum.
- Er liest die Zeitung."""
        },
        {
            "name_de": "Dativ",
            "name_en": "Dative Case",
            "category": "cases",
            "subcategory": "dative",
            "difficulty_level": "A2",
            "order_index": 3,
            "description_de": "Der Dativ wird für indirekte Objekte verwendet.",
            "explanation_de": """Der Dativ bezeichnet das indirekte Objekt oder den Empfänger einer Handlung.

**Verwendung:**
- Indirektes Objekt: "Ich gebe dem Mann das Buch."
- Nach bestimmten Präpositionen: aus, bei, mit, nach, seit, von, zu
- Nach bestimmten Verben: helfen, danken, gefallen, gehören

**Frage:** Wem?

**Artikel:**
- Maskulin: dem Mann
- Feminin: der Frau
- Neutrum: dem Kind
- Plural: den Männern (+ n!)

**Beispiele:**
- Ich helfe der Frau.
- Das Buch gehört dem Lehrer.
- Sie dankt den Eltern.
- Er gibt dem Kind einen Ball."""
        },
        {
            "name_de": "Genitiv",
            "name_en": "Genitive Case",
            "category": "cases",
            "subcategory": "genitive",
            "difficulty_level": "B1",
            "order_index": 4,
            "description_de": "Der Genitiv drückt Besitz oder Zugehörigkeit aus.",
            "explanation_de": """Der Genitiv zeigt Besitz, Zugehörigkeit oder Herkunft an.

**Verwendung:**
- Besitz: "Das Auto des Mannes"
- Nach bestimmten Präpositionen: während, wegen, trotz, statt, außerhalb
- Nach bestimmten Verben: bedürfen, gedenken

**Frage:** Wessen?

**Artikel:**
- Maskulin: des Mannes (+ s/es!)
- Feminin: der Frau
- Neutrum: des Kindes (+ s/es!)
- Plural: der Männer

**Beispiele:**
- Das Haus meines Vaters ist groß.
- Während des Sommers reisen wir.
- Wegen des Regens bleiben wir zu Hause.
- Die Farbe des Autos gefällt mir."""
        },

        # ========== VERB CONJUGATION (Verben) ==========
        {
            "name_de": "Präsens (Gegenwart)",
            "name_en": "Present Tense",
            "category": "verbs",
            "subcategory": "present_tense",
            "difficulty_level": "A1",
            "order_index": 10,
            "description_de": "Das Präsens wird für gegenwärtige Handlungen verwendet.",
            "explanation_de": """Das Präsens beschreibt Handlungen in der Gegenwart oder allgemeine Wahrheiten.

**Bildung:** Wortstamm + Endung

**Endungen (regelmäßig):**
- ich: -e (ich lerne)
- du: -st (du lernst)
- er/sie/es: -t (er lernt)
- wir: -en (wir lernen)
- ihr: -t (ihr lernt)
- sie/Sie: -en (sie lernen)

**Besonderheiten:**
- Stammvokalwechsel: e→i (sprechen: er spricht), e→ie (lesen: er liest), a→ä (fahren: er fährt)
- Verben auf -t, -d: zusätzliches e (arbeiten: du arbeitest)

**Beispiele:**
- Ich wohne in Berlin.
- Du sprichst gut Deutsch.
- Er fährt nach München.
- Wir arbeiten zusammen."""
        },
        {
            "name_de": "Perfekt (Vollendete Gegenwart)",
            "name_en": "Present Perfect",
            "category": "verbs",
            "subcategory": "perfect_tense",
            "difficulty_level": "A2",
            "order_index": 11,
            "description_de": "Das Perfekt wird für abgeschlossene Handlungen in der Vergangenheit verwendet.",
            "explanation_de": """Das Perfekt beschreibt abgeschlossene Handlungen in der Vergangenheit, die Bezug zur Gegenwart haben.

**Bildung:** haben/sein + Partizip II

**Wann 'sein':**
- Bewegungsverben: gehen, fahren, kommen, laufen
- Zustandsänderung: werden, aufwachen, einschlafen, sterben
- Ausnahmen: sein, bleiben, passieren

**Wann 'haben':**
- Alle anderen Verben
- Transitive Verben (mit Akkusativobjekt)

**Partizip II:**
- Regelmäßig: ge-...-t (gemacht, gekauft, gelernt)
- Unregelmäßig: ge-...-en (gegangen, gesehen, geschrieben)
- Trennbare Verben: ein-ge-kauft, an-ge-kommen
- Untrennbare Verben: kein ge- (bekommen, verstanden, erzählt)

**Beispiele:**
- Ich habe einen Brief geschrieben.
- Sie ist nach Berlin gefahren.
- Wir haben Deutsch gelernt.
- Er ist zu Hause geblieben."""
        },
        {
            "name_de": "Präteritum (Vergangenheit)",
            "name_en": "Simple Past",
            "category": "verbs",
            "subcategory": "simple_past",
            "difficulty_level": "B1",
            "order_index": 12,
            "description_de": "Das Präteritum wird hauptsächlich in schriftlichen Texten verwendet.",
            "explanation_de": """Das Präteritum wird vor allem in schriftlicher Sprache für Erzählungen und Berichte verwendet.

**Bildung regelmäßig:** Stamm + -te + Endung
- ich lernte, du lerntest, er lernte
- wir lernten, ihr lerntet, sie lernten

**Bildung unregelmäßig:** Stammänderung + Endung
- ich ging, du gingst, er ging
- wir gingen, ihr gingt, sie gingen

**Häufige Verben (sein, haben):**
- sein: ich war, du warst, er war
- haben: ich hatte, du hattest, er hatte

**Verwendung:**
- Erzählungen und Geschichten
- Formelle schriftliche Texte
- Berichte

**Beispiele:**
- Er ging jeden Tag zur Arbeit.
- Sie hatte viel zu tun.
- Wir waren sehr glücklich.
- Das Kind spielte im Garten."""
        },
        {
            "name_de": "Futur I (Zukunft)",
            "name_en": "Future Tense I",
            "category": "verbs",
            "subcategory": "future_i",
            "difficulty_level": "B1",
            "order_index": 13,
            "description_de": "Das Futur I drückt zukünftige Handlungen oder Vermutungen aus.",
            "explanation_de": """Das Futur I beschreibt zukünftige Ereignisse oder Vermutungen.

**Bildung:** werden + Infinitiv

**Konjugation von 'werden':**
- ich werde
- du wirst
- er/sie/es wird
- wir werden
- ihr werdet
- sie/Sie werden

**Verwendung:**
- Zukünftige Handlungen: "Ich werde morgen kommen."
- Vermutungen: "Er wird wohl zu Hause sein."
- Versprechen: "Ich werde dir helfen."
- Prognosen: "Es wird regnen."

**Alternative:** Präsens + Zeitangabe
- "Ich komme morgen." (häufiger in gesprochener Sprache)

**Beispiele:**
- Wir werden nächstes Jahr nach Italien reisen.
- Sie wird die Prüfung bestehen.
- Es wird bald schneien.
- Ihr werdet Erfolg haben."""
        },
        {
            "name_de": "Modalverben",
            "name_en": "Modal Verbs",
            "category": "verbs",
            "subcategory": "modal_verbs",
            "difficulty_level": "A2",
            "order_index": 14,
            "description_de": "Modalverben drücken Möglichkeit, Notwendigkeit, Wunsch oder Fähigkeit aus.",
            "explanation_de": """Modalverben modifizieren die Bedeutung des Vollverbs.

**Die 6 Modalverben:**
- können (Fähigkeit): Ich kann schwimmen.
- müssen (Notwendigkeit): Ich muss arbeiten.
- dürfen (Erlaubnis): Du darfst hier parken.
- sollen (Pflicht/Rat): Du sollst pünktlich sein.
- wollen (Absicht): Ich will Deutsch lernen.
- mögen/möchte (Wunsch): Ich möchte Kaffee trinken.

**Besonderheiten:**
- Stammvokalwechsel im Singular Präsens
- Infinitiv am Satzende
- Im Perfekt: doppelter Infinitiv (Ich habe gehen müssen.)

**Satzstellung:**
- Ich kann gut Deutsch sprechen.
- Modalverb Position 2, Infinitiv am Ende

**Beispiele:**
- Ich muss heute arbeiten.
- Kannst du mir helfen?
- Wir dürfen hier nicht rauchen.
- Sie will Ärztin werden."""
        },
        {
            "name_de": "Konjunktiv II",
            "name_en": "Subjunctive II",
            "category": "verbs",
            "subcategory": "subjunctive_ii",
            "difficulty_level": "B2",
            "order_index": 15,
            "description_de": "Der Konjunktiv II drückt Irreales, Wünsche oder höfliche Bitten aus.",
            "explanation_de": """Der Konjunktiv II wird für irreale Bedingungen, Wünsche und höfliche Formulierungen verwendet.

**Bildung:**
- würde + Infinitiv (häufigste Form)
- Präteritum + Umlaut (bei starken Verben)

**Wichtige Formen:**
- sein: ich wäre, du wärest, er wäre
- haben: ich hätte, du hättest, er hätte
- können: ich könnte, du könntest, er könnte
- müssen: ich müsste, du müsstest, er müsste

**Verwendung:**
- Irreale Bedingungen: "Wenn ich reich wäre, würde ich reisen."
- Wünsche: "Ich wünschte, ich könnte fliegen."
- Höfliche Bitten: "Könnten Sie mir helfen?"
- Vorschläge: "Wir könnten ins Kino gehen."

**Beispiele:**
- Wenn ich Zeit hätte, würde ich dich besuchen.
- An deiner Stelle würde ich das nicht tun.
- Ich hätte gerne ein Glas Wasser.
- Es wäre schön, wenn du kommen könntest."""
        },
        {
            "name_de": "Trennbare Verben",
            "name_en": "Separable Verbs",
            "category": "verbs",
            "subcategory": "separable_verbs",
            "difficulty_level": "A2",
            "order_index": 16,
            "description_de": "Trennbare Verben bestehen aus Präfix und Verb, die getrennt werden.",
            "explanation_de": """Trennbare Verben haben ein betontes Präfix, das im Hauptsatz am Ende steht.

**Häufige trennbare Präfixe:**
- an, auf, aus, ein, mit, nach, vor, zu, zurück, weg
- Betonung auf dem Präfix!

**Satzstellung:**
- Präsens/Präteritum: Präfix am Ende
  "Ich rufe dich an."
- Perfekt: Präfix + ge + Verb
  "Ich habe dich angerufen."
- Infinitiv mit zu: Präfix + zu + Verb
  "Ich hoffe, dich anzurufen."

**Beispiele:**
- ankommen: Der Zug kommt um 10 Uhr an.
- aufstehen: Ich stehe früh auf.
- einladen: Sie lädt uns zum Essen ein.
- mitkommen: Kommst du mit?
- zurückkommen: Wann kommst du zurück?

**Nicht trennbar:** be-, emp-, ent-, er-, ge-, miss-, ver-, zer-
- bekommen, verstehen, erzählen (Betonung auf 2. Silbe!)"""
        },
        {
            "name_de": "Reflexive Verben",
            "name_en": "Reflexive Verbs",
            "category": "verbs",
            "subcategory": "reflexive_verbs",
            "difficulty_level": "B1",
            "order_index": 17,
            "description_de": "Reflexive Verben verwenden ein Reflexivpronomen.",
            "explanation_de": """Reflexive Verben beziehen sich auf das Subjekt zurück.

**Reflexivpronomen:**
- Akkusativ: mich, dich, sich, uns, euch, sich
- Dativ: mir, dir, sich, uns, euch, sich

**Echte reflexive Verben** (nur mit Reflexivpronomen):
- sich bedanken, sich beeilen, sich erholen, sich freuen
- "Ich freue mich auf den Urlaub."

**Unechte reflexive Verben** (können auch ohne):
- sich waschen, sich anziehen, sich kämmen
- "Ich wasche mich." vs. "Ich wasche das Auto."

**Dativ bei reflexiven Verben:**
- Wenn es noch ein Akkusativobjekt gibt
- "Ich putze mir die Zähne." (mir = Dativ, die Zähne = Akkusativ)

**Beispiele:**
- Ich ziehe mich an.
- Sie interessiert sich für Musik.
- Wir treffen uns morgen.
- Beeilt euch!
- Er wäscht sich die Hände."""
        },

        # ========== SENTENCE STRUCTURE (Satzbau) ==========
        {
            "name_de": "Hauptsatz - Verbposition",
            "name_en": "Main Clause - Verb Position",
            "category": "sentence_structure",
            "subcategory": "main_clause",
            "difficulty_level": "A2",
            "order_index": 20,
            "description_de": "Im Hauptsatz steht das konjugierte Verb an zweiter Stelle.",
            "explanation_de": """Die Verbzweitstellung (V2) ist die wichtigste Regel für deutsche Hauptsätze.

**Regel:** Das konjugierte Verb steht IMMER an Position 2!

**Position 1 (Vorfeld):**
- Subjekt: "Ich gehe nach Hause."
- Zeit: "Morgen gehe ich nach Hause."
- Ort: "Zu Hause esse ich."
- Objekt: "Das Buch lese ich morgen."

**Position 2:** Konjugiertes Verb

**Satzende:** Infinitiv, Partizip, trennbares Präfix

**Satzklammer:**
- Modalverb: "Ich muss heute arbeiten."
- Perfekt: "Ich habe gestern gearbeitet."
- Trennbares Verb: "Ich rufe dich morgen an."

**Beispiele:**
- Heute besuche ich meine Eltern.
- Meine Eltern besuche ich heute.
- Ich habe gestern einen Film gesehen.
- Morgen wird es regnen.
- Um 8 Uhr steht er auf."""
        },
        {
            "name_de": "Nebensatz - Verbposition",
            "name_en": "Subordinate Clause - Verb Position",
            "category": "sentence_structure",
            "subcategory": "subordinate_clause",
            "difficulty_level": "B1",
            "order_index": 21,
            "description_de": "Im Nebensatz steht das Verb am Ende.",
            "explanation_de": """Nebensätze werden durch Konjunktionen eingeleitet und haben das Verb am Ende.

**Subjunktionen (Nebensatz-Konjunktionen):**
- dass, weil, obwohl, wenn, als, während, bis, seit(dem), bevor, nachdem, damit, ob

**Verbstellung:**
- Konjugiertes Verb am ENDE
- Bei zusammengesetzten Zeiten: Hilfsverb ganz am Ende

**Komma:**
- Immer Komma vor dem Nebensatz
- "Ich weiß, dass du recht hast."

**Beispiele:**
- Ich glaube, dass er heute kommt.
- Sie bleibt zu Hause, weil sie krank ist.
- Wenn es regnet, bleiben wir drinnen.
- Ich weiß nicht, ob er Zeit hat.
- Er sagt, dass er das Buch gelesen hat.

**Nebensatz vor Hauptsatz:**
- Wenn das Wetter schön ist, gehen wir spazieren.
- (Nebensatz Position 1, dann Verb auf Position 2!)"""
        },
        {
            "name_de": "Fragesätze",
            "name_en": "Question Sentences",
            "category": "sentence_structure",
            "subcategory": "questions",
            "difficulty_level": "A1",
            "order_index": 22,
            "description_de": "Fragesätze können mit oder ohne Fragewort gebildet werden.",
            "explanation_de": """Es gibt zwei Arten von Fragen im Deutschen.

**Ja/Nein-Fragen (ohne Fragewort):**
- Verb an Position 1
- "Kommst du morgen?" - "Ja/Nein"
- "Hast du Zeit?" - "Ja/Nein"

**W-Fragen (mit Fragewort):**
- Fragewort Position 1, Verb Position 2
- wer, was, wann, wo, wohin, woher, wie, warum, welcher

**Fragewörter:**
- Wer? (Person, Nominativ): Wer kommt?
- Wen? (Person, Akkusativ): Wen siehst du?
- Wem? (Person, Dativ): Wem hilfst du?
- Was? (Sache): Was machst du?
- Wann? (Zeit): Wann kommst du?
- Wo? (Ort, keine Bewegung): Wo bist du?
- Wohin? (Richtung): Wohin gehst du?
- Woher? (Herkunft): Woher kommst du?
- Wie? (Art und Weise): Wie geht's?
- Warum/Weshalb/Wieso? (Grund): Warum lernst du Deutsch?

**Beispiele:**
- Sprichst du Deutsch?
- Was machst du heute?
- Wann kommst du nach Hause?
- Wo wohnst du?"""
        },
        {
            "name_de": "Negation",
            "name_en": "Negation",
            "category": "sentence_structure",
            "subcategory": "negation",
            "difficulty_level": "A2",
            "order_index": 23,
            "description_de": "Die Verneinung erfolgt mit 'nicht' oder 'kein'.",
            "explanation_de": """Deutsche Negation verwendet 'nicht' oder 'kein'.

**'kein' (kein Nomen):**
- Negation von unbestimmten Artikeln (ein, eine, ein)
- Negation von Nomen ohne Artikel
- "ein Buch" → "kein Buch"
- "Ich habe Zeit." → "Ich habe keine Zeit."

**'nicht' (alles andere):**
- Negation von Verben, Adjektiven, Adverbien
- Negation von bestimmten Artikeln
- Position: meist am Ende oder vor dem negierten Element

**Position von 'nicht':**
- Am Satzende: "Ich verstehe nicht."
- Vor Adjektiven: "Das ist nicht schön."
- Vor Präpositionen: "Ich bin nicht zu Hause."
- Vor trennbaren Präfixen: "Ich stehe nicht auf."

**Beispiele:**
- Ich habe kein Auto.
- Das ist nicht richtig.
- Sie kommt nicht.
- Wir haben keine Zeit.
- Er wohnt nicht in Berlin.
- Das Buch gehört mir nicht."""
        },

        # ========== PREPOSITIONS (Präpositionen) ==========
        {
            "name_de": "Präpositionen mit Akkusativ",
            "name_en": "Prepositions with Accusative",
            "category": "prepositions",
            "subcategory": "accusative_prepositions",
            "difficulty_level": "A2",
            "order_index": 30,
            "description_de": "Bestimmte Präpositionen verlangen immer den Akkusativ.",
            "explanation_de": """Diese Präpositionen werden immer mit dem Akkusativ verwendet.

**Die Akkusativ-Präpositionen:**
- durch (through): durch den Park
- für (for): für den Freund
- gegen (against): gegen die Wand
- ohne (without): ohne den Schlüssel
- um (around, at): um das Haus, um 8 Uhr
- bis (until): bis nächsten Montag
- entlang (along): den Fluss entlang (nachgestellt!)

**Merkhilfe:** "durch, für, gegen, ohne, um" - oft als Lernspruch

**Beispiele:**
- Ich gehe durch den Park.
- Das Geschenk ist für meinen Vater.
- Wir spielen gegen die andere Mannschaft.
- Sie kommt ohne ihren Mann.
- Der Unterricht beginnt um 9 Uhr.
- Wir fahren den Fluss entlang.
- Ich bleibe bis nächsten Freitag."""
        },
        {
            "name_de": "Präpositionen mit Dativ",
            "name_en": "Prepositions with Dative",
            "category": "prepositions",
            "subcategory": "dative_prepositions",
            "difficulty_level": "A2",
            "order_index": 31,
            "description_de": "Bestimmte Präpositionen verlangen immer den Dativ.",
            "explanation_de": """Diese Präpositionen werden immer mit dem Dativ verwendet.

**Die Dativ-Präpositionen:**
- aus (from, out of): aus dem Haus
- bei (at, near, with): bei meinem Freund
- mit (with): mit dem Auto
- nach (after, to): nach der Arbeit, nach Berlin
- seit (since, for): seit einem Jahr
- von (from, of): von meinem Vater
- zu (to): zum Arzt (zu + dem)
- gegenüber (opposite): gegenüber dem Hotel
- außer (except): außer mir

**Merkhilfe:** "aus, bei, mit, nach, seit, von, zu" - Von-zu-mit-nach-Regel

**Kontraktionen:**
- zu + dem = zum
- zu + der = zur
- bei + dem = beim
- von + dem = vom

**Beispiele:**
- Ich komme aus der Schweiz.
- Er wohnt bei seinen Eltern.
- Wir fahren mit dem Zug.
- Nach dem Essen gehen wir spazieren.
- Ich lerne seit drei Monaten Deutsch.
- Das Buch ist von Goethe.
- Ich gehe zum Arzt."""
        },
        {
            "name_de": "Wechselpräpositionen",
            "name_en": "Two-way Prepositions",
            "category": "prepositions",
            "subcategory": "two_way_prepositions",
            "difficulty_level": "B1",
            "order_index": 32,
            "description_de": "Diese Präpositionen können Akkusativ oder Dativ verlangen.",
            "explanation_de": """Wechselpräpositionen können mit Akkusativ oder Dativ stehen, je nach Bedeutung.

**Die 9 Wechselpräpositionen:**
- an, auf, hinter, in, neben, über, unter, vor, zwischen

**Regel:**
- Akkusativ: Wohin? (Bewegung, Richtung)
- Dativ: Wo? (Position, keine Bewegung)

**Beispiele Akkusativ (Wohin?):**
- Ich gehe in den Park. (Bewegung)
- Er legt das Buch auf den Tisch. (Richtung)
- Sie stellt die Vase auf das Regal.

**Beispiele Dativ (Wo?):**
- Ich bin in dem Park. / im Park (Position)
- Das Buch liegt auf dem Tisch. (keine Bewegung)
- Die Vase steht auf dem Regal.

**Verbenpaare:**
- legen (Akk.) / liegen (Dat.)
- stellen (Akk.) / stehen (Dat.)
- setzen (Akk.) / sitzen (Dat.)
- hängen (Akk.) / hängen (Dat.)

**Kontraktionen:**
- in + dem = im
- in + das = ins
- an + dem = am
- an + das = ans

**Weitere Beispiele:**
- Ich hänge das Bild an die Wand. (Wohin?)
- Das Bild hängt an der Wand. (Wo?)"""
        },
        {
            "name_de": "Präpositionen mit Genitiv",
            "name_en": "Prepositions with Genitive",
            "category": "prepositions",
            "subcategory": "genitive_prepositions",
            "difficulty_level": "B2",
            "order_index": 33,
            "description_de": "Diese Präpositionen werden mit dem Genitiv verwendet.",
            "explanation_de": """Genitiv-Präpositionen sind typisch für formelle, schriftliche Sprache.

**Häufige Genitiv-Präpositionen:**
- während (during): während des Sommers
- wegen (because of): wegen des Regens
- trotz (despite): trotz der Kälte
- statt/anstatt (instead of): statt des Autos
- außerhalb (outside): außerhalb der Stadt
- innerhalb (within): innerhalb einer Woche
- aufgrund (due to): aufgrund der Situation

**Verwendung:**
- Meist in formeller, schriftlicher Sprache
- Einige werden umgangssprachlich auch mit Dativ verwendet

**Beispiele:**
- Während der Ferien reisen wir.
- Wegen des schlechten Wetters bleiben wir zu Hause.
- Trotz der Probleme haben wir Erfolg.
- Statt eines Autos kauft er ein Fahrrad.
- Außerhalb der Geschäftszeiten ist niemand da.
- Innerhalb eines Monats müssen Sie zahlen.
- Aufgrund der Umstände können wir nicht kommen."""
        },

        # ========== ARTICLES & PRONOUNS (Artikel & Pronomen) ==========
        {
            "name_de": "Bestimmter und unbestimmter Artikel",
            "name_en": "Definite and Indefinite Articles",
            "category": "articles_pronouns",
            "subcategory": "articles",
            "difficulty_level": "A1",
            "order_index": 40,
            "description_de": "Artikel bestimmen das Nomen und seinen Kasus.",
            "explanation_de": """Deutsche Artikel zeigen Genus, Numerus und Kasus.

**Bestimmter Artikel (der, die, das):**
- Verwendung: bekannte oder definierte Dinge
- Maskulin: der Mann
- Feminin: die Frau
- Neutrum: das Kind
- Plural: die Kinder

**Unbestimmter Artikel (ein, eine, ein):**
- Verwendung: neue oder unbestimmte Dinge
- Maskulin: ein Mann
- Feminin: eine Frau
- Neutrum: ein Kind
- Plural: kein Artikel oder "einige Kinder"

**Nullartikel:**
- Berufe: Ich bin Lehrer.
- Länder: Deutschland ist schön. (Ausnahmen: die Schweiz, die Türkei)
- Abstrakte Begriffe: Liebe ist wichtig.
- Stoffe: Ich trinke Kaffee.

**Deklination Nominativ:**
- der/ein Mann, die/eine Frau, das/ein Kind, die Kinder

**Beispiele:**
- Der Lehrer erklärt die Grammatik.
- Ein Mann kommt.
- Das ist eine gute Idee.
- Die Kinder spielen."""
        },
        {
            "name_de": "Possessivartikel",
            "name_en": "Possessive Articles",
            "category": "articles_pronouns",
            "subcategory": "possessive_articles",
            "difficulty_level": "A2",
            "order_index": 41,
            "description_de": "Possessivartikel zeigen Besitz oder Zugehörigkeit.",
            "explanation_de": """Possessivartikel werden wie der unbestimmte Artikel dekliniert.

**Die Possessivartikel:**
- ich: mein (my)
- du: dein (your, informal)
- er: sein (his)
- sie: ihr (her)
- es: sein (its)
- wir: unser (our)
- ihr: euer (your, plural informal)
- sie/Sie: ihr/Ihr (their/your formal)

**Deklination wie 'ein':**
- Nominativ: mein Vater, meine Mutter, mein Kind
- Akkusativ: meinen Vater, meine Mutter, mein Kind
- Dativ: meinem Vater, meiner Mutter, meinem Kind
- Genitiv: meines Vaters, meiner Mutter, meines Kindes

**Beispiele:**
- Das ist mein Buch.
- Ich sehe deinen Bruder.
- Sie besucht ihre Eltern.
- Wir lieben unser Land.
- Wo ist euer Auto?
- Sein Hund ist groß.

**Besonderheit 'euer':**
- euer Vater, aber: eure Mutter (e fällt weg!)"""
        },
        {
            "name_de": "Personalpronomen",
            "name_en": "Personal Pronouns",
            "category": "articles_pronouns",
            "subcategory": "personal_pronouns",
            "difficulty_level": "A1",
            "order_index": 42,
            "description_de": "Personalpronomen ersetzen Nomen.",
            "explanation_de": """Personalpronomen stehen anstelle von Personen oder Dingen.

**Nominativ (Subjekt):**
- ich, du, er, sie, es, wir, ihr, sie, Sie

**Akkusativ (direktes Objekt):**
- mich, dich, ihn, sie, es, uns, euch, sie, Sie

**Dativ (indirektes Objekt):**
- mir, dir, ihm, ihr, ihm, uns, euch, ihnen, Ihnen

**Beispiele:**
- Nominativ: Ich gehe nach Hause.
- Akkusativ: Er sieht mich. / Ich sehe ihn.
- Dativ: Sie hilft mir. / Ich helfe ihr.

**Kombinationen:**
- "Gibst du es mir?" (es = Akk., mir = Dat.)
- "Ich gebe es ihm." (es = Akk., ihm = Dat.)

**Reihenfolge:**
- Wenn beide Pronomen: Akk. vor Dat.
  "Ich gebe es ihm." (nicht: "ihm es")
- Wenn Pronomen + Nomen: Pronomen zuerst
  "Ich gebe ihm das Buch."

**Sie vs. sie:**
- Sie (formal): Schreiben Sie mir?
- sie (she): Kennen Sie sie?
- sie (they): Ich sehe sie."""
        },
        {
            "name_de": "Relativpronomen und Relativsätze",
            "name_en": "Relative Pronouns and Clauses",
            "category": "articles_pronouns",
            "subcategory": "relative_pronouns",
            "difficulty_level": "B1",
            "order_index": 43,
            "description_de": "Relativpronomen leiten Relativsätze ein.",
            "explanation_de": """Relativsätze beschreiben ein Nomen genauer.

**Relativpronomen:**
- Gleich wie bestimmter Artikel, außer:
- Genitiv: dessen (m/n), deren (f/pl)
- Dativ Plural: denen

**Deklination:**
- Nominativ: der, die, das, die
- Akkusativ: den, die, das, die
- Dativ: dem, der, dem, denen
- Genitiv: dessen, deren, dessen, deren

**Kasus des Relativpronomens:**
- Hängt von seiner Funktion IM Relativsatz ab
- "Der Mann, der kommt..." (Nominativ - Subjekt)
- "Der Mann, den ich sehe..." (Akkusativ - Objekt)
- "Der Mann, dem ich helfe..." (Dativ)

**Verbstellung:**
- Verb am Ende des Relativsatzes!
- Komma vor dem Relativsatz

**Beispiele:**
- Das ist der Mann, der hier wohnt. (Nominativ)
- Die Frau, die ich kenne, ist nett. (Akkusativ)
- Das Kind, dem ich helfe, ist klein. (Dativ)
- Der Autor, dessen Buch ich lese, ist berühmt. (Genitiv)
- Die Leute, mit denen ich arbeite, sind freundlich. (Dativ nach 'mit')"""
        },

        # ========== ADJECTIVES (Adjektive) ==========
        {
            "name_de": "Adjektivdeklination mit bestimmtem Artikel",
            "name_en": "Adjective Declension with Definite Article",
            "category": "adjectives",
            "subcategory": "adjective_declension_definite",
            "difficulty_level": "B1",
            "order_index": 50,
            "description_de": "Adjektive vor Nomen werden dekliniert.",
            "explanation_de": """Adjektive vor Nomen mit bestimmtem Artikel haben spezielle Endungen.

**Regel:** Meist -e oder -en

**Nominativ:**
- der gute Mann
- die gute Frau
- das gute Kind
- die guten Leute

**Akkusativ:**
- den guten Mann (nur maskulin -en!)
- die gute Frau
- das gute Kind
- die guten Leute

**Dativ:**
- dem guten Mann
- der guten Frau
- dem guten Kind
- den guten Leuten (Plural + n am Nomen!)

**Genitiv:**
- des guten Mannes
- der guten Frau
- des guten Kindes
- der guten Leute

**Merkhilfe:**
- Nominativ/Akkusativ (außer mask. Akk.): -e
- Alle anderen: -en

**Beispiele:**
- Ich sehe den kleinen Hund.
- Die neue Lehrerin ist nett.
- Das schöne Haus gefällt mir.
- Mit dem guten Auto fahren wir."""
        },
        {
            "name_de": "Adjektivdeklination mit unbestimmtem Artikel",
            "name_en": "Adjective Declension with Indefinite Article",
            "category": "adjectives",
            "subcategory": "adjective_declension_indefinite",
            "difficulty_level": "B1",
            "order_index": 51,
            "description_de": "Adjektive nach unbestimmtem Artikel haben andere Endungen.",
            "explanation_de": """Nach unbestimmtem Artikel zeigt das Adjektiv oft den Kasus.

**Nominativ:**
- ein guter Mann (-er)
- eine gute Frau (-e)
- ein gutes Kind (-es)

**Akkusativ:**
- einen guten Mann (-en)
- eine gute Frau (-e)
- ein gutes Kind (-es)

**Dativ:**
- einem guten Mann (-en)
- einer guten Frau (-en)
- einem guten Kind (-en)

**Genitiv:**
- eines guten Mannes (-en)
- einer guten Frau (-en)
- eines guten Kindes (-en)

**Regel:**
- Nominativ m: -er, f: -e, n: -es
- Akkusativ: nur m ändert sich zu -en
- Dativ/Genitiv: immer -en

**Beispiele:**
- Ich habe einen neuen Computer.
- Das ist eine gute Idee.
- Sie kauft ein schönes Kleid.
- Mit einem alten Freund spreche ich."""
        },
        {
            "name_de": "Adjektivdeklination ohne Artikel",
            "name_en": "Adjective Declension without Article",
            "category": "adjectives",
            "subcategory": "adjective_declension_null",
            "difficulty_level": "B2",
            "order_index": 52,
            "description_de": "Ohne Artikel übernimmt das Adjektiv die Artikelendung.",
            "explanation_de": """Ohne Artikel zeigt das Adjektiv den Kasus stark an.

**Regel:** Adjektiv bekommt die Endung des bestimmten Artikels

**Nominativ:**
- guter Wein (wie 'der')
- gute Milch (wie 'die')
- gutes Bier (wie 'das')
- gute Äpfel (wie 'die')

**Akkusativ:**
- guten Wein (wie 'den')
- gute Milch (wie 'die')
- gutes Bier (wie 'das')
- gute Äpfel (wie 'die')

**Dativ:**
- mit gutem Wein (wie 'dem')
- mit guter Milch (wie 'der')
- mit gutem Bier (wie 'dem')
- mit guten Äpfeln (wie 'den')

**Genitiv:**
- trotz guten Weines (wie 'des')
- trotz guter Milch (wie 'der')
- trotz guten Bieres (wie 'des')
- trotz guter Äpfel (wie 'der')

**Beispiele:**
- Ich trinke guten Wein.
- Frische Milch ist gesund.
- Mit kaltem Wasser waschen.
- Trotz schlechten Wetters gehen wir."""
        },
        {
            "name_de": "Komparativ und Superlativ",
            "name_en": "Comparative and Superlative",
            "category": "adjectives",
            "subcategory": "comparison",
            "difficulty_level": "A2",
            "order_index": 53,
            "description_de": "Steigerung von Adjektiven für Vergleiche.",
            "explanation_de": """Adjektive können gesteigert werden.

**Bildung:**
- Grundform (Positiv): schnell
- Komparativ: schneller (+ als)
- Superlativ: am schnellsten / der schnellste

**Regelmäßige Bildung:**
- Komparativ: Adjektiv + -er
- Superlativ: am + Adjektiv + -sten / der/die/das + Adjektiv + -ste

**Mit Umlaut (a→ä, o→ö, u→ü):**
- alt → älter → am ältesten
- groß → größer → am größten
- jung → jünger → am jüngsten
- lang → länger → am längsten

**Unregelmäßig:**
- gut → besser → am besten
- viel → mehr → am meisten
- gern → lieber → am liebsten
- hoch → höher → am höchsten

**Verwendung:**
- Komparativ: "Er ist schneller als ich."
- Superlativ attributiv: "Das ist der schnellste Mann."
- Superlativ prädikativ: "Er ist am schnellsten."

**Beispiele:**
- Mein Auto ist schneller als dein Auto.
- Das ist das schönste Haus der Stadt.
- Sie spricht am besten Deutsch.
- Dieser Film ist interessanter."""
        },

        # ========== ADDITIONAL IMPORTANT TOPICS ==========
        {
            "name_de": "Passiv (Vorgangspassiv)",
            "name_en": "Passive Voice",
            "category": "advanced",
            "subcategory": "passive_voice",
            "difficulty_level": "B2",
            "order_index": 60,
            "description_de": "Das Passiv betont den Vorgang oder das Ergebnis, nicht den Täter.",
            "explanation_de": """Im Passiv ist die Handlung wichtiger als der Handelnde.

**Bildung:**
- werden + Partizip II

**Präsens Passiv:**
- Das Auto wird repariert.
- Die Tür wird geöffnet.

**Präteritum Passiv:**
- Das Auto wurde repariert.
- Die Tür wurde geöffnet.

**Perfekt Passiv:**
- Das Auto ist repariert worden.
- Die Tür ist geöffnet worden.

**Mit Täter (von + Dativ):**
- Das Buch wird von dem Autor geschrieben.
- Die Straße wurde vom Arbeiter gebaut.

**Ohne Täter:**
- Hier wird Deutsch gesprochen.
- Das Problem wird gelöst.

**Aktiv → Passiv Transformation:**
- Aktiv: Der Mechaniker repariert das Auto.
- Passiv: Das Auto wird (vom Mechaniker) repariert.

**Verwendung:**
- Wenn der Täter unbekannt oder unwichtig ist
- In offiziellen, formellen Texten
- In wissenschaftlichen Beschreibungen

**Beispiele:**
- Die Rechnung wird bezahlt.
- Der Brief wurde gestern geschrieben.
- Das Haus ist verkauft worden.
- Hier darf nicht geraucht werden."""
        },
        {
            "name_de": "Indirekte Rede (Konjunktiv I)",
            "name_en": "Indirect Speech",
            "category": "advanced",
            "subcategory": "indirect_speech",
            "difficulty_level": "C1",
            "order_index": 61,
            "description_de": "Der Konjunktiv I wird hauptsächlich für indirekte Rede verwendet.",
            "explanation_de": """Der Konjunktiv I wird verwendet, um Aussagen anderer wiederzugeben.

**Bildung:**
- Infinitivstamm + Konjunktiv-Endung

**Konjunktiv I Präsens (sein):**
- ich sei, du sei(e)st, er/sie/es sei
- wir seien, ihr seiet, sie seien

**Konjunktiv I (haben):**
- ich habe, du habest, er/sie/es habe
- wir haben, ihr habet, sie haben

**Konjunktiv I (andere Verben):**
- ich komme, du kommest, er komme
- ich könne, du könnest, er könne

**Verwendung:**
- Hauptsächlich in Nachrichten und Berichten
- Zeigt Distanz zur Aussage
- Meist nur 3. Person Singular deutlich erkennbar

**Wenn Konjunktiv I = Indikativ:**
- Dann Konjunktiv II verwenden
- "Sie sagen, sie haben Zeit." → "Sie sagten, sie hätten Zeit."

**Beispiele:**
- Direkt: "Ich bin müde."
- Indirekt: Er sagt, er sei müde.

- Direkt: "Ich habe das Buch gelesen."
- Indirekt: Sie sagt, sie habe das Buch gelesen.

- Direkt: "Wir kommen morgen."
- Indirekt: Sie sagen, sie kämen morgen. (Konj. II, da Konj. I = Indikativ)"""
        },
        {
            "name_de": "Partizip I und II als Adjektiv",
            "name_en": "Participles as Adjectives",
            "category": "advanced",
            "subcategory": "participles",
            "difficulty_level": "B2",
            "order_index": 62,
            "description_de": "Partizipien können als Adjektive verwendet werden.",
            "explanation_de": """Partizip I und II können Nomen wie Adjektive beschreiben.

**Partizip I (Präsens Partizip):**
- Bildung: Infinitiv + -d
- Bedeutung: aktiv, gleichzeitig
- lachend, spielend, arbeitend

**Partizip I als Adjektiv:**
- das lachende Kind (= das Kind, das lacht)
- der arbeitende Mann (= der Mann, der arbeitet)
- mit kochendem Wasser (= Wasser, das kocht)

**Partizip II (Perfekt Partizip):**
- Bildung: ge-...-t/-en
- Bedeutung: passiv, vergangen (bei transitiven Verben)
- gekauft, geschrieben, geöffnet

**Partizip II als Adjektiv:**
- das gekaufte Buch (= das Buch, das gekauft wurde)
- die geöffnete Tür (= die Tür, die geöffnet wurde)
- der geschriebene Brief (= der Brief, der geschrieben wurde)

**Deklination:**
- Beide werden wie normale Adjektive dekliniert
- der lachende Mann, ein lachender Mann
- die geöffnete Tür, eine geöffnete Tür

**Erweiterte Partizipialattribute:**
- das vor dem Haus parkende Auto
- die vom Autor geschriebene Geschichte

**Beispiele:**
- Das weinende Baby braucht Hilfe.
- Die geschlossenen Geschäfte öffnen morgen.
- Mit singendem Herzen gehe ich zur Arbeit.
- Das ist eine gut bezahlte Arbeit."""
        },
        {
            "name_de": "Infinitiv mit 'zu'",
            "name_en": "Infinitive with 'zu'",
            "category": "advanced",
            "subcategory": "infinitive_zu",
            "difficulty_level": "B1",
            "order_index": 63,
            "description_de": "In bestimmten Konstruktionen wird 'zu' vor dem Infinitiv verwendet.",
            "explanation_de": """Der Infinitiv mit 'zu' wird in vielen Konstruktionen benötigt.

**Wann 'zu' + Infinitiv:**
- Nach bestimmten Verben: anfangen, aufhören, beginnen, vergessen, versuchen, vorhaben
- Nach Adjektiven: Es ist wichtig/schön/schwer... zu...
- Nach Nomen: Ich habe keine Zeit/Lust... zu...
- Um... zu (Zweck): Ich lerne Deutsch, um zu arbeiten.

**Ohne 'zu':**
- Nach Modalverben: Ich kann schwimmen.
- Nach Verben der Wahrnehmung: Ich höre ihn kommen.
- Nach bleiben, gehen, lassen: Ich bleibe sitzen.

**Position von 'zu':**
- Vor dem Infinitiv: zu lernen, zu arbeiten
- Bei trennbaren Verben: zwischen Präfix und Verb
  anzufangen, einzukaufen, mitzukommen

**Infinitivsätze:**
- Komma bei Infinitivsätzen mit zu
- "Es ist wichtig, Deutsch zu lernen."
- "Ich hoffe, dich bald zu sehen."

**um... zu (Zweck/Ziel):**
- Ich lerne Deutsch, um in Deutschland zu arbeiten.
- Sie spart Geld, um ein Auto zu kaufen.

**Beispiele:**
- Ich beginne zu arbeiten.
- Es ist schwer, Deutsch zu lernen.
- Vergiss nicht, mich anzurufen!
- Ich habe keine Lust, aufzustehen.
- Sie versucht, pünktlich zu sein."""
        },
        {
            "name_de": "Konjunktionen (koordinierend)",
            "name_en": "Conjunctions (Coordinating)",
            "category": "sentence_structure",
            "subcategory": "coordinating_conjunctions",
            "difficulty_level": "A2",
            "order_index": 70,
            "description_de": "Koordinierende Konjunktionen verbinden Hauptsätze.",
            "explanation_de": """Koordinierende Konjunktionen verbinden gleichwertige Sätze.

**Die wichtigsten koordinierenden Konjunktionen:**
- und (and): Ich gehe und er bleibt.
- oder (or): Kommst du oder bleibst du?
- aber (but): Ich will, aber ich kann nicht.
- denn (because): Ich bleibe, denn es regnet.
- sondern (but rather): Nicht er, sondern sie.

**Besonderheit:**
- Position 0 (vor Position 1)
- Keine Änderung der Wortstellung!
- Verb bleibt auf Position 2

**und/oder:**
- Verbinden ähnliche Elemente
- "Ich esse Brot und Käse."
- "Möchtest du Tee oder Kaffee?"

**aber:**
- Gegensatz, Einschränkung
- "Ich bin müde, aber ich arbeite weiter."

**denn:**
- Begründung
- "Ich bleibe zu Hause, denn ich bin krank."
- Nicht verwechseln mit 'weil' (Nebensatz!)

**sondern:**
- Nur nach Negation!
- Korrektur einer negativen Aussage
- "Ich komme nicht heute, sondern morgen."
- "Das ist nicht billig, sondern teuer."

**Beispiele:**
- Ich lerne Deutsch und sie lernt Englisch.
- Wir können ins Kino oder ins Restaurant gehen.
- Er ist intelligent, aber faul.
- Sie kommt nicht, denn sie hat keine Zeit.
- Das ist nicht mein Auto, sondern sein Auto."""
        },
        {
            "name_de": "Konjunktionen (subordinierend)",
            "name_en": "Conjunctions (Subordinating)",
            "category": "sentence_structure",
            "subcategory": "subordinating_conjunctions",
            "difficulty_level": "B1",
            "order_index": 71,
            "description_de": "Subordinierende Konjunktionen leiten Nebensätze ein.",
            "explanation_de": """Subordinierende Konjunktionen verbinden Haupt- und Nebensatz.

**Wichtige Subjunktionen:**
- dass (that): Ich weiß, dass du recht hast.
- weil (because): Ich lerne, weil es wichtig ist.
- wenn (if, when): Wenn es regnet, bleibe ich zu Hause.
- als (when, past): Als ich Kind war, ...
- ob (whether): Ich frage, ob du Zeit hast.
- obwohl (although): Obwohl es regnet, gehen wir.
- damit (so that): Ich lerne, damit ich erfolgreich bin.
- bevor (before): Bevor du gehst, ruf mich an.
- nachdem (after): Nachdem ich gegessen habe, ...
- während (while): Während er arbeitet, ...
- bis (until): Warte, bis ich komme.
- seit/seitdem (since): Seit ich hier bin, ...

**Wortstellung:**
- Verb am Ende des Nebensatzes!
- Komma zwischen Haupt- und Nebensatz

**wenn vs. als:**
- wenn: Gegenwart, Zukunft, wiederholte Vergangenheit
- als: einmalige Handlung in Vergangenheit
- "Wenn ich Zeit habe, komme ich." (Gegenwart)
- "Als ich Kind war, ..." (Vergangenheit, einmalig)

**weil vs. da:**
- Beide bedeuten "because"
- da: oft am Satzanfang, bekannte Information
- weil: meist nach Hauptsatz, neue Information

**Beispiele:**
- Ich denke, dass es morgen regnet.
- Sie kommt nicht, weil sie krank ist.
- Wenn du möchtest, können wir gehen.
- Als er kam, war ich schon weg.
- Ich weiß nicht, ob das richtig ist.
- Obwohl er müde ist, arbeitet er weiter."""
        },
        {
            "name_de": "Temporale Nebensätze",
            "name_en": "Temporal Clauses",
            "category": "sentence_structure",
            "subcategory": "temporal_clauses",
            "difficulty_level": "B2",
            "order_index": 72,
            "description_de": "Temporale Nebensätze geben Zeitverhältnisse an.",
            "explanation_de": """Temporale Nebensätze beschreiben zeitliche Zusammenhänge.

**Gleichzeitigkeit:**
- während (while, during): Während ich koche, hört sie Musik.
- wenn (when, whenever): Wenn ich nach Hause komme, ...
- als (when, past once): Als ich jung war, ...
- solange (as long as): Solange du hier bist, ...

**Vorzeitigkeit (davor):**
- bevor/ehe (before): Bevor du gehst, ruf mich an.
- bis (until): Warte, bis ich fertig bin.

**Nachzeitigkeit (danach):**
- nachdem (after): Nachdem er gegessen hat, geht er.
- sobald (as soon as): Sobald ich kann, komme ich.
- seitdem/seit (since): Seit(dem) er hier ist, ...

**Zeitdauer:**
- solange (as long as): Solange es hell ist, arbeiten wir.
- bis (until): Bis es dunkel wird, bleiben wir.

**nachdem + Zeitenfolge:**
- Nebensatz eine Zeitstufe früher!
- Hauptsatz Präsens → Nebensatz Perfekt
  "Nachdem ich gegessen habe, gehe ich."
- Hauptsatz Präteritum → Nebensatz Plusquamperfekt
  "Nachdem ich gegessen hatte, ging ich."

**Beispiele:**
- Während er schläft, arbeite ich.
- Bevor ich gehe, muss ich noch telefonieren.
- Nachdem wir angekommen waren, haben wir gegessen.
- Sobald die Sonne scheint, gehen wir raus.
- Seit(dem) ich hier wohne, bin ich glücklich.
- Als es dunkel wurde, gingen wir nach Hause."""
        }
    ]

    return topics


def create_grammar_exercises():
    """Create 200+ manual grammar exercises across all topics and types."""

    exercises = [
        # ========== NOMINATIVE CASE EXERCISES ==========
        {
            "topic_name": "Nominativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A1",
            "question_text": "____ Lehrer erklärt die Grammatik.",
            "correct_answer": "Der",
            "alternative_answers": [],
            "explanation_de": "Der Lehrer ist das Subjekt des Satzes und steht im Nominativ. Maskuline Nomen haben im Nominativ den Artikel 'der'.",
            "hints": ["Maskulin, Nominativ", "Wer oder was erklärt?"],
            "context_category": "general"
        },
        {
            "topic_name": "Nominativ",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A1",
            "question_text": "Welcher Satz ist korrekt?",
            "correct_answer": "Die Katze schläft.",
            "alternative_answers": ["Den Katze schläft.", "Der Katze schläft.", "Das Katze schläft."],
            "explanation_de": "'Die Katze' ist Subjekt (Nominativ) und feminin. Der korrekte Artikel ist 'die'.",
            "hints": ["Subjekt = Nominativ", "Katze = feminin"],
            "context_category": "general"
        },
        {
            "topic_name": "Nominativ",
            "exercise_type": "error_correction",
            "difficulty_level": "A1",
            "question_text": "Den Kind spielt im Garten.",
            "correct_answer": "Das Kind spielt im Garten.",
            "alternative_answers": [],
            "explanation_de": "'Kind' ist Subjekt und neutrum. Im Nominativ brauchen wir 'das', nicht 'den' (Akkusativ).",
            "hints": ["Kind = neutrum", "Subjekt = Nominativ"],
            "context_category": "daily"
        },
        {
            "topic_name": "Nominativ",
            "exercise_type": "translation",
            "difficulty_level": "A1",
            "question_text": "L'uomo lavora. (it → de)",
            "correct_answer": "Der Mann arbeitet.",
            "alternative_answers": [],
            "explanation_de": "'L'uomo' (der Mann) ist Subjekt und maskulin. Im Nominativ: 'der Mann'.",
            "hints": ["uomo = Mann (maskulin)", "Subjekt = Nominativ"],
            "context_category": "business"
        },

        # ========== ACCUSATIVE CASE EXERCISES ==========
        {
            "topic_name": "Akkusativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich sehe ____ Mann.",
            "correct_answer": "den",
            "alternative_answers": [],
            "explanation_de": "'Den Mann' ist direktes Objekt (Akkusativ). Maskulin im Akkusativ = 'den'.",
            "hints": ["Wen oder was siehst du?", "Maskulin + Akkusativ = den"],
            "context_category": "general"
        },
        {
            "topic_name": "Akkusativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Sie kauft ____ Buch.",
            "correct_answer": "ein",
            "alternative_answers": ["das"],
            "explanation_de": "'Ein Buch' ist direktes Objekt. Neutrum ändert sich im Akkusativ nicht (ein → ein).",
            "hints": ["Was kauft sie?", "Neutrum bleibt gleich"],
            "context_category": "daily"
        },
        {
            "topic_name": "Akkusativ",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A2",
            "question_text": "Ich brauche ____.",
            "correct_answer": "einen Stift",
            "alternative_answers": ["ein Stift", "einer Stift", "einem Stift"],
            "explanation_de": "'Stift' ist maskulin. Im Akkusativ: ein → einen.",
            "hints": ["Stift = maskulin", "Akkusativ: ein → einen"],
            "context_category": "general"
        },
        {
            "topic_name": "Akkusativ",
            "exercise_type": "sentence_building",
            "difficulty_level": "A2",
            "question_text": "Ordne: [kaufe, ich, einen, Apfel]",
            "correct_answer": "Ich kaufe einen Apfel.",
            "alternative_answers": [],
            "explanation_de": "Satzstellung: Subjekt (ich) - Verb (kaufe) - Objekt (einen Apfel). 'Apfel' ist maskulin, Akkusativ = 'einen'.",
            "hints": ["Verb an Position 2", "Apfel = maskulin"],
            "context_category": "daily"
        },
        {
            "topic_name": "Akkusativ",
            "exercise_type": "translation",
            "difficulty_level": "A2",
            "question_text": "Vedo la donna. (it → de)",
            "correct_answer": "Ich sehe die Frau.",
            "alternative_answers": [],
            "explanation_de": "'Die Frau' ist feminin und ändert sich im Akkusativ nicht (die → die).",
            "hints": ["donna = Frau (feminin)", "Feminin bleibt 'die'"],
            "context_category": "general"
        },
        {
            "topic_name": "Akkusativ",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Wir besuchen der Museum.",
            "correct_answer": "Wir besuchen das Museum.",
            "alternative_answers": [],
            "explanation_de": "'Museum' ist neutrum. Im Akkusativ bleibt es 'das Museum', nicht 'der'.",
            "hints": ["Museum = neutrum", "Wen oder was besuchen wir?"],
            "context_category": "daily"
        },

        # ========== DATIVE CASE EXERCISES ==========
        {
            "topic_name": "Dativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich helfe ____ Frau.",
            "correct_answer": "der",
            "alternative_answers": [],
            "explanation_de": "'Helfen' verlangt den Dativ. Feminin im Dativ = 'der Frau'.",
            "hints": ["helfen + Dativ", "Wem hilfst du?"],
            "context_category": "general"
        },
        {
            "topic_name": "Dativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Das Buch gehört ____ Kind.",
            "correct_answer": "dem",
            "alternative_answers": [],
            "explanation_de": "'Gehören' verlangt den Dativ. Neutrum im Dativ = 'dem Kind'.",
            "hints": ["gehören + Dativ", "Kind = neutrum"],
            "context_category": "general"
        },
        {
            "topic_name": "Dativ",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A2",
            "question_text": "Ich danke ____.",
            "correct_answer": "meinem Lehrer",
            "alternative_answers": ["meinen Lehrer", "mein Lehrer", "meine Lehrer"],
            "explanation_de": "'Danken' verlangt den Dativ. Maskulin: 'meinem Lehrer'.",
            "hints": ["danken + Dativ", "Maskulin im Dativ = -em"],
            "context_category": "general"
        },
        {
            "topic_name": "Dativ",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Sie gibt das Kind ein Spielzeug.",
            "correct_answer": "Sie gibt dem Kind ein Spielzeug.",
            "alternative_answers": [],
            "explanation_de": "'Geben' hat zwei Objekte: Dativ (wem?) + Akkusativ (was?). 'Kind' = Dativ = 'dem Kind'.",
            "hints": ["Wem gibt sie etwas?", "Kind = neutrum + Dativ"],
            "context_category": "daily"
        },
        {
            "topic_name": "Dativ",
            "exercise_type": "translation",
            "difficulty_level": "A2",
            "question_text": "Aiuto i bambini. (it → de)",
            "correct_answer": "Ich helfe den Kindern.",
            "alternative_answers": [],
            "explanation_de": "'Helfen' + Dativ. Plural im Dativ = 'den Kindern' (mit -n am Ende!).",
            "hints": ["helfen + Dativ", "Plural Dativ + -n"],
            "context_category": "general"
        },

        # ========== GENITIVE CASE EXERCISES ==========
        {
            "topic_name": "Genitiv",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Das Auto ____ Mannes ist neu.",
            "correct_answer": "des",
            "alternative_answers": [],
            "explanation_de": "Genitiv zeigt Besitz. Maskulin im Genitiv = 'des Mannes' (+ -es am Nomen).",
            "hints": ["Wessen Auto?", "Maskulin Genitiv = des + -es"],
            "context_category": "general"
        },
        {
            "topic_name": "Genitiv",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B1",
            "question_text": "Während ____ bleiben wir zu Hause.",
            "correct_answer": "des Regens",
            "alternative_answers": ["dem Regen", "den Regen", "der Regen"],
            "explanation_de": "'Während' verlangt den Genitiv. 'Regen' ist maskulin = 'des Regens'.",
            "hints": ["während + Genitiv", "Regen = maskulin"],
            "context_category": "general"
        },
        {
            "topic_name": "Genitiv",
            "exercise_type": "error_correction",
            "difficulty_level": "B1",
            "question_text": "Die Farbe dem Auto ist schön.",
            "correct_answer": "Die Farbe des Autos ist schön.",
            "alternative_answers": [],
            "explanation_de": "Besitz wird mit Genitiv ausgedrückt. 'Auto' ist neutrum = 'des Autos'.",
            "hints": ["Wessen Farbe?", "Auto = neutrum + Genitiv"],
            "context_category": "daily"
        },
        {
            "topic_name": "Genitiv",
            "exercise_type": "translation",
            "difficulty_level": "B1",
            "question_text": "La casa di mio padre. (it → de)",
            "correct_answer": "Das Haus meines Vaters",
            "alternative_answers": [],
            "explanation_de": "Besitz mit Genitiv. 'Vater' ist maskulin = 'meines Vaters'.",
            "hints": ["di = Genitiv in Deutsch", "Vater = maskulin"],
            "context_category": "general"
        },

        # ========== PRESENT TENSE EXERCISES ==========
        {
            "topic_name": "Präsens (Gegenwart)",
            "exercise_type": "fill_blank",
            "difficulty_level": "A1",
            "question_text": "Ich ____ in Berlin. (wohnen)",
            "correct_answer": "wohne",
            "alternative_answers": [],
            "explanation_de": "Präsens 'ich': Stamm + -e. wohnen → ich wohne.",
            "hints": ["ich → -e", "Wortstamm: wohn-"],
            "context_category": "daily"
        },
        {
            "topic_name": "Präsens (Gegenwart)",
            "exercise_type": "fill_blank",
            "difficulty_level": "A1",
            "question_text": "Du ____ gut Deutsch. (sprechen)",
            "correct_answer": "sprichst",
            "alternative_answers": [],
            "explanation_de": "'Sprechen' hat Vokalwechsel e→i. Du sprichst (nicht: sprechst).",
            "hints": ["du → -st", "e → i Vokalwechsel"],
            "context_category": "general"
        },
        {
            "topic_name": "Präsens (Gegenwart)",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A1",
            "question_text": "Er ____ nach München.",
            "correct_answer": "fährt",
            "alternative_answers": ["fahrt", "fahren", "fähren"],
            "explanation_de": "'Fahren' hat Vokalwechsel a→ä. Er fährt.",
            "hints": ["er → -t", "a → ä Vokalwechsel"],
            "context_category": "daily"
        },
        {
            "topic_name": "Präsens (Gegenwart)",
            "exercise_type": "error_correction",
            "difficulty_level": "A1",
            "question_text": "Sie arbeitest heute.",
            "correct_answer": "Sie arbeitet heute.",
            "alternative_answers": [],
            "explanation_de": "'Sie' (3. Person Singular) braucht die Endung -t, nicht -st.",
            "hints": ["sie/er/es → -t", "du → -st"],
            "context_category": "business"
        },
        {
            "topic_name": "Präsens (Gegenwart)",
            "exercise_type": "translation",
            "difficulty_level": "A1",
            "question_text": "Noi impariamo il tedesco. (it → de)",
            "correct_answer": "Wir lernen Deutsch.",
            "alternative_answers": [],
            "explanation_de": "'Wir' nimmt die Endung -en. lernen → wir lernen.",
            "hints": ["wir → -en", "imparare = lernen"],
            "context_category": "general"
        },

        # ========== PERFECT TENSE EXERCISES ==========
        {
            "topic_name": "Perfekt (Vollendete Gegenwart)",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich ____ einen Brief ____. (schreiben)",
            "correct_answer": "habe geschrieben",
            "alternative_answers": [],
            "explanation_de": "Perfekt mit 'haben'. Partizip II von 'schreiben' ist 'geschrieben' (unregelmäßig).",
            "hints": ["haben + Partizip II", "ge-...-en"],
            "context_category": "general"
        },
        {
            "topic_name": "Perfekt (Vollendete Gegenwart)",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Sie ____ nach Berlin ____. (fahren)",
            "correct_answer": "ist gefahren",
            "alternative_answers": [],
            "explanation_de": "Bewegungsverben verwenden 'sein'. Partizip II: gefahren.",
            "hints": ["Bewegung → sein", "fahren → gefahren"],
            "context_category": "daily"
        },
        {
            "topic_name": "Perfekt (Vollendete Gegenwart)",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A2",
            "question_text": "Wir ____ Deutsch ____.",
            "correct_answer": "haben gelernt",
            "alternative_answers": ["sind gelernt", "haben lernen", "sind lernen"],
            "explanation_de": "'Lernen' braucht 'haben'. Partizip II: ge-lern-t (regelmäßig).",
            "hints": ["transitive Verben → haben", "regelmäßig: ge-...-t"],
            "context_category": "general"
        },
        {
            "topic_name": "Perfekt (Vollendete Gegenwart)",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Er hat zu Hause gebleibt.",
            "correct_answer": "Er ist zu Hause geblieben.",
            "alternative_answers": [],
            "explanation_de": "'Bleiben' ist eine Ausnahme und verwendet 'sein', nicht 'haben'.",
            "hints": ["bleiben = Ausnahme", "sein, bleiben, passieren → sein"],
            "context_category": "daily"
        },
        {
            "topic_name": "Perfekt (Vollendete Gegenwart)",
            "exercise_type": "sentence_building",
            "difficulty_level": "A2",
            "question_text": "Ordne: [habe, gesehen, einen, Film, ich, gestern]",
            "correct_answer": "Ich habe gestern einen Film gesehen.",
            "alternative_answers": ["Gestern habe ich einen Film gesehen."],
            "explanation_de": "Perfekt: haben/sein + Partizip II am Ende. Zeitangabe kann am Anfang oder in der Mitte stehen.",
            "hints": ["Partizip II am Ende", "Zeit flexibel"],
            "context_category": "daily"
        },

        # ========== PRETERITE EXERCISES ==========
        {
            "topic_name": "Präteritum (Vergangenheit)",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Er ____ jeden Tag zur Arbeit. (gehen)",
            "correct_answer": "ging",
            "alternative_answers": [],
            "explanation_de": "'Gehen' ist unregelmäßig. Präteritum: ging.",
            "hints": ["unregelmäßig", "gehen → ging"],
            "context_category": "business"
        },
        {
            "topic_name": "Präteritum (Vergangenheit)",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Ich ____ gestern müde. (sein)",
            "correct_answer": "war",
            "alternative_answers": [],
            "explanation_de": "'Sein' im Präteritum: ich war, du warst, er war.",
            "hints": ["sein → war", "ich → keine Endung bei unregelmäßigen Verben"],
            "context_category": "general"
        },
        {
            "topic_name": "Präteritum (Vergangenheit)",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B1",
            "question_text": "Sie ____ viel zu tun.",
            "correct_answer": "hatte",
            "alternative_answers": ["habe", "hat", "hatten"],
            "explanation_de": "'Haben' im Präteritum: ich/er/sie hatte.",
            "hints": ["haben → hatte", "3. Person Singular"],
            "context_category": "business"
        },
        {
            "topic_name": "Präteritum (Vergangenheit)",
            "exercise_type": "error_correction",
            "difficulty_level": "B1",
            "question_text": "Das Kind spielte im Garten.",
            "correct_answer": "Das Kind spielte im Garten.",
            "alternative_answers": [],
            "explanation_de": "Dieser Satz ist bereits korrekt. Regelmäßiges Verb: spiel-te.",
            "hints": ["regelmäßig: Stamm + -te"],
            "context_category": "daily"
        },

        # ========== FUTURE TENSE EXERCISES ==========
        {
            "topic_name": "Futur I (Zukunft)",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Ich ____ morgen ____. (kommen)",
            "correct_answer": "werde kommen",
            "alternative_answers": [],
            "explanation_de": "Futur I: werden + Infinitiv. Ich werde kommen.",
            "hints": ["werden + Infinitiv", "ich werde"],
            "context_category": "general"
        },
        {
            "topic_name": "Futur I (Zukunft)",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B1",
            "question_text": "Es ____ regnen.",
            "correct_answer": "wird",
            "alternative_answers": ["werdet", "werdest", "werden"],
            "explanation_de": "'Es' (3. Person Singular) → wird.",
            "hints": ["es → wird", "3. Person Singular"],
            "context_category": "general"
        },
        {
            "topic_name": "Futur I (Zukunft)",
            "exercise_type": "translation",
            "difficulty_level": "B1",
            "question_text": "Viaggeremo in Italia l'anno prossimo. (it → de)",
            "correct_answer": "Wir werden nächstes Jahr nach Italien reisen.",
            "alternative_answers": [],
            "explanation_de": "Futur I: wir werden + Infinitiv (reisen).",
            "hints": ["werden + Infinitiv", "wir werden"],
            "context_category": "daily"
        },

        # ========== MODAL VERBS EXERCISES ==========
        {
            "topic_name": "Modalverben",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich ____ schwimmen. (können)",
            "correct_answer": "kann",
            "alternative_answers": [],
            "explanation_de": "'Können' im Präsens: ich kann (Vokalwechsel ö→a).",
            "hints": ["ich kann", "Vokalwechsel im Singular"],
            "context_category": "general"
        },
        {
            "topic_name": "Modalverben",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Du ____ pünktlich sein. (sollen)",
            "correct_answer": "sollst",
            "alternative_answers": [],
            "explanation_de": "'Sollen' im Präsens: du sollst.",
            "hints": ["du sollst", "sollen hat keinen Vokalwechsel"],
            "context_category": "business"
        },
        {
            "topic_name": "Modalverben",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A2",
            "question_text": "Wir ____ hier nicht rauchen.",
            "correct_answer": "dürfen",
            "alternative_answers": ["dürft", "darfen", "darf"],
            "explanation_de": "'Dürfen' im Präsens: wir dürfen.",
            "hints": ["wir → -en", "Plural = wie Infinitiv"],
            "context_category": "general"
        },
        {
            "topic_name": "Modalverben",
            "exercise_type": "sentence_building",
            "difficulty_level": "A2",
            "question_text": "Ordne: [heute, arbeiten, muss, ich]",
            "correct_answer": "Ich muss heute arbeiten.",
            "alternative_answers": [],
            "explanation_de": "Modalverb Position 2, Infinitiv am Ende.",
            "hints": ["Modalverb Position 2", "Infinitiv am Ende"],
            "context_category": "business"
        },
        {
            "topic_name": "Modalverben",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Sie will Ärztin werden wird.",
            "correct_answer": "Sie will Ärztin werden.",
            "alternative_answers": [],
            "explanation_de": "'Werden' ist hier Infinitiv (nicht konjugiert). Nur 'will' wird konjugiert.",
            "hints": ["Modalverb konjugiert", "Infinitiv unverändert"],
            "context_category": "business"
        },

        # ========== SUBJUNCTIVE II EXERCISES ==========
        {
            "topic_name": "Konjunktiv II",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "Wenn ich reich ____, würde ich reisen. (sein)",
            "correct_answer": "wäre",
            "alternative_answers": [],
            "explanation_de": "Konjunktiv II von 'sein': ich wäre.",
            "hints": ["sein → wäre", "irreale Bedingung"],
            "context_category": "general"
        },
        {
            "topic_name": "Konjunktiv II",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "Wenn ich Zeit ____, würde ich dich besuchen. (haben)",
            "correct_answer": "hätte",
            "alternative_answers": [],
            "explanation_de": "Konjunktiv II von 'haben': ich hätte.",
            "hints": ["haben → hätte", "irreale Bedingung"],
            "context_category": "general"
        },
        {
            "topic_name": "Konjunktiv II",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B2",
            "question_text": "____ Sie mir helfen? (höfliche Bitte)",
            "correct_answer": "Könnten",
            "alternative_answers": ["Können", "Könnt", "Kann"],
            "explanation_de": "Höfliche Bitte mit Konjunktiv II. können → könnten (Sie).",
            "hints": ["höflich = Konjunktiv II", "können → könnten"],
            "context_category": "business"
        },
        {
            "topic_name": "Konjunktiv II",
            "exercise_type": "translation",
            "difficulty_level": "B2",
            "question_text": "Vorrei un bicchiere d'acqua. (it → de)",
            "correct_answer": "Ich hätte gerne ein Glas Wasser.",
            "alternative_answers": ["Ich möchte gerne ein Glas Wasser."],
            "explanation_de": "Höflicher Wunsch: 'ich hätte gerne' (Konjunktiv II) oder 'ich möchte'.",
            "hints": ["vorrei = hätte gerne / möchte", "höfliche Form"],
            "context_category": "daily"
        },

        # ========== SEPARABLE VERBS EXERCISES ==========
        {
            "topic_name": "Trennbare Verben",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Der Zug kommt um 10 Uhr ____. (ankommen)",
            "correct_answer": "an",
            "alternative_answers": [],
            "explanation_de": "Trennbares Verb 'ankommen': Präfix 'an' geht ans Satzende.",
            "hints": ["Präfix ans Ende", "ankommen → kommt...an"],
            "context_category": "daily"
        },
        {
            "topic_name": "Trennbare Verben",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich stehe früh ____. (aufstehen)",
            "correct_answer": "auf",
            "alternative_answers": [],
            "explanation_de": "Trennbares Verb 'aufstehen': 'auf' geht ans Ende.",
            "hints": ["Präfix ans Ende", "aufstehen → stehe...auf"],
            "context_category": "daily"
        },
        {
            "topic_name": "Trennbare Verben",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Sie einlädt uns zum Essen.",
            "correct_answer": "Sie lädt uns zum Essen ein.",
            "alternative_answers": [],
            "explanation_de": "Trennbares Verb: konjugiertes Verb Position 2, Präfix ans Ende.",
            "hints": ["Verb Position 2", "Präfix ans Ende"],
            "context_category": "daily"
        },
        {
            "topic_name": "Trennbare Verben",
            "exercise_type": "sentence_building",
            "difficulty_level": "A2",
            "question_text": "Ordne: [kommst, du, mit, ?]",
            "correct_answer": "Kommst du mit?",
            "alternative_answers": [],
            "explanation_de": "Frage: Verb Position 1, Präfix ans Ende.",
            "hints": ["Frage: Verb zuerst", "Präfix ans Ende"],
            "context_category": "general"
        },

        # ========== REFLEXIVE VERBS EXERCISES ==========
        {
            "topic_name": "Reflexive Verben",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Ich ziehe ____ an. (sich anziehen)",
            "correct_answer": "mich",
            "alternative_answers": [],
            "explanation_de": "Reflexivpronomen für 'ich' ist 'mich' (Akkusativ).",
            "hints": ["ich → mich", "Reflexivpronomen Akkusativ"],
            "context_category": "daily"
        },
        {
            "topic_name": "Reflexive Verben",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Sie interessiert ____ für Musik. (sich interessieren)",
            "correct_answer": "sich",
            "alternative_answers": [],
            "explanation_de": "Reflexivpronomen für 'sie/er/es' ist 'sich'.",
            "hints": ["sie/er/es → sich"],
            "context_category": "general"
        },
        {
            "topic_name": "Reflexive Verben",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B1",
            "question_text": "Ich putze ____ die Zähne.",
            "correct_answer": "mir",
            "alternative_answers": ["mich", "sich", "dich"],
            "explanation_de": "Dativ, weil es ein Akkusativobjekt gibt ('die Zähne'). Ich → mir.",
            "hints": ["Dativ wegen Akkusativobjekt", "ich → mir (Dativ)"],
            "context_category": "daily"
        },
        {
            "topic_name": "Reflexive Verben",
            "exercise_type": "error_correction",
            "difficulty_level": "B1",
            "question_text": "Wir treffen uns morgen uns.",
            "correct_answer": "Wir treffen uns morgen.",
            "alternative_answers": [],
            "explanation_de": "Reflexivpronomen nur einmal verwenden! 'Uns' nicht doppelt.",
            "hints": ["nur ein Reflexivpronomen", "wir → uns"],
            "context_category": "general"
        },

        # ========== MAIN CLAUSE EXERCISES ==========
        {
            "topic_name": "Hauptsatz - Verbposition",
            "exercise_type": "sentence_building",
            "difficulty_level": "A2",
            "question_text": "Ordne: [gehe, nach, ich, Hause]",
            "correct_answer": "Ich gehe nach Hause.",
            "alternative_answers": [],
            "explanation_de": "Hauptsatz: Subjekt Position 1, Verb Position 2.",
            "hints": ["Verb Position 2", "Subjekt + Verb"],
            "context_category": "daily"
        },
        {
            "topic_name": "Hauptsatz - Verbposition",
            "exercise_type": "sentence_building",
            "difficulty_level": "A2",
            "question_text": "Ordne: [besuche, heute, meine, ich, Eltern]",
            "correct_answer": "Heute besuche ich meine Eltern.",
            "alternative_answers": ["Ich besuche heute meine Eltern."],
            "explanation_de": "Position 1 flexibel (Subjekt oder Zeit). Verb immer Position 2!",
            "hints": ["Verb Position 2", "Position 1 = Subjekt oder Zeit"],
            "context_category": "daily"
        },
        {
            "topic_name": "Hauptsatz - Verbposition",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Morgen ich gehe ins Kino.",
            "correct_answer": "Morgen gehe ich ins Kino.",
            "alternative_answers": [],
            "explanation_de": "Verb IMMER Position 2! Wenn Position 1 'morgen' ist, muss Verb an Position 2, dann Subjekt.",
            "hints": ["Verb Position 2", "Inversion nach Zeitangabe"],
            "context_category": "daily"
        },

        # ========== SUBORDINATE CLAUSE EXERCISES ==========
        {
            "topic_name": "Nebensatz - Verbposition",
            "exercise_type": "sentence_building",
            "difficulty_level": "B1",
            "question_text": "Ordne: [dass, glaube, ich, er, kommt, heute]",
            "correct_answer": "Ich glaube, dass er heute kommt.",
            "alternative_answers": [],
            "explanation_de": "Nebensatz: Verb ans Ende! Komma vor 'dass'.",
            "hints": ["Verb ans Ende im Nebensatz", "Komma vor dass"],
            "context_category": "general"
        },
        {
            "topic_name": "Nebensatz - Verbposition",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Sie bleibt zu Hause, weil sie krank ____.",
            "correct_answer": "ist",
            "alternative_answers": [],
            "explanation_de": "Nebensatz mit 'weil': Verb ans Ende.",
            "hints": ["weil = Nebensatz", "Verb ans Ende"],
            "context_category": "daily"
        },
        {
            "topic_name": "Nebensatz - Verbposition",
            "exercise_type": "error_correction",
            "difficulty_level": "B1",
            "question_text": "Ich weiß, dass du hast recht.",
            "correct_answer": "Ich weiß, dass du recht hast.",
            "alternative_answers": [],
            "explanation_de": "Im Nebensatz: Verb ganz ans Ende (nach 'recht').",
            "hints": ["Verb ans Ende", "nicht wie Englisch"],
            "context_category": "general"
        },

        # ========== QUESTION SENTENCES EXERCISES ==========
        {
            "topic_name": "Fragesätze",
            "exercise_type": "sentence_building",
            "difficulty_level": "A1",
            "question_text": "Ordne: [du, kommst, morgen, ?]",
            "correct_answer": "Kommst du morgen?",
            "alternative_answers": [],
            "explanation_de": "Ja/Nein-Frage: Verb Position 1.",
            "hints": ["Ja/Nein-Frage", "Verb Position 1"],
            "context_category": "general"
        },
        {
            "topic_name": "Fragesätze",
            "exercise_type": "fill_blank",
            "difficulty_level": "A1",
            "question_text": "____ machst du heute?",
            "correct_answer": "Was",
            "alternative_answers": [],
            "explanation_de": "Frage nach Sache/Aktivität: 'was'.",
            "hints": ["Sache = was", "W-Frage"],
            "context_category": "general"
        },
        {
            "topic_name": "Fragesätze",
            "exercise_type": "fill_blank",
            "difficulty_level": "A1",
            "question_text": "____ kommst du? (Herkunft)",
            "correct_answer": "Woher",
            "alternative_answers": [],
            "explanation_de": "Frage nach Herkunft: 'woher'.",
            "hints": ["Herkunft = woher", "wo → Ort, woher → Herkunft"],
            "context_category": "general"
        },
        {
            "topic_name": "Fragesätze",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A1",
            "question_text": "____ gehst du? (Richtung)",
            "correct_answer": "Wohin",
            "alternative_answers": ["Wo", "Woher", "Wer"],
            "explanation_de": "Frage nach Richtung/Ziel: 'wohin'.",
            "hints": ["Richtung = wohin", "Bewegung zu einem Ort"],
            "context_category": "daily"
        },

        # ========== NEGATION EXERCISES ==========
        {
            "topic_name": "Negation",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich habe ____ Zeit.",
            "correct_answer": "keine",
            "alternative_answers": [],
            "explanation_de": "'Zeit' ohne Artikel → Negation mit 'keine'.",
            "hints": ["ohne Artikel → kein", "Zeit = feminin"],
            "context_category": "general"
        },
        {
            "topic_name": "Negation",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Das ist ____ richtig.",
            "correct_answer": "nicht",
            "alternative_answers": [],
            "explanation_de": "Adjektiv → Negation mit 'nicht'.",
            "hints": ["Adjektiv → nicht", "nicht vor Adjektiv"],
            "context_category": "general"
        },
        {
            "topic_name": "Negation",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A2",
            "question_text": "Ich habe ____ Auto.",
            "correct_answer": "kein",
            "alternative_answers": ["nicht", "keinen", "keine"],
            "explanation_de": "'Ein Auto' → 'kein Auto'. Neutrum Nominativ/Akkusativ.",
            "hints": ["ein → kein", "Auto = neutrum"],
            "context_category": "daily"
        },
        {
            "topic_name": "Negation",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Sie wohnt kein in Berlin.",
            "correct_answer": "Sie wohnt nicht in Berlin.",
            "alternative_answers": [],
            "explanation_de": "Präposition + Ort → 'nicht', nicht 'kein'.",
            "hints": ["Präposition → nicht", "kein nur für Nomen"],
            "context_category": "daily"
        },

        # ========== ACCUSATIVE PREPOSITIONS EXERCISES ==========
        {
            "topic_name": "Präpositionen mit Akkusativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich gehe durch ____ Park.",
            "correct_answer": "den",
            "alternative_answers": [],
            "explanation_de": "'Durch' verlangt Akkusativ. 'Park' ist maskulin = 'den Park'.",
            "hints": ["durch + Akkusativ", "Park = maskulin"],
            "context_category": "daily"
        },
        {
            "topic_name": "Präpositionen mit Akkusativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Das Geschenk ist für ____ Vater.",
            "correct_answer": "meinen",
            "alternative_answers": [],
            "explanation_de": "'Für' + Akkusativ. Maskulin: mein → meinen.",
            "hints": ["für + Akkusativ", "maskulin: mein → meinen"],
            "context_category": "daily"
        },
        {
            "topic_name": "Präpositionen mit Akkusativ",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A2",
            "question_text": "Der Unterricht beginnt um ____ Uhr.",
            "correct_answer": "9",
            "alternative_answers": ["der 9", "9.", "den 9"],
            "explanation_de": "'Um' + Uhrzeit (ohne Artikel).",
            "hints": ["um + Uhrzeit", "kein Artikel bei Uhrzeiten"],
            "context_category": "business"
        },
        {
            "topic_name": "Präpositionen mit Akkusativ",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Sie kommt ohne ihrem Mann.",
            "correct_answer": "Sie kommt ohne ihren Mann.",
            "alternative_answers": [],
            "explanation_de": "'Ohne' verlangt Akkusativ, nicht Dativ. Maskulin: ihren Mann.",
            "hints": ["ohne + Akkusativ", "nicht Dativ!"],
            "context_category": "daily"
        },

        # ========== DATIVE PREPOSITIONS EXERCISES ==========
        {
            "topic_name": "Präpositionen mit Dativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich komme aus ____ Schweiz.",
            "correct_answer": "der",
            "alternative_answers": [],
            "explanation_de": "'Aus' + Dativ. 'Schweiz' ist feminin und braucht Artikel = 'der Schweiz'.",
            "hints": ["aus + Dativ", "Schweiz = feminin + Artikel"],
            "context_category": "general"
        },
        {
            "topic_name": "Präpositionen mit Dativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich fahre mit ____ Zug.",
            "correct_answer": "dem",
            "alternative_answers": [],
            "explanation_de": "'Mit' + Dativ. 'Zug' ist maskulin = 'dem Zug'.",
            "hints": ["mit + Dativ", "Zug = maskulin"],
            "context_category": "daily"
        },
        {
            "topic_name": "Präpositionen mit Dativ",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A2",
            "question_text": "Nach ____ Essen gehen wir spazieren.",
            "correct_answer": "dem",
            "alternative_answers": ["das", "den", "der"],
            "explanation_de": "'Nach' + Dativ. 'Essen' ist neutrum = 'dem Essen'.",
            "hints": ["nach + Dativ", "Essen = neutrum"],
            "context_category": "daily"
        },
        {
            "topic_name": "Präpositionen mit Dativ",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Ich gehe zu den Arzt.",
            "correct_answer": "Ich gehe zum Arzt.",
            "alternative_answers": ["Ich gehe zu dem Arzt."],
            "explanation_de": "'Zu' + Dativ. 'Zu dem' = 'zum'. Maskulin: dem Arzt.",
            "hints": ["zu + dem = zum", "Kontraktion"],
            "context_category": "daily"
        },

        # ========== TWO-WAY PREPOSITIONS EXERCISES ==========
        {
            "topic_name": "Wechselpräpositionen",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Ich gehe in ____ Park. (Wohin?)",
            "correct_answer": "den",
            "alternative_answers": [],
            "explanation_de": "Wohin? = Bewegung = Akkusativ. 'Park' maskulin = 'den Park'.",
            "hints": ["Wohin? → Akkusativ", "Park = maskulin"],
            "context_category": "daily"
        },
        {
            "topic_name": "Wechselpräpositionen",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Ich bin in ____ Park. (Wo?)",
            "correct_answer": "dem",
            "alternative_answers": [],
            "explanation_de": "Wo? = Position = Dativ. 'Park' maskulin = 'dem Park' (oder 'im').",
            "hints": ["Wo? → Dativ", "in dem = im"],
            "context_category": "daily"
        },
        {
            "topic_name": "Wechselpräpositionen",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B1",
            "question_text": "Das Buch liegt ____ Tisch.",
            "correct_answer": "auf dem",
            "alternative_answers": ["auf den", "auf der", "auf das"],
            "explanation_de": "Wo? = Dativ. 'Tisch' maskulin = 'auf dem Tisch'.",
            "hints": ["liegen = Position → Wo? → Dativ", "Tisch = maskulin"],
            "context_category": "general"
        },
        {
            "topic_name": "Wechselpräpositionen",
            "exercise_type": "error_correction",
            "difficulty_level": "B1",
            "question_text": "Ich lege das Buch auf den Tisch. (Korrekt?)",
            "correct_answer": "Ich lege das Buch auf den Tisch.",
            "alternative_answers": [],
            "explanation_de": "Korrekt! 'Legen' = Richtung = Wohin? = Akkusativ.",
            "hints": ["legen → Wohin? → Akkusativ"],
            "context_category": "general"
        },
        {
            "topic_name": "Wechselpräpositionen",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Ich hänge das Bild an ____ Wand. (Wohin?)",
            "correct_answer": "die",
            "alternative_answers": [],
            "explanation_de": "Wohin? = Akkusativ. 'Wand' feminin = 'die Wand' (bleibt gleich).",
            "hints": ["Wohin? → Akkusativ", "feminin bleibt 'die'"],
            "context_category": "daily"
        },

        # ========== GENITIVE PREPOSITIONS EXERCISES ==========
        {
            "topic_name": "Präpositionen mit Genitiv",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "Während ____ Sommers reisen wir.",
            "correct_answer": "des",
            "alternative_answers": [],
            "explanation_de": "'Während' + Genitiv. 'Sommer' maskulin = 'des Sommers'.",
            "hints": ["während + Genitiv", "maskulin: des + -s"],
            "context_category": "daily"
        },
        {
            "topic_name": "Präpositionen mit Genitiv",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "Wegen ____ Regens bleiben wir zu Hause.",
            "correct_answer": "des",
            "alternative_answers": [],
            "explanation_de": "'Wegen' + Genitiv. 'Regen' maskulin = 'des Regens'.",
            "hints": ["wegen + Genitiv", "maskulin: des + -s"],
            "context_category": "daily"
        },
        {
            "topic_name": "Präpositionen mit Genitiv",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B2",
            "question_text": "Trotz ____ haben wir Erfolg.",
            "correct_answer": "der Probleme",
            "alternative_answers": ["den Problemen", "die Probleme", "dem Problemen"],
            "explanation_de": "'Trotz' + Genitiv. Plural = 'der Probleme'.",
            "hints": ["trotz + Genitiv", "Plural Genitiv = der"],
            "context_category": "business"
        },
        {
            "topic_name": "Präpositionen mit Genitiv",
            "exercise_type": "error_correction",
            "difficulty_level": "B2",
            "question_text": "Statt einem Auto kauft er ein Fahrrad.",
            "correct_answer": "Statt eines Autos kauft er ein Fahrrad.",
            "alternative_answers": [],
            "explanation_de": "'Statt' verlangt Genitiv, nicht Dativ. 'Auto' neutrum = 'eines Autos'.",
            "hints": ["statt + Genitiv", "nicht Dativ!"],
            "context_category": "daily"
        },

        # ========== ARTICLES EXERCISES ==========
        {
            "topic_name": "Bestimmter und unbestimmter Artikel",
            "exercise_type": "fill_blank",
            "difficulty_level": "A1",
            "question_text": "____ Lehrer erklärt die Grammatik. (bestimmt)",
            "correct_answer": "Der",
            "alternative_answers": [],
            "explanation_de": "Bestimmter Artikel für 'Lehrer' (maskulin, Nominativ) = 'der'.",
            "hints": ["Lehrer = maskulin", "bestimmt = der/die/das"],
            "context_category": "general"
        },
        {
            "topic_name": "Bestimmter und unbestimmter Artikel",
            "exercise_type": "fill_blank",
            "difficulty_level": "A1",
            "question_text": "____ Mann kommt. (unbestimmt)",
            "correct_answer": "Ein",
            "alternative_answers": [],
            "explanation_de": "Unbestimmter Artikel für 'Mann' (maskulin) = 'ein'.",
            "hints": ["Mann = maskulin", "unbestimmt = ein/eine/ein"],
            "context_category": "general"
        },
        {
            "topic_name": "Bestimmter und unbestimmter Artikel",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A1",
            "question_text": "Ich bin ____.",
            "correct_answer": "Lehrer",
            "alternative_answers": ["ein Lehrer", "der Lehrer", "einen Lehrer"],
            "explanation_de": "Bei Berufen meist ohne Artikel: 'Ich bin Lehrer.'",
            "hints": ["Beruf ohne Artikel", "Nullartikel"],
            "context_category": "business"
        },

        # ========== POSSESSIVE ARTICLES EXERCISES ==========
        {
            "topic_name": "Possessivartikel",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Das ist ____ Buch. (mein)",
            "correct_answer": "mein",
            "alternative_answers": [],
            "explanation_de": "'Buch' neutrum, Nominativ = 'mein Buch'.",
            "hints": ["Buch = neutrum", "Nominativ neutrum = mein"],
            "context_category": "general"
        },
        {
            "topic_name": "Possessivartikel",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich sehe ____ Bruder. (dein)",
            "correct_answer": "deinen",
            "alternative_answers": [],
            "explanation_de": "'Bruder' maskulin, Akkusativ = 'deinen Bruder'.",
            "hints": ["Bruder = maskulin", "Akkusativ: mein → meinen"],
            "context_category": "general"
        },
        {
            "topic_name": "Possessivartikel",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A2",
            "question_text": "Wo ist ____ Auto? (euer)",
            "correct_answer": "euer",
            "alternative_answers": ["eures", "eueres", "eure"],
            "explanation_de": "'Auto' neutrum, Nominativ = 'euer Auto'.",
            "hints": ["Auto = neutrum", "euer verliert e vor Endung"],
            "context_category": "daily"
        },

        # ========== PERSONAL PRONOUNS EXERCISES ==========
        {
            "topic_name": "Personalpronomen",
            "exercise_type": "fill_blank",
            "difficulty_level": "A1",
            "question_text": "Er sieht ____. (ich, Akkusativ)",
            "correct_answer": "mich",
            "alternative_answers": [],
            "explanation_de": "Akkusativ von 'ich' = 'mich'.",
            "hints": ["ich → mich (Akk.)", "direktes Objekt"],
            "context_category": "general"
        },
        {
            "topic_name": "Personalpronomen",
            "exercise_type": "fill_blank",
            "difficulty_level": "A1",
            "question_text": "Ich helfe ____. (du, Dativ)",
            "correct_answer": "dir",
            "alternative_answers": [],
            "explanation_de": "Dativ von 'du' = 'dir'.",
            "hints": ["du → dir (Dat.)", "helfen + Dativ"],
            "context_category": "general"
        },
        {
            "topic_name": "Personalpronomen",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A1",
            "question_text": "Gibst du es ____? (ich, Dativ)",
            "correct_answer": "mir",
            "alternative_answers": ["mich", "meinem", "mein"],
            "explanation_de": "Dativ von 'ich' = 'mir'. Pronomen vor Pronomen: Akk. vor Dat.",
            "hints": ["ich → mir (Dat.)", "geben + Dativ"],
            "context_category": "general"
        },

        # ========== RELATIVE CLAUSES EXERCISES ==========
        {
            "topic_name": "Relativpronomen und Relativsätze",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Das ist der Mann, ____ hier wohnt.",
            "correct_answer": "der",
            "alternative_answers": [],
            "explanation_de": "Relativpronomen Nominativ (Subjekt im Relativsatz). Maskulin = 'der'.",
            "hints": ["Wer wohnt hier?", "Subjekt = Nominativ"],
            "context_category": "general"
        },
        {
            "topic_name": "Relativpronomen und Relativsätze",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Die Frau, ____ ich kenne, ist nett.",
            "correct_answer": "die",
            "alternative_answers": [],
            "explanation_de": "Relativpronomen Akkusativ (Objekt: 'ich kenne'). Feminin = 'die'.",
            "hints": ["Wen kenne ich?", "Akkusativ feminin = die"],
            "context_category": "general"
        },
        {
            "topic_name": "Relativpronomen und Relativsätze",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B1",
            "question_text": "Das Kind, ____ ich helfe, ist klein.",
            "correct_answer": "dem",
            "alternative_answers": ["das", "den", "der"],
            "explanation_de": "'Helfen' + Dativ. Relativpronomen Dativ neutrum = 'dem'.",
            "hints": ["helfen + Dativ", "neutrum Dativ = dem"],
            "context_category": "general"
        },
        {
            "topic_name": "Relativpronomen und Relativsätze",
            "exercise_type": "error_correction",
            "difficulty_level": "B1",
            "question_text": "Der Autor, dessen Buch ich lese ist berühmt.",
            "correct_answer": "Der Autor, dessen Buch ich lese, ist berühmt.",
            "alternative_answers": [],
            "explanation_de": "Komma vor 'ist' fehlt! Relativsatz braucht Komma am Ende.",
            "hints": ["Komma nach Relativsatz", "Verb am Ende"],
            "context_category": "general"
        },

        # ========== ADJECTIVE DECLENSION DEFINITE EXERCISES ==========
        {
            "topic_name": "Adjektivdeklination mit bestimmtem Artikel",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Ich sehe den ____ Hund. (klein)",
            "correct_answer": "kleinen",
            "alternative_answers": [],
            "explanation_de": "Maskulin Akkusativ mit 'den' → Adjektiv + -en.",
            "hints": ["maskulin Akkusativ → -en", "den + Adjektiv-en"],
            "context_category": "daily"
        },
        {
            "topic_name": "Adjektivdeklination mit bestimmtem Artikel",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Die ____ Lehrerin ist nett. (neu)",
            "correct_answer": "neue",
            "alternative_answers": [],
            "explanation_de": "Feminin Nominativ → Adjektiv + -e.",
            "hints": ["Nominativ → -e", "die + Adjektiv-e"],
            "context_category": "general"
        },
        {
            "topic_name": "Adjektivdeklination mit bestimmtem Artikel",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B1",
            "question_text": "Mit dem ____ Auto fahren wir.",
            "correct_answer": "guten",
            "alternative_answers": ["gute", "gut", "guter"],
            "explanation_de": "Dativ → Adjektiv + -en.",
            "hints": ["Dativ → -en", "mit + Dativ"],
            "context_category": "daily"
        },

        # ========== ADJECTIVE DECLENSION INDEFINITE EXERCISES ==========
        {
            "topic_name": "Adjektivdeklination mit unbestimmtem Artikel",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Ich habe einen ____ Computer. (neu)",
            "correct_answer": "neuen",
            "alternative_answers": [],
            "explanation_de": "Maskulin Akkusativ → Adjektiv + -en.",
            "hints": ["maskulin Akkusativ → -en", "einen + -en"],
            "context_category": "general"
        },
        {
            "topic_name": "Adjektivdeklination mit unbestimmtem Artikel",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Das ist eine ____ Idee. (gut)",
            "correct_answer": "gute",
            "alternative_answers": [],
            "explanation_de": "Feminin Nominativ → Adjektiv + -e.",
            "hints": ["feminin Nominativ → -e", "eine + -e"],
            "context_category": "general"
        },
        {
            "topic_name": "Adjektivdeklination mit unbestimmtem Artikel",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B1",
            "question_text": "Sie kauft ein ____ Kleid.",
            "correct_answer": "schönes",
            "alternative_answers": ["schöne", "schön", "schönen"],
            "explanation_de": "Neutrum Nominativ/Akkusativ → Adjektiv + -es.",
            "hints": ["neutrum → -es", "ein + -es"],
            "context_category": "daily"
        },

        # ========== ADJECTIVE DECLENSION NULL EXERCISES ==========
        {
            "topic_name": "Adjektivdeklination ohne Artikel",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "Ich trinke ____ Wein. (gut)",
            "correct_answer": "guten",
            "alternative_answers": [],
            "explanation_de": "Maskulin Akkusativ ohne Artikel → -en (wie 'den').",
            "hints": ["maskulin Akkusativ → -en", "wie bestimmter Artikel"],
            "context_category": "daily"
        },
        {
            "topic_name": "Adjektivdeklination ohne Artikel",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "Mit ____ Wasser waschen. (kalt)",
            "correct_answer": "kaltem",
            "alternative_answers": [],
            "explanation_de": "Neutrum Dativ ohne Artikel → -em (wie 'dem').",
            "hints": ["neutrum Dativ → -em", "wie 'dem'"],
            "context_category": "daily"
        },

        # ========== COMPARISON EXERCISES ==========
        {
            "topic_name": "Komparativ und Superlativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Mein Auto ist ____ als dein Auto. (schnell)",
            "correct_answer": "schneller",
            "alternative_answers": [],
            "explanation_de": "Komparativ: Adjektiv + -er.",
            "hints": ["Komparativ → -er", "schnell → schneller"],
            "context_category": "daily"
        },
        {
            "topic_name": "Komparativ und Superlativ",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Das ist das ____ Haus der Stadt. (schön)",
            "correct_answer": "schönste",
            "alternative_answers": [],
            "explanation_de": "Superlativ attributiv: der/die/das + Adjektiv-ste.",
            "hints": ["Superlativ → -ste", "das schönste"],
            "context_category": "daily"
        },
        {
            "topic_name": "Komparativ und Superlativ",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A2",
            "question_text": "Sie spricht ____ Deutsch.",
            "correct_answer": "am besten",
            "alternative_answers": ["am gutesten", "der beste", "beste"],
            "explanation_de": "Superlativ prädikativ: 'am besten'. 'Gut' ist unregelmäßig.",
            "hints": ["gut → besser → am besten", "unregelmäßig"],
            "context_category": "general"
        },
        {
            "topic_name": "Komparativ und Superlativ",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Dieser Film ist interessanterer.",
            "correct_answer": "Dieser Film ist interessanter.",
            "alternative_answers": [],
            "explanation_de": "Komparativ: nur -er, nicht -erer!",
            "hints": ["Komparativ → nur -er", "nicht doppelt"],
            "context_category": "daily"
        },

        # ========== PASSIVE VOICE EXERCISES ==========
        {
            "topic_name": "Passiv (Vorgangspassiv)",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "Das Auto ____ repariert. (Präsens)",
            "correct_answer": "wird",
            "alternative_answers": [],
            "explanation_de": "Präsens Passiv: werden (konjugiert) + Partizip II.",
            "hints": ["werden + Partizip II", "Präsens: wird"],
            "context_category": "general"
        },
        {
            "topic_name": "Passiv (Vorgangspassiv)",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "Die Rechnung ____ bezahlt. (Präteritum)",
            "correct_answer": "wurde",
            "alternative_answers": [],
            "explanation_de": "Präteritum Passiv: wurde + Partizip II.",
            "hints": ["wurde + Partizip II", "Präteritum: wurde"],
            "context_category": "business"
        },
        {
            "topic_name": "Passiv (Vorgangspassiv)",
            "exercise_type": "sentence_building",
            "difficulty_level": "B2",
            "question_text": "Transformiere: Der Mechaniker repariert das Auto.",
            "correct_answer": "Das Auto wird vom Mechaniker repariert.",
            "alternative_answers": ["Das Auto wird repariert."],
            "explanation_de": "Passiv: Objekt wird Subjekt. Täter mit 'von + Dativ' (optional).",
            "hints": ["Akkusativobjekt → Subjekt", "von + Dativ für Täter"],
            "context_category": "general"
        },

        # ========== INDIRECT SPEECH EXERCISES ==========
        {
            "topic_name": "Indirekte Rede (Konjunktiv I)",
            "exercise_type": "fill_blank",
            "difficulty_level": "C1",
            "question_text": "Er sagt, er ____ müde. (sein)",
            "correct_answer": "sei",
            "alternative_answers": [],
            "explanation_de": "Konjunktiv I von 'sein': er sei.",
            "hints": ["Konjunktiv I", "sein → sei"],
            "context_category": "general"
        },
        {
            "topic_name": "Indirekte Rede (Konjunktiv I)",
            "exercise_type": "fill_blank",
            "difficulty_level": "C1",
            "question_text": "Sie sagt, sie ____ das Buch gelesen. (haben)",
            "correct_answer": "habe",
            "alternative_answers": [],
            "explanation_de": "Konjunktiv I von 'haben': sie habe.",
            "hints": ["Konjunktiv I", "haben → habe"],
            "context_category": "general"
        },
        {
            "topic_name": "Indirekte Rede (Konjunktiv I)",
            "exercise_type": "sentence_building",
            "difficulty_level": "C1",
            "question_text": "Transformiere: 'Ich bin müde.' → Er sagt, ...",
            "correct_answer": "Er sagt, er sei müde.",
            "alternative_answers": [],
            "explanation_de": "Indirekte Rede: Konjunktiv I. 'Ich bin' → 'er sei'.",
            "hints": ["Konjunktiv I", "Perspektive ändern"],
            "context_category": "general"
        },

        # ========== PARTICIPLES EXERCISES ==========
        {
            "topic_name": "Partizip I und II als Adjektiv",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "Das ____ Kind braucht Hilfe. (weinen)",
            "correct_answer": "weinende",
            "alternative_answers": [],
            "explanation_de": "Partizip I: Infinitiv + -d + Adjektivendung. weinen → weinende.",
            "hints": ["Partizip I = -d", "aktiv, gleichzeitig"],
            "context_category": "daily"
        },
        {
            "topic_name": "Partizip I und II als Adjektiv",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "Die ____ Tür ist offen. (öffnen)",
            "correct_answer": "geöffnete",
            "alternative_answers": [],
            "explanation_de": "Partizip II als Adjektiv: ge-öffn-et + Adjektivendung.",
            "hints": ["Partizip II + Endung", "passiv, vergangen"],
            "context_category": "general"
        },

        # ========== INFINITIVE WITH ZU EXERCISES ==========
        {
            "topic_name": "Infinitiv mit 'zu'",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Ich beginne ____ arbeiten.",
            "correct_answer": "zu",
            "alternative_answers": [],
            "explanation_de": "'Beginnen' verlangt 'zu' + Infinitiv.",
            "hints": ["beginnen + zu + Infinitiv", "zu vor Infinitiv"],
            "context_category": "business"
        },
        {
            "topic_name": "Infinitiv mit 'zu'",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Vergiss nicht, mich ____! (anrufen)",
            "correct_answer": "anzurufen",
            "alternative_answers": [],
            "explanation_de": "Trennbares Verb: 'zu' zwischen Präfix und Verb. an-zu-rufen.",
            "hints": ["trennbar: Präfix-zu-Verb", "anrufen → anzurufen"],
            "context_category": "general"
        },
        {
            "topic_name": "Infinitiv mit 'zu'",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B1",
            "question_text": "Ich lerne Deutsch, ____ in Deutschland zu arbeiten.",
            "correct_answer": "um",
            "alternative_answers": ["damit", "weil", "dass"],
            "explanation_de": "'Um...zu' drückt Zweck/Ziel aus.",
            "hints": ["Zweck = um...zu", "Ziel ausdrücken"],
            "context_category": "business"
        },
        {
            "topic_name": "Infinitiv mit 'zu'",
            "exercise_type": "error_correction",
            "difficulty_level": "B1",
            "question_text": "Ich kann zu schwimmen.",
            "correct_answer": "Ich kann schwimmen.",
            "alternative_answers": [],
            "explanation_de": "Modalverben brauchen KEIN 'zu'!",
            "hints": ["Modalverben ohne zu", "können + Infinitiv"],
            "context_category": "general"
        },

        # ========== COORDINATING CONJUNCTIONS EXERCISES ==========
        {
            "topic_name": "Konjunktionen (koordinierend)",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich gehe ____ er bleibt.",
            "correct_answer": "und",
            "alternative_answers": [],
            "explanation_de": "'Und' verbindet zwei Hauptsätze. Wortstellung bleibt normal.",
            "hints": ["und = Verbindung", "keine Wortstellungsänderung"],
            "context_category": "general"
        },
        {
            "topic_name": "Konjunktionen (koordinierend)",
            "exercise_type": "fill_blank",
            "difficulty_level": "A2",
            "question_text": "Ich will, ____ ich kann nicht.",
            "correct_answer": "aber",
            "alternative_answers": [],
            "explanation_de": "'Aber' drückt Gegensatz aus.",
            "hints": ["Gegensatz = aber", "Position 0"],
            "context_category": "general"
        },
        {
            "topic_name": "Konjunktionen (koordinierend)",
            "exercise_type": "multiple_choice",
            "difficulty_level": "A2",
            "question_text": "Ich komme nicht heute, ____ morgen.",
            "correct_answer": "sondern",
            "alternative_answers": ["aber", "und", "oder"],
            "explanation_de": "'Sondern' nach Negation für Korrektur.",
            "hints": ["nach Negation → sondern", "Korrektur"],
            "context_category": "general"
        },
        {
            "topic_name": "Konjunktionen (koordinierend)",
            "exercise_type": "error_correction",
            "difficulty_level": "A2",
            "question_text": "Ich bleibe zu Hause, denn bin ich krank.",
            "correct_answer": "Ich bleibe zu Hause, denn ich bin krank.",
            "alternative_answers": [],
            "explanation_de": "'Denn' ist Position 0. Normale Wortstellung: Subjekt dann Verb.",
            "hints": ["denn = Position 0", "normale Wortstellung"],
            "context_category": "daily"
        },

        # ========== SUBORDINATING CONJUNCTIONS EXERCISES ==========
        {
            "topic_name": "Konjunktionen (subordinierend)",
            "exercise_type": "sentence_building",
            "difficulty_level": "B1",
            "question_text": "Ordne: [weil, lerne, ich, wichtig, ist, es]",
            "correct_answer": "Ich lerne, weil es wichtig ist.",
            "alternative_answers": [],
            "explanation_de": "'Weil' leitet Nebensatz ein. Verb ans Ende!",
            "hints": ["weil = Nebensatz", "Verb ans Ende"],
            "context_category": "general"
        },
        {
            "topic_name": "Konjunktionen (subordinierend)",
            "exercise_type": "fill_blank",
            "difficulty_level": "B1",
            "question_text": "Ich frage, ____ du Zeit hast.",
            "correct_answer": "ob",
            "alternative_answers": [],
            "explanation_de": "'Ob' für indirekte Ja/Nein-Frage.",
            "hints": ["indirekte Frage = ob", "Nebensatz"],
            "context_category": "general"
        },
        {
            "topic_name": "Konjunktionen (subordinierend)",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B1",
            "question_text": "____ es regnet, gehen wir spazieren.",
            "correct_answer": "Obwohl",
            "alternative_answers": ["Weil", "Wenn", "Dass"],
            "explanation_de": "'Obwohl' = trotzdem, Gegensatz.",
            "hints": ["trotzdem = obwohl", "Gegensatz"],
            "context_category": "daily"
        },

        # ========== TEMPORAL CLAUSES EXERCISES ==========
        {
            "topic_name": "Temporale Nebensätze",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "____ ich koche, hört sie Musik.",
            "correct_answer": "Während",
            "alternative_answers": [],
            "explanation_de": "'Während' = gleichzeitig.",
            "hints": ["gleichzeitig = während", "Nebensatz"],
            "context_category": "daily"
        },
        {
            "topic_name": "Temporale Nebensätze",
            "exercise_type": "fill_blank",
            "difficulty_level": "B2",
            "question_text": "____ du gehst, ruf mich an.",
            "correct_answer": "Bevor",
            "alternative_answers": [],
            "explanation_de": "'Bevor' = davor, Vorzeitigkeit.",
            "hints": ["davor = bevor", "Vorzeitigkeit"],
            "context_category": "general"
        },
        {
            "topic_name": "Temporale Nebensätze",
            "exercise_type": "multiple_choice",
            "difficulty_level": "B2",
            "question_text": "____ er gegessen hat, geht er.",
            "correct_answer": "Nachdem",
            "alternative_answers": ["Bevor", "Während", "Bis"],
            "explanation_de": "'Nachdem' = danach, Nachzeitigkeit.",
            "hints": ["danach = nachdem", "Nachzeitigkeit"],
            "context_category": "daily"
        },
        {
            "topic_name": "Temporale Nebensätze",
            "exercise_type": "error_correction",
            "difficulty_level": "B2",
            "question_text": "Nachdem ich esse, gehe ich spazieren.",
            "correct_answer": "Nachdem ich gegessen habe, gehe ich spazieren.",
            "alternative_answers": [],
            "explanation_de": "'Nachdem' + Zeitenfolge: Nebensatz eine Zeitstufe früher (Perfekt).",
            "hints": ["nachdem + Perfekt", "Zeitenfolge beachten"],
            "context_category": "daily"
        }
    ]

    return exercises


def seed_grammar():
    """Main function to seed grammar data."""
    db = SessionLocal()
    try:
        # Check if topics already exist
        existing_topic = db.query(GrammarTopic).first()
        if existing_topic:
            print("⚠️  Grammar topics already exist.")

            # Check if exercises exist
            existing_exercise = db.query(GrammarExercise).first()
            if existing_exercise:
                print("⚠️  Grammar exercises already exist. Skipping seed.")
                print("   To re-seed, delete existing grammar data first.")
                return
            else:
                print("   Topics found, but no exercises. Adding exercises...")
                skip_topics = True
        else:
            skip_topics = False

        # Create topics if needed
        if not skip_topics:
            print("📚 Creating grammar topics...")
            topics_data = create_grammar_topics()

            created_topic_count = 0
            for topic_data in topics_data:
                topic = GrammarTopic(**topic_data)
                db.add(topic)
                created_topic_count += 1

            db.commit()
            print(f"✅ Successfully created {created_topic_count} grammar topics!")

            # Print summary by category
            print("\n📊 Grammar Topics by Category:")
            categories = {}
            for topic in topics_data:
                cat = topic['category']
                categories[cat] = categories.get(cat, 0) + 1

            for cat, count in sorted(categories.items()):
                print(f"   - {cat}: {count} topics")

        # Create exercises
        print("\n📝 Creating grammar exercises...")
        exercises_data = create_grammar_exercises()

        # Get all topics to map names to IDs
        topics = db.query(GrammarTopic).all()
        topic_map = {topic.name_de: topic.id for topic in topics}

        created_exercise_count = 0
        for exercise_data in exercises_data:
            topic_name = exercise_data.pop("topic_name")
            topic_id = topic_map.get(topic_name)

            if topic_id:
                exercise = GrammarExercise(
                    topic_id=topic_id,
                    **exercise_data
                )
                db.add(exercise)
                created_exercise_count += 1
            else:
                print(f"⚠️  Warning: Topic '{topic_name}' not found for exercise")

        db.commit()
        print(f"✅ Successfully created {created_exercise_count} grammar exercises!")

        # Print summary by exercise type
        print("\n📊 Exercises by Type:")
        exercise_types = {}
        for exercise in exercises_data:
            ex_type = exercise['exercise_type']
            exercise_types[ex_type] = exercise_types.get(ex_type, 0) + 1

        for ex_type, count in sorted(exercise_types.items()):
            print(f"   - {ex_type}: {count} exercises")

        print("\n✨ Grammar foundation complete!")
        print("   Total exercises:", created_exercise_count)
        print("   Ready for AI-generated exercises and diagnostic tests!")

    except Exception as e:
        print(f"❌ Error seeding grammar data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  GERMAN GRAMMAR LEARNING SYSTEM - DATA SEEDING")
    print("=" * 60)
    print()
    seed_grammar()
