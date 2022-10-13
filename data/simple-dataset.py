import random
import re
from types import SimpleNamespace

from numpy import place

vocab = SimpleNamespace(
    # human nouns
    HN = ['Alice', 'Bob', 'Clara', 'Doug', 'Ellen'],

    # human verbs
    HV = ['likes/dislikes', 'loves/hates', 'sees', 'meets', 'calls'],

    # drink nouns
    DN = ['tea/coffee', 'soda', 'water'],

    # drink adjectives
    DA = ['cold/warm'],

    # drink verbs
    DV = ['likes/dislikes', 'drinks', 'sips', 'pours'],

    # fruit nouns
    FN = ['apples/oranges/bananas/pears'],

    # fruit adjectives
    FA = ['mushy', 'unripe', 'sour/sweet'],

    # fruit verbs
    FV = ['likes/dislikes', 'eats', 'slices', 'picks', 'peels'],
)

# Alice loves Bob but hates Clara
# 'HN1 HVP1 HN2 but HVP2 HN3',
formats = [
    # Alice likes Bob
    'HN1 HV1 HN2',

    # Alice loves Bob but hates Clara
    'HN1 HVP1 HN2 but HVP2 HN3',

    # Alice meets Bob and Clara
    'HN1 HV1 HN2 and HN3',

    # Alice loves Bob and Clara but hates Dan
    'HN1 HVP1 HN2 and HN3 but HVP2 HN4',

    # Alice likes tea
    'HN1 DV1 DN1',

    # Alice likes apples
    'HN1 FV1 FN1',

    # Alice likes tea and soda
    'HN1 DV1 DN1 and DN2',

    # Alice likes apples and bananas
    'HN1 FV1 FN1 and FN2',

    # Alice likes tea but hates coffee
    'HN1 DVP1 DNP1 but DVP2 DNP2',

    # Alice likes apples but hates pears
    'HN1 FVP1 FNP1 but FVP2 FNP2',

    # Alice likes sweet oranges but dislikes sour oranges
    'HN1 FVP1 FAP1 FN1 but FVP2 FAP2 FN1',

    # Ellen likes warm tea but dislikes cold tea
    'HN1 DVP1 DAP1 DN1 but DVP2 DAP2 DN1',

    # Ellen likes warm tea but dislikes cold tea
    'HN1 DVP1 DAP1 DN1 but DVP2 DAP2 DN1',

    # Ellen likes cold soda and warm tea.
    'HN1 DV1 DA1 DN1 and DA2 DN2',

    # Clara pours warm tea and coffee.
    'HN1 DV1 DA1 DN1 and DN2',

    # Bob slices sour oranges and sweet bananas.
    'HN1 FV1 FA1 FN1 and FA2 FN2',

    # Clara slices sweet pears and oranges.
    'HN1 FV1 FA1 FN1 and FN2',

    # Ellen peels unripe pears and pours warm tea.
    'HN1 FV1 FA1 FN1 and DV1 DA1 DN1',

    # Clara dislikes bananas and dislikes cold coffee.
    'HN1 FV1 FN1 and DV1 DA1 DN1',

    # Bob likes sour bananas and sips tea.
    'HN1 FV1 FA1 FN1 and DV1 DN1',
]


def is_placeholder(token):
    return token.isupper()


def analyze_token(token):
    if not is_placeholder(token):
        return None, None, None, None

    # Ends with a single number
    assert re.search(r'\D\d$', token)
    number = token[-1]
    sans_number = token[:-1]

    is_pair = sans_number.endswith('P')
    root = sans_number[:-1] if is_pair else sans_number
    assert len(root) == 2

    return root, sans_number, is_pair, number


# 'HN1 FVP1 FNP1 but FVP2 FNP2',
def sentence():
    format = random.choice(formats)
    # format = 'HN1 FVP1 FNP1 but FVP2 FNP2'
    # format = 'HN1 FV1 FN1 and FN2'
    # format = 'HN1 FVP1 FAP1 FN1 but FVP2 FAP2 FN1'
    # format = 'HN1 DVP1 DAP1 DN1 but DVP2 DAP2 DN1'


    # print(format)

    # This list will get modified to contain the output
    tokens = format.split()

    for i in range(len(tokens)):
        token = tokens[i]
        if not is_placeholder(token):
            continue

        root, sans_number, is_pair, number = analyze_token(token)

        family = [t for t in tokens if analyze_token(t)[1] == sans_number]

        vocab_category = getattr(vocab, root)  # type: ignore
        if is_pair:
            pairs = [word for word in vocab_category if '/' in word]
            pair = random.choice(pairs)
            vocab_category = pair.split('/')
        else:
            new_vocab_category = []
            for w1 in vocab_category:
                if '/' not in w1:
                    new_vocab_category.append(w1)
                else:
                    for w2 in w1.split('/'):
                        new_vocab_category.append(w2)
            vocab_category = new_vocab_category

        family_unique = list(set(family))
        words = random.sample(vocab_category, len(family_unique))
        placeholder_to_word = {placeholder: word for placeholder, word in zip(family_unique, words)}

        for j in range(len(tokens)):
            if tokens[j] in placeholder_to_word:
                tokens[j] = placeholder_to_word[tokens[j]]
    
    sentence = f"{' '.join(tokens)}."
    # print(sentence)
    # print()
    return sentence

def generate_and_save_dataset(num_sentences):
    sentences = [sentence() for _ in range(num_sentences)]
    text = ' '.join(sentences)

    print('UNIQUE SENTENCES:', len(set(sentences)))

    with open('simple-english-dataset.txt', 'w') as f:
        f.write(text)
    
    return text

generate_and_save_dataset(num_sentences=1_000_000)

# print( sentence() )
