from operator import add
from Lab05tester import test_batch


### Reprezentare - construcție
CONST = "const"
ATOM = "atom"
VAR = "var"
CALL = "call"
AND = "&"
OR = "|"
NEG = "~"
OPS = [AND, OR, NEG]

TYPE = FUNC = 0
ARGS = 1

# întoarce un termen constant, cu valoarea specificată.
def make_const(value):
    return (CONST, value)

# întoarce un termen care este o variabilă, cu numele specificat.
def make_var(name):
    return (VAR, name)

# întoarce un termen care este un apel al funcției specificate, pe restul argumentelor date.
# E.g. pentru a construi termenul add[1, 2, 3] vom apela
#  make_function_call(add, make_const(1), make_const(2), make_const(3))
# !! ATENȚIE: python dă args ca tuplu cu restul argumentelor, nu ca listă. Se poate converti la listă cu list(args)
def make_function_call(function, *args):
    return (CALL, (function, list(args)))

# întoarce o formulă formată dintr-un atom care este aplicarea predicatului dat pe restul argumentelor date.
# !! ATENȚIE: python dă args ca tuplu cu restul argumentelor, nu ca listă. Se poate converti la listă cu list(args)
def make_atom(predicate, *args):
    return (ATOM, (predicate, list(args)))

# întoarce o formulă care este negarea propoziției date.
# get_args(make_neg(s1)) va întoarce [s1]
def make_neg(sentence):
    return (NEG, [sentence])

# întoarce o formulă care este conjuncția propozițiilor date (2 sau mai multe).
# e.g. apelul make_and(s1, s2, s3, s4) va întoarce o structură care este conjuncția s1 ^ s2 ^ s3 ^ s4
#  și get_args pe această structură va întoarce [s1, s2, s3, s4]
def make_and(sentence1, sentence2, *others):
    return (AND, [sentence1, sentence2] + list(others))

# întoarce o formulă care este disjuncția propozițiilor date.
# e.g. apelul make_or(s1, s2, s3, s4) va întoarce o structură care este disjuncția s1 V s2 V s3 V s4
#  și get_args pe această structură va întoarce [s1, s2, s3, s4]
def make_or(sentence1, sentence2, *others):
    return (OR, [sentence1, sentence2] + list(others))

# întoarce o copie a formulei sau apelul de funcție date, în care argumentele au fost înlocuite
#  cu cele din lista new_args.
# e.g. pentru formula p(x, y), înlocuirea argumentelor cu lista [1, 2] va rezulta în formula p(1, 2).
# Noua listă de argumente trebuie să aibă aceeași lungime cu numărul de argumente inițial din formulă.
def replace_args(formula, new_args):
    if is_atom(formula) or is_function_call(formula):
        return (formula[TYPE], (formula[ARGS][TYPE], new_args))
    return (formula[TYPE], new_args)


### Reprezentare - verificare

# întoarce adevărat dacă f este un termen.
def is_term(f):
    return is_constant(f) or is_variable(f) or is_function_call(f)

# întoarce adevărat dacă f este un termen constant.
def is_constant(f):
    return f[TYPE] == CONST

# întoarce adevărat dacă f este un termen ce este o variabilă.
def is_variable(f):
    return f[TYPE] == VAR

# întoarce adevărat dacă f este un apel de funcție.
def is_function_call(f):
    return f[TYPE] == CALL

# întoarce adevărat dacă f este un atom (aplicare a unui predicat).
def is_atom(f):
    return f[TYPE] == ATOM

# întoarce adevărat dacă f este o propoziție validă.
def is_sentence(f):
    return is_atom(f) or f[TYPE] in OPS

# întoarce adevărat dacă formula f este ceva ce are argumente.
def has_args(f):
    return is_function_call(f) or is_sentence(f)


### Reprezentare - verificare

# pentru constante (de verificat), se întoarce valoarea constantei; altfel, None.
def get_value(f):
    return f[ARGS] if is_constant(f) else None

# pentru variabile (de verificat), se întoarce numele variabilei; altfel, None.
def get_name(f):
    return f[ARGS] if is_variable(f) else None

# pentru apeluri de funcții, se întoarce funcția;
# pentru atomi, se întoarce numele predicatului;
# pentru propoziții compuse, se întoarce un șir de caractere care reprezintă conectorul logic (e.g. ~, A sau V);
# altfel, None
def get_head(f):
    if is_atom(f) or is_function_call(f):
        return f[ARGS][FUNC]
    if is_sentence(f):
        return f[TYPE]

# pentru propoziții sau apeluri de funcții, se întoarce lista de argumente; altfel, None.
# Vezi și "Important:", mai sus.
def get_args(f):
    if is_atom(f) or is_function_call(f):
        return f[ARGS][ARGS]
    if is_sentence(f):
        return f[ARGS]


test_batch(0, globals())


# Afișează formula f. Dacă argumentul return_result este True, rezultatul nu este afișat la consolă, ci întors.
def print_formula(f, return_result = False):
    ret = ""
    if is_term(f):
        if is_constant(f):
            ret += str(get_value(f))
        elif is_variable(f):
            ret += "?" + get_name(f)
        elif is_function_call(f):
            ret += str(get_head(f)) + "[" + "".join([print_formula(arg, True) + "," for arg in get_args(f)])[:-1] + "]"
        else:
            ret += "???"
    elif is_atom(f):
        ret += str(get_head(f)) + "(" + "".join([print_formula(arg, True) + ", " for arg in get_args(f)])[:-2] + ")"
    elif is_sentence(f):
        # negation, conjunction or disjunction
        args = get_args(f)
        if len(args) == 1:
            ret += str(get_head(f)) + print_formula(args[0], True)
        else:
            ret += "(" + str(get_head(f)) + "".join([" " + print_formula(arg, True) for arg in get_args(f)]) + ")"
    else:
        ret += "???"
    if return_result:
        return ret
    print(ret)
    return

# Verificare construcție și afișare
# Ar trebui ca ieșirea să fie similară cu: (A (V ~P(?x) Q(?x)) T(?y, <built-in function add>[1,2]))
formula1 = make_and(
    make_or(make_neg(make_atom("P", make_var("x"))), make_atom("Q", make_var("x"))),
    make_atom("T", make_var("y"), make_function_call(add, make_const(1), make_const(2))))
print_formula(formula1)


# Aplică în formula f toate elementele din substituția dată și întoarce formula rezultată
def substitute(f, substitution):
    if substitution is None:
        return None
    if is_variable(f) and (get_name(f) in substitution):
        return substitute(substitution[get_name(f)], substitution)
    if has_args(f):
        return replace_args(f, [substitute(arg, substitution) for arg in get_args(f)])
    return f

def test_formula(x, copyy = False):
    fun = make_function_call(add, make_const(1), make_const(2))
    return make_and(make_or(make_neg(make_atom("P", make_const(x))), make_atom("Q", make_const(x))),                     make_atom("T", fun if copyy else make_var("y"), fun))

# Test (trebuie să se vadă efectele substituțiilor în formulă)
test_batch(1, globals())


# Verifică dacă variabila v apare în termenul t, având în vedere substituția subst.
# Întoarce True dacă v apare în t (v NU poate fi înlocuită cu t), și False dacă v poate fi înlocuită cu t.
from functools import partial

def occur_check(v, t, subst):
    if v == t:
        return True
    if get_name(t) in subst:
        return occur_check(v, substitute(t, subst), subst)
    if is_function_call(t):
        return any(map(lambda arg: occur_check(v, arg, subst), get_args(t)))
    return False

# Test!
test_batch(2, globals())


# Unifică formulele f1 și f2, sub o substituție existentă subst.
# Rezultatul unificării este o substituție (dicționar nume-variabilă -> termen),
#  astfel încât dacă se aplică substituția celor două formule, rezultatul este identic.
def unify(f1, f2, subst = None):
    if not subst:
        subst = {}

    st = [(f1, f2)]

    while st:
        f1, f2 = st.pop()

        while get_name(f1) in subst:
            f1 = substitute(f1, subst)
        while get_name(f2) in subst:
            f2 = substitute(f2, subst)

        if f1 == f2:
            continue

        if is_variable(f1):
            if occur_check(f1, f2, subst):
                return False

            subst[get_name(f1)] = f2
        elif is_variable(f2):
            if occur_check(f2, f1, subst):
                return False

            subst[get_name(f2)] = f1
        elif has_args(f1) and has_args(f2):
            if get_head(f1) == get_head(f2):
                f1_args = get_args(f1)
                f2_args = get_args(f2)

                if len(f1_args) == len(f2_args):
                    st += zip(f1_args, f2_args)
            else:
                return False
        else:
            return False

    return subst

# Test!
test_batch(3, globals())
