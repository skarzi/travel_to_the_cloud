import functools
import os
import unicodedata

import Levenshtein
import pexpect
from many_stop_words import get_stop_words
from moviepy.editor import (
    concatenate_videoclips,
    VideoFileClip
)

from ivr.wdnet import get_synonyms


def speed_by(func=None, by=1.0):
    if func is None:
        return functools.partial(speed_by, by=by)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("SPEEDING!", result)
        if result is not None:
            print("SPEEDING!", result)
            return result.speedx(by)
        return result

    return wrapper


class TextToSilentLanguageConverter:
    def __init__(self, movies_dir):
        self._movies_dir = movies_dir
        self._stopwords = get_stop_words('pl')
        self._movies_dict = self._create_movies_dict()
        self._storage = 'tmp'
        if not os.path.exists(self._storage):
            os.mkdir(self._storage)

    def convert(self, sentence):
        clip = self._sentence2movie(sentence)
        movie_path = os.path.join(
            self._storage,
            self._create_name(sentence),
        )

        movie_path = unicodedata.normalize('NFKD', movie_path).encode('ascii', 'ignore').decode('utf-8')
        print(movie_path)

        clip.write_videofile(movie_path)
        return movie_path

    def _create_name(self, sentence):
        name = unicodedata.normalize('NFC', sentence.lower().replace(' ', '_'))
        return name.strip('.') + '.mp4'

    def _lemmatize(self, word):
        child = pexpect.spawn('morfeusz_analyzer')
        child.expect('\)\r\n')
        child.sendline(word)
        child.readline()
        response = child.readline()
        return response.decode('utf-8').split(',')[3].split(':')[0]

    def _find_synonym(self, word):
        for k, p in self._movies_dict.items():
            if Levenshtein.ratio(k, word) >= 0.7:
                return k, p
        synonyms = get_synonyms(word)
        for syn in synonyms:
            for k, p in self._movies_dict.items():
                if Levenshtein.ratio(k, syn) >= 0.7:
                    return k, p
        return None, None

    @speed_by(by=1.5)
    def _word2clip(self, word):
        if word in self._stopwords:
            return
        if word not in self._movies_dict:
            lemmatized = self._lemmatize(word) or word
        else:
            lemmatized = word
        clip = self._movies_dict.get(lemmatized, None)
        if clip:
            print(
                'original: ', word,
                'lemmatized: ', lemmatized,
                'clip', clip, type(clip),
            )
            return VideoFileClip(os.path.join(self._movies_dir, clip))
        else:
            synonym, clip = self._find_synonym(word)
            print(
                'original: ', word,
                'synnonym: ', synonym,
                'clip', clip, type(clip),
            )
            if clip:
                return VideoFileClip(os.path.join(self._movies_dir, clip))

    def _sentence2movie(self, sentence):
        clips = []
        for w in sentence.split():
            clip = self._word2clip(w)
            if clip:
                clips.append(clip.resize((460, 460)))
        return concatenate_videoclips(clips)

    def _create_movies_dict(self):
        dictionary = dict()
        for movie in os.listdir(self._movies_dir):
            key = unicodedata.normalize('NFC', movie.split('-')[0].lower())
            dictionary[key] = movie
        dictionary['latać'] = dictionary['latać samolotem']
        dictionary['odlecieć'] = dictionary['latać samolotem']

        dictionary['jechać'] = dictionary['jeździć']
        dictionary['odjechać'] = dictionary['jeździć']
        dictionary['odjeżdżać'] = dictionary['jeździć']

        return dictionary


text_to_silent_language_converter = TextToSilentLanguageConverter('./movies')
