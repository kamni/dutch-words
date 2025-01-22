# Dutch Words

This provides a list of top 10,000 Dutch words for the purposes of personal study,
based on word frequencies from the *Projekt Deutscher Wortschatz* from the
Universität Leipzig.

## Data License

The data is licensed differently from the Python code.
It comes from the Universität Leipzig Corpora Collection for Dutch,
[mixed-typical collection from 2012](https://wortschatz.uni-leipzig.de/en/download/Dutch).

Many of the words in the original list are duplicates because of capitalization
and punctuation. When possible, the Python script strips duplicates.

The data has the following usage information:

Any data and applications provided by *Projekt Deutscher Wortschatz* are subject
to copyright. Permission for use is granted free of charge solely for
non-commercial personal and scientific purposes licensed under the
Creative Commons License [CC BY-NC](http://creativecommons.org/licenses/by-nc/4.0/).
Any use that exceeds the means of query provided by the WWW-Interface, any
automated queries (except using our [RESTful](http://api.corpora.uni-leipzig.de/)
Webservices) and any commercial use of the data obtained is forbidden without
explicit written permission by the copyright owner.

All corpora provided for download are licensed under
[CC BY](http://creativecommons.org/licenses/by/4.0/). If you are interested in
larger data sets, please contact [us](mailto:wort@informatik.uni-leipzig.de).

© 2025 Universität Leipzig / Sächsische Akademie der Wissenschaften / InfAI.

## Development

Install python requirements:

```sh
pip install -r requirements.txt
```

Copy the configuration:

```sh
cp config.ini.example config.ini
```

Generate the database (say 'yes' to the prompt):

```sh
. ./scripts/initialize_database.py -d
```
