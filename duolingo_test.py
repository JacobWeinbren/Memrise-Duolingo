import duolingo
lingo  = duolingo.Duolingo(username='', jwt='')
words = list(lingo.get_vocabulary(language_abbr='he')['vocab_overview'])
print(words)
#print(lingo.get_audio_url('באה'))