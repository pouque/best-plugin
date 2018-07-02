# -*- coding: utf-8 -*-
import weechat
import random

weechat.register("translit", "1kasper", "14.88", "HUJ-NA", "Delaet translit is tvoego teksta, bro", "", "")

idfun = lambda a: a # a -> a
head = lambda xs: xs[0] # list a -> a
last = lambda xs: xs[-1] # list a -> a
tail = lambda xs: xs[1:] # list a -> a
single = lambda x: [x] # a -> list a
zip_self = lambda a: zip(a, tail(a) + single(last(a))) # list a -> list

# (n : int) -> {cond : n > 0 ∧ n ≤ 1} -> bool
# returns True with p probality
probality_choice = lambda p: random.random() < p

same_case = lambda ch1, ch2: ch1.upper() if (ch1.istitle() and head(ch2).isupper()) else ch1

class PluginState:
    modes = [] # list PluginMode
    current_level = 0 # int
    random_mode = False # bool

    @classmethod
    def toggle_random_mode(cls): # () -> ()
        cls.random_mode = not cls.random_mode

    @classmethod
    def increment_level(cls): # () -> ()
        cls.current_level += 1
        cls.current_level %= len(cls.modes)

    @classmethod
    def get_level_by_name(cls, name): # string -> ()
        finded = next((mode for mode in cls.modes \
                       if mode.name == name), None)
        if finded != None: return finded
        else: raise IndexError(u"level “%s” not found" % name)

    @classmethod
    def set_level(cls, lvl): # int -> ()
        if lvl < len(cls.modes): cls.current_level = lvl
        else: raise IndexError("mode level out of range (maximum is %i)" % \
                               len(cls.modes))

    @classmethod
    def current_level_desc(cls): # () -> string
        return cls.modes[cls.current_level].name

    @classmethod
    def convert(cls, args): # bytes -> bytes
        return cls.modes[cls.current_level].convert(args)

    @classmethod
    def overflow_level(cls): return len(cls.modes) # () -> int

class PluginMode:
    # name : string
    # function : string -> string
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def convert(self, args): # bytes -> bytes
        return self.function(args.decode("utf-8")).encode("utf-8")

class TranslitMode(PluginMode):
    convert_table = {
        u'А' : u'A', u'а' : u'a',
        u'Б' : u'B', u'б' : u'b',
        u'В' : u'W', u'в' : u'v',
        u'Г' : u'G', u'г' : u'gu',
        u'Д' : u'D', u'д' : u'd',
        u'Е' : u'Je', u'е' : u'ie',
        u'Ё' : u'Jo', u'ё' : u'jo',
        u'Ж' : u'Zh', u'ж' : u'zh',
        u'З' : u'Z', u'з' : u'z',
        u'И' : u'Iee', u'и' : u'iee',
        u'Й' : u'J', u'й' : u'j',
        u'К' : u'K', u'к' : u'que',
        u'Л' : u'L', u'л' : u'l',
        u'М' : u'M', u'м' : u'm',
        u'Н' : u'N', u'н' : u'n',
        u'О' : u'O', u'о' : u'oue',
        u'П' : u'P', u'п' : u'p',
        u'Р' : u'R', u'р' : u'r',
        u'С' : u'S', u'с' : u'ss',
        u'Т' : u'T', u'т' : u't',
        u'У' : u'U', u'у' : u'ou',
        u'Ф' : u'F', u'ф' : u'ph',
        u'Х' : u'H', u'х' : u'kh',
        u'Ц' : u'C', u'ц' : u'ts',
        u'Ч' : u'Tsch', u'ч' : u'tsch',
        u'Ш' : u'Sch', u'ш' : u'sch',
        u'Щ' : u'Schtsch', u'щ' : u'schtsch',
        u'Ъ' : u'’', u'ъ' : u'’',
        u'Ы' : u'Ji', u'ы' : u'hi',
        u'Ь' : u'’', u'ь' : u'’',
        u'Э' : u'E', u'э' : u'e',
        u'Ю' : u'Jy', u'ю' : u'iou',
        u'Я' : u'Ja', u'я' : u'ja'
    }

    def convert_char(self, ch):
        if ch in self.convert_table: return self.convert_table[ch]
        else: return ch
    
    def to_translit(self, string):
        converted = list(map(self.convert_char, string))
        new_word = []
        for (fst, snd) in zip_self(converted):
            new_word.append(same_case(fst, snd))
        return "".join(new_word)

    def __init__(self, name):
        PluginMode.__init__(self, name, lambda s: self.to_translit(s))

class UprlsMode(PluginMode):
    def to_uprls(self, string):
        nullable = [u'а', u'о', u'у', u'е', u'и', u'ы', u'я', u'ё', u'ю',
                    u'А', u'О', u'У', u'Е', u'И', u'Ы', u'Я', u'Ё', u'Ю']
        def handle_word(word):
            if len(word) <= 1: return word
            word = list(word)
            for i in range(0, len(word) - 1):
                if (word[i] in nullable) and probality_choice(0.5):
                    word[i] = ""
            return "".join(word)
        string = string.split(" ")
        new_string = list(map(handle_word, string))
        return " ".join(new_string)

    def __init__(self, name):
        PluginMode.__init__(self, name, lambda s: self.to_uprls(s))

class HuettaMode(PluginMode):
    def get_random_word(self):
        words = [u'блядь', u'сука', u'нахуй', u'пидор', u'чмо', u'хер', \
                 u'дебил', u'придурок', u'хуесос', u'гомогей', \
                 u'блядина', u'хуита', u'даун', u'рукожоп', \
                 u'геегомик', u'гомогомик', u'говноед', \
                 u'мудак', u'кретин', u'еблан', u'шизик']
        word = words[random.randint(0, len(words) - 1)]
        if probality_choice(self.word_insert_probality): return word
        else: return word.upper()

    def to_huetta_pure(self, string):
        string = string.split(u" ")
        new_string = single(head(string))
        for i in range(1, len(string)):
            if last(string[i]).isalpha():
                for_push = u"%s, %s" % (string[i], self.get_random_word())
                if i != len(string) - 1: for_push += ","
                
                new_string.insert(i, for_push)
            else:
                new_string.insert(i, string[i])
        return " ".join(new_string)

    def to_huetta(self, args):
        if probality_choice(self.attack_probality) and (not args.startswith("/")):
            return self.to_huetta_pure(args)
        else: return args

    def __init__(self, name, attack_probality, word_insert_probality):
        self.attack_probality = attack_probality
        self.word_insert_probality = word_insert_probality
        PluginMode.__init__(self, name, lambda s: self.to_huetta(s))

# Commands registration

# WARNING
# Dirty code starts here
def tr_command(data, buffer, args):
    weechat.command(buffer, "/say %s" % \
                    PluginState.get_level_by_name("translit").convert(args))
    # oh fuck!

    return weechat.WEECHAT_RC_OK

weechat.hook_command("tr", "vot takoueu translit", "[text]", "description-huiction", "list", "tr_command", "")
# Dirty code stops here
# WARNING
        
def translit_command(data, buffer, args):
    args = args.split(" ")

    if len(args) <= 1:
        weechat.prnt(buffer, "invalid sytnax: use /translit <mode> <text>")
        return weechat.WEECHAT_RC_ERROR

    mode, text = head(args).decode("utf-8"), " ".join(tail(args))

    weechat.command(buffer, "/say %s" % \
                    PluginState.get_level_by_name(mode).convert(text))

    return weechat.WEECHAT_RC_OK

weechat.hook_command("translit", "make your text great again", "[text]", "description-huiction", "list", "translit_command", "")

def toggle_translit(date, buffer, args):
    PluginState.increment_level()
    weechat.prnt(buffer, "plugin level is now “%s”" % \
                 PluginState.current_level_desc())
    return weechat.WEECHAT_RC_OK

weechat.hook_command("toggle_translit", "perekljutschaet lutschschiij plagin", "", "", "", "toggle_translit", "")

def translit_info(date, buffer, args):
    weechat.prnt(buffer, "plugin level is “%s”" % \
                 PluginState.current_level_desc())
    return weechat.WEECHAT_RC_OK

weechat.hook_command("translit_info", "eenoframcija", "", "", "", "translit_info", "")

def toggleable_translit(data, modifier, modifier_data, string):
    if PluginState.random_mode:
        new_level = random.randint(1, PluginState.overflow_level() - 1)
        PluginState.set_level(new_level)
    return PluginState.convert(string)

weechat.hook_modifier("input_text_for_buffer", "toggleable_translit", "")

def random_toggle(date, buffer, args):
    PluginState.toggle_random_mode()

    if PluginState.random_mode:
        weechat.prnt(buffer, "random mode on!")
    else:
        weechat.prnt(buffer, "random mode off!")
    return weechat.WEECHAT_RC_OK

weechat.hook_command("random_toggle", "random toggle", "", "", "", "random_toggle", "")

PluginState.modes = [PluginMode("normal", idfun), \
                     TranslitMode("translit"), \
                     UprlsMode("uprls"), \
                     HuettaMode("huetta", 0.3, 0.3)]
