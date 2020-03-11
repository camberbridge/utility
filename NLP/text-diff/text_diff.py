import hashlib

def hamming_distance(chaine1, chaine2):
    distance = sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))
    print("Distance: ", distance)
    return distance

def text_hashing(text):
  text = text.encode("utf8")
  code = hashlib.sha512(text).hexdigest()
  return code

def prepro(file_name):
  with open(file_name, "r") as f:
    text = f.read()
    text = text.replace("\n", "").replace(" ", "").replace("　", "").replace("(", "").replace(")", "").replace("（", "").replace("）", "")
    code = text_hashing(text)
    return code
  return None

def similarity():
  pre_code = prepro("pre.txt")
  post_code = prepro("post.txt")

  if pre_code is not None and post_code is not None:
    if 0 < hamming_distance(pre_code, post_code):
      return u"差異あり"
    else:
      return u"差異なし"
  else:
    return u"テキストが読めませんでした。目視確認をお願い致します。"


if __name__ == "__main__":
  print(similarity())
