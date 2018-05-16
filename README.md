# Sample of «big data» parser

## Inputs

On input parser accepts some xml/csv file with millions records about products.
Schema of products can be different for different files.
Each file can keeps duplicates or variants of loaded products (e.g. same id, but different colour, size etc.)

## Requirements to parser

1) save data to database (insert and update) with high performance
2) support several inputs data format (and be easy extendible)
3) handle duplicates

### Installation

    git clone https://github.com/onary/bigdata.git
    cd bigdata
    pip install -r requirements.txt

### Run

    python parser.py xml

    or

    python parser.py csv

### infrastructure

I. As databese was chosen MongoDB. There was several arguments in favor of this decision

    1. Changable data schema
    2. Data-set has just one table and no relationships
    3. In case with really large data mongodb can be replicated on several servers
    4. Good performance
    5. Usefull features: Indexing, Bulk-insert, addToSet

    P.S. However in case when we can predefined one schema for all inputs, and ensure that one server can cover all our need - I would choose postgres.


II. Reading large files: Common approach to read files by chunks, string by string using python generator

III. Handling duplicates in several steps:

    1. Load all revisions from DB and store to the memory
    2. Parse datafile and each record convert to object with certain format
    3. Serialize object to string
    4. Make hash from string using sha1 algorithm
    5. Check if we have such hash stored, (quit iteration if hash exists)
    6. Save hash in memory (and append to the record as revision for saving in DB)

    P.S. when large data might be used with Redis


IV. To use parser you need to write config for your dataset. (e.g. configs/csv.json)
Then add map to readers.py in READER dict ({config_file_name: function_reader})
Then you can use parser with command

    python parser.py config_file_name


V. Launch tests

    python -m unittest tests.py
