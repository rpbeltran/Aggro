
import subprocess, sys




print( "Installing NLTK..." )

try:
	bashCommand = "pip install nltk"
	print( subprocess.check_output(['bash','-c', bashCommand]) )
	import nltk

except:
	print( "Failed to install nltk. Make sure pip is installed.")
	sys.exit()




print( "\nDownloading required packages from NLTK..." )

try:
	nltk.download('punkt')
	nltk.download('stopwords')
	nltk.download('averaged_perceptron_tagger')
	nltk.download('maxent_ne_chunker')
	nltk.download('words')
except:
	print( "Failed to install required nltk packages.")
	sys.exit()



print( "\nSuccess!" )
