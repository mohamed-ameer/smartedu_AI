# -*- coding: utf-8 -*-
"""Quiz Generator.ipynb

# NLP Model
"""
from django.conf import settings
import os
import string 
import traceback 
import numpy as np 
import scipy 
import nltk 
from nltk.corpus import stopwords 
from nltk.corpus import wordnet 
nltk.download('stopwords') 
nltk.download('wordnet') 
nltk.download('punkt') 
import pke 
from nltk.tokenize import sent_tokenize 
from sentence_transformers import SentenceTransformer 
hugging_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2') 
# return list of questions
def nlp_model(text):
  def sent_tokenizer(text):
    sentences=[]
    for s in sent_tokenize(text) :
      sentences.append(s)
    return sentences

  def get_keyword(text):
      out_list=[]
      try:
        extractor = pke.unsupervised.MultipartiteRank()
        stoplist = list(string.punctuation)
        stoplist += pke.lang.stopwords.get('en')
        extractor.load_document(input=text, stoplist=stoplist)
        pos = {'NOUN', 'PROPN', 'ADJ'}
        extractor.candidate_selection(pos=pos)
        extractor.candidate_weighting(alpha=1.1, threshold=0.74, method='average')
        keyphrases = extractor.get_n_best(n=10)
        for val in keyphrases:
            out_list.append(val[0])
      except:
          out_list = []
          traceback.print_exc()
      return out_list

  def wordnet_distractors(keywords):
      distractors=[]
      for word in keywords:
          wr = word.lower()
          if len(wr.split())>0:
              # wordnet works with single words
              wr = wr.replace(" ","_")
          # synsets of each word
          synset = wordnet.synsets(wr)   
          for syn in synset:
              # hypernyms of each synset, work with only synsets that have hypernym
              hypernym = syn.hypernyms()
              if len(hypernym) == 0: 
                  continue
              # get hyponyms of the first hypernym 
              for item in hypernym[0].hyponyms():
                  # get root word of each hyponym
                  name = item.lemmas()[0].name()
                  # accept hyponyms wich are not the original keyword
                  if name == word:
                      continue
                  # return hyponyms in a proper format
                  name = name.replace("_"," ")
                  if name is not None and name not in distractors:
                      distractors.append(name)
          # take first keyword in the list has ditractors  
          if len(distractors) > 0 :
              break
      return word, distractors

  # first three distractors using minimum similarity distance, return list of three wrong options
  def options_gen(distractors,distances,key):
    opts = []
    num = 5
    try:
      for i in range(num):
          # get index of minimum distance to take its corresponding distractor
          index, = np.where(distances == min(distances))
          dist = distractors[index[0]]
          # not accept replicated distractor even it with s or without
          if (key+'s' == dist) or (key == dist+'s') or (dist in opts):
            # delete the minimum to repeat process in the seconde minimum and so on
            distances = np.delete(distances,index[0])
            continue
          # add dist if it not in options
          opts.append(dist)
          distances = np.delete(distances,index[0])

    except:
        print("No Options")

    return opts[:3]

  # ruturn list of questions, list of answers, and list of wrong answers lists
  def mcq_generator(sentences):
    questions = []
    answers = []
    wrong_options = []
    for sent in sentences:
      keyword = get_keyword(sent)
      key , distractors = wordnet_distractors(keyword)
      # get distractors and keyword embeddings 
      distractors_embeddings = hugging_model.encode(distractors)
      key_embedding = hugging_model.encode([key])
      try:
        # Compute distance between each pair of the two collections of inputs.
        distances = scipy.spatial.distance.cdist(key_embedding, distractors_embeddings, 'cosine')[0]
        options = options_gen(distractors,distances,key)
      except:
        options = []
      # replace answer with blank space
      question = sent.replace(key,"______",1)

      questions.append(question)
      answers.append(key)
      wrong_options.append(options)

    return questions, answers, wrong_options

  # ruturn list of questions, list of answers[True,False]
  def truefalse_generator(sentences):
    final_ans = []
    final_sents = []
    for sent in sentences:
      # original sentence is correct 
      final_sents.append(sent)
      final_ans.append("True")

      keyword1 = get_keyword(sent)
      key1 , distractors1 = wordnet_distractors(keyword1)
      # get distractors and keyword embeddings 
      distractors_embeddings1 = hugging_model.encode(distractors1)
      key_embedding1 = hugging_model.encode([key1])
      try:
        # Compute distance between each pair of the two collections of inputs.
        distances1 = scipy.spatial.distance.cdist(key_embedding1, distractors_embeddings1, 'cosine')[0]
        options = options_gen(distractors1,distances1,key1)
      except:
        options = []
      for op in range(len(options)) : 
        # replace answer with a distractor
        false_statement = sent.replace(key1, options[op])
        final_sents.append(false_statement)
        final_ans.append("False")
        # one wrong sentence is enough for each original sentence
        break
    return final_sents,final_ans

  # Enter text file path here (OR) comment the read_file function and enter text directly
  # file_path = 'sun.txt'
  # text = read_file(file_path)
  text="test"
  text_sents= sent_tokenizer(text)
  # if user check MCQ Checkbox
  questions, answers, wrong_options = mcq_generator(text_sents)
  # if user check True/False Checkbox
  # questions1 , answers1 = truefalse_generator(text_sents)
  return questions,answers,wrong_options
  """# Deep Learning Model"""


# return list of q & a &op
def dl_model(text):
  from transformers import T5ForConditionalGeneration,T5Tokenizer

  Qu_model_path = os.path.join(settings.FILES_DIR, 'Qmodel')
  Qu_tokenizer_path = os.path.join(settings.FILES_DIR, 'Qtokenizer')

  Dis_model_path = os.path.join(settings.FILES_DIR, 'Dmodel')
  Dis_tokenizer_path = os.path.join(settings.FILES_DIR, 'Dtokenizer')

  Qmodel = T5ForConditionalGeneration.from_pretrained(Qu_model_path)
  Qtokenizer = T5Tokenizer.from_pretrained(Qu_tokenizer_path)

  Dmodel = T5ForConditionalGeneration.from_pretrained(Dis_model_path)
  Dtokenizer = T5Tokenizer.from_pretrained(Dis_tokenizer_path)

  # context1 ="It is a common misconception that the Sun is yellow, or orange or even red. However, the Sun is essentially all colors mixed together, which appear to our eyes as white. Rainbows are light from the Sun, separated into its colors. Each color in the rainbow (red, orange, yellow, green, blue, violet) has a different wavelength. Red is the longest, blue the shortest."

  def get_keyword(text):
    out_list=[]
    try:
      extractor = pke.unsupervised.MultipartiteRank()
      stoplist = list(string.punctuation)
      stoplist += pke.lang.stopwords.get('en')
      extractor.load_document(input=text, stoplist=stoplist)
      pos = {'NOUN', 'PROPN', 'ADJ'}
      extractor.candidate_selection(pos=pos)
      extractor.candidate_weighting(alpha=1.1, threshold=0.74, method='average')
      keyphrases = extractor.get_n_best(n=10)
      for val in keyphrases:
          out_list.append(val[0])
    except:
        out_list = []
        traceback.print_exc()
    return out_list

  keywords = get_keyword(text)
  questions = []
  distractors = []

  for ans in keywords:
    input = "answer: %s  context: %s  </s>" % (str(ans), str(text))
    encoding = Qtokenizer.encode_plus(input,max_length =512, padding=True, return_tensors="pt")
    input_ids,attention_mask  = encoding["input_ids"], encoding["attention_mask"]

    # Question Generator
    Qmodel.eval()
    beam_output = Qmodel.generate(
        input_ids=input_ids,attention_mask=attention_mask,
        max_length=72,
        early_stopping=True,
        num_beams=5,
        num_return_sequences=1

    )
    sent = Qtokenizer.decode(beam_output[0], skip_special_tokens=True,clean_up_tokenization_spaces=True)
    questions.append(sent.replace("question: ","",1))

  for i in range(len(keywords)):
    input1 = "question: %s  answer: %s  context: %s  </s>" % (str(questions[i]), str(keywords[i]), str(text))
    encoding1 = Dtokenizer.encode_plus(input1,max_length =512, padding=True, return_tensors="pt")
    input_ids1,attention_mask1  = encoding1["input_ids"], encoding1["attention_mask"]

    # Distractors Generator
    Dmodel.eval()
    beam_output1 = Dmodel.generate(
        input_ids=input_ids1,attention_mask=attention_mask1,
        max_length=72,
        early_stopping=True,
        num_beams=5,
        num_return_sequences=1

    )
    sent1 = Dtokenizer.decode(beam_output1[0], skip_special_tokens=True,clean_up_tokenization_spaces=True)
    stop = ["distractor1:", "distractor2:", "distractor3:"]
    sentwords = sent1.split()

    resultwords  = [word for word in sentwords if word.lower() not in stop]
    result = ' '.join(resultwords)
    distractors.append(result.split())
  return questions,keywords,distractors


