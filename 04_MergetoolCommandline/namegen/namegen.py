import cmd
import pynames
from pynames import generators

gens = {}
race = {}

for o in pynames.get_all_generators() :
    gen_name = o.__module__.split('.')[-1]
    sub_gen_name = o.__name__
    if gen_name not in gens :
        race[gen_name] = []
        gens[gen_name] = []
    if sub_gen_name not in gens[gen_name] :
        gens[gen_name].append(sub_gen_name)
        tmp = 'Generator'
        if 'NamesGenerator' in sub_gen_name :
            tmp = 'NamesGenerator'
        if 'FullnameGenerator' in sub_gen_name :
            tmp = 'FullnameGenerator'
        race[gen_name].append(sub_gen_name[:sub_gen_name.index(tmp)])

lang_opts = {'ru' : pynames.LANGUAGE.RU, 'en' : pynames.LANGUAGE.EN}

gender_opts = { 'female' : pynames.GENDER.FEMALE , 'male' : pynames.GENDER.MALE }

curr_lang = 'en'


def multiple_assert(*args) :
    if not all(args) :
        print("Input error")
        return False
    return True

class name_gen_shell(cmd.Cmd):

    def do_language(self, arg):
        global curr_lang
        arg = arg.split()
        if multiple_assert(arg, len(arg)==1, arg[0] in lang_opts) :
            curr_lang = 'ru' if arg[0] == 'ru' else 'en'

    def complete_language(self, text, line, start_index, end_index) :
        if len(line.split()) == 1 :
            return [*lang_opts.keys()]
        if text and len(line.split()) == 2 :
            return [ln for ln in [*lang_opts.keys()] if ln.startswith(text)]

    def do_generate(self, arg) :
        arg = arg.split()

        sub_gen = ''
        gender = pynames.GENDER.MALE
        
        if 0 < len(arg) < 4 and multiple_assert(arg[0] in gens) :
            if len(arg) == 1 :
                pass
            elif len(arg) == 2 and multiple_assert(arg[1] in race[arg[0]] or arg[1] in gender_opts) :
                if arg[1] in race[arg[0]] :
                    sub_gen = arg[1]
                else :
                    gender = gender_opts[arg[1]]
            elif len(arg) == 3 and multiple_assert(arg[1] in race[arg[0]] and arg[2] in gender_opts) :
                sub_gen = arg[1]
                gender = gender_opts[arg[2]]
            else :
                return 
        else :
            return 

        sub_gen = race[arg[0]][0] if not sub_gen else sub_gen

        for ss in gens[arg[0]] :
            if ss.startswith(sub_gen) :
                sub_gen = ss 

        tmp = getattr(getattr(generators, arg[0]), sub_gen)()
        lang = lang_opts[curr_lang] if curr_lang in tmp.languages else pynames.LANGUAGE.NATIVE
        print(tmp.get_name_simple(gender, lang))

    def complete_generate(self, text, line, start_index, end_index) :
        toks = line.split()

        if len(toks) == 1 :
            return[*gens.keys()]

        if len(toks) == 2 :
            if text :
                return [s for s in [*gens.keys()] if s.startswith(text)]
            if toks[1] in gens:
                return race[toks[1]] + [*gender_opts.keys()]

        if len(toks) == 3 :
            if text and toks[1] in gens: 
                return [s for s in race[toks[1]] + [*gender_opts.keys()] if s.startswith(text)]
            if toks[1] in gens and toks[2] in race[toks[1]] :
                return [*gender_opts.keys()]

        if len(toks) == 4 :
            if text and toks[1] in gens and toks[2] in race[toks[1]]:
                return [s for s in [*gender_opts.keys()] if s.startswith(text)]

    def do_info(self, arg) :
        arg = arg.split()

        if 0 < len(arg) < 3 and multiple_assert(arg[0] in gens) :
            if len(arg) == 1 :
                res = 0
                for sub in gens[arg[0]] :
                    tmp = getattr(getattr(generators, arg[0]), sub)()
                    res += tmp.get_names_number()
                print(res)
            elif len(arg) == 2 and multiple_assert( arg[0] in gens, arg[1] in (['language'] + [*gender_opts.keys()]) ) :
                tmp = getattr(getattr(generators, arg[0]), gens[arg[0]][0])()
                if arg[1] == 'language' :
                    print(*tmp.languages)
                else :
                    print(tmp.get_names_number(gender_opts[arg[1]]))

    def complete_info(self, text, line, start_index, end_index) :
        toks = line.split()

        if len(toks) == 1 :
            return [*gens.keys()]

        if len(toks) == 2 :
            if text :
                return [s for s in [*gens.keys()] if s.startswith(text)]
            if toks[-1] in gens :
                return ['language'] + [*gender_opts.keys()]

        if len(toks) == 3:
            if text :
                return [s for s in ['language'] + [*gender_opts.keys()] if s.startswith(text)]

    def do_exit(self, arg) :
        return True

