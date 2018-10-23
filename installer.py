

print( "Installing NLTK" )

bashCommand = "pip install nltk"
print( subprocess.check_output(['bash','-c', bashCommand]) )



print( "Downloading required packages from NLTK" )

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
