pip install pyannotate
python -m pytest

for f in $(find src/ -name '*.py'); do pyannotate -w --python-version 3 --type-info type_info.json $f; done
for f in $(find tests/ -name '*.py'); do pyannotate -w --python-version 3 --type-info type_info.json $f; done