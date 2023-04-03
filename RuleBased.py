import json

with open ("NLP\data.txt", "r", encoding="utf-8") as f: # r for read
    text = f.read().split("\n\n")[3:4] # removes all line breakes. [] = work with first chunk of data
    # print(text)

character_names = []
with open ("NLP\HPNames.json", "r", encoding="utf-8") as f: # r for read
    characters = json.load(f)
    for character in characters:
        names = character.split()
        for name in names:
            if name != "and" and name != "the" and name != "The":
                name = name.replace(",","").strip()
                character_names.append(name)
    # print(text)

# try grabbing the named entities
for segment in text:
    # print(segment)

    segment = segment.strip() # removes spaces from begining and end
    segment = segment.replace("\n"," ")
    # print()
    # print(segment)

    punc = '''!()-[]{};:'"\,<>?@£$%^&*_~'''
    punc = set(punc)
    segment = "".join(ch for ch in segment if ch not in punc)
    # print()
    # print(segment)

    # get individual words of text 
    words = segment.split() # splits words individually
    # print(words)

    i = 0
    for word in words:
        if word in character_names:
            if words[i-1][0].isupper(): # [previous word][first character of previous word]
                print(f"Found Characters: {words[i-1]} {word}")
            else:
                print(f"Found Character(s): {word}")

        i=+1

